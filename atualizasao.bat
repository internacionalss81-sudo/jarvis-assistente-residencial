@echo off
echo ========================================
echo   Enviando atualizacoes para o GitHub
echo ========================================

:: Adiciona todas as alteracoes feitas
git add .

:: Pergunta a mensagem do commit para voce digitar
set /p mensagem="Digite a mensagem da atualizacao: "

:: Faz o commit com a mensagem informada
git commit -m "%mensagem%"

:: Envia para o repositorio oficial (branch main)
git push origin main

echo ========================================
echo   Processo concluido com sucesso!
echo ========================================
pause