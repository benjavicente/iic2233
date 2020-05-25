# Tarea 02: DCCafé :coffee:

- [Tarea 02: DCCafé :coffee:](#tarea-02-dccafé-️)
  - [Importante :heavy_exclamation_mark:](#importante-️)
  - [Ejecución :computer:](#ejecución-)
  - [Supuestos y consideraciones :thinking:](#supuestos-y-consideraciones-)
    - [Aclaraciones](#aclaraciones)
  - [Librerías :books:](#librerías-)
    - [Librerías externas utilizadas :clipboard:](#librerías-externas-utilizadas-)
    - [Librerías propias :pencil:](#librerías-propias-)
  - [Código externo utilizado :package:](#código-externo-utilizado-)
  - [Características implementadas :wrench:](#características-implementadas-)
  - [Notas adicionales :moyai:](#notas-adicionales-)

## Importante :heavy_exclamation_mark:


## Ejecución :computer:

El programa a ejecutar es **`main.py`**.

Se debe agregar los archivos `mapa.csv` y `datos.csv` y la carpeta `sprites` en el
mismo nivel que `main.py`, de modo que el directorio quede de la siguiente manera:

```txt
T02
├── backend
├── config
├── frontend
├── sprites    <--
├── README.md
├── main.py
├── mapa.py    <--
└── datos.csv  <--
```

## Supuestos y consideraciones :thinking:

### Aclaraciones

El proceso que se realiza el juego es:

1. Cada cierto tiempo establecido en `parametros.py` se genera un cliente en una mesa desocupada aleatoria.
2. El jugador interactúa con el chef para entregar un pedido.
3. El chef prepara la orden que le ha sido entregada. Si falla en preparar la orden, el chef intenta nuevamente.
4. El jugador receive la orden preparada por el chef.
5. El jugador entrega la orden al cliente.
6. El cliente consume la orden y se va.

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
