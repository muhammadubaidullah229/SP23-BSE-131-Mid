import os
from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.models import db, User, Student, Course, Enrollment

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access the Student Portal.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def seed_initial_data():
    """Seeds realistic university student and course records if database is empty"""
    if User.query.count() == 0:
        admin_user = User(
            username='admin',
            email='admin@university.edu.pk',
            full_name='Dr. M. Hasanain Ch',
            role='Administrator',
            reg_number='FA22-FAC-001'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)

        student_user = User(
            username='student',
            email='sp23-bse-131@university.edu.pk',
            full_name='Muhammad Hamza (SP23-BSE-131)',
            role='Student',
            reg_number='SP23-BSE-131'
        )
        student_user.set_password('student123')
        db.session.add(student_user)

    if Student.query.count() == 0:
        students_data = [
            Student(reg_number='SP23-BSE-131', full_name='Muhammad Hamza', email='sp23-bse-131@university.edu.pk', department='Software Engineering', semester='7th', cgpa=3.82, status='Active'),
            Student(reg_number='FA22-BCS-045', full_name='Ayesha Tariq', email='fa22-bcs-045@university.edu.pk', department='Computer Science', semester='7th', cgpa=3.65, status='Active'),
            Student(reg_number='SP23-BSE-019', full_name='Bilal Ahmed', email='sp23-bse-019@university.edu.pk', department='Software Engineering', semester='7th', cgpa=3.41, status='Active'),
            Student(reg_number='FA23-BAI-088', full_name='Zainab Fatima', email='fa23-bai-088@university.edu.pk', department='Artificial Intelligence', semester='5th', cgpa=3.91, status='Active'),
            Student(reg_number='SP22-BCS-112', full_name='Usman Khan', email='sp22-bcs-112@university.edu.pk', department='Computer Science', semester='8th', cgpa=3.28, status='Graduated'),
            Student(reg_number='FA23-BCY-034', full_name='Danish Ali', email='fa23-bcy-034@university.edu.pk', department='Cyber Security', semester='5th', cgpa=3.55, status='Active'),
        ]
        db.session.add_all(students_data)

    if Course.query.count() == 0:
        courses_data = [
            Course(code='CSC418', title='DevOps for Cloud Computing', credit_hours=3, instructor='Dr. M. Hasanain Ch', department='Software Engineering'),
            Course(code='CSC339', title='Software Design & Architecture', credit_hours=3, instructor='Dr. Farhan Riaz', department='Software Engineering'),
            Course(code='CSC471', title='Distributed Systems & Microservices', credit_hours=3, instructor='Prof. Sajjad Mohsin', department='Computer Science'),
            Course(code='AI302', title='Deep Learning & Neural Networks', credit_hours=4, instructor='Dr. Samina Khalid', department='Artificial Intelligence'),
            Course(code='SEC410', title='Network Security & Cryptography', credit_hours=3, instructor='Engr. Tariq Mehmood', department='Cyber Security'),
        ]
        db.session.add_all(courses_data)

    db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.course_routes import course_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/students')
    app.register_blueprint(course_bp, url_prefix='/courses')

    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app
