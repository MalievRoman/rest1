import flask
from flask import request, jsonify
from . import db_session
from .jobs import Jobs
from .category import Category
from .users import User

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


# получение всех работ
@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify({'jobs': [item.to_dict() for item in jobs]})


# получение одной работы
@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': jobs.to_dict()
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader_id', 'work_size', 'hazard_category', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.id == request.json['team_leader_id']).first():
        return jsonify({'error': 'I dont know this team_leader'})
    if 'id' in request.json and db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    job = Jobs()
    if 'id' in request.json:
        job.id = request.json['id']
    job.job = request.json['job']
    job.team_leader = request.json['team_leader_id']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.start_date = request.json['start_date']
    job.end_date = request.json['end_date']
    job.is_finished = request.json['is_finished']

    category = Category()
    category.name = request.json['hazard_category']
    job.categories.append(category)

    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_jobs(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader_id', 'work_size', 'hazard_category', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not db_sess.query(Jobs).filter(Jobs.id == request.json['team_leader_id']).first():
        return jsonify({'error': 'I dont know this team_leader'})
    if not job:
        return jsonify({'error': 'There is no such job'})
    job.job = request.json['job']
    job.team_leader = request.json['team_leader_id']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.start_date = request.json['start_date']
    job.end_date = request.json['end_date']
    job.is_finished = request.json['is_finished']

    category = Category()
    category.name = request.json['hazard_category']
    job.categories.append(category)

    db_sess.commit()
    return jsonify({'success': 'OK'})
