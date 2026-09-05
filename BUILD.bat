@echo off
setlocal

echo.
echo  =============================================
echo   CARTAS_SB - Generando instalador .exe
echo  =============================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python no encontrado.
    pause & exit /b 1
)

:: Instalar dependencias
echo  [1/5] Instalando dependencias Python...
python -m pip install flask pyinstaller pillow --quiet --no-warn-script-location

:: Verificar estructura
if not exist "static" mkdir static
if not exist "static\index.html" (
    echo  [ERROR] Falta static\index.html
    pause & exit /b 1
)
if not exist "cartas" mkdir cartas
if exist "TESON-MENDEZ.png" copy /Y "TESON-MENDEZ.png" "static\" >nul
if exist "TIGRE-UDH.png"    copy /Y "TIGRE-UDH.png"    "static\" >nul

:: Generar icono con script separado
echo  [2/5] Generando icono...
python make_ico.py

:: Cerrar exe anterior y limpiar
echo  [3/5] Limpiando builds anteriores...
taskkill /f /im "CARTAS_SB.exe" >nul 2>&1
timeout /t 1 /nobreak >nul
if exist "dist"           rmdir /s /q dist   >nul 2>&1
if exist "build"          rmdir /s /q build  >nul 2>&1
if exist "CARTAS_SB.spec" del /q CARTAS_SB.spec >nul 2>&1

:: Compilar exe
echo  [4/5] Compilando aplicacion...
if exist "icon.ico" (
    python -m PyInstaller --onefile --windowed --name "CARTAS_SB" --add-data "static;static" --icon "icon.ico" app.py
) else (
    python -m PyInstaller --onefile --windowed --name "CARTAS_SB" --add-data "static;static" app.py
)
if errorlevel 1 (
    echo  [ERROR] Fallo la compilacion.
    pause & exit /b 1
)

:: Copiar cartas al dist
if not exist "dist\cartas" mkdir "dist\cartas"
if exist "cartas\*.pdf" copy /Y "cartas\*.pdf" "dist\cartas\" >nul

:: Generar script Inno Setup
echo  [5/5] Generando instalador con Inno Setup...

set INNO=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "INNO=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe"       set "INNO=C:\Program Files\Inno Setup 6\ISCC.exe"

if not defined INNO (
    echo  [AVISO] Inno Setup no encontrado. Instala desde https://jrsoftware.org/isdl.php
    echo  El exe esta en dist\CARTAS_SB.exe
    pause & exit /b 0
)

:: Escribir setup.iss correctamente
> setup.iss echo #define AppName "Sistema de Cartas - Santa Barbara"
>> setup.iss echo #define AppVersion "1.0"
>> setup.iss echo #define AppExeName "CARTAS_SB.exe"
>> setup.iss echo.
>> setup.iss echo [Setup]
>> setup.iss echo AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
>> setup.iss echo AppName={#AppName}
>> setup.iss echo AppVersion={#AppVersion}
>> setup.iss echo AppPublisher=Santa Barbara
>> setup.iss echo DefaultDirName={autopf}\CartasSB
>> setup.iss echo DefaultGroupName={#AppName}
>> setup.iss echo OutputDir=installer
>> setup.iss echo OutputBaseFilename=Setup_CARTAS_SB
if exist "icon.ico" >> setup.iss echo SetupIconFile=icon.ico
>> setup.iss echo Compression=lzma2
>> setup.iss echo SolidCompression=yes
>> setup.iss echo WizardStyle=modern
>> setup.iss echo PrivilegesRequired=lowest
>> setup.iss echo.
>> setup.iss echo [Languages]
>> setup.iss echo Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
>> setup.iss echo.
>> setup.iss echo [Tasks]
>> setup.iss echo Name: "desktopicon"; Description: "Crear icono en el Escritorio"; GroupDescription: "Iconos adicionales:"; Flags: unchecked
>> setup.iss echo.
>> setup.iss echo [Files]
>> setup.iss echo Source: "dist\CARTAS_SB.exe"; DestDir: "{app}"; Flags: ignoreversion
>> setup.iss echo Source: "dist\cartas\*"; DestDir: "{app}\cartas"; Flags: ignoreversion recursesubdirs createallsubdirs
if exist "icon.ico" >> setup.iss echo Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
>> setup.iss echo.
>> setup.iss echo [Icons]
>> setup.iss echo Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
>> setup.iss echo Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
>> setup.iss echo Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
>> setup.iss echo.
>> setup.iss echo [Run]
>> setup.iss echo Filename: "{app}\{#AppExeName}"; Description: "Abrir Sistema de Cartas"; Flags: nowait postinstall skipifsilent

"%INNO%" setup.iss
if errorlevel 1 (
    echo  [ERROR] Fallo Inno Setup.
    pause & exit /b 1
)

echo.
echo  =============================================
echo   LISTO!
echo   Instalador: installer\Setup_CARTAS_SB.exe
echo  =============================================
echo.
pause
