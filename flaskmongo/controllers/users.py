from flaskmongo.models.models import User


def UserLogin(username, password):
    user = User.query.filter_by(username=username).first()
    if user.password == password and user.username == username:
        return True
    else:
        return False
