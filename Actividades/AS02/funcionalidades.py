from functools import reduce
# En este archivo tendrás que completar las funciones entregadas.


def desencriptar(cliente_encriptado):
    # No modificar
    nombre_encriptado = list(cliente_encriptado[1])
    letras = list('consumir')
    numeros = [str(i) for i in range(1, 9)]
    clave = [list(i) for i in zip(letras, numeros)]
    for i in range(len(nombre_encriptado)):
        for elemento in clave:
            if nombre_encriptado[i] in elemento:
                if nombre_encriptado[i] == elemento[0]:
                    nombre_encriptado[i] = elemento[1]
                elif nombre_encriptado[i] == elemento[1]:
                    nombre_encriptado[i] = elemento[0]
    nombre_desencriptado = ''.join(nombre_encriptado)
    cliente_desencriptado = cliente_encriptado
    cliente_desencriptado[1] = nombre_desencriptado
    return cliente_desencriptado


def obtener_clientes(lista_clientes_encriptados):
    return list(map(desencriptar, lista_clientes_encriptados))


def categorizar(productos, categoria):
    return list(filter(lambda producto: categoria == producto.categoria, productos))


def calcular_precio(productos):
    return int(reduce(lambda acumulado, p: acumulado + p.precio, productos, 0))


def generar_productos_disponibles(clientes):
    for cliente in clientes:
        for producto in cliente.carrito:
            if producto.disponible:
                yield (cliente, producto)
