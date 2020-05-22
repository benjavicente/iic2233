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

TODO

## Ejecución :computer:

El programa a ejecutar es **`main.py`**.

## Supuestos y consideraciones :thinking:



### Aclaraciones

El proceso que se realiza el juego es:

1. Cada cierto tiempo establecido en `parametros.py` se genera un cliente en una mesa desocupada aleatoria.
2. El jugador recibe la orden del cliente.
3. El jugador entrega la orden a un chef arbitrario.
4. El chef prepara la orden que le ha sido entregada. Si falla en preparar la orden, el chef intenta nuevamente.
5. El jugador receive la orden preparada por el chef.
6. El jugador entrega la orden al cliente.
7. El cliente consume la orden y se va.

Es importante notar que:

- El cliente puede recibir cualquier orden.
- El jugador puede atender a varios clientes al mismo tiempo.
- El jugador interactúa con el cliente y el chef con colisiones.

## Librerías :books:

### Librerías externas utilizadas :clipboard:

- **`PyQt`**:
  - Encargada del interfaz gráfica.
- **`math`**
  - Operaciones matemáticas como la función `floor`.

### Librerías propias :pencil:

TODO

## Código externo utilizado :package:

No utilicé código externo :tada:

## Características implementadas :wrench:

TODO (De _TO DO_ (por hacer), no todo)

## Notas adicionales :moyai:

Algunas animaciones de PyQt pueden no funcionar correctamente en un monitor adicional (Windows).

Disfrute el programa :tada:
