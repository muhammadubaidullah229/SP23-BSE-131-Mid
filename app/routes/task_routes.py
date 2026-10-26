from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    
    # Categorize tasks for Kanban view
    pending_tasks = [t for t in tasks if t.status == 'Pending']
    in_progress_tasks = [t for t in tasks if t.status == 'In Progress']
    completed_tasks = [t for t in tasks if t.status == 'Completed']

    return render_template(
        'tasks/index.html',
        tasks=tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks
    )

@task_bp.route('/create', methods=['POST'], strict_slashes=False)
@login_required
def create_task():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

    if request.is_json:
        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        priority = data.get('priority', 'Medium')
        due_date = data.get('due_date', '')
    else:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'Medium')
        due_date = request.form.get('due_date', '')

    if not title:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Task title is required.'}), 400
        flash('Task title cannot be empty.', 'danger')
        return redirect(url_for('tasks.index'))

    new_task = Task(
        title=title,
        description=description,
        status='Pending',
        priority=priority,
        due_date=due_date,
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    if is_ajax:
        return jsonify({
            'success': True,
            'message': 'Task created successfully!',
            'task': new_task.to_dict()
        }), 201

    flash('Task successfully created!', 'success')
    return redirect(url_for('tasks.index'))

@task_bp.route('/<int:task_id>/update-status', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

    if request.is_json:
        new_status = request.get_json().get('status')
    else:
        new_status = request.form.get('status')

    if new_status in ['Pending', 'In Progress', 'Completed']:
        task.status = new_status
        db.session.commit()
        if is_ajax:
            return jsonify({'success': True, 'message': f'Status updated to {new_status}'})
        flash(f'Task marked as {new_status}', 'success')
    else:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        flash('Invalid status update.', 'danger')

    return redirect(url_for('tasks.index'))

@task_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    db.session.delete(task)
    db.session.commit()

    if is_ajax:
        return jsonify({'success': True, 'message': 'Task deleted successfully!'})

    flash('Task deleted successfully.', 'info')
    return redirect(url_for('tasks.index'))
