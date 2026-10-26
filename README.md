# EduCore — Enterprise Student Management System (SMS)

**Project Name:** `SP23-BSE-131-Mid`  
**Student Registration:** `SP23-BSE-131`  
**Application Type:** Real-World Academic & Student Lifecycle Management Platform  
**Architecture:** Modern Multi-Tier Application with Modular Front-End, Scalable Back-End & Relational Database  

---

## 🏛️ Application Overview & Real-World Features

**EduCore** is a comprehensive, production-ready Student Information and Academic Management System designed for universities and academic institutions:

1. **Student Directory & Enrollment (`/students`):**
   - Full student profile management (Name, Roll / Registration Number, Academic Email, Department, Current Semester, CGPA, Status).
   - Real-time instant search filter by name, registration number, or email.
   - Dynamic department filter (Software Engineering, Computer Science, AI, Cyber Security).
   - Interactive modal dialog to enroll new students with immediate validation.
   - Record deletion and status updates (`Active`, `On Leave`, `Graduated`).

2. **Academic Analytics Dashboard (`/dashboard`):**
   - Live KPI cards: Total Enrolled Students, Active Students, Courses Offered, and Average Campus CGPA.
   - Top Performing Students Honor Roll table with CGPA pills.
   - Department enrollment distribution with visual progress bars.

3. **University Course Catalog (`/courses`):**
   - Catalog of academic offerings with course codes, credit hours, instructors, and departments.
   - Course creation modal.

4. **Multi-Role Authentication & Security (`/auth`):**
   - Secure Student & Faculty sign in and registration.
   - Cryptographic password hashing (`werkzeug.security`).
   - Session protection with `@login_required`.

5. **Separated Templates & Stylesheets (Modular Architecture):**
   - Each page and module has its own dedicated template and stylesheet:
     - `templates/base.html` + `static/css/base.css` (Portal master layout & navigation)
     - `templates/home.html` + `static/css/home.css` (University portal landing & showcase)
     - `templates/auth/login.html` & `register.html` + `static/css/auth.css` (Campus authentication cards)
     - `templates/dashboard/index.html` + `static/css/dashboard.css` (Academic statistics & honor roll)
     - `templates/students/index.html` + `static/css/students.css` (Directory cards, search, & modal)
     - `templates/courses/index.html` + `static/css/courses.css` (Course catalog & credit cards)
     - `static/js/students.js` (Live client-side search, filtering, & modal controls)

6. **AWS & DevOps Readiness:**
   - `GET /health` endpoint returning `200 OK` JSON for AWS Application Load Balancer target group probes.
   - Automatic database flexibility: uses SQLite locally for testing without Docker, and connects to PostgreSQL when deployed via Docker Compose.

---

## 🚀 How to Run & Test on Localhost

The server is currently running! Open your browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)** (or `http://127.0.0.1:5000`)

### Pre-Seeded Accounts for Testing:
- **Administrator / Faculty Account:**
  - **Username:** `admin`
  - **Password:** `admin123`
- **Student Account:**
  - **Username:** `student`
  - **Password:** `student123`
- *(Or click **"Enroll / Register"** in the top navbar to create your own account)*

### To Restart Manually in Terminal:
```powershell
cd F:\SP23-BSE-131-Mid
python run.py
```

---

## 🧪 Automated Testing with Selenium WebDriver

While the server is running on `http://localhost:5000`, you can run the automated end-to-end Selenium test:

```powershell
cd F:\SP23-BSE-131-Mid
python tests/test_selenium.py
```

The script will:
1. Load the EduCore Student Portal homepage and assert registration badge `SP23-BSE-131`.
2. Register a new student portal account.
3. Authenticate and verify the student dashboard welcome greeting.
4. Navigate to the Student Directory, open the enrollment modal, enroll a new student record, and assert its presence in the directory.
5. Verify the AWS `/health` endpoint.

---

## 📁 Project Directory Structure

```
F:\SP23-BSE-131-Mid\
├── app/
│   ├── __init__.py                # App factory & database seed logic
│   ├── config.py                  # Dual-mode DB configuration (PostgreSQL / SQLite)
│   ├── models.py                  # User, Student, Course, Enrollment models
│   ├── routes/
│   │   ├── auth_routes.py         # Login, Register, Logout
│   │   ├── main_routes.py         # Home, Dashboard, /health
│   │   ├── student_routes.py      # Student Directory, Add, Delete
│   │   └── course_routes.py       # Course Catalog, Add Course
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css           # Global typography & navbar
│   │   │   ├── home.css           # Landing page styles
│   │   │   ├── auth.css           # Authentication card styles
│   │   │   ├── dashboard.css      # Academic analytics styles
│   │   │   ├── students.css       # Student directory & modal styles
│   │   │   └── courses.css        # Course catalog styles
│   │   └── js/
│   │       ├── main.js            # Toast notification helpers
│   │       └── students.js        # Live search & modal handlers
│   └── templates/
│       ├── base.html              # University portal layout
│       ├── home.html              # Campus landing page
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── dashboard/
│       │   └── index.html         # Academic stats & honor roll
│       ├── students/
│       │   └── index.html         # Student directory & enrollment
│       └── courses/
│           └── index.html         # Course catalog
├── tests/
│   └── test_selenium.py           # Automated browser test suite
├── scripts/
│   ├── setup_linux.sh             # Linux directory & permission setup
│   └── demonstrate_persistence.sh # Docker volume persistence proof
├── Dockerfile                     # Custom production Dockerfile
├── docker-compose.yml             # Web App + PostgreSQL Compose spec
├── AWS_DEPLOYMENT.md              # ALB & Auto Scaling deployment guide
├── VIVA_GUIDE.md                  # Section B Viva exam answers (15 Marks)
├── requirements.txt
├── run.py                         # Application entrypoint
└── README.md
```
