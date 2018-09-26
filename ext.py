import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from flask_babel import Babel, _, lazy_gettext as _l
from config import Config
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES


from flask_httpauth import HTTPBasicAuth

# VIDEOS = ('mp4','flv','mkv','avi')

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

login = LoginManager()
babel = Babel()
auth = HTTPBasicAuth()


photos = UploadSet('photos', IMAGES)
sphotos = UploadSet('posts', IMAGES)
# videos = UploadSet('videos', VIDEOS)
desc = sqlalchemy.desc
