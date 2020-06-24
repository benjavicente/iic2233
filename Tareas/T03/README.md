# DCCuadrado :black_joker:

![DCCuadrado](.readme/logo.png)

<!-- La tabla de contenidos está hecha para VSCode -->
- [Importante :heavy_exclamation_mark:](#Importante-%E2%9D%97%EF%B8%8F)
- [Ejecución :computer:](#Ejecuci%C3%B3n-%F0%9F%92%BB)
- [Supuestos, aclaraciones y consideraciones :thinking:](#Supuestos-aclaraciones-y-consideraciones-%F0%9F%A4%94)
  - [Envío de información :satellite:](#Env%C3%ADo-de-informaci%C3%B3n-%F0%9F%93%A1)
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
|  1 |           :penguin: | color de carta       | `str`    | al actualizar el mazo o el pozo $^1$ **(no implementado)**
|  2 |           :penguin: | tipo de carta        | `str`    | al actualizar el mazo o el pozo $^1$ **(no implementado)**
|  3 |           :penguin: | imagen de carta      | `bytes`  | al actualizar el mazo o el pozo $^1$ **(no implementado)**
|  4 | :computer:          | nombre del jugador   | `str`    | al unirse
|  5 | :computer:          | carta seleccionada   | `str`    | en la sala de juego **(no implementado)**
|  6 | :computer::penguin: | chat                 | `str`    | al enviar y recibir un chat
|  8 |           :penguin: | jugadores            | `list`   | al entrar un jugador, añadiéndolo en el cliente
| 16 | :computer::penguin: | información de error | `dict`   | al no poderse realizar una acción
| 17 |           :penguin: | detalles jugadores   | `dict`   | al iniciar la sala de juego
| 24 |           :penguin: | reverso de la carta  | `bytes`  | al iniciar la sala de juego

Tanto en `str`,`list`, `dict` se usa `.decode('utf-8)`.
Además en las `list` se usará `.split('\n')` y en los `dict` `json.load`.

Para ver donde se usa cada una se puede buscar ` {id_}: `.

- \[1\]: Establecido en el enunciado

## Librerías :books:

<!-- Falta una pequeña descripción -->

### Librerías externas utilizadas :clipboard:

- `PyQt5`

- `sys`
- `socket`
  - `socket as Socket`
  - `AF_INET as IPv4`
  - `SOCK_STREAM as TPC`
- `threading`
  - `Thread`
  - `Lock`
- `os`
  - `path`
- `json`

### Librerías propias :pencil:

- `protocol`

- `application`
- frontend
  - `windows`
- backend
  - `client`

- `log`
- `game`
- `generador_de_mazos`
- `server`

## Código externo utilizado :package:

<!-- TODO -->

## Características implementadas :wrench:

<!-- TODO -->
Listo:

- Conexión servidor-clientes
- Sala de entrada
- Sala de espera
- Lógica inicial del juego

En desarrollo:

- Lógica del juego
- Envío de cartas
- Seleccionar cartas
- Conexión de botones (DCCuadrádo!)
- Sala de espera

Bonus:

- Chat (con soporte _básico_ de **MarkDown**)

Posibles bonus:

- Selector de mazos
- Tiempo límite
- Relámpago

## Notas adicionales :moyai:

Disfrute el ~~programa~~ juego :tada:
