from flask import Flask,jsonify
from flask_restful import Api
from resources.emp import Emp,Emplogin
from flask_jwt_extended import JWTManager

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='https'
app.config['JWT_SECRET_KEY']='coscinternshipdrive'
api=Api(app)
jwt=JWTManager(app)

@jwt.unauthorized_loader
def missingtoken(error):
    return jsonify({
    'error':'authorization-required',
    'description':'didnot provide accesstoken'
    }),403

@jwt.invalid_token_loader
def invalidtoken(error):
    return jsonify({
    'error':'invalidtoken',
    'description':'Signature verification failed'
    }),401

api.add_resource(Emp,'/emp')
api.add_resource(Emplogin,'/login')

if __name__ == "__main__":
    app.run()
