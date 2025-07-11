@echo off
:: Executar script Python com administrador
powershell -Command "Start-Process python -ArgumentList 'desactivar-net.py' -Verb runAs"
