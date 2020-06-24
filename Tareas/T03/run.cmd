SET ruta_servidor="server"
SET ruta_clientes="client"
SET cantidad_clientes=2

START CMD /k "CD %ruta_servidor% & main.py & EXIT"

FOR /L %%_ IN (1, 1, %cantidad_clientes%) DO START CMD /k "CD %ruta_clientes% & main.py & EXIT"

EXIT
