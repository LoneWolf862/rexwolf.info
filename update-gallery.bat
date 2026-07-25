@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py build_gallery.py
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    python build_gallery.py
  ) else (
    echo Python was not found.
    echo Install Python from python.org and select "Add Python to PATH".
    echo Then run this file again.
  )
)
echo.
pause
