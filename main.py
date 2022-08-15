from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    date = db.Column(db.DateTime, unique=False, nullable=True)
    date_completed = db.Column(db.Date, unique=False, nullable=False)

    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


## Only run this line once to create databases
db.create_all()

class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    description = StringField("Detailed Description")
    date = DateField("Due Date")
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
        print(request.form.get("date"))
        new_task = Tasks(
            task=request.form.get("task"),
            description=request.form.get("description"),
            date=datetime.strptime(request.form.get("date"), "%Y-%m-%d").date(),
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html', form=form)
    


if __name__ == '__main__':
    app.run(debug=True)
