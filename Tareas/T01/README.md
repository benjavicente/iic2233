# Tarea 01: DCCriaturas Fantásticas :bird:

- [Tarea 01: DCCriaturas Fantásticas :bird:](#tarea-01-dccriaturas-fant%c3%a1sticas-bird)
  - [Importante :heavy_exclamation_mark:](#importante-heavyexclamationmark)
  - [Ejecución :computer:](#ejecuci%c3%b3n-computer)
  - [Supuestos y consideraciones :thinking:](#supuestos-y-consideraciones-thinking)
  - [Diagrama de clases :bookmark_tabs:](#diagrama-de-clases-bookmarktabs)
    - [Aclaraciones](#aclaraciones)
  - [Librerías :books:](#librer%c3%adas-books)
    - [Librerías externas utilizadas :clipboard:](#librer%c3%adas-externas-utilizadas-clipboard)
    - [Librerías propias :pencil:](#librer%c3%adas-propias-pencil)
  - [Código externo utilizado :package:](#c%c3%b3digo-externo-utilizado-package)
  - [Características implementadas :wrench:](#caracter%c3%adsticas-implementadas-wrench)
  - [Notas adicionales :moyai:](#notas-adicionales-moyai)

## Importante :heavy_exclamation_mark:

:question:

## Ejecución :computer:

El programa a ejecutar es **`main.py`**.

Los archivos de datos (`criatuas.csv` y `magizoologos.csv`) deben estar creados en una carpeta llamada `data`. El formato de cada uno es de `csv`, donde cada campo termina con una nueva linea. Los nombres y la ubicación de los archivos puede modificarse en el archivo `parametros.py`.

Los módulos `dcc`, `dccriaturas`, `magizoologos`, `alimentos`, `procesos`, `parametros` y `zoologico_magico` deben encontrarse en el mismo _path_ que `main.py`.

## Supuestos y consideraciones :thinking:

Considero que la DCCriatura Augurey puede entregar un alimento a su dueño **si esta se escapó**.

Utilizo `SuperMagizoologoDocencioTareoHibrido` como `MagizoologoSuper`.

Asumo que se debe guardar los datos solo al salir. He agradado la opción de guardar sin salir para no tener que salir para guardar el progreso.

Asumo que se debe eliminar los **caracteres de espacios** en el input del usuario (uso siempre `input().strip()`).

Asumo que las **multas** se pagan por separado. Es decir, que las multas se van pagando hasta que el Magizoólogo no tenga Sickles o no queden multas por pagar. Además, las multas que al DCC se les olvido cobrar no son mostradas.

Asumo que al ingresar un nombre para cargar un Magizoólogo, no se diferencia entre mayúsculas y minúsculas. Por ejemplo, al cargar el usuario, `lily416potter` y `Lily416Potter`, corresponden al mismo usuario.

Asumo que se debe poder alimentar a una criatura en **cualquier momento** para sanar parte de su salud.

Asumo que cuando Erkling roba un alimento, los efectos del alimento robado no son aplicados al Erkling.

Asumo que el orden de los eventos al pasar el día es:

- Por cada DCCriatura
  - Habilidad especial (si cumple requisitos)
  - Perder salud por enfermedad
  - Perder salud por hambre
  - Mostrar su salud si perdió alguna
  - Posibilidad de enfermarse
  - Posibilidad de escaparse
  - Aumento en los días sin comer
- Lista de DCCriaturas escapadas
- Lista de DCCriaturas enfermas
- DCC
  - Calcular la aprobación
  - Pagar Magizoólogo
  - Fiscalizar Magizoólogo
- Transformar a `SuperMagizoologo` (si la aprobación es mayor o igual a 100 y está activado en `parametros.py`)
- Recuperar toda la energía del Magizoólogo

## Diagrama de clases :bookmark_tabs:

![Diagrama de Clases](diagrama_clases.png?raw=true "Diagrama de Clases")

[Versión PDF](diagrama_clases.pdf)

### Aclaraciones

- `ZoologicoMagico`
  - El atributo `menu` es la estructura que tiene el programa. En el módulo `procesos` se explica el formato que tiene este. Se podría decir que el atributo `menu` es _el plano_ del programa, mientras que el modulo `procesos` es el que lo ejecuta.
  - Los métodos `crear_magizoologo` y `cargar_magizoologo` retornan `True` si la acción fue realizada correctamente, `False` en el caso contrario. Tienen relación con la estructura del atributo menú.
  - La property `magizoologo_actual` entrega el Magizoólogo actual, que está determinado por el `indice_magizoologo_actual`.
- `Magizoologos`
  - Los métodos `alimentar_criatura` y `recuperar_criatura` son llamados en las clases hijas, para realizar el procedimiento en común entre todos los Magizoólogos. Esta retornan una `DCCriatura` o `False`. En el caso que sea una `DCCriatura`, se le aplican a esta las habilidades pasivas de cada Magizoólogos. En el caso que sea `False`, no se hace nada. En las criaturas heredadas, el método retorna `None`.
- `DCCriaturas`
  - El método `caracteristica_unica` es un método abstracto.
- Generales
  - No pude combinar las clases `ZoologicoMagico` y `DCC`, ya que ambas tienen métodos complejos difíciles de realizar en 400 lineas. `DCC` se utiliza como una extensión de `ZoologicoMagico`.****

## Librerías :books:

### Librerías externas utilizadas :clipboard:

- **`abc`**
  - `ABC`: Genera clases abstractas.
  - `abstractmethod`: Genera métodos abstractos.
- **`random`**
  - `random`: Obtiene un número entre 0 y 1 al azar.
  - `randint`: Obtiene un número entero en un rango dado  al azar.
  - `choice`: Obtiene un elemento de un conjunto al azar.
- **`operator`**
  - `attrgetter`: Obtiene atributos de los objetos.
- **`os`**
  - `path` Para crear los paths de los archivos.

### Librerías propias :pencil:

- **`zoologico_magico`**
  - Encargado de la clase ZoologicoMagico.
- **`dcc`**
  - Encargado de la clase DCC.
- **`dccriaturas`**
  - Encargado de las clases DCCriaturas. Contiene un transformador de `str` a clase DCCriatura.
- **`magizoologos`**
  - Encargado de las clases Magizoologos. Contiene un transformador de `str` a clase Magizoologo.
- **`alimentos`**
  - Encargado de las clases de Alimentos. Contiene un transformador de `str` a clase Alimento.
- **`procesos`**
  - Encargado de el flujo del programa. Contiene 3 funciones:
    - `loop_menus()`: Encargada de administrar los menús.
    - `volver_a_intentarlo()`: Encargada de administrar los errores del usuario.
    - `proceso_multipaso()`: Encargada de administrar los procesos donde se piden multiples _inputs_.
- **`parametros`**: Encargada de los parametros del programa

## Código externo utilizado :package:

No utilicé código externo :tada:

## Características implementadas :wrench:

Todo fue implementado :tada:

- **OOP: 38pts (34%)**
  - Diagrama
    - [X] **2pt** Entrega el diagrama respetando el formato solicitado.
    - [X] **4pts** El diagrama contiene suficientes clases para modelar las entidades y funcionalidades pedidas. Cada clase contiene atributos y métodos respectivos para modelar el programa.
    - [X] **4pts** El diagrama contiene relaciones (agregación, composición y herencia) entre las clases incluidas, y mantiene consistencia de modelación.
  - Definición de clases, atributos y métodos
    - [X] **5pts** Los Magizoólogos están bien modelados.
    - [X] **5pts** Las DCCriaturas están bien modeladas.
    - [X] **3pts** Los alimentos están bien modelados.
    - [X] **4pts** El DCC está bien modelado.
  - Relaciones entre clases
    - [X] **8pts** Se utilizan clases abstractas cuando corresponde.
    - [X] **3pts** Utiliza consistentemente relaciones de agregación y composición.

- **Partidas: 14pts (13%)**
  - Crear Partidas
    - [X] **1pt** Se verifica que los nombres (del Magizoólogo y la DCCriatura) sean válidos y únicos.
    - [X] **1pt** Se permite elegir el tipo de Magizoólogo y de DCCriatura.
    - [X] **2pts** Se instancia correctamente el Magizoólogo seleccionado, considerando los valores iniciales de sus atributos.
    - [X] **2pts** Se instancia correctamente la DCCriatura seleccionada, considerando los valores iniciales de sus atributos.
    - [X] **1pt** Se muestra mensaje de error cuando el nombre que se ingresa no es válido y se deja volver a ingresar, volver atrás o salir.
  - Cargar partida
    - [X] **1pt** Se logra cargar un Magizoologo existente.
    - [X] **3pts** Poblar el sistema desde los archivos (magizoologo.csv y criaturas.csv) con las instancias correspondientes.
    - [X] **1pt** Se muestra mensaje de error cuando el nombre que se ingresa no es válido y se deja volver a ingresar, volver atrás o salir.
  - Guardar
    - [X] **4pt** Se actualiza correctamente la información de la partida en los archivos correspondientes (magizoologos.csv, criaturas.csv).

- **Acciones: 35pst (32%)**
  - Cuidar DCCriaturas
    - [X] **3pts** Se puede elegir a una criatura para alimentar y el alimento a utilizar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [X] **1pt** Se aplica correctamente los efectos de los alimentos.
    - [X] **1pt** Se implementa correctamente la posibilidad de ataque de las DCCriaturas sus dueños.
    - [X] **3pts** Se muestra las criaturas que se han escapado y se puede elegir una para recuperar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [X] **3pts** Se muestran todas las DCCriaturas que se han enfermado y se puede elegir una para sanar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [X] **2pts** Se implementa correctamente la habilidad especial según el tipo de Magizoólogo.
    - [X] **2pts** Se descuenta el costo de energía mágica correspondiente a las acciones alimentar, recuperar y sanar.
    - [X] **1pts** Se notifica en caso de no tener energía suficiente para realizar la acción.
  - DCC
    - [X] **2pts** Se puede adoptar una DCCriatura correctamente, si se cumplen las condiciones.
    - [X] **2pts** Se puede comprar cualquiera de los alimentos disponibles correctamente.
    - [X] **1.5pts** Se descuenta el valor de sickles correspondiente al adoptar DCCriaturas y se notifica en caso de no poder realizarse la acción.
    - [X] **1.5pts** Se descuenta el valor de sickles correspondiente al comprar alimentos y se notifica en caso de no poder realizarse la acción.
    - [X] **2pts** Se pueden visualizar los datos actualizados del estado del Magizoólogo y de las DCCriaturas correctamente.
  - Pasar al día siguiente
    - [X] **2pts** Se aplican correctamente las habilidades especiales de cada DCCriatura.
    - [X] **2pts** Se actualiza correctamente el estado de salud de las DCCriaturas.
    - [X] **1pt** Se actualiza el estado de hambre de cada DCCriatura dependiendo del tiempo que lleva sin comer.
    - [X] **1pt** Se actualiza correctamente el estado de salud de las DCCriaturas.
    - [X] **2pts** Se actualiza correctamente la cantidad de DCCriaturas escapadas.
    - [X] **2pts** Se actualiza correctamente el nivel de aprobación y el estado de la licencia del Magizoólogo.
    - [X] **2pts** Se paga correctamente la cantidad de sickles al Magizoólogo y se actualiza la cantidad de sickles que tiene.
    - [X] **2pts** La fiscalización se realiza correctamente: se calculan multas según los eventos de DCCriaturas.

- **Consola: 15 pts (14%)**
  - Menú de inicio
    - [X] **2pts** El menú contiene las opciones mínimas pedidas.
  - Menú de acciones
    - [X] **2pts** El menú contiene las opciones mínimas pedidas.
  - Menú DCCriaturas
    - [X] **2pts** El menú contiene las opciones mínimas pedidas.
  - Menú DCC
    - [X] **2pts** El menú contiene las opciones mínimas pedidas.
  - Pasar al día siguiente
    - [X] **3pts** Visualiza los resúmenes de todos los eventos del día que se mencionan en el enunciado.
  - Robustez
    - [X] **4pts** Todos los menús son a prueba de errores.

- **Manejo de archivos: 9pts (8%)**
  - Archivos CSV
    - [X] **5pts** Trabaja correctamente con todos los archivos CSV entregados.
  - parámetros
    - [X] **2pts** Utiliza e importa correctamente `parametros.py`.
    - [X] **2pts** Archivo `parametros.py` contiene todos los parámetros especificados en el enunciado.

- Bonus
  - Super MagizoólogoDocencioTareoHíbrido (3 décimas)
    - [X] Se implementa correctamente el bonus con todo lo que se pide.
      - Se transforma a Super
  - Peleas entre DCCriaturas (5 décimas)
    - [X] Se implementa correctamente el bonus con todo lo que se pide.
  - Bonus avance (2 décimas)
    - [X] 1/2
  - Bonus README (de-descuento 5 décimas)
    - [ ] :thinking:

## Notas adicionales :moyai:

Estoy probando documentar mi código con [type hinting](https://www.python.org/dev/peps/pep-0484/#type-definition-syntax) y [docstring](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring). No estoy siguiendo una convención y tampoco he documentado todo.

Traté de modelar las clases de una forma que sean lo más independientes entre ellas. No pude lograrlo completamente, como es el caso de `DCC` y `MagizoologicoMagico` que deberían ser una única clase, pero la clase `Magizoologico` debería poder funcionar fuera de la clase `MagizoologicoMagico`.

Agregué algunas opciónes adicionales a las pedidas en `parametros.py`, como por ejemplo, que el DCC elija la criatura en la batalla y que la clase SuperMagizoólogo esté desactivada.

Disfrute el programa :tada:
