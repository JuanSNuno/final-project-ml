@echo off
REM NO DEBES MODIFICAR ESTE ARCHIVO
REM ===================================
REM Purpose: Script to setup a Python virtual environment, install requirements
REM ===================================

setlocal EnableDelayedExpansion

echo.
echo === Python Virtual Environment Setup ===
echo.

REM Usar nombre fijo para el venv para simplificar
set "VENV_NAME=.venv"

echo Creando nuevo ambiente virtual: %VENV_NAME%
python -m venv %VENV_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: No se pudo crear el ambiente virtual.
    echo Asegurate de que Python esta instalado y disponible en el PATH.
    pause
    exit /b 1
)

echo.
echo Activando ambiente virtual...
call %VENV_NAME%\Scripts\activate.bat

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Ambiente virtual activado correctamente!
    echo Python actual: 
    where python
    
    echo.
    echo === Instalando requisitos ===
    if exist requirements.txt (
        echo requirements.txt encontrado, instalando librerias...
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo Todas las librerias instaladas correctamente.

            echo.
            echo === Registrando ambiente virtual con Jupyter ===
            echo Registrando kernel con Jupyter...
            python -m pip install ipykernel
            python -m ipykernel install --user --name=ml-venv --display-name="ML Project Python"
            
            if %ERRORLEVEL% EQU 0 (
                echo Ambiente virtual registrado como kernel de Jupyter correctamente.
                echo Ahora puedes seleccionar "ML Project Python" en Jupyter notebook.
            ) else (
                echo Advertencia: Fallo al registrar el ambiente virtual como kernel de Jupyter.
            )

        ) else (
            echo.
            echo Error instalando las librerias desde requirements.txt. Revisar los mensajes de error.
        )
    ) else (
        echo.
        echo Advertencia: requirements.txt no fue encontrado en el directorio actual.
    )
) else (
    echo.
    echo Error activando el ambiente virtual.
)

echo.
pause

