# DCCuatro :black_joker:

![DCCuatro](.readme/logo.png)

<!-- La tabla de contenidos está hecha para VSCode -->
- [Importante :heavy_exclamation_mark:](#Importante-%E2%9D%97%EF%B8%8F)
- [Ejecución :computer:](#Ejecuci%C3%B3n-%F0%9F%92%BB)
- [Supuestos, aclaraciones y consideraciones :thinking:](#Supuestos-aclaraciones-y-consideraciones-%F0%9F%A4%94)
  - [Envío de información :satellite:](#Env%C3%ADo-de-informaci%C3%B3n-%F0%9F%93%A1)
  - [El juego :black_joker:](#El-juego-%F0%9F%83%8F)
  - [Interfaz :pushpin:](#Interfaz-%F0%9F%93%8C)
- [Librerías :books:](#Librer%C3%ADas-%F0%9F%93%9A)
  - [Librerías externas utilizadas :clipboard:](#Librer%C3%ADas-externas-utilizadas-%F0%9F%93%8B)
  - [Librerías propias :pencil:](#Librer%C3%ADas-propias-%F0%9F%93%9D)
- [Código externo utilizado :package:](#C%C3%B3digo-externo-utilizado-%F0%9F%93%A6)
- [Características implementadas :wrench:](#Caracter%C3%ADsticas-implementadas-%F0%9F%94%A7)
- [Notas adicionales :moyai:](#Notas-adicionales-%F0%9F%97%BF)

## Importante :heavy_exclamation_mark:

Tener una versión de PyQt5 menor a 5.14 causa un pequeño error.

Añadir los sprites y el módulo entregado a `server`.

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
se envía un diccionario serializado con el siguiente formato:

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
|  1 | :computer::penguin: | color de carta       | `str`    | al actualizar el mazo o el pozo $^1$ y al elegir color
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

Para ver donde se usa cada una se puede buscar ` {id_}: ` en el código.

Todo esto es manejado por el módulo `protocol.py`, tanto en el cliente como
sel servidor.

### El juego :black_joker:

- Los efectos de la primera carta del poso son omitidos
- Robar cartas **siempre es voluntario**. Si el jugador recibió una penalización por
decir DCCuatro, deberá robar un número de cartas de la penalización es su turno
- El servidor espera a señales de los clientes para avanzar el juego. **Si jugadores
se desconectan repentinamente y queda uno solo, debería ser necesario realizar una
acción en el juego**, como robar o jugar una carta
- Robar se denota como jugar la carta de índice `-1`
- Una carta es válida si tiene el mismo color o tipo, no se jugó una
carta +2 en el turno anterior, y no se está jugando una carta de color.
(Ver `game.py@is_valid_card`)
- No implemente un mazo único por cada jugador. Hay un **maso central en
el que se puede robar**
- Un jugador puede gritar DCCuadrado cuando perdió, pero no tendrá efecto

### Interfaz :pushpin:

- Se interactúa con el juego con clics
- Arriba a la izquierda se mostrará el color y el jugador actual
- Los clientes mostraran una versión simplificada de los logs del servidor
- El interfaz puede verse mal en espacios pequeños. Un nombre de
jugador muy largo puede ocultar las cartas
- Los campos de texto son ingresados apretando la tecla return (enter)
- El tamaño de las cartas puede ser cambiado en los parámetros del cliente
- El mensaje cuando alguien gana **muestra solo quien ganó. Al cerrarlo se vuelve
al menu inicial, donde el jugador puede volver a jugar**.
- **Cuando un jugador pierde** o se pierde la conexión con el se **mostrará
un `:(`** sobre donde se encontraban sus cartas
- No se avisa si otro jugador grito DCCuatro, ni tampoco a quien se penaliza

## Librerías :books:


### Librerías externas utilizadas :clipboard:

- **`PyQt5`**: interfaz gráfica (GUI)

- **`sys`**: para cerrar el programa al cerrar el interfaz
- **`socket`:** `socket`, `AF_INET`, `SOCK_STREAM` , creación de sockets
- **`threading`:** `Thread`, `Lock`, para escuchar al socket
- **`os`:** `path`, para unir los paths
- **`json`:** para serializar y deserializar diccionarios
- **`collections`**: uso de `deque` para la cola de cartas a enviar

- **`generador_de_mazos`:** genera las cartas, entregado para la tarea

### Librerías propias :pencil:

- **`protocol`:** Módulo que sigue el
[protocolo definido](#Env%C3%ADo-de-informaci%C3%B3n-%F0%9F%93%A1) con sockets

- client
  - **`application`:** Conecta el frontend (GUI) con el backend (socket),
                       creando la aplicación
  - frontend:
    - **`windows`:** Ventanas y objetos gráficos del interfaz
  - backend
    - **`client`:** Cliente que escucha y manda información al servidor
- server
  - **`log`:** Ordena la información del servidor en una tabla
  - **`game`:** Lógica del juego
  - **`server`:** Servidor del juego

## Código externo utilizado :package:

Use pequeños trozos de código:

- `style().polish(widget)` en `windows.py@action_waiting`
de [JasonGenX](https://stackoverflow.com/a/9067046)
- una simplificación de la respuesta de
[Akash D G](https://stackoverflow.com/a/43389466) para eliminar widgets
en `windows.py@remove_card`


## Características implementadas :wrench:

Todo fue implementado :tada:

Partes de corrección de código:

- Uso de TPC / IP: `client.py:20` y `server.py:21`
- Inicio de sockets: `client.py:28` y `server.py:33`
- Sockets con threading: `client.py:30` y `server.py:53`
- Separación cliente y servidor: directorio `server` y `client`
- Responsabilidad del cliente: funciones desde `application.py:109`
- Responsabilidad del servidor: función `server.py@manage_response` y
módulo `game.py`
- Uso de locks: `server.py@lock_edit_client` y `server.py@lock_play` para
- evitar añadir multiples jugadores o cambiar el juego a la vez respectivamente
- Se utiliza el formato big y little endian: `protocol.py:24` y `protocol.py:66`
para mandar y recibir el id y `protocol.py:26` y `protocol.py:79` para recibir el
tamaño, con big y little respectivamente
- Implementación del protocolo: todo el módulo `protocol.py`
- Separación front-end y back-end para el cliente: directorios `frontend`
y `backend` con módulos que unidos en `application.py`
- Jugar una carta: toda la función `game.py@play`
- Uso del generador de mazos: al empezar en `game.py@start.game` y al
robar `game.py:122`.
- Uso de json: tanto en `main.py` del servidor como del cliente se abre
el archivo y se pasan los parámetros a la entidad principal del programa.

Bonus:

- Chat (con soporte _básico_ de **MarkDown**)


## Notas adicionales :moyai:

El código de la lógica del servidor y del juego no está ordenado,
pero hay comentarios que explican que se hace en cada paso.

**Para la corrección** puede ser util añadir la linea

```py
self.setWindowTitle(game_info['0'])
```

al inicio del método `setup_players` de `GameWindow`,
que se encuentra en la linea `276` del módulo `windows`.
Cambiará el nombre de la ventana de DCCuatro al nombre
del jugador que le corresponde al cliente de la ventana.

**Disfrute el ~~programa~~ juego :tada:**
