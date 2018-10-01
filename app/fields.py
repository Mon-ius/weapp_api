from flask import abort, url_for
from flask_restful import Resource, fields, marshal, reqparse
from passlib.apps import custom_app_context as pwd_context

stu_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'nickname': fields.String,
    'realname': fields.String,
    'engname': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'exam_date': fields.DateTime,
    'exam_type': fields.String,
    'score': fields.Float,
    'avatar': fields.String
}

task_fields = {
    'title': fields.String,
    'body': fields.String,
    'picture': fields.String,
    'author': fields.String,
    # 'uri': fields.Url('task')
}

tasks_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'done': fields.Boolean,
}
