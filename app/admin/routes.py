from flask import flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_images import resized_img_src
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.admin import bp
from app.admin.forms import LoginForm
from app.models import User,Student,Teacher,Task,Answer
import base64

@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    students = Student.query.all()
    
    col = ['avatar', 'id', 'username', 'realname',
           'engname', 'email', 'exam_type', 'score','exam_date']

    form = [{k: v.__dict__[k] for k in col} for v in students]
    for i, j in enumerate(form):
        form[i]['avatar'] = "data:image/png;base64," + \
            base64.b64encode(j['avatar']).decode('utf8')
    print(form)
    return render_template('admin/index.html', title=_('Controler'), form=form,student="is-active")

@bp.route('/techer', methods=['GET', 'POST'])
@login_required
def teacher():
    teachers = Teacher.query.all()
    
    col = ['avatar', 'id', 'username', 'engname', 'email',
           'teach_type',   'teach_type_part', 'teach_date']

    form = [{k: v.__dict__[k] for k in col} for v in teachers]
    for i, j in enumerate(form):
        form[i]['avatar'] = "data:image/png;base64," + \
            base64.b64encode(j['avatar']).decode('utf8')
    print(form)
    return render_template('admin/teacher.html', title=_('Controler'), form=form, teacher="is-active")


@bp.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    tasks = Task.query.all()
    
    col = ['picture', 'id',  'teach_id', 'title', 'timestamp']


    form = [{k: v.__dict__[k] for k in col} for v in tasks]

    for i,j in enumerate(form):
        form[i]['picture'] = "data:image/png;base64," + \
            base64.b64encode(j['picture']).decode('utf8')
    # formx = list(map(lambda x:base64.b64encode(x['avatar']),form))

    print(form)
    return render_template('admin/task.html', title=_('Controler'), form=form, task="is-active")


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or not user.is_admin:
            flash(_('Invalid username or password'))
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('admin/login.html', title=_('Fuck In'), form=form)
