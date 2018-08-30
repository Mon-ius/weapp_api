from flask import (abort, flash, g, jsonify, redirect, render_template,
                   request, url_for)
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_images import resized_img_src
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, reqparse, fields, marshal
from app.auth import bp
from app.models import Student
from ext import db,auth
from app.fields import stu_fields


def abort_if_stu_doesnt_exist(id):
    stu = Student.query.get(id)
    if not stu:
        abort(400, "Stu {} doesn't exist".format(id))
    return stu


class StuAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str, location='json')
        self.reqparse.add_argument(
            'password', type=str, location='json')
        super(StuAPI, self).__init__()

    @auth.login_required
    def get(self, id):
        stu = abort_if_stu_doesnt_exist(id)
        return {'task': marshal(stu, stu_fields)}

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

    @auth.verify_password
    def put(self):
        args = self.reqparse.parse_args()
        username_or_token = args['username']
        password = args['password']

        stu = Student.verify_auth_token(username_or_token)
        if not stu:
            # try to authenticate with username/password
            stu = Student.query.filter_by(username=username_or_token).first()
            if not stu or not stu.verify_password(password):
                return False
        g.stu = stu
        return True

    @auth.login_required
    def delete(self):
        token = g.stu.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}
