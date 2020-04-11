# Tarea 01: DCCriaturas Fantásticas :bird:

- [Tarea 01: DCCriaturas Fantásticas :bird:](#tarea-01-dccriaturas-fant%c3%a1sticas-bird)
  - [Importante :heavy_exclamation_mark:](#importante-heavyexclamationmark)
  - [Ejecución :computer:](#ejecuci%c3%b3n-computer)
  - [Supuestos y consideraciones :thinking:](#supuestos-y-consideraciones-thinking)
  - [Diagrama de clases :bookmark_tabs:](#diagrama-de-clases-bookmarktabs)
  - [Características implementadas :wrench:](#caracter%c3%adsticas-implementadas-wrench)
  - [Librerías :books:](#librer%c3%adas-books)
    - [Librerías externas utilizadas :clipboard:](#librer%c3%adas-externas-utilizadas-clipboard)
    - [Librerías propias :pencil:](#librer%c3%adas-propias-pencil)
  - [Código externo utilizado :package:](#c%c3%b3digo-externo-utilizado-package)
  - [Notas adicionales :moyai:](#notas-adicionales-moyai)

## Importante :heavy_exclamation_mark:

**Estoy organizando mi progreso en [TODO.md](/avance/TODO.md) y la carpeta avance**
(Voy a eliminarlos entes de terminar la tarea).

Hay strings incompletos, por lo que en la consola existen menús pocos descriptivos.

## Ejecución :computer:

El programa a ejecutar _(por ahora)_ es **`ZoologicoMagico.py`**

Los archivos de datos, `criatuas` y `magizoologos`, deben estar creados en una carpeta llamada `data`. El formato de cada uno es de `csv`, donde cada campo termina con una nueva linea.

Los módulos `dcc`, `dccriaturas`, `magizoologos`, `alimentos` y `procesos` deben encontrarse en el mismo _path_ que `ZoologicoMagico.py`.

## Supuestos y consideraciones :thinking:

Considero que la DCCriatura Augurey puede entregar un alimento a su dueño si esta se escapó.

Asumo que los cambios en los datos solo se guardan al salir por el menú y no por el proceso fallido. He agradado la opción de guardar sin salir para no tener que salir para guardar el progreso.

Asumo que se debe eliminar los caracteres de espacios en el input del usuario (uso siempre `input().strip()`).

Asumo que las licencias se pagan por separado. Es decir, que las multas se van pagando hasta que el Magizoólogo no tenga Sickles o halla pagado todas las multas.

Asumo que al ingresar un nombre para cargar un Magizoólogo, no se diferencia entre mayúsculas y minúsculas. Por ejemplo, cargar el usuario `lily416potter` se puede usar (por ejemplo) `lily416potter` y `Lily416Potter`, que corresponden al mismo usuario.

Asumo que se debe poder alimentar a una criatura en cualquier momento para sanar parte de su salud. Tanto criaturas hambrientas como satisfechas pueden ser alimentadas.

## Diagrama de clases :bookmark_tabs:

![Diagrama de Clases](diagrama_clases.png?raw=true "Diagrama de Clases")

:point_right: Hasta ahora tengo en el ZoologicoMágico métodos que corresponden a _acciones_ en el menú. Estoy testeando la posibilidad de almacenar estas _acciones_ en `lambda`s.

:point_right: Todavía no implemento completamente Magizoólogos ni DCCriaturas, por lo que algunos métodos pueden cambiar.

:point_right: No existen relaciones de _agregación simple_, ya que las DCCriaturas, Magizoólogos y DCC dependen de que exista un ZoologicoMagico.

:point_right: MagizoologoSuper (o SuperMagizoólogoDocencioTareoHíbrido) no lo he implementado aún. Este puede terminar con métodos propios.

## Características implementadas :wrench:

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
    - [ ] **3pts** Se puede elegir a una criatura para alimentar y el alimento a utilizar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [ ] **1pt** Se aplica correctamente los efectos de los alimentos.
    - [ ] **1pt** Se implementa correctamente la posibilidad de ataque de las DCCriaturas sus dueños.
    - [ ] **3pts** Se muestra las criaturas que se han escapado y se puede elegir una para recuperar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [ ] **3pts** Se muestran todas las DCCriaturas que se han enfermado y se puede elegir una para sanar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [ ] **2pts** Se implementa correctamente la habilidad especial según el tipo de Magizoólogo.
    - [ ] **2pts** Se descuenta el costo de energía mágica correspondiente a las acciones alimentar, recuperar y sanar.
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
  - parametros
    - [X] **2pts** Utiliza e importa correctamente `parametros.py`.
    - [X] **2pts** Archivo `parametros.py}` contiene todos los parámetros especificados en el enunciado.

- Bonus
  - Super MagizoólogoDocencioTareoHíbrido (3 décimas)
    - [ ] Se implementa correctamente el bonus con todo lo que se pide.
  - Peleas entre DCCriaturas (5 décimas)
    - [ ] Se implementa correctamente el bonus con todo lo que se pide.
  - Bonus avance (2 décimas)
    - [ ] :question:
  - Bonus README (de-descuento 5 décimas)
    - [ ] :question:

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

- **`dcc`**
  - Encargado de la clase DCC.
- **`dccriaturas`**
  - Encargado de las clases DCCriaturas. Contiene un transformador de str a clase DCCriatura.
- **`magizoologos`**
  - Encargado de las clases Magizoologos. Contiene un transformador de str a clase Magizoologo.
- **`alimentos`**
  - Encargado de las clases de Alimentos. Contiene un transformador de str a clase Alimento.
- **`procesos`**
  - Encargado de el flujo del programa. Contiene 3 funciones:
    - `loop_menus()`: Encargada de administrar los menús.
    - `volver_a_intentarlo()`: Encargada de administrar los errores del usuario.
    - `proceso_multipaso()`: Encargada de administrar los procesos donde se piden multiples _inputs_.

## Código externo utilizado :package:

Ninguno :tada:

## Notas adicionales :moyai:

Disfrute el programa :tada:
