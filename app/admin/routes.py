from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _, lazy_gettext as _l
from flask_images import resized_img_src
from werkzeug.urls import url_parse
from app.admin import bp
from app.admin.forms import LoginForm

from app.models import User


@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    Hight = 1920
    Width = 800

    return 'admin'


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
