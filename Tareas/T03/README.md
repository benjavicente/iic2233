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

## Ejecución :computer:

Los archivos a ejecutar son para cliente y servidor son
`main.py` en los directorios `client` y `server` respectivamente.


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

Los tipos de objetos (`str`, `list`, `dict`, `object`) están agrupados
por ids en intervalos de 8.

| id | de                  | tipo objecto         | objeto   | uso
| -: | :-----------------: |:-------------------: | :------: | :-  
|  0 | :computer::penguin: | tipo de acción       | `str`    | siempre
|  1 |           :penguin: | color de carta       | `str`    | al actualizar un mazo, al robar o actualizar el pozo
|  3 |           :penguin: | tipo de carta        | `str`    | al actualizar un mazo, al robar o actualizar el pozo
|  4 | :computer:          | nombre del jugador   | `str`    | al unirse
|  5 | :computer:          | carta seleccionada   | `str`    | al elegir carta en el turno
|  8 |           :penguin: | jugadores            | `list`   | al entrar un jugador, añadiéndolo en el cliente
| 16 | :computer::penguin: | información de error | `dict`   | al no poderse realizar una acción
| 24 |           :penguin: | imagen de carta      | `object` | al actualizar un mazo, al robar o actualizar el pozo

Tanto en `str`,`list`, `dict` se usa `.decode('utf-8)`.
Además en las `list` se usará `.split('\n')` y en los `dict` `json.load`.
Pará `object` se usará `pickle.loads(content, encoding='utf-8')`.


## Librerías :books:

### Librerías externas utilizadas :clipboard:

### Librerías propias :pencil:

## Código externo utilizado :package:

## Características implementadas :wrench:

## Notas adicionales :moyai:

Disfrute el programa juego :tada:
