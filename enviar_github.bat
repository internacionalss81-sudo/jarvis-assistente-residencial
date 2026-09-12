@echo off
title Enviar Atualizacao para o GitHub
color 0A

echo ====================================================
echo      ENVIANDO CODIGO PARA O GITHUB
echo ====================================================
echo.

echo 1. Salvando alteracoes locais...
git add .

echo.
echo 2. Criando mensagem de atualizacao...
git commit -m "Atualizacao automatica do app"

echo.
echo 3. Baixando alteracoes do GitHub para sincronizar...
git pull origin main --rebase

echo.
echo 4. Enviando para o repositorio no GitHub...
git push origin main

echo.
echo ====================================================
echo Codigo enviado com sucesso!
echo O GitHub Actions iniciara a criacao do novo APK.
echo ====================================================
pause