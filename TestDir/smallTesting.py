from flaskmongo.models.models import CarOwner

user = CarOwner.query.filter_by(user_name="ASahip1").all()

print(len(user))