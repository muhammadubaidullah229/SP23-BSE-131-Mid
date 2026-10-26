from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Course

course_bp = Blueprint('courses', __name__)

@course_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def index():
    courses = Course.query.order_by(Course.code.asc()).all()
    return render_template('courses/index.html', courses=courses)

@course_bp.route('/add', methods=['POST'], strict_slashes=False)
@login_required
def add_course():
    code = request.form.get('code', '').strip().upper()
    title = request.form.get('title', '').strip()
    instructor = request.form.get('instructor', '').strip()
    department = request.form.get('department', 'Software Engineering')
    credit_hours = int(request.form.get('credit_hours', 3))

    if not code or not title or not instructor:
        flash('Course code, title, and instructor are required.', 'danger')
        return redirect(url_for('courses.index'))

    if Course.query.filter_by(code=code).first():
        flash(f'Course code {code} already exists.', 'warning')
        return redirect(url_for('courses.index'))

    new_course = Course(
        code=code,
        title=title,
        instructor=instructor,
        department=department,
        credit_hours=credit_hours
    )
    db.session.add(new_course)
    db.session.commit()

    flash(f'Course {code}: {title} successfully added to catalog.', 'success')
    return redirect(url_for('courses.index'))
