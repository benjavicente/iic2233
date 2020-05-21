# Tarea 02: DCCafé :coffee:

- [Tarea 02: DCCafé :coffee:](#tarea-02-dccaf%c3%a9-coffee)
  - [Importante :heavy_exclamation_mark:](#importante-heavyexclamationmark)
  - [Ejecución :computer:](#ejecuci%c3%b3n-computer)
  - [Supuestos y consideraciones :thinking:](#supuestos-y-consideraciones-thinking)
    - [Aclaraciones](#aclaraciones)
  - [Librerías :books:](#librer%c3%adas-books)
    - [Librerías externas utilizadas :clipboard:](#librer%c3%adas-externas-utilizadas-clipboard)
    - [Librerías propias :pencil:](#librer%c3%adas-propias-pencil)
  - [Código externo utilizado :package:](#c%c3%b3digo-externo-utilizado-package)
  - [Características implementadas :wrench:](#caracter%c3%adsticas-implementadas-wrench)
  - [Notas adicionales :moyai:](#notas-adicionales-moyai)

## Importante :heavy_exclamation_mark:

Los paths no están como paths relativos aún!

Hay un problema en las señales que causa un error inesperado.

Hasta ahora el programa se inicia correctamente pero las instancias
no son cargadas bien en la ventana de juego, causando el error.
```py
...
    getattr(self, data['object'])[data['id']].move(*data['pos'])
IndexError: list index out of range
```
Deje unos prints para ver que está pasando.

## Ejecución :computer:

El programa a ejecutar es **`main.py`**.

## Supuestos y consideraciones :thinking:

TODO

### Aclaraciones

TODO

## Librerías :books:

### Librerías externas utilizadas :clipboard:

- **`PyQt`**
- **`math`**

### Librerías propias :pencil:

TODO

## Código externo utilizado :package:

No utilicé código externo :tada:

## Características implementadas :wrench:

TODO

## Notas adicionales :moyai:

Disfrute el programa :tada:
