from flask import render_template, redirect, url_for, flash, request, session, Flask, Response
from flask_login import logout_user, login_user, current_user
import pytz
from pykafka import KafkaClient
from pytz import timezone
from datetime import datetime

from flaskmongo import logindb, app, get_kafka_client
from flaskmongo.forms import LoginForm
from flaskmongo.models import LoginTime, LogoutTime, User
from flaskmongo.models.models import CarOwner


@app.route('/')
@app.route('/home')
def home():
    session['attempt'] = 3
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        session['username'] = username
        password = request.form.get('password')
        if user and user.password == password and user.username == username:
            utc_now = datetime.utcnow()
            utc = pytz.timezone('UTC')
            aware_date = utc.localize(utc_now)
            turkey = timezone('Europe/Istanbul')
            now_turkey = aware_date.astimezone(turkey)
            usertime = LoginTime(username=user.username, user_id=user.id, date_login=now_turkey)

            logindb.session.add(usertime)
            logindb.session.commit()
            login_user(user)
            session['logged_in'] = True
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        attempt = session.get('attempt')
        attempt -= 1
        session['attempt'] = attempt
        #   print(attempt, flush=True)

        if user and attempt == 1:
            print(password)
            print(user.password)

            client_ip = session.get('client_ip')
            flash('Son şansınız, %s adresi 24 Saat Boyunca Bloke Olacaktır, Deneme Hakkı: %d / 3' % (client_ip, attempt),
                  'error')
        elif attempt == 0:
            return redirect(url_for('logError'))
        else:
            flash('Bilgileriniz Yanlıştır, Deneme Hakkı: %d / 3' % attempt, 'error')
        return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        utc_now = datetime.utcnow()
        utc = pytz.timezone('UTC')
        aware_date = utc.localize(utc_now)
        turkey = timezone('Europe/Istanbul')
        now_turkey = aware_date.astimezone(turkey)
        usertime = LogoutTime(username=current_user.username, user_id=current_user.id, date_logout=now_turkey)
        logindb.session.add(usertime)
        logindb.session.commit()
        logout_user()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/logError')
def logError():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('logError.html')


## Consumer API

###CONSUMER API, KAFKANIN PRODUCER İLE YOLLADIGI BİLGİLERİ CONSUMER BURADA ALARAK SAKLAR VE JAVASCRİPTTE FONKSİYON İLE ÇAĞIRIR
@app.route('/topic/<topicname>')
def get_messages(topicname):
    kclient = get_kafka_client()
    def events():
        for i in kclient.topics[topicname].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())

    return Response(events(), mimetype="text/event-stream")

@app.route('/map')
def map():
    if current_user.is_authenticated:
        username = current_user.username
        user = CarOwner.query.all()

        return render_template('map.html', username=username, usercars=user)
    else:
        return render_template('home.html')

@app.route('/map2')
def map2():
    if current_user.is_authenticated:
        username = current_user.username
        user = CarOwner.query.filter_by(user_name=username).all()
        return render_template('map2.html', username=username, usercars=user)
    else:
        redirect(url_for('home'))