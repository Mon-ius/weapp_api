import base64

import requests
from flask import (abort, current_app, flash, g, jsonify, make_response,
                   redirect, render_template, request, url_for)
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, fields, marshal, reqparse

from app.auth import bp
from app.fields import stu_fields
from app.models import Student
from ext import auth, db


def abort_if_stu_doesnt_exist(id):
    stu = Student.query.filter_by(username=id).first()
    print("--- Find user : "+ stu.username)
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
    print("--- Login user : " + stu.username)
    g.stu = stu
    return True


class StuAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str, location='json')
        self.reqparse.add_argument(
            'nickname', type=str, location='json')
        self.reqparse.add_argument(
            'realname', type=str, location='json')
        self.reqparse.add_argument(
            'engname', type=str, location='json')
        self.reqparse.add_argument(
            'email', type=str, location='json')
        self.reqparse.add_argument(
            'phone', type=str, location='json')
        self.reqparse.add_argument(
            'exam_type', type=str, location='json')
        self.reqparse.add_argument(
            'score', type=str, location='json')
        self.reqparse.add_argument(
            'avatar', type=str, location='json')
        super(StuAPI, self).__init__()

    def get(self, id):
        stu = abort_if_stu_doesnt_exist(id)
        return {'Student': marshal(stu, stu_fields)}

    def put(self, id):
        stu = abort_if_stu_doesnt_exist(id)

        print("--- PUT user : " + stu.username)
        print("--- PUT current user : " + stu.username)
        args = self.reqparse.parse_args()
        if stu != g.stu:
            print(g.stu)
            print(stu)
            return {
                'student': marshal(stu, stu_fields),
                'error': "failed,not owner"
            }
        print(args)
        for k, v in args.items():
            if v != None:
                stu.__setattr__(k, v)

        if stu.avatar:
            stu.__setattr__("avatar", base64.b64decode(
                stu.avatar.encode('utf8')))

        db.session.commit()
        return {'student': marshal(stu, stu_fields)}

    def delete(self, id):
        if g.stu.username == "monius":
            stu = abort_if_stu_doesnt_exist(id)
            db.session.delete(stu)
            db.session.commit()
            return {'result': True}
        return {'result': False}


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

    def post(self):  # Need changed
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        print("CREATE")
        print(username,password)
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

    @auth.login_required
    def delete(self):
        print(g.stu)
        # token = g.stu.generate_auth_token(600)
        token = g.stu.generate_auth_token()
        return {'token': token.decode('ascii'), 'duration': 600}


class We_Api(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'js_code', type=str, required=True, help='No js code provided', location='json')

        super(We_Api, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        appid = current_app.config['APP_ID']
        secret = current_app.config['APP_KEY']

        js_code = args['js_code']
        print("--- weapp appid :"+ appid)
        print("--- weapp js_code :" + js_code)

        if js_code is None:
            abort(400)

        tmp = {}
        data = {
            "appid": appid,
            "secret": secret,
            "js_code": js_code,
            "grant_type": "grant_type"
        }
        
        url = "https://api.weixin.qq.com/sns/jscode2session"
        r = requests.get(url, params=data)

        if r.status_code == 200:
            tmp = r.json()
            # print(tmp)
            # tmp['openid']=js_code
            # tmp['expires_in']=233
            if not "expires_in" in tmp.keys() or not "openid" in tmp.keys():
                print("nonononono")
                return tmp
            stu = Student.query.filter_by(username=tmp['openid']).first()
            print(stu)
            if stu is None:
                stu = Student(username=tmp['openid'])
                stu.hash_password(tmp['openid'][:-2])
                db.session.add(stu)
                db.session.commit()
            
            
            session_value = stu.generate_auth_token()
            tmp['session_value'] = session_value.decode('ascii')
            return tmp

        return {
            'js_code': js_code,
            'error': True
        }
