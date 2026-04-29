from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Feedback, Complaint, Subject, Faculty, Student, Branch
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    total_feedbacks = Feedback.query.count()
    total_complaints = Complaint.query.count()
    pending_complaints = Complaint.query.filter_by(status='pending').count()
    total_students = Student.query.count()
    
    return render_template('admin/dashboard.html',
                         total_feedbacks=total_feedbacks,
                         total_complaints=total_complaints,
                         pending_complaints=pending_complaints,
                         total_students=total_students)

@admin_bp.route('/feedbacks')
@login_required
def view_feedbacks():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    branch = request.args.get('branch')
    semester = request.args.get('semester')
    subject_id = request.args.get('subject_id')
    
    query = Feedback.query
    
    if branch:
        query = query.join(Student).filter(Student.branch == branch)
    if semester:
        query = query.join(Student).filter(Student.semester == int(semester))
    if subject_id:
        query = query.filter(Feedback.subject_id == int(subject_id))
    
    feedbacks = query.all()
    branches = Branch.query.all()
    subjects = Subject.query.all()
    
    return render_template('admin/feedbacks.html',
                         feedbacks=feedbacks,
                         branches=branches,
                         subjects=subjects)

@admin_bp.route('/complaints')
@login_required
def view_complaints():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    status = request.args.get('status', 'all')
    
    if status == 'all':
        complaints = Complaint.query.all()
    else:
        complaints = Complaint.query.filter_by(status=status).all()
    
    return render_template('admin/complaints.html', complaints=complaints)

@admin_bp.route('/complaint/<int:complaint_id>/resolve', methods=['POST'])
@login_required
def resolve_complaint(complaint_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = 'resolved'
    complaint.resolved_at = db.func.current_timestamp()
    db.session.commit()
    
    flash('Complaint resolved!', 'success')
    return redirect(url_for('admin.view_complaints'))

@admin_bp.route('/analytics')
@login_required
def analytics():
    if current_user.role != 'admin':
        return redirect(url_for('auth.index'))
    
    # Faculty-wise average ratings
    faculty_ratings = db.session.query(
        Faculty.name,
        func.avg(Feedback.rating).label('avg_rating'),
        func.count(Feedback.id).label('feedback_count')
    ).join(Feedback, Faculty.id == Feedback.faculty_id).group_by(Faculty.id).all()
    
    # Subject-wise feedback
    subject_feedback = db.session.query(
        Subject.name,
        func.avg(Feedback.rating).label('avg_rating'),
        func.count(Feedback.id).label('feedback_count')
    ).join(Feedback, Subject.id == Feedback.subject_id).group_by(Subject.id).all()
    
    return render_template('admin/analytics.html',
                         faculty_ratings=faculty_ratings,
                         subject_feedback=subject_feedback)
