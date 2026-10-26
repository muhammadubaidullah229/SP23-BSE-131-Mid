from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import db, Student, Course, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    featured_courses = Course.query.limit(4).all()
    total_students = Student.query.count()
    total_courses = Course.query.count()
    return render_template('home.html', featured_courses=featured_courses, total_students=total_students, total_courses=total_courses)

@main_bp.route('/health')
def health_check():
    """Health check endpoint required by AWS Application Load Balancer Target Group"""
    db_status = "healthy"
    try:
        db.session.execute(db.text('SELECT 1'))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'app_name': 'EduCore Student Management System',
        'reg_number': 'SP23-BSE-131',
        'database': db_status
    }), 200 if db_status == 'healthy' else 500

@main_bp.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()
    courses = Course.query.all()

    total_students = len(students)
    active_students = sum(1 for s in students if s.status == 'Active')
    total_courses = len(courses)
    
    # Calculate Average CGPA
    avg_cgpa = round(sum(s.cgpa for s in students) / total_students, 2) if total_students > 0 else 0.0

    # Department distribution
    dept_counts = {}
    for s in students:
        dept_counts[s.department] = dept_counts.get(s.department, 0) + 1

    # Top performing students
    top_students = Student.query.order_by(Student.cgpa.desc()).limit(5).all()

    return render_template(
        'dashboard/index.html',
        total_students=total_students,
        active_students=active_students,
        total_courses=total_courses,
        avg_cgpa=avg_cgpa,
        dept_counts=dept_counts,
        top_students=top_students
    )
