@echo off
title Enviar Atualizacao para o GitHub
color 0A

echo ====================================================
echo      ENVIANDO CODIGO PARA O GITHUB
echo ====================================================
echo.

echo Salvando alteracoes locais...
git add .

echo.
echo Criando mensagem de atualizacao...
git commit -m "Atualizacao automatica do app"

echo.
echo Enviando para o repositorio no GitHub...
git push origin main

echo.
echo ====================================================
echo Codigo enviado com sucesso!
echo O GitHub Actions iniciara a criacao do novo APK.
echo ====================================================
pause