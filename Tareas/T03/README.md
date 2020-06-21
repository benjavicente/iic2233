# DCCuadrado :black_joker:

![DCCuadrado](.readme/logo.png)

- [Importante :heavy_exclamation_mark:](#Importante-%E2%9D%97%EF%B8%8F)
- [Ejecución :computer:](#Ejecuci%C3%B3n-%F0%9F%92%BB)
- [Supuestos, aclaraciones y consideraciones :thinking:](#Supuestos-aclaraciones-y-consideraciones-%F0%9F%A4%94)
  - [Envío de información hacia el servidor :penguin:](#Env%C3%ADo-de-informaci%C3%B3n-hacia-el-servidor-%F0%9F%90%A7)
  - [Envío de información hacia el cliente :computer:](#Env%C3%ADo-de-informaci%C3%B3n-hacia-el-cliente-%F0%9F%92%BB)
- [Librerías :books:](#Librer%C3%ADas-%F0%9F%93%9A)
  - [Librerías externas utilizadas :clipboard:](#Librer%C3%ADas-externas-utilizadas-%F0%9F%93%8B)
  - [Librerías propias :pencil:](#Librer%C3%ADas-propias-%F0%9F%93%9D)
- [Código externo utilizado :package:](#C%C3%B3digo-externo-utilizado-%F0%9F%93%A6)
- [Características implementadas :wrench:](#Caracter%C3%ADsticas-implementadas-%F0%9F%94%A7)
- [Notas adicionales :moyai:](#Notas-adicionales-%F0%9F%97%BF)

## Importante :heavy_exclamation_mark:

## Ejecución :computer:

Los archivos a ejecutar son para cliente y servidor son
`main.py` en los directorios `client` y `server` respectivamente.


## Supuestos, aclaraciones y consideraciones :thinking:

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

### Envío de información del servidor al cliente :penguin:

| id | tipo objecto    | objeto  | uso     |
| -: | :-------------: | :-----: | :------ |
|  0 | tipo de acción  | `str`   | siempre |
|  1 | color de carta  | `str`   | al actualizar un mazo, al robar o actualizar el pozo |
|  2 | número de carta | `str`   | al actualizar un mazo, al robar o actualizar el pozo |
|  3 | imagen de carta | ?       | al actualizar un mazo, al robar o actualizar el pozo |
|  4 | info jugadores  | `dict`  | al entrar un jugador, añadiéndolo en el cliente  |

El tipo de acción puede ser:

<!-- TODO -->
1. Un jugador jugó una carta, actualizándose el pozo.

### Envío de información del cliente al servidor :computer:

| id | tipo objecto       | objeto  | uso     |
| -: | :----------------: | :-----: | :------ |
|  0 | tipo de acción     | `str`   | siempre |
|  1 | nombre del jugador | `str`   | al unirse |
|  2 | carta seleccionada | `str`   | al elegir carta en el turno |

<!-- TODO -->
El tipo de acción puede ser:

1. El jugador jugó una carta.
2. El jugador entró al juego, entregando al servidor su información.


## Librerías :books:

### Librerías externas utilizadas :clipboard:

### Librerías propias :pencil:

## Código externo utilizado :package:

## Características implementadas :wrench:

## Notas adicionales :moyai:

Disfrute el programa juego :tada:
