from flask import (abort, flash, g, jsonify, redirect, render_template, make_response,
                   request, url_for)
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_images import resized_img_src
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, fields, marshal, reqparse

from app.auth import bp
from app.fields import stu_fields
from app.models import Student
from ext import auth, db


def abort_if_stu_doesnt_exist(id):
    stu = Student.query.get(id)
    if not stu:
        abort(400, "Stu {} doesn't exist".format(id))
    return stu

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@auth.verify_password
def verify_password(username_or_token, password):
    stu = Student.verify_auth_token(username_or_token)
    if not stu:
        # try to authenticate with username/password
        stu = Student.query.filter_by(username=username_or_token).first()
        if not stu or not stu.verify_password(password):
            return False
    g.stu = stu
    return True

class StuAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str, location='json')
        self.reqparse.add_argument(
            'realname', type=str, location='json')
        self.reqparse.add_argument(
            'engname', type=str, location='json')
        self.reqparse.add_argument(
            'exam_date', type=str, location='json')
        self.reqparse.add_argument(
            'exam_type', type=str, location='json')
        self.reqparse.add_argument(
            'score', type=str, location='json')
        super(StuAPI, self).__init__()

    def get(self, id):
        stu = abort_if_stu_doesnt_exist(id)
        return {'Student': marshal(stu, stu_fields)}

    def post(self,id):
        stu = abort_if_stu_doesnt_exist(id)
        print(stu)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                stu.__dict__[k] = v

        print(stu.__dict__)
        db.session.merge(stu)
        return {'student': marshal(stu, stu_fields)}


    def delete(self):
        token = g.stu.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}

class StuListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str, location='json')
        self.reqparse.add_argument(
            'password', type=str, location='json')
        super(StuListAPI, self).__init__()

    @auth.login_required
    def get(self):
        ss = Student.query.all()
        if not len(ss):
            abort(400, "Student doesn't exist")

        students = list(map(lambda x: marshal(x.__dict__, stu_fields), ss))
        return {'students': students}

    def post(self):##Need changed
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        if username is None or password is None:
            abort(400)
        if Student.query.filter_by(username=username).first() is not None:
            abort(400)
        stu = Student(username=username)
        stu.hash_password(password)
        db.session.add(stu)
        db.session.commit()
        return {
            'username': username
        }


