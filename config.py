import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images/users')
    UPLOADED_POSTS_DEST = os.path.join(basedir, 'app/static/images/posts')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                'you-will-never-guess-key'
    BOOTSTRAP_SERVE_LOCAL = True
    IMAGES_PATH = ["static/images"]

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 25