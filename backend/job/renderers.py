from rest_framework_csv import renderers


class JobCsvRenderer(renderers.CSVRenderer):

    header = [
        'company', 'title', 'created_at', 'publish_date', 'author', 'status',
        'country', 'state', 'city', 'zip', 'industry',
        'position_type', 'education', 'experience', 'travel', 'salary_min',
        'salary_max', 'salary_negotiable', 'clearance', 'benefits',
        'description', 'required_skills', 'optional_skills'
    ]

    labels = {
        'company': 'Company',
        'title': 'Job title',
        'created_at': 'Created Date',
        'publish_date': 'Published Date',
        'author': 'Author',
        'status': 'Status',
        'country': 'Country',
        'state': 'State',
        'city': 'City',
        'zip': 'Zip',
        'industry': 'Industry',
        'position_type': 'Position type',
        'education': 'Education',
        'experience': 'Years of experience',
        'travel': 'Travel opportunities',
        'salary_min': 'Salary min',
        'salary_max': 'Salary max',
        'salary_negotiable': 'Negotiable salary',
        'clearance': 'Clearance',
        'benefits': 'Benefits',
        'description': 'Description',
        'required_skills': 'Must Have Skills',
        'optional_skills': 'Nice Have skills'
    }
