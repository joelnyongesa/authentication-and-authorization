from faker import Faker
from random import choice as rc
from app import app
from models import db, Owner, Car

fake = Faker()

with app.app_context():
    Owner.query.delete()
    Car.query.delete()

    owners = []

    for _ in range(20):
        owner = Owner(
            name=fake.name()
        )
        owners.append(owner)
    
    db.session.add_all(owners)


    car_models = [
        "Toyota", "Nissan", "Mercedes", "BMW", "Audi", "Mazda", "Land Rover", "Peugeot", "Volkswagen"
        ]
    
    cars = []

    for _ in range(30):
        car = Car(
            model=rc(car_models),
            owner=rc(owners)
        )

        cars.append(car)
    
    db.session.add_all(cars)
    db.session.commit()