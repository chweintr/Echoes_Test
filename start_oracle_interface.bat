@echo off
echo Starting Indiana Oracle Interface on port 8500...
echo.
echo Web interface will be available at: http://localhost:8500
echo.
cd /d "E:\Interactive\interactive_project\indiana-oracle-main"
python test_conversation_interface.py
pause