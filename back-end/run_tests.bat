@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo CCW Mirror Test Runner
echo =====================

if "%1"=="" (
    echo Please specify test type:
    echo    all        - Run all tests
    echo    db         - Database tests only
    echo    api        - API tests only
    echo    pytest     - Run pytest tests
    goto :eof
)

set TEST_TYPE=%1

if "%TEST_TYPE%"=="db" (
    echo Running database tests...
    .\env\Scripts\python tests\test_db_connection.py
    goto :end
)

if "%TEST_TYPE%"=="api" (
    echo Running API tests...
    pushd tests
    ..\env\Scripts\python test_api.py
    popd
    goto :end
)

if "%TEST_TYPE%"=="all" (
    echo Running database tests...
    .\env\Scripts\python tests\test_db_connection.py
    
    echo.
    echo Running API tests...
    pushd tests
    ..\env\Scripts\python test_api.py
    popd
    goto :end
)

if "%TEST_TYPE%"=="pytest" (
    echo Running pytest framework tests...
    .\env\Scripts\python -m pytest -xvs tests\test_api_pytest.py
    goto :end
)

echo Unknown test type: %TEST_TYPE%
echo Valid options: all, db, api, pytest

:end
echo Tests completed.