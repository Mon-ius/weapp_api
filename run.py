from app import create_app

from ext import db
from app.models import User,Student, Teacher, Task,Answer


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Student': Student, 'Teacher': Teacher, 'Task': Task, 'Answer': Answer}

if __name__ == '__main__': 
    app.run(debug=True)  
