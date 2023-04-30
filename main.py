from flask import Flask
from data import db_session, jobs_api, users_api
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.category import Category
from datetime import datetime
from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_wtf import FlaskForm
from forms.user import RegisterForm, LoginForm
from forms.job import JobForm
from forms.department import DepartmentForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def base():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        data = []
        for job in db_sess.query(Jobs).all():
            job_id = job.id
            title = job.job
            time = f'{job.work_size} hours'
            team_leader = job.user.surname + ' ' + job.user.name
            collaborators = job.collaborators if job.collaborators else "Alone"
            finish = job.is_finished
            team_lead_id = job.user.id
            lvl = ", ".join([str(i.name) for i in job.categories]) if len(job.categories) else ""
            data.append([job_id, title, team_leader, time, collaborators, finish, team_lead_id, lvl])
        return render_template('jobs_table.html', params=data)
    else:
        return render_template('base.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            address=form.address.data,
            speciality=form.speciality.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.work_size = form.w_size.data
        jobs.collaborators = form.collab.data
        jobs.start_date = form.start.data
        jobs.end_date = form.end.data
        jobs.is_finished = form.finish.data
        jobs.team_leader = current_user.id
        for i in map(int, form.hazard_category.data):
            cat = Category()
            cat.name = i
            jobs.categories.append(cat)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')

    return render_template('jobs.html', title='Добавление работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            form.title.data = jobs.job
            form.w_size.data = jobs.work_size
            form.collab.data = jobs.collaborators
            form.start.data = jobs.start_date
            form.end.data = jobs.end_date
            form.finish.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            jobs.job = form.title.data
            jobs.work_size = form.w_size.data
            jobs.collaborators = form.collab.data
            jobs.start_date = form.start.data
            jobs.end_date = form.end.data
            jobs.is_finished = form.finish.data
            for i in map(int, form.hazard_category.data):
                cat = Category()
                cat.name = i
                jobs.categories.append(cat)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html', title='Редактирование работы', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def list_departs():
    db_sess = db_session.create_session()
    res = db_sess.query(Department).all()
    return render_template('departments.html', departs=res)


@app.route('/add_dep', methods=['GET', 'POST'])
@login_required
def add_depar():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = Department()
        depart.title = form.title.data
        depart.members = form.members.data
        depart.chief = current_user.id
        depart.email = form.email_dep.data
        db_sess.add(depart)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_depart.html', title='Добавление департамента', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id,
                                               ((Department.user == current_user) | (current_user.id == 1))).first()
        if dep:
            form.title.data = dep.title
            form.email_dep.data = dep.email
            form.members.data = dep.members
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id,
                                               ((Department.user == current_user) | (current_user.id == 1))).first()
        if dep:
            dep.title = form.title.data
            dep.email = form.email_dep.data
            dep.members = form.members.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_depart.html', title='Редактирование департамента', form=form)


@app.route('/dep_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id,
                                           ((Department.user == current_user) | (current_user.id == 1))).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/users_show/<int:user_id>')
def user_show(user_id):
    response_1 = get(f'http://127.0.0.1:8080/api/users/{user_id}').json().get('user')
    pos = ",".join(
        get(f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={response_1["city_from"]}&format=json').json()[
            'response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())
    map_params = {
        "ll": pos,
        "l": 'sat',
        "z": '13'
    }
    response = get("http://static-maps.yandex.ru/1.x/", params=map_params)
    with open("static/img/map.png", mode="wb") as file:
        file.write(response.content)
    return render_template('nostalgia.html', params=response_1)


if __name__ == '__main__':
    db_session.global_init("db/blogs2.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
