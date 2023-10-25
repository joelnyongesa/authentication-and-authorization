from flask import Flask, make_response, jsonify, request, session
from models import db, Owner, Car
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt

app = Flask(__name__)


app.secret_key = 'qwertyu12345'

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact=False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class CheckSession(Resource):
    def get(self):
        if session.get('owner_id'):
            owner = Owner.query.filter(Owner.id == session['owner_id']).first()
            return owner.to_dict(), 200
        return {"error": "resource not found"}


class SignUp(Resource):
    def post(self):
        name = request.get_json()['name']
        password = request.get_json()['password']

        if name and password:
            new_owner  = Owner(name=name)
            new_owner.password_hash = password

            db.session.add(new_owner)
            db.session.commit()

            session['owner_id'] = new_owner.id

            return new_owner.to_dict(), 201
        
class Login(Resource):
    def post(self):
        name = request.get_json()['name']
        password = request.get_json()['password']

        owner = Owner.query.filter(Owner.name == name).first()
        
        if owner and owner.authenticate(password):
            session['owner_id'] =  owner.id

            owner_dict = owner.to_dict()

            response = make_response(jsonify(owner_dict), 200)

            return response
        
        else:
            return {"error": "owner or password id not correct"}, 401

class Logout(Resource):
    def delete(self):
        if session.get('owner_id'):
            session['owner_id'] = None
            
            return {"info": "user logged out successfully!"}, 200
        
        else:
            return {"error": "unauthorized"}, 401


class Owners(Resource):
    def get(self):
        owners = [owner.to_dict() for owner in Owner.query.all()]

        response = make_response(
            jsonify(owners),
            200
        )

        return response
    
    def post(self):
        new_owner = Owner(
            name=request.get_json()['name']
        )

        db.session.add(new_owner)
        db.session.commit()

        new_owner_dict = new_owner.to_dict()

        response = make_response(
            jsonify(new_owner_dict),
            201
        )

        return response
    
class Cars(Resource):

    def get(self):
        cars = [car.to_dict() for car in Car.query.all()]

        response = make_response(
            jsonify(cars),
            200
        )

        return response
    
    def post(self):
        new_car = Car(
            model=request.get_json()['model'],
            owner_id=request.get_json()['owner_id']
        )

        db.session.add(new_car)
        db.session.commit()

        new_car_dict = new_car.to_dict()

        response = make_response(
            jsonify(new_car_dict),
            201
        )

        return response
    
class OwnerByID(Resource):

    def get(self, id):
        owner = Owner.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(owner),
            200
        )

        return response
    
    def patch(self, id):
        owner = Owner.query.filter_by(id=id).first()

        for attr in request.get_json():
            setattr(owner, attr, request.get_json()[attr])

        db.session.add(owner)
        db.session.commit()

        owner_dict = owner.to_dict()

        response = make_response(
            jsonify(owner_dict),
            200
        )

        return response
    
    def delete(self, id):
        owner = Owner.query.filter_by(id=id).first()

        db.session.delete(owner)
        db.session.commit()

        response = make_response(
            jsonify({"message": "Owner deleted successfully!"}),
            200
        )

        return response
    
class CarsByID(Resource):
    
    def get(self, id):
        car = Car.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(car),
            200
        )

        return response
    
    def patch(self, id):
        car = Car.query.filter_by(id=id).first()

        for attr in request.get_json():
            setattr(car, attr, request.get_json()[attr])

        db.session.add(car)
        db.session.commit()

        car_dict = car.to_dict()

        response = make_response(
            jsonify(car_dict),
            200
        )

        return response
    
    def delete(self, id):
        car = Car.query.filter_by(id=id).first()

        db.session.delete(car)
        db.session.commit()

        response = make_response(
            jsonify({"message": "car deleted successfully!"}),
            200
        )

        return response

api.add_resource(Owners, '/owners', endpoint='owners')
api.add_resource(Cars, '/cars', endpoint='cars')
api.add_resource(OwnerByID, '/owners/<int:id>', endpoint='owners_id')
api.add_resource(CarsByID, '/cars/<int:id>', endpoint='cars_id')
api.add_resource(SignUp, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(CheckSession, '/session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')



if __name__ == "__main__":
    app.run(port=5555, debug=True)