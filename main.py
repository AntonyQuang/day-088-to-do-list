from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)


# TODO: bootstrap
# TODO: create website
# TODO: add entry
# TODO: edit entry
# TODO: delete entry
# TODO: move

class Tasks(db.Model):
    __tablename__ = "to_do"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.String(280), unique=False, nullable=True)
    date = db.Column(db.Date, unique=False, nullable=True)

    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class OngoingTasks(db.Model):
    __tablename__ = "ongoing"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.String(280), unique=False, nullable=True)
    date = db.Column(db.Date, unique=False, nullable=True)

    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class CompletedTasks(db.Model):
    __tablename__ = "completed"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.String(280), unique=False, nullable=True)
    date = db.Column(db.Date, unique=False, nullable=True)
    date_completed = db.Column(db.Date, unique=False, nullable=False)

    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


## Only run this line once to create databases
# db.create_all()


class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    description = StringField("Detailed Description")
    date = DateField("Due Date")
    submit = SubmitField("Submit")


class CompletedForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    description = StringField("Detailed Description")
    date = DateField("Due Date")
    date_completed = DateField('Date completed')
    submit = SubmitField("Submit")


@app.route("/")
def home():
    tasks_to_do = Tasks.query.all()
    tasks_ongoing = OngoingTasks.query.all()
    tasks_completed = CompletedTasks.query.all()
    return render_template("index.html", tasks=tasks_to_do, ongoing_tasks=tasks_ongoing, completed_tasks=tasks_completed)


@app.route("/start", methods=["GET", "POST"])
def task_start():
    task_id = request.args.get('id')
    task_selected = Tasks.query.get(task_id)
    db.session.delete(task_selected)
    task_to_add = OngoingTasks(
        task=task_selected.task,
        description=task_selected.description,
        date=task_selected.date,
    )
    db.session.add(task_to_add)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def task_add():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Tasks(
            task=request.form.get("task"),
            description=request.form.get("description"),
            date=datetime.strptime(request.form.get("date"), "%Y-%m-%d").date(),
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html', form=form)
    

@app.route("/complete", methods=["GET", "POST"])
def task_complete():
    task_id = request.args.get('id')
    task_type = request.args.get('type')
    
    if task_type == "todo":
        task_selected = Tasks.query.get(task_id)
    else:
        task_selected = OngoingTasks.query.get(task_id)
    db.session.delete(task_selected)
    task_to_add = CompletedTasks(
        task=task_selected.task,
        description=task_selected.description,
        date=task_selected.date,
        date_completed=date.today(),
    )
    db.session.add(task_to_add)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit", methods=["GET", "POST"])
def task_edit():
    task_id = request.args.get('id')
    task_type = request.args.get('type')

    if task_type == "todo":
        task_to_edit = Tasks.query.get(task_id)
    elif task_type == "ongoing":
        task_to_edit = OngoingTasks.query.get(task_id)
    else:
        task_to_edit = CompletedTasks.query.get(task_id)

    if task_type == "todo" or task_type == "ongoing":
        form = TaskForm(
            task=task_to_edit.task,
            description=task_to_edit.description,
            date=task_to_edit.date
        )
        if form.validate_on_submit():
            task_to_edit.task = request.form["task"]
            task_to_edit.description = request.form["description"]
            task_to_edit.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            db.session.commit()
            return redirect(url_for("home"))

    else:
        form = CompletedForm(
            task=task_to_edit.task,
            description=task_to_edit.description,
            date=task_to_edit.date,
            date_completed=task_to_edit.date_completed
        )

        if form.validate_on_submit():
            task_to_edit.task = request.form["task"]
            task_to_edit.description = request.form["description"]
            task_to_edit.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            task_to_edit.date_completed = datetime.strptime(request.form.get("date_completed"), "%Y-%m-%d").date()
            db.session.commit()
            return redirect(url_for("home"))

    return render_template("edit.html", task=task_to_edit, form=form)


@app.route("/delete", methods=["GET", "POST"])
def task_delete():
    task_id = request.args.get('id')
    task_type = request.args.get('type')

    if task_type == "todo":
        task_to_delete = Tasks.query.get(task_id)
    elif task_type == "ongoing":
        task_to_delete = OngoingTasks.query.get(task_id)
    else:
        task_to_delete = CompletedTasks.query.get(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

#
# if __name__ == '__main__':
#     app.run(debug=True)
