import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images/users')
    UPLOADED_POSTS_DEST = os.path.join(basedir, 'app/static/images/posts')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'POSTGRE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                'dasdaa13as12SQ'
    BOOTSTRAP_SERVE_LOCAL = True
    # IMAGES_PATH = ["static/images"]

    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMINS = os.environ.get('ADMIN') or ['your-email@example.com']
    POSTS_PER_PAGE = 25

    APP_ID = os.environ.get('APP_ID')
    APP_KEY = os.environ.get('APP_KEY')

