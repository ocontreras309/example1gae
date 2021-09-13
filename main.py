from datetime import datetime
from flask import Flask, render_template, request

from google.cloud import ndb

app = Flask(__name__)
client = ndb.Client()

def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with client.context():
            return wsgi_app(environ, start_response)

    return middleware

app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)  # Wrap the app in middleware.

class Student(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    semester = ndb.IntegerProperty()
    city = ndb.StringProperty()
    birth_date = ndb.DateProperty()


@app.route('/poststudent', methods=['POST'])
def post_student():
    student = Student()
    student.first_name = request.form['first_name']
    student.last_name = request.form['last_name']
    student.city = request.form['city']
    student.semester = int(request.form['semester'])
    student.birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')

    student.put()
    return render_template('studentconfirmation.html')
    

@app.route('/', methods=['GET'])
def index():
    students = Student.query()
    return render_template('index.html', students=students)

@app.route('/newstudent', methods=['GET'])
def student_form():
    return render_template('newstudent.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# [END ndb_flask]
