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

    def post(self):
        args = self.reqparse.parse_args()
        

    def put(self, id):
        task = abort_if_task_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                task[k] = v
        db.session.save(task)
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
            'description', type=str, default="", location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        task = [t for t in tasks.find({'id': {"$gt": 0}})]
        if not len(task):
            abort(400, "Tasks doesn't exist")
        task = list(map(lambda x: marshal(x, tasks_fields), task))

        return {'tasks': task}

    def post(self):

        t = {
            'id': None,
            'title': None,
            'description': None,
            'done': False
        }

        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                t[k] = v
        t['id'] = tasks.count()+1
        # t['id']=30
        tasks.insert(t)
        return {'task': marshal(t, tasks_fields)}