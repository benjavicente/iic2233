# Tarea 02: DCCafé :coffee:

- [Tarea 02: DCCafé :coffee:](#tarea-02-dccafé-️)
  - [Importante :heavy_exclamation_mark:](#importante-️)
  - [Ejecución :computer:](#ejecución-)
  - [Supuestos, aclaraciones y consideraciones :thinking:](#supuestos-aclaraciones-y-consideraciones-)
  - [Librerías :books:](#librerías-)
    - [Librerías externas utilizadas :clipboard:](#librerías-externas-utilizadas-)
    - [Librerías propias :pencil:](#librerías-propias-)
  - [Código externo utilizado :package:](#código-externo-utilizado-)
  - [Características implementadas :wrench:](#características-implementadas-)
  - [Notas adicionales :moyai:](#notas-adicionales-)

## Importante :heavy_exclamation_mark:

TODO

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

## Supuestos, aclaraciones y consideraciones :thinking:

**El proceso que se realiza el juego es:**

1. Cada cierto tiempo se genera
un cliente en una mesa desocupada aleatoria
2. El jugador interactúa con el cliente y recibe un pedido
3. El jugador interactúa con el chef para entregar un pedido
4. El chef prepara la orden que le ha sido entregada, si falla
en prepararla, intenta nuevamente
5. El jugador receive la orden preparada por el chef
6. El jugador entrega la orden al cliente
7. El cliente consume la orden y se va, pagando el pedido, con la propina añadida.

**Es importante que:**

- Cada cliente genera un único pedido, pero puede recibir cualquier pedido
- Si cliente se retira y no ha recibido, el pedido no se elimina

**Las _teclas trampa_ son:**

- `M` + `O` + `Y`: dinero
- `B` + `T` + `G`: reputación
- `F` + `I` + `N`: termina la ronda, espera la salida de los clientes

Todas estas deben ser presionadas en conjunto por lo menos un segundo.

**En el menú principal hay 3 botones**:

- Información: TODO
- Jugadores: número de jugadores, al presionarlo aumenta la cantidad
- Configuración: TODO 


## Librerías :books:

### Librerías externas utilizadas :clipboard:

- **`PyQt`**
  - Encargada del interfaz gráfica.
- **`sys`**
  - Función `exit` para cerrar el programa al cerrar el UI.
- **`math`**
  - Operaciones matemáticas como la función `floor`.
- **`random`**
  - Funciones `random`, `randint`, `choice` y `shuffle`.
- **`functools`**
  - Función `namedtuple`

### Librerías propias :pencil:

- **backend**
  - `game_objects.py`: clases de los objetos visuales del juego
  - `clock.py`: clase `GameClock` (los relojes del juego)
  - `game_core.py`: clase `GameCore`, _cerebro_ del programa
  - `cafe.py`: clase `Cafe`, que almacena los datos de la partida
  - `paths.py`: paths de los archivos de datos
- **frontend**
  - _windows_: ventanas del juego (`initial.py`, `game.py` y `summary.py`)
  - `paths.py`: Clase `SpritePath` y paths de los sprites
  - `themes.py`: Lee los archivos `css` y los guarda para las ventanas

## Código externo utilizado :package:

Usé [código de David Wallance](https://stackoverflow.com/a/48203489)
(adaptación de [la respuesta de Avaris](https://stackoverflow.com/a/14410888) en
la pregunta [PyQt4 - Drag and Drop](https://stackoverflow.com/q/14395799)
de StackOverflow) para modelar el funcionamiento del drag and drop de la tienda.


Donde usé código externo de menor extensión marqué que hace y de donde lo obtuve con `#!`.

Por ejemplo:

```python
#! Invertir un diccionario
#! https://stackoverflow.com/a/483833
clases_objects = {obj_c: name for name, obj_c in self.object_classes.items()}
```

## Características implementadas :wrench:

Se implementó todo menos:

- El menú pre-ronda

De los bonús:

- Presidente
- Multijugador

## Notas adicionales :moyai:

Algunas animaciones de Qt pueden no funcionar correctamente en un monitor adicional (Windows).

Disfrute el programa :tada:
