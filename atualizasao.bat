@echo off
chcp 65001 >nul
echo ========================================
echo   Enviando atualizacoes para o GitHub...
echo ========================================

git add .
git commit -m "Atualizacao automatica via script"

:: Envia diretamente para a branch main
git push origin main

echo ========================================
echo   Processo finalizado!
echo ========================================
pause