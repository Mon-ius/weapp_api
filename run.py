from app import create_app
from app.models import Answer, Student, Task, Teacher, User
from ext import db,flag
import click
app = create_app()

if flag:
    admin = User.query.filter_by(username=app.config['ADMINS']).first()
    if not admin:
        admin = User(username=app.config['ADMINS'],email=app.config['ADMINS'],is_admin=True)
        admin.set_password(app.config['SECRET_KEY'])
        db.session.add(admin)
        db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Student': Student, 'Teacher': Teacher, 'Task': Task, 'Answer': Answer}

if __name__ == '__main__': 
    app.run(debug=True)  
