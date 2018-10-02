from flask import abort, flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, fields, marshal, reqparse

from app.fields import task_fields, tasks_fields
from app.main import bp
from app.models import Task
from ext import auth, db


def abort_if_task_doesnt_exist(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        abort(400, "Task {} doesn't exist".format(id))
    return task

class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('body', type=str, location='json')
        self.reqparse.add_argument('picture', type=str, location='json')

        super(TaskAPI, self).__init__()

    def get(self, id):
        task = abort_if_task_doesnt_exist(id)
        return {'task': marshal(task, task_fields)}

    def put(self, id):
        task = abort_if_task_doesnt_exist(id)
        print(task)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                task.__setattr__(k,v)

        print(task.__dict__)
        db.session.commit()
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = abort_if_task_doesnt_exist(id)
        db.session.delete(task)
        db.session.commit()
        return {'result': True}


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument(
            'body', type=str, default="", location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        ts = Task.query.all()
        if not len(ts):
            abort(400, "Tasks doesn't exist")
        # for i in ts:

        task = list(map(lambda x: marshal(x.__dict__, tasks_fields), ts))

        return {'tasks': task}

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        t = Task(**args)
        # g.teach.tasks.append(t)
        # print(t)
        db.session.add(t)
        db.session.commit()
        # print(t.__dict__)
        args['id']=len(Task.query.all())

        return {'task': marshal(args, tasks_fields)}


class OpenRes(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'id', type=str, location='json')
        super(OpenRes, self).__init__()

    def get(self):

        return {'message': "get success"}
        

    def post(self):
        args = self.reqparse.parse_args()
        message = args['id']

        return {'message': message}

    def put(self):
        args = self.reqparse.parse_args()
        message = args['id']

        return {'message': "put success"}

    def delete(self):
        return {'message': "delete success"}
