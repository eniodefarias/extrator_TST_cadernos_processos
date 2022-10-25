@ECHO OFF

color a

TITLE Instalador do Extrator TST

ECHO Iniciando instalacao do DOCKER
ECHO .
ECHO .
ECHO .


START "Instalacao DOCKER" /I /B src\win_Docker_Desktop_Installer.exe

ECHO .
ECHO .
ECHO .

ECHO Iniciando Build da Imagem no Docker
ECHO .
ECHO .
ECHO .

START "Build da Imagem DOCKER" /WAIT /I /B /D %cd%  "docker build -t extrator_tst_cadernos_processos ."

ECHO .
ECHO .
ECHO .

ECHO Instalacao concluida
ECHO .
ECHO .
ECHO .
ECHO Digite ENTER para fechar esse terminal
move Instalador.bat TMP\