# DCCuatro :black_joker:

![DCCuatro](.readme/logo.png)

<!-- La tabla de contenidos está hecha para VSCode -->
- [Importante :heavy_exclamation_mark:](#Importante-%E2%9D%97%EF%B8%8F)
- [Ejecución :computer:](#Ejecuci%C3%B3n-%F0%9F%92%BB)
- [Supuestos, aclaraciones y consideraciones :thinking:](#Supuestos-aclaraciones-y-consideraciones-%F0%9F%A4%94)
  - [Envío de información :satellite:](#Env%C3%ADo-de-informaci%C3%B3n-%F0%9F%93%A1)
  - [El juego :black_joker:](#El-juego-%F0%9F%83%8F)
- [Librerías :books:](#Librer%C3%ADas-%F0%9F%93%9A)
  - [Librerías externas utilizadas :clipboard:](#Librer%C3%ADas-externas-utilizadas-%F0%9F%93%8B)
  - [Librerías propias :pencil:](#Librer%C3%ADas-propias-%F0%9F%93%9D)
- [Código externo utilizado :package:](#C%C3%B3digo-externo-utilizado-%F0%9F%93%A6)
- [Características implementadas :wrench:](#Caracter%C3%ADsticas-implementadas-%F0%9F%94%A7)
- [Notas adicionales :moyai:](#Notas-adicionales-%F0%9F%97%BF)

## Importante :heavy_exclamation_mark:

Tener una versión de PyQt5 menor a 5.14 causa un pequeño error.

## Ejecución :computer:

Los archivos a ejecutar son para cliente y servidor son
`main.py` en los directorios `client` y `server` respectivamente.

Hay que añadir la carpeta `sprites` y el módulo `generador_de_mazos.py`
en la carpeta `server`.

Cree un archivo `run.cmd` para simplifica el abrir todas las consolas
sin tener que repetir múltiples comandos (Windows). Al ejecutar `run`
se abre el servidor y un número de clientes, definido en el mismo
archivo.

Es conveniente cerrar el servidor antes que los clientes, ya que cada
cliente mostrará una alerta con un botón para salir en la misma posición.

## Supuestos, aclaraciones y consideraciones :thinking:

### Envío de información :satellite:

Al enviar información desde el servidor y hacia el servidor,
se envía un `json` serializado con el siguiente formato:

```py
n_obj + (id_obj1 + largo_obj1 + obj_1) + (id_obj2 + largo_obj2 + obj_2) + ...
```

El cual se almacena como:

```py
{
    id_obj1: obj_1,
    id_obj2: obj_2
}
```

`n_obj` es un `int` de 2 bytes, `id_objX` un `int` de 4 bytes,
`largo_objX` un `int = L` de 4 bytes y `obj_X` un objeto de L bytes.

Los tipos de objetos (`str`, `list`, `dict`, `bytes`) están agrupados
por ids en intervalos de 8 (a excepción de 3, establecido en el enunciado).

| id | de                  | tipo objecto         | objeto   | uso
| -: | :-----------------: |:-------------------: | :------: | :-  
|  0 | :computer::penguin: | tipo de acción       | `str`    | siempre
|  1 | :computer::penguin: | color de carta       | `str`    | al actualizar el mazo o el pozo $^1$ y pedir el color al cambiarlo
|  2 |           :penguin: | tipo de carta        | `str`    | al actualizar el mazo o el pozo $^1$
|  3 |           :penguin: | imagen de carta      | `bytes`  | al actualizar el mazo o el pozo $^1$
|  4 | :computer::penguin: | nombre del jugador   | `str`    | al unirse, al mandar una carta a los jugadores
|  5 | :computer::penguin: | carta seleccionada   | `str`    | para eliminar cartas
|  6 | :computer::penguin: | chat                 | `str`    | al enviar y recibir un chat
|  8 |           :penguin: | jugadores            | `list`   | al entrar un jugador, añadiéndolo en el cliente
| 16 | :computer::penguin: | información de error | `dict`   | al no poderse realizar una acción
| 17 |           :penguin: | detalles jugadores   | `dict`   | al iniciar la sala de juego
| 24 |           :penguin: | reverso de la carta  | `bytes`  | al iniciar la sala de juego

\[1\]: Establecido en el enunciado

Tanto en `str`,`list`, `dict` se usa `.decode('utf-8')`.
Además en las `list` se usará `.split('\n')` y en los `dict` `json.load`.

Para ver donde se usa cada una se puede buscar ` {id_}: `.


### El juego :black_joker:

<!-- TODO -->
- Los efectos de la primera carta del poso son omitidos.
- Robar cartas **siempre es voluntario**. Si el jugador recibió una penalización por decir DCCuatro, deberá robar un número de cartas de penalización.

## Librerías :books:

<!-- Falta una pequeña descripción -->

### Librerías externas utilizadas :clipboard:

- **`PyQt5`**: interfaz gráfica (GUI)

- **`sys`**: para serrar el programa al cerrar el interfaz
- **`socket`:** `socket`, `AF_INET`, `SOCK_STREAM `, creación de sockets
- **`threading`:** `Thread`, `Lock`, para escuchar al socket
- **`os`:** `path`, para unir los paths
- **`json`:** para serializar y deserializar diccionarios

- **`generador_de_mazos`:** genera las cartas

### Librerías propias :pencil:

- **`protocol`:** Módulo que sigue el [protocolo definido](#Env%C3%ADo-de-informaci%C3%B3n-%F0%9F%93%A1) con sockets

- client
  - **`application`:** Conecta el frontend (GUI) con el backend (socket)
  - frontend:
    - **`windows`:** Ventanas y objetos gráficos del interfaz
  - backend
    - **`client`:** Cliente que escucha y manda información al servidor
- server
  - **`log`:** Ordena la información del servidor en una tabla
  - **`game`:** Lógica del juego
  - **`server`:** Servidor del juego

## Código externo utilizado :package:

<!-- TODO -->

## Características implementadas :wrench:

<!-- TODO -->
Listo:

- Conexión servidor-clientes
- Sala de entrada
- Sala de espera
- Lógica del juego
- Envío de cartas
- Seleccionar cartas

En desarrollo:

- Carta de color
- Conexión de botones (DCCuadrádo!, robar)
- Sala de espera (Chat)

Bonus:

- Chat (con soporte _básico_ de **MarkDown**) (Falta en la sala de espera)

Posibles bonus:

- Tiempo límite
- Relámpago

## Notas adicionales :moyai:

Hay un error al recibir objetos muy largos de un servidor externo.

Disfrute el ~~programa~~ juego :tada:
