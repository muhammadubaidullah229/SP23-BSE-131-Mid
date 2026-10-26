from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='Student')  # Student, Faculty, Administrator
    reg_number = db.Column(db.String(50), default='SP23-BSE-131')
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(80), nullable=False)  # Software Engineering, Computer Science, etc.
    semester = db.Column(db.String(20), default='7th', nullable=False)
    cgpa = db.Column(db.Float, default=3.5, nullable=False)
    status = db.Column(db.String(20), default='Active', nullable=False)  # Active, Graduated, On Leave
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'reg_number': self.reg_number,
            'full_name': self.full_name,
            'email': self.email,
            'department': self.department,
            'semester': self.semester,
            'cgpa': self.cgpa,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f'<Student {self.reg_number} - {self.full_name}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g. CSC418
    title = db.Column(db.String(150), nullable=False)  # e.g. Cloud Computing & DevOps
    credit_hours = db.Column(db.Integer, default=3, nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(80), nullable=False)

    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.code}: {self.title}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.String(20), default='Fall 2026')
    grade = db.Column(db.String(5), default='In Progress')  # A, B+, B, C, In Progress
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
