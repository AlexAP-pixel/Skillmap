from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect, Document, StringField
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Conecta a MongoDB
connect('LOGIN', host='mongodb://localhost:27017/', alias='default')

# Define un modelo de usuario
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    hashed_password = generate_password_hash(request.json['password'])
    user = User(username=username, password=hashed_password)
    user.save()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    user = User.objects(username=request.json['username']).first()
    if user and check_password_hash(user.password, request.json['password']):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
