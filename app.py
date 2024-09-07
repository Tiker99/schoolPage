import os

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for

from utils import load_students, save_students, load_events, save_events

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/classrooms')
def classrooms():
    return render_template('classrooms.html')


events = load_events()
@app.route('/events', methods=['GET', 'POST'])
def events_handler():
    if request.method == 'POST':
        # Handle the form submission for adding a new event
        event_name = request.form['name']
        event_date = request.form['date']
        event_location = request.form['location']

        # Add the new event to the events "database"
        new_event_id = max(map(int, events.keys()), default=0) + 1
        events[str(new_event_id)] = {
            'name': event_name,
            'date': event_date,
            'location': event_location
        }

        # Save the updated events list to the JSON file
        save_events(events)

        return redirect(url_for('events_handler'))

    elif request.method == 'GET':
        return render_template('events.html', events=events)

# Directory to store uploaded student photos
# Directory to store uploaded student photos
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

students_data = load_students()

@app.route('/students', defaults={'student_id': None}, methods=['GET', 'POST'])
@app.route('/students/<int:student_id>', methods=['GET'])
def students(student_id):
    if request.method == 'POST':
        # Handle the form submission for adding a new student
        student_name = request.form['name']
        student_grade = request.form['grade']
        
        # Save the uploaded photo
        file = request.files['photo']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            photo_path = f'images/{filename}'  # Save the relative path to the photo

            # Add the new student to the database
            new_student_id = max(map(int, students_data.keys()), default=0) + 1  # Generate new student ID
            students_data[str(new_student_id)] = {
                'name': student_name,
                'grade': student_grade,
                'photo': photo_path
            }

            # Save the updated student list to the JSON file
            save_students(students_data)

        return redirect(url_for('students'))  # Redirect back to the students page

    elif request.method == 'GET':
        if student_id is None:
            # No specific student ID, show all students
            return render_template('students.html', students=students_data)
        else:
            # Specific student ID, show details for that student
            student = students_data.get(str(student_id))
            if student:
                return render_template('student_detail.html', student=students_data)
            else:
                return "Student not found", 404


@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student_handler(student_id):
    student_id_str = str(student_id)
    if student_id_str in students_data:
        del students_data[student_id_str]
        save_students(students_data)
    return redirect(url_for('students'))


@app.route('/teachers')
def teachers():
    return render_template('teachers.html')

if __name__ == '__main__':
    app.run(debug=True)
