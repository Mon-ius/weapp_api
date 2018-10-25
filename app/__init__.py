import os
import logging
from flask import Flask, request, current_app
from flask_uploads import configure_uploads, patch_request_class
from ext import db, migrate, bootstrap, Config, login, photos, sphotos, babel
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_restful import Api, Resource, url_for

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  
    migrate.init_app(app, db)  
    bootstrap.init_app(app)  
    babel.init_app(app) 

    login.init_app(app)  
    login.login_view = 'admin.login'

    configure_uploads(app, (photos, sphotos))  
    patch_request_class(app)  

    from app.admin import bp as admin_bp  
    app.register_blueprint(admin_bp)
    
    from app.auth import bp as auth_bp  
    from app.auth.routes import StuAPI, StuListAPI, We_Api

    api_stu = Api(auth_bp)

    api_stu.add_resource(StuListAPI, '/stu')
    api_stu.add_resource(StuAPI, '/stu/<id>')
    api_stu.add_resource(We_Api, '/weapi')
    app.register_blueprint(auth_bp)
    
    from app.main import bp as main_bp  
    from app.main.routes import TaskAPI , TaskListAPI,OpenRes

    api_main = Api(main_bp)

    api_main.add_resource(TaskListAPI, '/tasks')
    api_main.add_resource(TaskAPI, '/tasks/<int:id>')
    api_main.add_resource(OpenRes, '/res')

    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/weapi.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('*'*45)
        app.logger.info('*'*3+'    '*3+'Weapp_API Startup'+'    '*3+'*'*3)
        app.logger.info('*'*45)

        if app.config['ADMIN']:
            app.logger.info('*'*45)
            app.logger.info('*'*3+'    '*3+app.config['ADMIN']+'    '*3+'*'*3)
            app.logger.info('*'*3+'    '*3+app.config['SECRET_KEY']+'    '*3+'*'*3)
            app.logger.info('*'*45)
        
    return app




from app import models

