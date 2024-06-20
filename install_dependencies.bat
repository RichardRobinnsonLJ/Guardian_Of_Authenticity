@echo off
REM Check if conda is installed
conda --version >nul 2>&1
IF ERRORLEVEL 0 (
    echo Conda detected. Installing dependencies using conda...
    
    REM Create a requirements.txt file
    echo Creating requirements.txt file...
    echo Flask > requirements.txt
    echo Werkzeug >> requirements.txt
    echo opencv-python >> requirements.txt
    echo numpy >> requirements.txt
    echo Pillow >> requirements.txt
    echo matplotlib >> requirements.txt
    echo tensorflow >> requirements.txt
    echo lime >> requirements.txt

    REM Create a conda environment (if not already created) and install the required libraries
    conda create --name ml_env --yes
    conda activate ml_env
    conda install --file requirements.txt --yes

    REM Clean up the requirements.txt file
    del requirements.txt

    REM Done
    echo All required libraries have been installed in the conda environment 'ml_env'.
    pause
    exit /b
)

REM Check if pip is installed
python -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Pip is not installed. Please install pip and run this script again.
    pause
    exit /b
)

REM Create a requirements.txt file
echo Creating requirements.txt file...
echo Flask > requirements.txt
echo Werkzeug >> requirements.txt
echo opencv-python >> requirements.txt
echo numpy >> requirements.txt
echo Pillow >> requirements.txt
echo matplotlib >> requirements.txt
echo tensorflow >> requirements.txt
echo lime >> requirements.txt

REM Install the required libraries
echo Installing required libraries...
pip install -r requirements.txt

REM Clean up the requirements.txt file
del requirements.txt

REM Done
echo All required libraries have been installed.
pause
