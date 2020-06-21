# DCCuadrado :black_joker:

![DCCuadrado](.readme/logo.png)

- [Importante :heavy_exclamation_mark:](#importante-%e2%9d%97%ef%b8%8f)
- [Ejecución :computer:](#ejecuci%c3%b3n-%f0%9f%92%bb)
- [Supuestos, aclaraciones y consideraciones :thinking:](#supuestos-aclaraciones-y-consideraciones-%f0%9f%a4%94)
  - [Envío de información hacia el servidor :penguin:](#env%c3%ado-de-informaci%c3%b3n-hacia-el-servidor-%f0%9f%90%a7)
  - [Envío de información hacia el cliente :computer:](#env%c3%ado-de-informaci%c3%b3n-hacia-el-cliente-%f0%9f%92%bb)
- [Librerías :books:](#librer%c3%adas-%f0%9f%93%9a)
  - [Librerías externas utilizadas :clipboard:](#librer%c3%adas-externas-utilizadas-%f0%9f%93%8b)
  - [Librerías propias :pencil:](#librer%c3%adas-propias-%f0%9f%93%9d)
- [Código externo utilizado :package:](#c%c3%b3digo-externo-utilizado-%f0%9f%93%a6)
- [Características implementadas :wrench:](#caracter%c3%adsticas-implementadas-%f0%9f%94%a7)
- [Notas adicionales :moyai:](#notas-adicionales-%f0%9f%97%bf)

## Importante :heavy_exclamation_mark:

## Ejecución :computer:

Los archivos a ejecutar son para cliente y servidor son
`main.py` en los directorios `client` y `server` respectivamente.


## Supuestos, aclaraciones y consideraciones :thinking:

### Envío de información hacia el servidor :penguin:

Al enviar información desde el servidor, se envía un
`json` serializado con el siguiente formato:

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

donde los ids corresponden a:

| id | tipo objecto    | objeto  |uso     |
| -: | :-------------: | :-----: | :------ |
|  0 | tipo de acción  | `int`   | siempre |
|  1 | color de carta  | `str`   | al actualizar un mazo, al robar o actualizar el pozo |
|  2 | número de carta | `str`   | al actualizar un mazo, al robar o actualizar el pozo |
|  3 | imagen de carta | ?       | al actualizar un mazo, al robar o actualizar el pozo |
|  4 | jugador         | `dict`  | al entrar un jugador, añadiéndolo en el cliente  |

### Envío de información hacia el cliente :computer:

## Librerías :books:

### Librerías externas utilizadas :clipboard:

### Librerías propias :pencil:

## Código externo utilizado :package:

## Características implementadas :wrench:

## Notas adicionales :moyai:

Disfrute el programa juego :tada:
