@ECHO OFF

TITLE Extrator de Processos TST

ECHO Inicializando Extrator
ECHO .
ECHO .
ECHO .

REM docker run --rm --mount type=bind,source=%cd%,target=/app --name gerador extrator_tst_cadernos_processos
START "Build da Imagem DOCKER" /WAIT /I /B  "%cd%"  docker run --rm --mount type=bind,source="%cd%",target=/app --name gerador extrator_tst_cadernos_processos

ECHO .
ECHO .
ECHO .

ECHO Digite ENTER para fechar esse terminal
PAUSE