[Setup]
AppId=Lollo-Pubblica
AppName=Pubblica
AppVersion=1.0
AppPublisher=by Lollo
DefaultDirName={localappdata}\Programs\Pubblica
DefaultGroupName=Pubblica
PrivilegesRequired=lowest
OutputDir=uscita
OutputBaseFilename=Pubblica-1.0-Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\Pubblica.exe
[Files]
Source: "dist\Pubblica.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\Pubblica"; Filename: "{app}\Pubblica.exe"
Name: "{autodesktop}\Pubblica"; Filename: "{app}\Pubblica.exe"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Crea icona sul desktop"; Flags: checkedonce
[Run]
Filename: "{app}\Pubblica.exe"; Description: "Avvia Pubblica"; Flags: nowait postinstall skipifsilent
