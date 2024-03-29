import threading
import json
import socket
from color_canvas import Canvas

class Servidor:

    def __init__(self, host, port):
        print("Inicializando servidor...")
        # Crear el objeto Canvas
        self.canvas = Canvas(50, 50)
        self.host = host
        self.port = port

        # Crear un socket IPv4, TCP
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Ligar socket al host y al puerto del servidor
        self.socket_server.bind((self.host, self.port))

        # Activar escuchar en el socket
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}")
        print("Servidor aceptando conexiones!")

        # Diccionario que contendrá los sockets de multiples clientes
        self.sockets_clientes = dict()

        # ============================ ADVERTENCIA ============================

        # Si se implementa el método conectar_varios_clientes, cambiar este
        # valor a False para recibir múltiples clientes.
        self.un_cliente = False

        # El servidor verifica automáticamente si se aceptará uno o
        # varios clientes y ejecuta la función correspondiente en un Thread.
        if self.un_cliente:
            funcion_target = self.conectar_un_cliente
        else:
            funcion_target = self.conectar_varios_clientes
        thread = threading.Thread(target=funcion_target, daemon=True)
        thread.start()

    def conectar_un_cliente(self):
        """
        Permite que el servidor maneje un solo cliente durante su ejecución.
        """
        # ============================= COMPLETAR =============================
        socket_cliente, (ip, direc) = self.socket_server.accept()
        print('un cliente se ha conectado!')
        self.escuchar_cliente(socket_cliente, direc)
        # =====================================================================

    def escuchar_cliente(self, socket_cliente, id_cliente=0):
        """
        Permite que el servidor escuche los mensajes de un cliente.
        El socket de dicho cliente se encuentra en la variable socket_cliente.
        Para el caso de múltiples clientes, también se recibe id_cliente
        Debes procesar el mensaje enviado y generar una respuesta que
        posteriormente será enviada.
        """
        try:
            # =========================== COMPLETAR ===========================
            while True:
                data = socket_cliente.recv(5)
                largo_restante = int.from_bytes(data, byteorder='little')
                mensaje = bytearray()
                while largo_restante > 0:
                    largo = min(largo_restante, 128)
                    mensaje += self.sockets_clientes[id_cliente].recv(largo)
                    largo_restante -= 128
                info = json.loads(mensaje.decode('utf-8'))
                if info['comando'] == "nuevo":
                    tablero = self.canvas.obtener_tablero()
                    self.enviar_respuesta(socket_cliente, tablero)
                elif info['comando'] == "pintar":
                    self.canvas.pintar_pixel(info)
                    tablero = self.canvas.obtener_tablero()
                    self.enviar_respuesta(socket_cliente, tablero)
                elif info['comando'] == "cerrar":
                    break
            # =================================================================
        except ConnectionResetError:
            print("Error de conexión con el cliente!")
        finally:
            mensaje = {"cerrar" : True}
            self.enviar(socket_cliente, mensaje)
            socket_cliente.close()
            if id_cliente == 0:
                print("Cerrando conexión con el cliente...")
            else:
                print(f"Cerrando conexión con el cliente {id_cliente}...")
                if self.sockets_clientes.get(id_cliente):
                    del self.sockets_clientes[id_cliente]
                    print(f"Se ha eliminado el socket del cliente {id_cliente}.")

    def enviar_respuesta(self, socket_cliente, respuesta):
        """
        Recibe el socket del cliente que envió el mensaje, y un diccionario
        que contiene la respuesta a enviar.
        Si sólo se implementó una conexión, se envía al cliente en socket_cliente
        Si hay múltiples clientes, se envía a todos sus sockets.
        """
        if self.un_cliente:
            self.enviar(socket_cliente, respuesta)
        else:
            self.enviar_a_todos(respuesta)

    def enviar(self, socket_cliente, mensaje):
        """
        Recibe un socket y un diccionario. El diccionario debe ser codificado,
        y enviado al socket.
        """
        # ============================= COMPLETAR =============================
        codificado = json.dumps(mensaje).encode('utf-8')
        largo = len(codificado).to_bytes(5, byteorder='little')
        socket_cliente.send(largo)
        socket_cliente.send(codificado)
        # =====================================================================

    # =========================================================================
    # ========================= SECCION MULTI-CLIENTE =========================
    def conectar_varios_clientes(self):
        """
        Permite que el servidor acepte paralelamente múltiples conexiones de
        varios clientes.
        Este método solo se usa en el caso de múltiples clientes.
        """
        # ============================= COMPLETAR =============================
        while True:
            socket_cliente, (ip, direc) = self.socket_server.accept()
            self.sockets_clientes[direc] = socket_cliente
            thread_extra = threading.Thread(
                target=self.escuchar_cliente,
                args=[socket_cliente, direc]
            )
            thread_extra.start()
        # =====================================================================

    def enviar_a_todos(self, mensaje):
        """
        Envía el mensaje a todos los sockets actualmente conectados.
        Este método solo se usa en el caso de múltiples clientes.
        """
        # No usar diccionario directamente, así se previene
        # RuntimeError: dictionary changed size during iteration
        ids_cliente = list(self.sockets_clientes.keys())
        for id_cliente in ids_cliente:
            try:
                self.enviar(self.sockets_clientes[id_cliente], mensaje)
            except ConnectionResetError:
                print(f"El cliente {id_cliente} ha sido desconectado! (enviar_a_todos)")
                if self.sockets_clientes.get(id_cliente):
                    del self.sockets_clientes[id_cliente]
                    print(f"Se ha eliminado el socket del cliente {id_cliente}.")
            except ConnectionAbortedError:
                print(f"El cliente {id_cliente} ha sido desconectado! (enviar_a_todos)")
                if self.sockets_clientes.get(id_cliente):
                    del self.sockets_clientes[id_cliente]
                    print(f"Se ha eliminado el socket del cliente {id_cliente}.")
                print('Error de conexion con cliente')
            except IndexError:
                print(f"El cliente {id_cliente} no se encuentra en el diccionario.")
