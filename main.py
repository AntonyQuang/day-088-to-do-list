from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

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
    date = db.Column(db.DateTime, unique=False, nullable=True)

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
    date_completed = db.Column(db.DateTime, unique=False, nullable=False)

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
    date = DateField("Due Date", format='%d/%m/%Y')
    submit = SubmitField("Submit")


@app.route("/")
def home():
    tasks_to_do = Tasks.query.all()
    return render_template("index.html", tasks=tasks_to_do)


if __name__ == '__main__':
    app.run(debug=True)
