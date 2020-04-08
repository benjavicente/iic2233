# Tarea 01: DCCriaturas Fantásticas :bird:


## Importante :heavy_exclamation_mark:

**Estoy organizando mi progreso en [TODO.md](/avance/TODO.md) y la carpeta avance**
(Voy a eliminarlos entes de terminar la tarea).


## Ejecución :computer:

El programa a ejecutar _(por ahora)_ es **`ZoologicoMagico.py`**

Los archivos de datos, `criatuas` y `magizoologos`, deben estar creados en una carpeta llamada `data`. El formato de cada uno es de `csv`, donde cada campo termina con una nueva linea.

Los módulos `dcc`, `dccriaturas`, `magizoologos`, `alimentos` y `procesos` deben encontrarse en el mismo _path_ que `ZoologicoMagico.py`.

## Supuestos y consideraciones :thinking:

~~Ninguno? :thinking:~~

Asumo que se debe eliminar los caracteres de espacios en el input del usuario (uso siempre `input().strip()`).


## Diagrama de clases :bookmark_tabs:

![Diagrama de Clases](diagrama_clases.png?raw=true "Diagrama de Clases")

:point_right: Hasta ahora tengo en el ZoologicoMágico métodos que corresponden a _acciones_ en el menú. Estoy testeando la posibilidad de almacenar estas _acciones_ en `lambda`s.

:point_right: Todavía no implemento completamente Magizoólogos ni DCCriaturas, por lo que algunos métodos pueden cambiar.

:point_right: No existen relaciones de _agregación simple_, ya que las DCCriaturas, Magizoólogos y DCC dependen de que exista un ZoologicoMagico.

## Características implementadas :wrench:

Los puntos de la pauta 

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
    - [ ] Se puede elegir a una criatura para alimentar y el alimento a utilizar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [ ] Se aplica correctamente los efectos de los alimentos.
    - [ ] Se implementa correctamente la posibilidad de ataque de las DCCriaturas sus dueños.
    - [ ] Se muestra las criaturas que se han escapado y se puede elegir una para recuperar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [ ] Se muestran todas las DCCriaturas que se han enfermado y se puede elegir una para sanar correctamente. Se actualiza correctamente el estado de la DCCriatura.
    - [ ] Se implementa correctamente la habilidad especial según el tipo de Magizoólogo.
    - [ ] Se descuenta el costo de energía mágica correspondiente a las acciones alimentar, recuperar y sanar.
    - [X] Se notifica en caso de no tener energía suficiente para realizar la acción.
  - DCC (En testeo)
    - [ ] Se puede adoptar una DCCriatura correctamente, si se cumplen las condiciones.
    - [ ] Se puede comprar cualquiera de los alimentos disponibles correctamente.
    - [ ] Se descuenta el valor de sickles correspondiente al adoptar DCCriaturas y se notifica en caso de no poder realizarse la acción.
    - [ ] Se descuenta el valor de sickles correspondiente al comprar alimentos y se notifica en caso de no poder realizarse la acción.
    - [X] Se pueden visualizar los datos actualizados del estado del Magizoólogo y de las DCCriaturas correctamente.
  - Pasar al día siguiente
    - [ ] Se aplican correctamente las habilidades especiales de cada DCCriatura.
    - [ ] Se actualiza correctamente el estado de salud de las DCCriaturas.
    - [ ] Se actualiza el estado de hambre de cada DCCriatura dependiendo del tiempo que lleva sin comer.
    - [ ] Se actualiza correctamente el estado de salud de las DCCriaturas.
    - [ ] Se actualiza correctamente la cantidad de DCCriaturas escapadas.
    - [ ] Se actualiza correctamente el nivel de aprobación y el estado de la licencia del Magizoólogo.
    - [ ] Se paga correctamente la cantidad de sickles al Magizoólogo y se actualiza la cantidad de sickles que tiene.
    - [ ] La fiscalización se realiza correctamente: se calculan multas según los eventos de DCCriaturas.

- Consola
  - Menú de inicio
    - [X] El menú contiene las opciones mínimas pedidas.
  - Menú de acciones
    - [X] El menú contiene las opciones mínimas pedidas.
  - Menú DCCriaturas
    - [X] El menú contiene las opciones mínimas pedidas.
  - Menú DCC
    - [X] El menú contiene las opciones mínimas pedidas.
  - Pasar al día siguiente
    - [ ] Visualiza los resumenes de todos los eventos del día que se mencionan en el enunciado.
  - Robustez
    - [X] Todos los menús son a prueba de errores.

- Manejo de archivos
  - Archivos CSV
    - [X] Trabaja correctamente con todos los archivos CSV entregados.
  - parametros
    - [X] Utiliza e importa correctamente `parametros.py`.
    - [X] Archivo `parametros.py}` contiene todos los parámetros especificados en el enunciado.

- Bonus
  - Super MagizoólogoDocencioTareoHíbrido
    - [ ] Se implementa correctamente el bonus con todo lo que se pide.
  - Peleas entre DCCriaturas
    - [ ] Se implementa correctamente el bonus con todo lo que se pide.

## Librerías :books:

### Librerías externas utilizadas :clipboard:

- **`abc`**
  - `ABC`: Genera clases abstractas.
  - `abstractmethod`: Genera métodos abstractos.
- **`random`**
  - `random`: Obtiene un número entre 0 y 1.
  - `randint`: Obtiene un número entero en un rango dado.
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
