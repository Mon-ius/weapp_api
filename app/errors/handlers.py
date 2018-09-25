from flask import render_template, make_response
from flask_babel import _, lazy_gettext as _l
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
    # return make_response(jsonify({'error': 'Not found'}), 404)


@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500



