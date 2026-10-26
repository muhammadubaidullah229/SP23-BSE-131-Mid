from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, Student

student_bp = Blueprint('students', __name__)

@student_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def index():
    query = request.args.get('q', '').strip()
    department = request.args.get('department', '').strip()
    status = request.args.get('status', '').strip()

    students_query = Student.query

    if query:
        search_filter = f"%{query}%"
        students_query = students_query.filter(
            (Student.full_name.ilike(search_filter)) | 
            (Student.reg_number.ilike(search_filter)) | 
            (Student.email.ilike(search_filter))
        )

    if department:
        students_query = students_query.filter_by(department=department)

    if status:
        students_query = students_query.filter_by(status=status)

    students = students_query.order_by(Student.id.desc()).all()

    # Get unique departments for filter dropdown
    departments = [d[0] for d in db.session.query(Student.department).distinct().all()]

    return render_template(
        'students/index.html',
        students=students,
        departments=departments,
        selected_dept=department,
        selected_status=status,
        search_query=query
    )

@student_bp.route('/add', methods=['POST'], strict_slashes=False)
@login_required
def add_student():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

    if request.is_json:
        data = request.get_json()
        reg_number = data.get('reg_number', '').strip().upper()
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        department = data.get('department', 'Software Engineering')
        semester = data.get('semester', '1st')
        cgpa = float(data.get('cgpa', 3.0))
        status = data.get('status', 'Active')
    else:
        reg_number = request.form.get('reg_number', '').strip().upper()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', 'Software Engineering')
        semester = request.form.get('semester', '1st')
        try:
            cgpa = float(request.form.get('cgpa', 3.0))
        except ValueError:
            cgpa = 3.0
        status = request.form.get('status', 'Active')

    if not reg_number or not full_name or not email:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Registration number, name, and email are required.'}), 400
        flash('Registration number, name, and email are required.', 'danger')
        return redirect(url_for('students.index'))

    # Check for existing student
    if Student.query.filter_by(reg_number=reg_number).first():
        if is_ajax:
            return jsonify({'success': False, 'message': f'Student with {reg_number} already exists.'}), 400
        flash(f'Student with registration {reg_number} is already enrolled.', 'warning')
        return redirect(url_for('students.index'))

    new_student = Student(
        reg_number=reg_number,
        full_name=full_name,
        email=email,
        department=department,
        semester=semester,
        cgpa=cgpa,
        status=status
    )

    db.session.add(new_student)
    db.session.commit()

    if is_ajax:
        return jsonify({
            'success': True,
            'message': 'Student enrolled successfully!',
            'student': new_student.to_dict()
        }), 201

    flash(f'Student {full_name} ({reg_number}) successfully registered!', 'success')
    return redirect(url_for('students.index'))

@student_bp.route('/<int:student_id>/delete', methods=['POST'], strict_slashes=False)
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    name = student.full_name
    reg = student.reg_number
    db.session.delete(student)
    db.session.commit()

    if is_ajax:
        return jsonify({'success': True, 'message': f'Student {reg} deleted.'})

    flash(f'Student record for {name} ({reg}) has been removed.', 'info')
    return redirect(url_for('students.index'))
