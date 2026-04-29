import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app import create_app, db
from app.models import Branch, Subject, Faculty, User

app = create_app()

BRANCHES_DATA = {
    'CSE': 'Computer Science & Engineering',
    'CSE-AI&ML': 'CSE - AI & Machine Learning',
    'CSE-DS': 'CSE - Data Science',
    'ECE': 'Electronics & Communication Engineering',
    'EEE': 'Electrical & Electronics Engineering',
    'Mechanical': 'Mechanical Engineering',
    'Civil': 'Civil Engineering'
}

SUBJECTS_DATA = {
    1: {
        'common': [
            ('Linear Algebra and Calculus', 'LAC', 'theory'),
            ('Engineering Physics', 'EP', 'theory'),
            ('Engineering Chemistry', 'EC', 'theory'),
            ('Basics of Civil and Mechanical Engineering', 'BCME', 'theory'),
            ('Engineering Graphics', 'EG', 'theory'),
            ('Problem Solving Using C', 'PSC', 'theory'),
            ('Physics Lab', 'PL', 'lab'),
            ('Chemistry Lab', 'CL', 'lab'),
            ('C Programming Lab', 'CPL', 'lab'),
            ('Engineering Workshop Practice', 'EWP', 'lab'),
        ]
    },
    2: {
        'common': [
            ('Differential Equations & Vector Calculus', 'DEVC', 'theory'),
            ('Engineering Chemistry / Physics', 'ECP', 'theory'),
            ('Basic Electronics and Electrical Engineering', 'BEEE', 'theory'),
            ('Data Structures', 'DS', 'theory'),
            ('Electrical and Electronics Workshop', 'EEW', 'lab'),
            ('Data Structures Lab', 'DSL', 'lab'),
            ('Chemistry Lab / Physics Lab', 'CL/PL', 'lab'),
            ('NSS / NCC / Sports / Yoga', 'NSS', 'mandatory'),
            ('Skill Development Course', 'SDC-I', 'mandatory'),
            ('Constitution of India', 'CI', 'mandatory'),
        ]
    },
    3: {
        'common': [
            ('Environmental Science', 'ES', 'theory'),
            ('Universal Human Values', 'UHV', 'theory'),
        ],
        'CSE': [
            ('Discrete Mathematics', 'DM', 'theory'),
            ('Digital Logic Design', 'DLD', 'theory'),
            ('Data Structures & Algorithms', 'DSA', 'theory'),
            ('Object Oriented Programming through Java', 'OOP', 'theory'),
            ('Digital Logic Design Lab', 'DLDL', 'lab'),
            ('Data Structures & Algorithms Lab', 'DSAL', 'lab'),
            ('Java Programming Lab', 'JPL', 'lab'),
        ],
        'CSE-AI&ML': [
            ('Discrete Mathematics', 'DM', 'theory'),
            ('Digital Logic Design', 'DLD', 'theory'),
            ('Data Structures & Algorithms', 'DSA', 'theory'),
            ('Python Programming for AI', 'PPA', 'theory'),
            ('Digital Logic Design Lab', 'DLDL', 'lab'),
            ('Data Structures Lab', 'DSL', 'lab'),
            ('Python Programming Lab', 'PPL', 'lab'),
        ],
        'CSE-DS': [
            ('Discrete Mathematics', 'DM', 'theory'),
            ('Digital Logic Design', 'DLD', 'theory'),
            ('Data Structures & Algorithms', 'DSA', 'theory'),
            ('Python Programming', 'PP', 'theory'),
            ('Digital Logic Design Lab', 'DLDL', 'lab'),
            ('Data Structures Lab', 'DSL', 'lab'),
            ('Python Programming Lab', 'PPL', 'lab'),
        ],
        'ECE': [
            ('Complex Variables & Numerical Methods', 'CVNM', 'theory'),
            ('Electronic Devices & Circuits', 'EDC', 'theory'),
            ('Signals & Systems', 'SS', 'theory'),
            ('Network Analysis', 'NA', 'theory'),
            ('Electronic Devices Lab', 'EDL', 'lab'),
            ('Network Analysis Lab', 'NAL', 'lab'),
            ('Signals & Systems Simulation Lab', 'SSSL', 'lab'),
        ],
        'EEE': [
            ('Complex Variables & Numerical Methods', 'CVNM', 'theory'),
            ('Electrical Circuit Analysis-II', 'ECA', 'theory'),
            ('DC Machines & Transformers', 'DCMT', 'theory'),
            ('Electromagnetic Field Theory', 'EMFT', 'theory'),
            ('Circuit Simulation Lab', 'CSL', 'lab'),
            ('DC Machines Lab', 'DML', 'lab'),
        ],
        'Mechanical': [
            ('Complex Variables & Numerical Methods', 'CVNM', 'theory'),
            ('Engineering Mechanics', 'EM', 'theory'),
            ('Thermodynamics', 'TD', 'theory'),
            ('Material Science & Metallurgy', 'MSM', 'theory'),
            ('Engineering Mechanics Lab', 'EML', 'lab'),
            ('Metallurgy Lab', 'ML', 'lab'),
            ('Thermodynamics Lab', 'TDL', 'lab'),
        ],
        'Civil': [
            ('Complex Variables & Numerical Methods', 'CVNM', 'theory'),
            ('Strength of Materials', 'SOM', 'theory'),
            ('Building Materials & Construction', 'BMC', 'theory'),
            ('Engineering Geology', 'EG', 'theory'),
            ('Strength of Materials Lab', 'SOML', 'lab'),
            ('Engineering Geology Lab', 'EGL', 'lab'),
            ('Building Materials Lab', 'BML', 'lab'),
        ]
    }
}

