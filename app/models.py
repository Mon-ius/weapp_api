
from datetime import datetime, timedelta, timezone
from hashlib import md5
from time import time

import jwt
from flask import abort, current_app, url_for, current_app
from flask_httpauth import HTTPBasicAuth
from flask_login import UserMixin
from flask_restful import Resource, fields, marshal, reqparse
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import check_password_hash, generate_password_hash

from ext import db, desc, login

#Teacher is not neeeded

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):  # 用户 ORM注册
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


ass = db.Table('ass',
                     db.Column('stu_id', db.Integer,
                               db.ForeignKey('student.id')),
                     db.Column('teach_id', db.Integer,
                               db.ForeignKey('teacher.id'))
                     )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    realname = db.Column(db.String(64))
    engname = db.Column(db.String(64))

    password_hash = db.Column(db.String(128))

    email = db.Column(db.String(120), index=True, unique=True)
    exam_date = db.Column(db.DateTime, default=datetime.utcnow)
    exam_type = db.Column(db.String(64))
    score = db.Column(db.Float(5))
    avatar = db.Column(db.LargeBinary)

    # teach_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teachers = db.relationship(
        'Teacher', secondary=ass, lazy='dynamic')

    answers = db.relationship('Answer', backref='stu', lazy='dynamic')

    def __repr__(self):
        return '<Student {}>'.format(self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    engname = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    email = db.Column(db.String(120), index=True, unique=True)
    teach_type = db.Column(db.String(64))
    teach_date = db.Column(db.DateTime, default=datetime.utcnow)
    teach_type_part = db.Column(db.String(64))
    avatar = db.Column(db.LargeBinary)

    students = db.relationship(
        'Student', secondary=ass, lazy='dynamic')

    tasks = db.relationship('Task', backref='teach', lazy='dynamic')

    def __repr__(self):
        return '<Teacher {}>'.format(self.username)

    def teach(self,student):
        if not self.is_teaching(student):
            self.students.append(student)

    def unteach(self,student):
        if  self.is_teaching(student):
            self.students.remove(student)

    def is_teaching(self, student):
        return self.students.filter(ass.c.stu_id == student.id).count() > 0

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    picture = db.Column(db.LargeBinary)
    # sound = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship('Answer', backref='parent', lazy='dynamic')
    teach_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return '<Task {}>'.format(self.title)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    picture = db.Column(db.LargeBinary)
    sound = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    stu_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<Anwser {}>'.format(self.title)
