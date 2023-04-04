from app import app, db
from app.models import User, ActiveTask
from app.forms import LoginForm, SignupForm, TaskForm, \
    EditTaskForm, TakeForm, DeleteForm, EditTaskForm_mod

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from sqlalchemy import text

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignupForm()

    if form.validate_on_submit():
        if form.password.data != form.confirmPassword.data:
            return render_template("signup.html", form=form)

        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            login=form.login.data,
            email=form.email.data,
            password_hash=form.email.data,
        )

        user.set_password(form.password.data)
        user.set_accountype(form.accountype.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user is None or not user.check_password(form.password.data):
            return redirect(url_for("login"))

        login_user(user, remember=1)

        return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/account", methods=["GET", "POST"])
def account():
    
    taskForm = TaskForm()
    editTaskForm = EditTaskForm()

    tasks = ActiveTask.query.filter_by(executor_login=current_user.login).all()
    arch_tasks = ActiveTask.query.filter_by().all()

    if taskForm.validate_on_submit():

        task = ActiveTask(
            consumer_login=current_user.login,
            description=taskForm.description.data,
            comments=taskForm.comments.data,
            status="Зарегистрирована",
            deadline="Не установлен"
        )


        db.session.add(task)
        db.session.commit()

        return redirect(url_for("account"))

    if editTaskForm.validate_on_submit():

        task_id = request.form.get("lastname")
        task_db = ActiveTask.query.get(int(task_id))

        task_db.status = editTaskForm.status.data
        task_db.deadline = editTaskForm.deadline.data

        if editTaskForm.status.data == "Выполнена":
            print(1)
        print(task_db.deadline)

        db.session.commit()

        return redirect(url_for("account"))

    return render_template(
        "account.html",
        tasks=tasks,
        arch_tasks=arch_tasks,
        taskForm=taskForm,
        editTaskForm=editTaskForm
    )

@app.route("/loginedTasks_mod", methods=["GET", "POST"])
def loginedTasks_mod():

    if not current_user.is_moderator():
        return redirect(url_for('loginedTasks'))
    
    editTaskForm = EditTaskForm_mod()
    deleteForm = DeleteForm()

    tasks = ActiveTask.query.all()

    if editTaskForm.validate_on_submit():

        task_id = request.form.get("tid")

        if task_id != None:

            task_db = ActiveTask.query.get(int(task_id))

            task_db.status = editTaskForm.status.data

            if editTaskForm.status.data == "Выполнена":
                pass

            db.session.commit()

            return redirect(url_for("loginedTasks_mod"))
    
    if deleteForm.validate_on_submit():

        task_id = request.form.get("tid")
        print(task_id)

        if task_id != None:

            task_db = ActiveTask.query.filter_by(id=int(task_id)).delete()
            db.session.commit()

            return redirect(url_for('loginedTasks_mod'))

    return render_template(
        "loginedTasks_mod.html",
        editTaskForm=editTaskForm,
        deleteForm=deleteForm,
        tasks=tasks
    )

@app.route("/recovery")
def recovery():
    return render_template("recovery.html")

@app.route("/loginedTasks", methods=["GET", "POST"])
def loginedTasks():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if current_user.is_moderator():
        return redirect(url_for('loginedTasks_mod'))
    
    taskForm = TaskForm()
    takeForm = TakeForm()

    tasks = ActiveTask.query.all()

    if taskForm.validate_on_submit():

        task = ActiveTask(
            consumer_login=current_user.login,
            description=taskForm.description.data,
            comments=taskForm.comments.data,
            status="Зарегистрирована",
            deadline="Не установлен"
        )

        db.session.add(task)
        db.session.commit()

        return redirect(url_for("loginedTasks"))

    if takeForm.validate_on_submit():

        task_id = request.form.get('tid')

        if task_id != None:
            task_db = ActiveTask.query.get(int(task_id))

            if task_db == None:
                redirect(url_for("loginedTasks"))
            else:
                task_db.executor_login = current_user.login
                task_db.status = "Принята в обработку"

                db.session.commit()

        return redirect(url_for("account"))        

    arch_tasks = ArchivedTask.query.all()

    return render_template(
        "loginedTasks.html",
        tasks=tasks,
        arch_tasks=arch_tasks,
        taskForm=taskForm,
        takeForm=takeForm
    )

@app.route("/unloginedTasks")
def unloginedTasks():

    tasks = ActiveTask.query.all()
    arch_tasks = ArchivedTask.query.all()

    return render_template(
        "unloginedTasks.html",
        tasks=tasks,
        arch_tasks=arch_tasks
    )
