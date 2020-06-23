'''
Módulo que se encarga de recibir y mandar información de los sockets,
siguiendo el protocolo definido en el Enunciado y el README
    recv_data
    send_data
'''

from socket import SocketType as Socket
from pickle import loads as _pickle_loads, dumps as _pickle_dumps
from json import loads as _json_loads, dumps as _json_dumps

def recv_data(receiver_socket: Socket, chunk_size=128) -> dict:
    '''
    Recibe información del socket recibido y deserializa la
    información siguiendo un protocolo establecido en README
    '''
    if not isinstance(receiver_socket, Socket):
        raise TypeError("'receiver_socket' no es un socket")
    if not isinstance(chunk_size, int):
        raise TypeError("'chunk_size' no es un int")
    data = dict()
    object_count = int.from_bytes(receiver_socket.recv(2), 'big')
    for _ in range(object_count):
        # ID del objeto
        object_id = int.from_bytes(receiver_socket.recv(4), 'big')
        # Largo del objeto
        object_size = int.from_bytes(receiver_socket.recv(4), 'big')
        # Objeto serializado cargado por chunks
        object_content = bytearray()
        reamining_size = object_size
        while reamining_size > 0:
            chunk = min(reamining_size, chunk_size)
            object_content += receiver_socket.recv(chunk)
            reamining_size -= chunk_size
        # Transformación de objetos
        if   object_id < 0b001000:  # str
            content = object_content.decode('utf-8')
        elif object_id < 0b010000:  # list
            content = object_content.decode('utf-8').split('\n')
        elif object_id < 0b011000:  # dict
            content = _json_loads(object_content.decode('utf-8'))
        elif object_id < 0b100000:  # objetc
            content = _pickle_loads(object_content, encoding='utf-8')
        # Se guarda en un diccionario
        data[object_id] = content
    return data


def send_data(sender_socket: Socket, data: dict) -> None:
    '''
    Manda información desde el socket, serializando la
    información siguiendo un protocolo establecido en README
    '''
    if not isinstance(sender_socket, Socket):
        raise TypeError("'sender_socket' no es un socket")
    if not isinstance(data, dict):
        raise TypeError("'data' no es un diccionario")
    serialized_data = bytearray()
    # Serialización la cantidad de objetos
    serialized_data += len(data).to_bytes(2, 'big')
    for id_, obj in data.items():
        # Serialización del ID
        serialized_data += id_.to_bytes(4, 'big')
        # Serialización de objectos
        if   isinstance(obj, str):  # id < 8
            serialized_obj = obj.encode('utf-8')
        elif isinstance(obj, list):  # id < 16
            serialized_obj = '\n'.join(obj).encode('utf-8')
        elif isinstance(obj, dict):  # id < 24
            serialized_obj = _json_dumps(obj).encode('utf-8')
        elif isinstance(obj, object):  # id < 36
            serialized_obj = _pickle_dumps(obj)
        # Serialización del tamaño de objetos
        serialized_data += len(serialized_obj).to_bytes(4, 'big')
        # Envío de objeto
        serialized_data += serialized_obj
    # Se enviá al socket
    sender_socket.send(serialized_data)
