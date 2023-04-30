import flask
from flask import request, jsonify
from . import db_session
from .jobs import Jobs
from .category import Category
from .users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


# получение всех юзеров
@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify({'users': [item.to_dict() for item in users]})


# получение одного юзера
@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict()
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == request.json['email']).first():
        return jsonify({'error': 'Email is already used'})
    if 'id' in request.json and db_sess.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    user = User()
    if 'id' in request.json:
        user.id = request.json['id']
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.set_password(request.json['password'])

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if 'id' in request.json and db_sess.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    user.email = request.json['email']
    user.set_password(request.json['password'])
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']

    db_sess.commit()
    return jsonify({'success': 'OK'})
