@ECHO OFF

SET ruta_servidor="server"
SET ruta_clientes="client"
SET cantidad_clientes=2

FOR /L %%? IN (1, 1, %cantidad_clientes%) DO START CMD /k "TITLE cliente & CD %ruta_clientes% & main.py & EXIT"

START CMD /K "TITLE servidor & CD %ruta_servidor% & main.py & EXIT"
