[Setup]
AppName=Cartas SB
AppVersion=1.0
DefaultDirName={autopf}\Cartas SB
DefaultGroupName=Cartas SB
OutputDir=C:\Users\DolfoZR\Downloads\CDT\INSTALADORES
OutputBaseFilename=CartasSB_Installer
Compression=lzma2/normal
SolidCompression=yes
LZMANumBlockThreads=4
LZMABlockSize=65536
ArchitecturesInstallIn64BitMode=x64
DisableDirPage=no
PrivilegesRequired=admin
SetupIconFile=C:\Users\DolfoZR\Downloads\Íconos Santa Bárbara\iconos\Mapas.ico
UninstallDisplayIcon={app}\CartasSB.exe

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: checkedonce

[Files]
; PyInstaller build folder (exe + _internal + static + cartas)
Source: "C:\Users\DolfoZR\OneDrive\Documentos\CARTAS_SB\dist\CartasSB\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Cartas SB"; Filename: "{app}\CartasSB.exe"; WorkingDir: "{app}"; IconFilename: "{app}\_internal\mapas.ico"
Name: "{autodesktop}\Cartas SB"; Filename: "{app}\CartasSB.exe"; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{app}\_internal\mapas.ico"

[Run]
Filename: "{app}\CartasSB.exe"; Description: "Iniciar Cartas SB ahora"; Flags: nowait postinstall skipifsilent