"""
===================================================================
Test Data Suite for Automated Selenium Testing
Project: SP23-BSE-131-Mid | EduCore Student Management System
===================================================================
"""

TEST_DATA = {
    # TC01: Home Page Elements
    "tc01_home": {
        "expected_title": "EduCore",
        "brand_id": "brand-logo",
        "expected_badge": "SP23-BSE-131",
        "expected_nav_items": ["Home", "Sign In", "Enroll / Register"]
    },

    # TC02: Valid Student Registration
    "tc02_valid_registration": {
        "full_name": "Hamza Automated Student",
        "reg_number": "SP23-AUT-101",
        "username": "hamza_aut_101",
        "email": "hamza_aut_101@university.edu.pk",
        "role": "Student",
        "password": "Password123!",
        "confirm_password": "Password123!"
    },

    # TC03: Duplicate Registration (Validation test)
    "tc03_duplicate_registration": {
        "full_name": "Duplicate Student Attempt",
        "reg_number": "SP23-AUT-101",
        "username": "hamza_aut_101",  # Same username as TC02
        "email": "hamza_aut_101@university.edu.pk",
        "role": "Student",
        "password": "Password123!",
        "confirm_password": "Password123!"
    },

    # TC04: Password Mismatch (Validation test)
    "tc04_password_mismatch": {
        "full_name": "Mismatch Tester",
        "reg_number": "SP23-MIS-999",
        "username": "mismatch_user",
        "email": "mismatch@university.edu.pk",
        "role": "Student",
        "password": "SecurePassword123",
        "confirm_password": "DifferentPassword456"
    },

    # TC05: Invalid Login Credentials (Security test)
    "tc05_invalid_login": {
        "username": "non_existent_user_999",
        "password": "WrongPasswordXYZ"
    },

    # TC06: Valid Administrator Login (Happy path)
    "tc06_valid_login": {
        "username": "admin",
        "password": "admin123",
        "expected_welcome_name": "Dr. M. Hasanain Ch",
        "expected_role": "Administrator"
    },

    # TC07: Academic Dashboard KPIs
    "tc07_dashboard_kpis": {
        "kpi_ids": [
            "stat-total-students",
            "stat-active-students",
            "stat-total-courses",
            "stat-avg-gpa"
        ]
    },

    # TC08: Enroll New Student Record via Modal
    "tc08_enroll_student": {
        "full_name": "Zayd Tariq Malik",
        "reg_number": "SP23-BSE-888",
        "email": "zayd.malik@university.edu.pk",
        "department": "Software Engineering",
        "semester": "7th",
        "cgpa": "3.85",
        "status": "Active"
    },

    # TC09: Directory Live Search & Filter
    "tc09_directory_search": {
        "search_query": "SP23-BSE-888",
        "expected_name": "Zayd Tariq Malik",
        "department_filter": "Software Engineering"
    },

    # TC10: Course Catalog & ALB Health Check
    "tc10_course_and_health": {
        "expected_course_code": "CSC418",
        "health_endpoint": "/health",
        "expected_health_status": "healthy"
    }
}