def seed_database():
    with app.app_context():
        # Check if branches exist
        if Branch.query.first():
            print("Database already seeded!")
            return
        
        # Create admin user
        admin = User(email='admin@nsrit.edu', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create branches
        for code, name in BRANCHES_DATA.items():
            branch = Branch(name=name, code=code)
            db.session.add(branch)
        db.session.flush()
        
        # Create sample faculties
        faculties = [
            Faculty(name='Dr. Rajesh Kumar', email='rajesh@nsrit.edu', department='CSE'),
            Faculty(name='Prof. Priya Singh', email='priya@nsrit.edu', department='CSE'),
            Faculty(name='Dr. Amit Patel', email='amit@nsrit.edu', department='ECE'),
            Faculty(name='Dr. Sneha Desai', email='sneha@nsrit.edu', department='EEE'),
            Faculty(name='Prof. Vikram Sharma', email='vikram@nsrit.edu', department='Mechanical'),
            Faculty(name='Dr. Anita Roy', email='anita@nsrit.edu', department='Civil'),
        ]
        for faculty in faculties:
            db.session.add(faculty)
        db.session.flush()
        
        # Create subjects for each semester
        faculty_list = Faculty.query.all()
        for semester, subjects_by_semester in SUBJECTS_DATA.items():
            # Common subjects for all branches
            branches = Branch.query.all()
            if 'common' in subjects_by_semester:
                for branch in branches:
                    for subject_name, code, subject_type in subjects_by_semester['common']:
                        subject = Subject(
                            name=subject_name,
                            code=code,
                            branch_id=branch.id,
                            semester=semester,
                            subject_type=subject_type,
                            faculty_id=faculty_list[semester % len(faculty_list)].id if faculty_list else None
                        )
                        db.session.add(subject)
            
            # Branch-specific subjects
            for branch_code, branch_subjects in subjects_by_semester.items():
                if branch_code != 'common':
                    branch = Branch.query.filter_by(code=branch_code).first()
                    if branch:
                        for subject_name, code, subject_type in branch_subjects:
                            subject = Subject(
                                name=subject_name,
                                code=code,
                                branch_id=branch.id,
                                semester=semester,
                                subject_type=subject_type,
                                faculty_id=faculty_list[semester % len(faculty_list)].id if faculty_list else None
                            )
                            db.session.add(subject)
        
        db.session.commit()
        print("✓ Database seeded successfully!")
        print(f"✓ Created {Branch.query.count()} branches")
        print(f"✓ Created {Subject.query.count()} subjects")
        print(f"✓ Created {Faculty.query.count()} faculties")
        print(f"✓ Admin user created: admin@nsrit.edu / admin123")

if __name__ == '__main__':
    seed_database()
