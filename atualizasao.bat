@echo off
chcp 65001 >nul
echo ========================================
echo   Enviando atualizacoes para o GitHub...
echo ========================================

:: Adiciona todos os arquivos modificados
git add .

:: Faz o commit automaticamente com a data e hora atuais
git commit -m "Atualizacao automatica via script"

:: Tenta enviar para a branch main, se nao conseguir tenta master
git push origin main
if %errorlevel% neq 0 (
    echo Tentando enviar pela branch master...
    git push origin master
)

echo ========================================
echo   Processo finalizado!
echo ========================================
pause