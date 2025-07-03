@echo off
REM MarketFlow Module Backup and Replacement Script
REM This script safely backs up original modules and replaces them with fixed versions

echo ========================================
echo MarketFlow Module Replacement Script
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "marketflow" (
    echo ERROR: marketflow directory not found!
    echo Please run this script from your MarketFlow project root directory.
    echo.
    pause
    exit /b 1
)

REM Create backup directory structure
echo Creating backup directory structure...
if not exist "deprecated_backup" mkdir deprecated_backup
if not exist "deprecated_backup\modules" mkdir deprecated_backup\modules
if not exist "deprecated_backup\logs" mkdir deprecated_backup\logs
echo ✓ Backup directories created

REM Check if original modules exist
if not exist "marketflow\marketflow_config_manager.py" (
    echo WARNING: marketflow_config_manager.py not found in marketflow directory
    echo Skipping config manager backup...
) else (
    echo Backing up marketflow_config_manager.py...
    copy "marketflow\marketflow_config_manager.py" "deprecated_backup\modules\marketflow_config_manager_original.py" >nul
    echo ✓ Config manager backed up
)

if not exist "marketflow\marketflow_logger.py" (
    echo WARNING: marketflow_logger.py not found in marketflow directory
    echo Skipping logger backup...
) else (
    echo Backing up marketflow_logger.py...
    copy "marketflow\marketflow_logger.py" "deprecated_backup\modules\marketflow_logger_original.py" >nul
    echo ✓ Logger backed up
)

REM Create backup metadata
echo Creating backup metadata...
echo Backup Date: %date% %time% > deprecated_backup\backup_info.txt
echo Reason: Module compatibility fixes and improvements >> deprecated_backup\backup_info.txt
echo Original Files: >> deprecated_backup\backup_info.txt
echo - marketflow_config_manager.py (backed up as marketflow_config_manager_original.py) >> deprecated_backup\backup_info.txt
echo - marketflow_logger.py (backed up as marketflow_logger_original.py) >> deprecated_backup\backup_info.txt
echo. >> deprecated_backup\backup_info.txt
echo Issues Fixed: >> deprecated_backup\backup_info.txt
echo - Circular import dependency >> deprecated_backup\backup_info.txt
echo - Hardcoded Windows-specific paths >> deprecated_backup\backup_info.txt
echo - Cross-platform compatibility >> deprecated_backup\backup_info.txt
echo - Encoding parameter usage >> deprecated_backup\backup_info.txt
echo - Error handling improvements >> deprecated_backup\backup_info.txt
echo - Dependency injection pattern >> deprecated_backup\backup_info.txt
echo ✓ Backup metadata created

REM Check if fixed modules exist
if not exist "marketflow_logger_fixed.py" (
    echo ERROR: marketflow_logger_fixed.py not found!
    echo Please ensure the fixed modules are in the current directory.
    echo.
    pause
    exit /b 1
)

if not exist "marketflow_config_manager_fixed.py" (
    echo ERROR: marketflow_config_manager_fixed.py not found!
    echo Please ensure the fixed modules are in the current directory.
    echo.
    pause
    exit /b 1
)

REM Ask for confirmation
echo.
echo Ready to replace modules with fixed versions.
echo This will:
echo - Replace marketflow\marketflow_logger.py with the fixed version
echo - Replace marketflow\marketflow_config_manager.py with the fixed version
echo.
set /p confirm="Continue with replacement? (y/N): "
if /i not "%confirm%"=="y" (
    echo Operation cancelled by user.
    echo.
    pause
    exit /b 0
)

REM Replace the modules
echo.
echo Replacing modules...
copy "marketflow_logger_fixed.py" "marketflow\marketflow_logger.py" >nul
echo ✓ Logger module replaced

copy "marketflow_config_manager_fixed.py" "marketflow\marketflow_config_manager.py" >nul
echo ✓ Config manager module replaced

REM Copy integration example if examples directory exists
if exist "marketflow\examples" (
    echo Copying integration example...
    copy "marketflow_integration_example.py" "marketflow\examples\integration_example.py" >nul
    echo ✓ Integration example copied
) else (
    echo Creating examples directory and copying integration example...
    mkdir "marketflow\examples"
    copy "marketflow_integration_example.py" "marketflow\examples\integration_example.py" >nul
    echo ✓ Examples directory created and integration example copied
)

REM Copy test files if tests directory exists
if exist "tests" (
    echo Copying test files...
    copy "test_marketflow_modules.py" "tests\test_marketflow_modules.py" >nul
    copy "demo_marketflow_modules.py" "tests\demo_marketflow_modules.py" >nul
    echo ✓ Test files copied to tests directory
) else (
    echo Creating tests directory and copying test files...
    mkdir "tests"
    copy "test_marketflow_modules.py" "tests\test_marketflow_modules.py" >nul
    copy "demo_marketflow_modules.py" "tests\demo_marketflow_modules.py" >nul
    echo ✓ Tests directory created and test files copied
)

echo.
echo ========================================
echo ✓ Module replacement completed successfully!
echo ========================================
echo.
echo What was done:
echo - Original modules backed up to deprecated_backup\modules\
echo - Fixed modules installed in marketflow\
echo - Integration example added to marketflow\examples\
echo - Test files added to tests\
echo.
echo Next steps:
echo 1. Install dependencies: pip install python-dotenv
echo 2. Run tests: python tests\test_marketflow_modules.py
echo 3. Run demo: python tests\demo_marketflow_modules.py
echo 4. Update your application imports (see module_replacement_guide.md)
echo.
echo Backup location: deprecated_backup\modules\
echo - marketflow_config_manager_original.py
echo - marketflow_logger_original.py
echo.
pause

