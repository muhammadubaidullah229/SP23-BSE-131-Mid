"""
===================================================================
Automated Selenium WebDriver Test Suite (10 Test Cases)
Project: SP23-BSE-131-Mid | EduCore Student Management System
Target: Localhost (http://localhost:5000) or Cloud Load Balancer
===================================================================
"""

import os
import sys
import time
import logging
from datetime import datetime

# Ensure safe console output encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Import Test Data
from test_data import TEST_DATA

# Configuration
BASE_URL = os.environ.get('APP_URL', 'http://localhost:5000').rstrip('/')
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_results.log')

# ===================================================================
# Logger Configuration (Console + Dedicated Log File)
# ===================================================================
logger = logging.getLogger("SeleniumTestSuite")
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_formatter = logging.Formatter('%(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def get_driver():
    """Initializes Chrome or Edge WebDriver in headless or headed mode"""
    headless = os.environ.get('HEADLESS', 'true').lower() == 'true'

    try:
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        return webdriver.Chrome(options=chrome_options)
    except Exception:
        try:
            edge_options = EdgeOptions()
            if headless:
                edge_options.add_argument('--headless=new')
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            edge_options.add_argument('--window-size=1920,1080')
            return webdriver.Edge(options=edge_options)
        except Exception as e:
            logger.error(f"Could not initialize browser driver: {e}")
            sys.exit(1)


class TestRunner:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.results = []
        self.start_time = time.time()
        self.dynamic_user = None

    def record_result(self, tc_id, title, status, details=""):
        self.results.append({
            "id": tc_id,
            "title": title,
            "status": status,
            "details": details
        })
        if status == "PASS":
            logger.info(f"  [PASS] {tc_id}: {title}")
        else:
            logger.error(f"  [FAIL] {tc_id}: {title} | Error: {details}")

    # -------------------------------------------------------------
    # TC-01: Portal Home Page & Branding Elements
    # -------------------------------------------------------------
    def test_01_home_page_branding(self):
        tc_id = "TC-01"
        title = "Portal Home Page & Brand Navigation Verification"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            self.driver.get(BASE_URL)
            assert TEST_DATA["tc01_home"]["expected_title"] in self.driver.title, f"Title mismatch: {self.driver.title}"

            brand_el = self.wait.until(EC.presence_of_element_located((By.ID, TEST_DATA["tc01_home"]["brand_id"])))
            assert TEST_DATA["tc01_home"]["expected_badge"] in brand_el.text, f"Badge missing in: {brand_el.text}"

            # Check public nav buttons
            login_btn = self.driver.find_element(By.ID, "nav-login")
            register_btn = self.driver.find_element(By.ID, "nav-register")
            assert login_btn.is_displayed() and register_btn.is_displayed()

            self.record_result(tc_id, title, "PASS", "Home page, title, and registration badge verified.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-02: Student User Registration Workflow (Happy Path)
    # -------------------------------------------------------------
    def test_02_valid_registration(self):
        tc_id = "TC-02"
        title = "Student User Registration Workflow (Happy Path)"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            # Generate unique username and registration number
            ts = int(time.time())
            data = TEST_DATA["tc02_valid_registration"]
            username = f"aut_{ts}"
            reg_num = f"SP23-AUT-{ts % 1000:03d}"
            email = f"aut_{ts}@university.edu.pk"
            self.dynamic_user = {
                "username": username,
                "reg_num": reg_num,
                "email": email,
                "password": data["password"],
                "full_name": data["full_name"]
            }

            self.driver.get(f"{BASE_URL}/auth/register")
            self.driver.find_element(By.ID, "full_name").send_keys(data["full_name"])
            self.driver.find_element(By.ID, "reg_number").send_keys(reg_num)
            self.driver.find_element(By.ID, "username").send_keys(username)
            self.driver.find_element(By.ID, "email").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(data["password"])
            self.driver.find_element(By.ID, "confirm_password").send_keys(data["confirm_password"])
            self.driver.find_element(By.ID, "register-submit-btn").click()

            # Redirects to login
            self.wait.until(EC.presence_of_element_located((By.ID, "login-submit-btn")))
            page_text = self.driver.page_source
            assert "Registration successful" in page_text or "log in" in page_text

            self.record_result(tc_id, title, "PASS", f"Registered new student user '{username}' successfully.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-03: Duplicate Registration Validation
    # -------------------------------------------------------------
    def test_03_duplicate_registration_validation(self):
        tc_id = "TC-03"
        title = "Duplicate Registration Prevention Validation"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            if not self.dynamic_user:
                raise Exception("Dynamic user from TC-02 not available.")

            self.driver.get(f"{BASE_URL}/auth/register")
            self.driver.find_element(By.ID, "full_name").send_keys("Duplicate Student")
            self.driver.find_element(By.ID, "reg_number").send_keys(self.dynamic_user["reg_num"])
            self.driver.find_element(By.ID, "username").send_keys(self.dynamic_user["username"])
            self.driver.find_element(By.ID, "email").send_keys(self.dynamic_user["email"])
            self.driver.find_element(By.ID, "password").send_keys("Password123!")
            self.driver.find_element(By.ID, "confirm_password").send_keys("Password123!")
            self.driver.find_element(By.ID, "register-submit-btn").click()

            # Expect warning/danger flash alert
            alert = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert")))
            assert "already taken" in alert.text or "already registered" in alert.text

            self.record_result(tc_id, title, "PASS", f"System correctly blocked duplicate registration: '{alert.text.strip()}'.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-04: Password Mismatch Validation
    # -------------------------------------------------------------
    def test_04_password_mismatch(self):
        tc_id = "TC-04"
        title = "Registration Password Confirmation Mismatch Validation"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            data = TEST_DATA["tc04_password_mismatch"]
            self.driver.get(f"{BASE_URL}/auth/register")
            self.driver.find_element(By.ID, "full_name").send_keys(data["full_name"])
            self.driver.find_element(By.ID, "reg_number").send_keys(data["reg_number"])
            self.driver.find_element(By.ID, "username").send_keys(f"mis_{int(time.time())}")
            self.driver.find_element(By.ID, "email").send_keys(f"mis_{int(time.time())}@university.edu.pk")
            self.driver.find_element(By.ID, "password").send_keys(data["password"])
            self.driver.find_element(By.ID, "confirm_password").send_keys(data["confirm_password"])
            self.driver.find_element(By.ID, "register-submit-btn").click()

            alert = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            assert "Passwords do not match" in alert.text

            self.record_result(tc_id, title, "PASS", "Password mismatch alert displayed correctly.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-05: Invalid Credentials Login Rejection
    # -------------------------------------------------------------
    def test_05_invalid_login(self):
        tc_id = "TC-05"
        title = "Authentication Security - Invalid Credentials Rejection"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            data = TEST_DATA["tc05_invalid_login"]
            self.driver.get(f"{BASE_URL}/auth/login")
            self.driver.find_element(By.ID, "username_or_email").send_keys(data["username"])
            self.driver.find_element(By.ID, "password").send_keys(data["password"])
            self.driver.find_element(By.ID, "login-submit-btn").click()

            alert = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            assert "Invalid credentials" in alert.text

            self.record_result(tc_id, title, "PASS", "Invalid login correctly rejected with security alert.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-06: Valid Administrator Login & Session Verification
    # -------------------------------------------------------------
    def test_06_valid_login(self):
        tc_id = "TC-06"
        title = "Valid User Authentication & Protected Dashboard Access"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            data = TEST_DATA["tc06_valid_login"]
            self.driver.get(f"{BASE_URL}/auth/login")
            self.driver.find_element(By.ID, "username_or_email").send_keys(data["username"])
            self.driver.find_element(By.ID, "password").send_keys(data["password"])
            self.driver.find_element(By.ID, "login-submit-btn").click()

            welcome_el = self.wait.until(EC.presence_of_element_located((By.ID, "dashboard-welcome")))
            assert data["expected_welcome_name"] in welcome_el.text, f"Welcome text mismatch: {welcome_el.text}"

            # Verify session navbar items
            assert self.driver.find_element(By.ID, "nav-students").is_displayed()
            assert self.driver.find_element(By.ID, "nav-courses").is_displayed()
            assert self.driver.find_element(By.ID, "btn-logout").is_displayed()

            self.record_result(tc_id, title, "PASS", f"Authenticated as '{data['expected_welcome_name']}' with active session.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-07: Academic Dashboard KPIs & Honor Roll
    # -------------------------------------------------------------
    def test_07_dashboard_kpis(self):
        tc_id = "TC-07"
        title = "Academic Dashboard KPIs & Honor Roll Verification"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            self.driver.get(f"{BASE_URL}/dashboard")
            kpis = TEST_DATA["tc07_dashboard_kpis"]["kpi_ids"]

            for kpi_id in kpis:
                el = self.wait.until(EC.presence_of_element_located((By.ID, kpi_id)))
                val = el.text.strip()
                assert len(val) > 0 and (val.replace('.', '', 1).isdigit() or int(val) >= 0), f"Invalid KPI value '{val}' for {kpi_id}"

            # Check honor roll table
            table = self.driver.find_element(By.CLASS_NAME, "academic-table")
            assert table.is_displayed()

            self.record_result(tc_id, title, "PASS", "All 4 Academic KPI cards and Honor Roll table verified.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-08: Student Directory - Modal Enrollment
    # -------------------------------------------------------------
    def test_08_enroll_student_modal(self):
        tc_id = "TC-08"
        title = "Student Directory - Modal Enrollment & DOM Injection"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            data = TEST_DATA["tc08_enroll_student"]
            # Dynamic roll number to allow repeated runs
            dynamic_reg = f"SP23-BSE-{int(time.time()) % 1000:03d}"
            dynamic_name = f"Zayd Malik {int(time.time()) % 100}"
            self.search_target_reg = dynamic_reg
            self.search_target_name = dynamic_name

            self.driver.get(f"{BASE_URL}/students")

            # Click open modal
            open_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "openAddStudentModalBtn")))
            open_btn.click()

            # Fill modal fields
            self.wait.until(EC.visibility_of_element_located((By.ID, "inputStudentName"))).send_keys(dynamic_name)
            self.driver.find_element(By.ID, "inputStudentReg").send_keys(dynamic_reg)
            self.driver.find_element(By.ID, "inputStudentEmail").send_keys(f"{dynamic_reg.lower()}@university.edu.pk")

            # Select department
            dept_select = Select(self.driver.find_element(By.ID, "inputStudentDept"))
            dept_select.select_by_visible_text(data["department"])

            # Submit
            self.driver.find_element(By.ID, "btnSubmitStudent").click()

            # Verify presence in directory cards
            cards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "student-card")))
            found = any(dynamic_reg in card.text for card in cards)
            assert found, f"Student {dynamic_reg} not found in directory cards after submission."

            self.record_result(tc_id, title, "PASS", f"Enrolled student '{dynamic_name}' ({dynamic_reg}) and verified in DOM.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-09: Directory Real-Time Search & Department Filter
    # -------------------------------------------------------------
    def test_09_directory_search_filter(self):
        tc_id = "TC-09"
        title = "Student Directory Real-Time Instant Search & Filter"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            self.driver.get(f"{BASE_URL}/students")
            search_query = getattr(self, "search_target_reg", "SP23-BSE-131")

            search_box = self.wait.until(EC.presence_of_element_located((By.ID, "studentSearchInput")))
            search_box.clear()
            search_box.send_keys(search_query)
            # Dispatch input event to ensure JS filter executes reliably in headless mode
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", search_box)
            time.sleep(0.5)

            cards = self.driver.find_elements(By.CLASS_NAME, "student-card")
            visible_cards = [c for c in cards if c.is_displayed()]
            assert len(visible_cards) >= 1, f"Expected at least 1 matching card for '{search_query}', found 0."
            assert search_query in visible_cards[0].text, f"Search query '{search_query}' not found in visible card text."

            # Test clearing search to restore full directory
            self.driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", search_box)
            time.sleep(0.5)
            all_visible = [c for c in self.driver.find_elements(By.CLASS_NAME, "student-card") if c.is_displayed()]
            assert len(all_visible) > len(visible_cards), f"Expected more cards ({len(all_visible)}) after clearing search than when filtered ({len(visible_cards)})."

            self.record_result(tc_id, title, "PASS", f"Real-time search and clear correctly filtered directory ({len(visible_cards)} -> {len(all_visible)} cards).")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # TC-10: Course Catalog & Health Check Endpoint
    # -------------------------------------------------------------
    def test_10_course_catalog_and_health(self):
        tc_id = "TC-10"
        title = "Course Catalog Inspection & AWS ALB Health Endpoint"
        logger.info(f"\n--- Running {tc_id}: {title} ---")
        try:
            # 1. Course Catalog
            self.driver.get(f"{BASE_URL}/courses")
            assert "Course Catalog" in self.driver.title or "EduCore" in self.driver.title
            course_cards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "course-card")))
            assert len(course_cards) >= 1
            assert TEST_DATA["tc10_course_and_health"]["expected_course_code"] in self.driver.page_source

            # 2. ALB Health Endpoint
            self.driver.get(f"{BASE_URL}{TEST_DATA['tc10_course_and_health']['health_endpoint']}")
            page_text = self.driver.page_source
            assert '"status": "healthy"' in page_text or '"status":"healthy"' in page_text

            self.record_result(tc_id, title, "PASS", "Course catalog rendered and /health endpoint returned 200 healthy.")
        except Exception as e:
            self.record_result(tc_id, title, "FAIL", str(e))

    # -------------------------------------------------------------
    # Execute All Tests & Generate Report
    # -------------------------------------------------------------
    def run_all(self):
        logger.info("=" * 70)
        logger.info("   SELENIUM AUTOMATED TEST SUITE EXECUTION START")
        logger.info(f"   Target URL : {BASE_URL}")
        logger.info(f"   Log File   : {LOG_FILE}")
        logger.info(f"   Started At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)

        tests = [
            self.test_01_home_page_branding,
            self.test_02_valid_registration,
            self.test_03_duplicate_registration_validation,
            self.test_04_password_mismatch,
            self.test_05_invalid_login,
            self.test_06_valid_login,
            self.test_07_dashboard_kpis,
            self.test_08_enroll_student_modal,
            self.test_09_directory_search_filter,
            self.test_10_course_catalog_and_health
        ]

        for test in tests:
            test()

        # Summary Generation
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = total - passed
        duration = round(time.time() - self.start_time, 2)
        pass_rate = round((passed / total) * 100, 1)

        summary_table = [
            "\n" + "=" * 70,
            "                   TEST EXECUTION SUMMARY REPORT",
            "=" * 70,
            f"{'Test ID':<8} | {'Status':<6} | {'Test Case Description':<50}",
            "-" * 70
        ]
        for r in self.results:
            status_symbol = "[PASS]" if r["status"] == "PASS" else "[FAIL]"
            summary_table.append(f"{r['id']:<8} | {status_symbol:<6} | {r['title'][:50]:<50}")

        summary_table.extend([
            "-" * 70,
            f"Total Test Cases : {total}",
            f"Passed           : {passed}",
            f"Failed           : {failed}",
            f"Success Rate     : {pass_rate}%",
            f"Total Duration   : {duration} seconds",
            f"Log Output File  : {LOG_FILE}",
            "=" * 70 + "\n"
        ])

        summary_str = "\n".join(summary_table)
        logger.info(summary_str)

        return passed == total


def main():
    driver = get_driver()
    driver.implicitly_wait(8)
    try:
        runner = TestRunner(driver)
        success = runner.run_all()
        if not success:
            sys.exit(1)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
