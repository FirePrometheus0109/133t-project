from rest_framework_csv import renderers


class CandidateCsvRenderer(renderers.CSVRenderer):

    header = [
        'first_name', 'last_name', 'job', 'applied_date', 'location',
        'updated_at', 'email', 'phone', 'address', 'industries',
        'position_type', 'education', 'experience', 'travel', 'salary_min',
        'salary_max', 'clearance', 'benefits', 'skills', 'education_details',
        'experience_details', 'workflow_step', 'rating'
    ]

    labels = {
        'first_name': 'First name',
        'last_name': 'Last name',
        'job': 'Applied Job title',
        'applied_date': 'Applied Date',
        'location': 'Location',
        'updated_at': 'Date of profile update',
        'email': 'Email',
        'phone': 'Phone',
        'address': 'Address',
        'industries': 'Industry(s)',
        'position_type': 'Position type',
        'education': 'Education',
        'experience': 'Years of experience',
        'travel': 'Travel opportunities',
        'salary_min': 'Salary min',
        'salary_max': 'Salary max',
        'clearance': 'Clearance',
        'benefits': 'Benefits',
        'skills': 'Skills',
        'education_details': 'Education details',
        'experience_details': 'Experience details',
        'workflow_step': 'Workflow step',
        'rating': 'Rate'
    }
