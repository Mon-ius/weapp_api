from app import create_app
from app.models import Answer, Student, Task, Teacher, User
from ext import db
import click
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Student': Student, 'Teacher': Teacher, 'Task': Task, 'Answer': Answer}

if __name__ == '__main__': 
    app.run(debug=True)  
