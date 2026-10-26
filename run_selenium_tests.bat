@echo off
REM ===================================================================
REM Batch Script to Execute 10 Selenium Test Cases & Save Logs
REM Student: SP23-BSE-131
REM ===================================================================

echo =============================================================
echo Running 10 Automated Selenium Test Cases...
echo =============================================================

cd /d "F:\SP23-BSE-131-Mid"
python tests\test_selenium.py

echo.
echo =============================================================
echo Test Execution Finished!
echo View detailed logs at: F:\SP23-BSE-131-Mid\tests\test_results.log
echo =============================================================
pause
