from flask_restful import Resource, reqparse, fields, marshal
from passlib.apps import custom_app_context as pwd_context
from flask import abort, url_for

stu_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'realname': fields.String,
    'engname': fields.String,
    'email': fields.String,
    'exam_date': fields.DateTime,
    'exam_type': fields.String,
    'score': fields.Float
}

task_fields = {
    'title': fields.String,
    'body': fields.String,
    'picture': fields.Boolean,
    'author': fields.String,
    'uri': fields.Url('task')
}

tasks_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
}


