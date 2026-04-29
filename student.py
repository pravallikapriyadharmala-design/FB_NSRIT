from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Subject, Student, Feedback, Complaint, Faculty, Branch
from sqlalchemy import func

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('auth.index'))
    
    student = current_user.student
    
    # Get the branch by code/name
    branch = Branch.query.filter_by(code=student.branch).first()
    if not branch:
        # Try by full name
        branch = Branch.query.filter(Branch.name.like(f'%{student.branch}%')).first()
    
    if branch:
        subjects = Subject.query.filter_by(
            branch_id=branch.id,
            semester=student.semester
        ).all()
    else:
        subjects = []
    
    feedback_count = Feedback.query.filter_by(student_id=student.id).count()
    
    return render_template('student/dashboard.html', 
                         subjects=subjects, 
                         feedback_count=feedback_count)

@student_bp.route('/feedback/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def give_feedback(subject_id):
    if current_user.role != 'student':
        return redirect(url_for('auth.index'))
    
    subject = Subject.query.get_or_404(subject_id)
    student = current_user.student
    
    # Check if feedback already submitted
    existing_feedback = Feedback.query.filter_by(
        student_id=student.id,
        subject_id=subject_id
    ).first()
    
    if existing_feedback:
        flash('You have already submitted feedback for this subject!', 'info')
        return redirect(url_for('student.dashboard'))
    
    if request.method == 'POST':
        feedback = Feedback(
            student_id=student.id,
            subject_id=subject_id,
            faculty_id=subject.faculty_id,
            rating=int(request.form.get('rating', 3)),
            content_quality=int(request.form.get('content_quality', 3)),
            teaching_method=int(request.form.get('teaching_method', 3)),
            communication=int(request.form.get('communication', 3)),
            feedback_text=request.form.get('feedback_text', '')
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/feedback_form.html', subject=subject)

@student_bp.route('/complaint', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if current_user.role != 'student':
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        from flask import request
        complaint = Complaint(
            student_id=current_user.student.id,
            title=request.form.get('title'),
            description=request.form.get('description')
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/complaint_form.html')

@student_bp.route('/my-complaints')
@login_required
def my_complaints():
    if current_user.role != 'student':
        return redirect(url_for('auth.index'))
    
    complaints = Complaint.query.filter_by(student_id=current_user.student.id).all()
    return render_template('student/my_complaints.html', complaints=complaints)
