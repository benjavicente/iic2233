# TODO

Mezcla de "Resumen" del enunciado y notas.

**TODO**: todo

- Modelar los diagramas (diagrams.net) (listo?)
- Ver como guardar y cargar las los datos de las clases, y como utilizar valores predeterminados
- Crear un esquema para los menús

Tengo que ver como puedo organizar los menús de manera que no tenga que repetir código. Se me ocurrió usar diccionarios de la siguiente forma:

```py
menu = {
    "menu de inicio": ("Crear Magizoólogo", "Cargar Magizoólogo")
    ...
}
actual = "menu de inicio"
for n, opc in enumerate(menu[actual]):
    print(f"[{n}] {opc}")
print(f"[{n+1}] Volver")
print(f"[{n+2}] Salir")
```

Pero con esto tengo hasta ahora dos problemas:

1. Tengo que encontrar una manera de ejecutar funciones. Por ejemplo, si el usuario se encuentra en el menu de crear Magizoólogo, debe existir una función que tome el nombre del Magizoólogo y lo cree si es valido.
2. Tengo que encontrar una manera evitar casos bordes. Por ejemplo, como saltar del menú volver a intentarlo a el menu de inicio.


**Notas generales**:
Puede ser mejor cambiar el nombre de _puntos de salud_ a _puntos de vida_ para evitar la confusión con _estado de salud_.

- [TODO](#todo)
  - [Menús](#men%c3%bas)
    - [General](#general)
    - [Menús de inicio](#men%c3%bas-de-inicio)
    - [Menú de acciones](#men%c3%ba-de-acciones)
    - [Menú cuidar DCCriaturas](#men%c3%ba-cuidar-dccriaturas)
    - [Menú DCC](#men%c3%ba-dcc)
    - [Pasar al día siguiente](#pasar-al-d%c3%ada-siguiente)
  - [Entidades](#entidades)
    - [Magizoólogos](#magizo%c3%b3logos)
      - [Atributos Magizoólogos](#atributos-magizo%c3%b3logos)
      - [Métodos Magizoólogos](#m%c3%a9todos-magizo%c3%b3logos)
      - [Magizoólogo Docencio](#magizo%c3%b3logo-docencio)
      - [Magizoólogo Tareo](#magizo%c3%b3logo-tareo)
      - [Magizoólogo Híbrido](#magizo%c3%b3logo-h%c3%adbrido)
    - [DCCriaturas](#dccriaturas)
      - [Atributos DCCriaturas](#atributos-dccriaturas)
      - [Métodos DCCriaturas](#m%c3%a9todos-dccriaturas)
      - [DCCriatura Augurey](#dccriatura-augurey)
      - [DCCriatura Niffler](#dccriatura-niffler)
      - [DCCriatura Erkling](#dccriatura-erkling)
    - [Alimentos](#alimentos)
      - [Atributo Alimentos](#atributo-alimentos)
      - [Alimento Tarta de Maleza](#alimento-tarta-de-maleza)
      - [Alimento Hígado de Dragon](#alimento-h%c3%adgado-de-dragon)
      - [Alimento Buñuelo de Gusarajo](#alimento-bu%c3%b1uelo-de-gusarajo)
    - [DCC](#dcc)
      - [Métodos DCC](#m%c3%a9todos-dcc)
  - [Archivos](#archivos)
    - [`magizoologos.csv`](#magizoologoscsv)
    - [`criaturas.csv`](#criaturascsv)
    - [`parametros.py`](#parametrospy)
  - [_Bonus_ del programa :tada:](#bonus-del-programa-tada)
    - [Super Mágizoólogo DocencioTareaHíbrido (3 décimas)](#super-m%c3%a1gizo%c3%b3logo-docenciotareah%c3%adbrido-3-d%c3%a9cimas)
    - [Peleas entre DCCriaturas (5 décimas)](#peleas-entre-dccriaturas-5-d%c3%a9cimas)
  - [_Bonus_ de la entrega](#bonus-de-la-entrega)
    - [Bonus avance (2 décimas)](#bonus-avance-2-d%c3%a9cimas)
    - [Bonus README?](#bonus-readme)

## Menús

**Notas:** Se puede crear una clase `InterfazDeUsuario` que administre el menú del usuario. Como atributos puede tener:

- `lista_menus_anteriores`:
  - Lista que almacene los menús anteriores.
- `menu_anterior`:
  - String que retorne el menu anterior.
- `menú_actual`:
  - String que almacene el menu actual.
- `opciones`:
  - Diccionario que almacene las opciones exclusivas de cada menú.
- `mostrar_opciones()`:
  - Método encargado de printear las opciones al usuario.
- `elegir(menu)`:
  - Método que se encargue de entrar al nuevo menú. Recibe un string.

### General

- [ ] A prueba de errores de usuario
- [ ] Opción de volver atrás
- [ ] Opción de salir

### Menús de inicio

Menú de entrada al programa

- [ ] Crear Magizoólogo
  - [ ] Nombres alfanuméricos
  - [ ] Nombres únicos (no importa las mayúsculas, Al == al)
  - [ ] Al ser no válido:
    - [ ] Se indica el error
    - [ ] Volver a intentarlo
    - [ ] Volver atrás
    - [ ] Salir
  - [ ] Al ser válido:
    - [ ] Elegir entre Docencio, Tarea o Híbrido
    - [ ] Desplegar una lista de especies de DCCriaturas
    - [ ] Elegir DCCriatura con nombre único alfanumérico
    - [ ] Volver a intentarlo
    - [ ] Volver atrás
    - [ ] Salir
- [ ] Cargar Magizoólogo
- [ ] Salir

### Menú de acciones

Menu principal, donde se accede iniciar sesión o crear un nuevo Magizoólogo

- [ ] Menú cuidar DCCriaturas
- [ ] Menú DCC
- [ ] Pasar al día siguiente
- [ ] Volver atrás
- [ ] Salir

### Menú cuidar DCCriaturas

Todas las acciones poseen un costo de energía. Si el usuario no posee energía suficiente, se le avisa y no se realiza la acción.

- [ ] Alimentar DCCriatura
  - [ ] Seleccionar criatura a alimentar
  - [ ] Seleccionar que alimento
- [ ] Recuperar DCCriatura
  - [ ] Mostrar DCCriaturas que han escapado
  - [ ] Seleccionar criatura
- [ ] Sanar DCCriatura
  - [ ] Mostrar criaturas enfermas
  - [ ] Seleccionar criatura
- [ ] Usar habilidad especial
  - [ ] Habilidad única
- [ ] Volver atrás
- [ ] Salir

### Menú DCC

Las acciones Adoptar y Comprar tienen un costo monetario. Si no se posee fondos, se avisa.

- [ ] Adoptar DCCriaturas
  - [ ] Opción de adoptar una criatura por Sickles.
- [ ] Comprar alimentos
  - [ ] Opción de comprar alimentos por Sickles.
- [ ] Ver estado de Magizoólogo
  - [ ] Imprime los datos del Magizoólogo
- [ ] DCCriaturas
  - [ ] Imprime los datos de las DCCriaturas
- [ ] Volver atrás
- [ ] Salir

### Pasar al día siguiente

**Nota:** Creo que es importante añadir una confirmación para evitar pasar de día por error.

- [ ] Cada día existe una probabilidad que una DCCriatura se enferme o se escape.
- [ ] Si una criatura lleva días sin comer, entonces cambia su hambre.

Todo lo anterior puede ocurrir simultáneamente.

- [ ] Luego, se fiscaliza al usuario.
- [ ] Según los los atributos del usuario y sus criaturas, se calcula si este debe mantener su licencia.
- [ ] DCC le paga el sueldo al usuario, y lo multa si es necesario.

Todo lo anterior debe ser reportado al usuario,
junto a su nivel de aprobación y su saldo.

Finalmente, vuelve al menu de acciones.

## Entidades

Los datos de las entidades deben almacenarse en los archivos.

### Magizoólogos

#### Atributos Magizoólogos

- [ ] **Nombre** `str`: nombre elegido y único.
- [ ] **Sickles** `int`: inicialmente 500, no puede ser negativo.
- [ ] **Criaturas** `list`: inicialmente una criatura elegida.
- [ ] **Alimentos** `list`: inicialmente 1 alimento aleatorio.
- [ ] **Licencia** `bool`: inicialmente True.
- [ ] **Nivel mágico** `int`.
- [ ] **Destreza** `int`.
- [ ] **Energía total** `int`.
- [ ] **Responsabilidad** `int`.
- [ ] **Energía actual** `int`: Entre 0 y un valor máximo. Su valor inicial y máximo dependen del tipo de Magizoólogo.
- [ ] **Nivel de aprobación** `int`: entre 0 y 100, si es menor que 60 se pierde la licencia.

#### Métodos Magizoólogos

- [ ] **Adoptar DCCriaturas al DCC**: Se adopta una criatura si se posee licencia y dinero suficiente.
- [ ] **Comprar alimentos al DCC**: Se compra alimentos si posee suficiente dinero.
- [ ] **Alimentar DCCriatura**: Alimenta a una criatura si posee alimentos, la criatura puede atacar a su dueño, el costo energético es de 5 puntos.
- [ ] **Recuperar DCCriatura**: El costo energético es de 5 puntos, la probabilidad de éxito es:

$$
  \min\left(1, \max\left(0, \dfrac{\text{destreza} + \text{nivel\_magico\_magizoologo} - \text{nivel\_magico\_criatura}}{\text{destreza} - \text{nivel\_magico\_magizoologo} - \text{nivel\_magico\_criatura}}\right)\right)
$$

- [ ] **Sanar DCCriatura**: El coste energético es de 8 puntos, la probabilidad de éxito es:

$$
  \min\left(1, \max\left(0, \dfrac{\text{nivel\_magico\_magizoologo} - \text{salud\_actual\_criatura}}{\text{nivel\_magico\_magizoologo} - \text{salud\_actual\_criatura}}\right)\right)
$$

- [ ] **Habilidad especial**: utiliza la habilidad especial, tiene un costo energético de 15 puntos.

#### Magizoólogo Docencio

- Al alimentar sus DCCriaturas logran aumentar 5 puntos de salud a ella.
- Al recuperar sus criaturas , _merman_ la salud de la criatura en 7 puntos.
- Su habilidad especial es saciar el hambre de todas sus criaturas. Solo puede realizarse una vez.
- El nivel mágico varia entre 40 y 60.
- La destreza varia entre 30 y 40.
- La energía total estarán entre 40 y 50.
- La responsabilidad varía entre 15 y 20.

#### Magizoólogo Tareo

- Alimentar sus DCCriaturas tiene una probabilidad de 70% de recuperar toda su salud
- Habilidad especial de recuperar todas sus criaturas que se hayan escapado. Solo se puede ocupar una vez
- El nivel mágico varia entre 40 y 55
- La destreza varia entre 40 y 50
- La energía total estarán entre 35 y 45
- La responsabilidad varía entre 10 y 25

#### Magizoólogo Híbrido

- Al alimentar a una DCCriatura aumentan 10 puntos la salud de ella
- La habilidad especial es sanar a todas sus criaturas, solo una vez
- El nivel mágico varia entre 35 y 45
- La destreza varia entre 30 y 50
- La energía total estarán entre 50 y 55
- La responsabilidad varía entre 15 y 25

### DCCriaturas

#### Atributos DCCriaturas

- [ ] **Nombre** `str`: identificador de cada criatura.
- [ ] **Nivel mágico** `int`.
- [ ] **Puntos de salud total** `int`.
- [ ] **Puntos de salud actual** `int`: mínimo 1.
- [ ] **Probabilidad de escape** `float`: entre 0 y 1.
- [ ] **Probabilidad de enfermarse** `float`: entre 0 y 1.
- [ ] **Estado de salud** `bool`: si es false, pierde 7 de salud.
- [ ] **Nivel de hambre** `str`: es `"satisfecha"` o `"hambrienta"`, si esta hambrienta, pierde 3 de salud.
- [ ] **Días sin comer** `int`.
- [ ] **Nivel de agresividad** `str`: es `"inofensiva"`, `"arisca"`  o `"peligrosa"`

#### Métodos DCCriaturas

Las probabilidad de realizar estas acciones se administran dentro del objeto.

- [ ] **Alimentarse**: Si la criatura esta hambrienta, pasa a estar satisfecha, la probabilidad de que este ataque a su Magizoólogo es:

$$
  \min\left(1, \dfrac{\text{efecto\_hambre} + \text{efecto\_agresividad}}{100}\right)
$$

Donde $\text{efecto\_hambre}$ es 0 si la criatura está satisfecha y 15 si esta hambrienta, y $\text{efecto\_agresividad}$ es 0, 20 y 40 si la criatura es inofensiva, arisca y peligrosa respectivamente.

En caso de ocurrir un ataque, los puntos de energía perdidos son:

$$
  \max\left(10, \text{nivel\_magico\_magizoologo} - \text{nivel\_magico\_criatura}\right)
$$

- [ ] **Escaparse**: La probabilidad de escaparse es:

$$
  \min\left(1, \text{prob\_escaparse} + \max\left(0, \dfrac{\text{efecto\_hambre} - \text{resp\_magizoologo}}{100}\right)\right)
$$

Donde $\text{efecto\_hambre}$ es 0 si la criatura está satisfecha y 20 si esta hambrienta.

- [ ] **Enfermarse**: La probabilidad de enfermarse es:

$$
  \min\left(1, \text{prob\_enfermase} + \max\left(0, \dfrac{\text{salud\_total} - \text{salud\_actual}}{\text{salud\_total}} - \dfrac{\text{resp\_magizoologo}}{100}\right)\right)
$$

#### DCCriatura Augurey

Pájaro delgado, pequeño y triste, con plumaje brillante. Es capaz de predecir la lluvia con muchos días de anticipación y le gusta volar solo cuando esta bien cuidado. Es poco probable que ataque a su dueño.

- Su nivel mágico varia entre 20 y 50
- Su probabilidad de escaparse es 0.2
- Su probabilidad de enfermase es 0.3
- Sus puntos de salud oscilan entre 35 y 45
- Pasa de satisfecha a hambrienta en 3 días
- Su nivel de agresividad es inofensiva
- Especial: Si al inicio del día no tiene hambre, no esta enfermo y tiene los puntos de salud al máximo, entregará un alimento a su dueño

#### DCCriatura Niffler

Criatura pequeña, de pelaje sedoso y hocico largo, similar a un ornitorrinco. Es increíblemente inquieto y le encantan las cosas brillantes, por lo que suele robar Sickles para luego guardarlos en su pelaje. Tiende a ser agresivo.

- Su nivel mágico varia entre 10 y 20
- Su probabilidad de escaparse es 0.3
- Su probabilidad de enfermase es 0.2
- Sus puntos de salud oscilan entre 20 y 30
- Pasa de satisfecha a hambrienta en 2 días
- Su nivel de agresividad es arisca
- Especial: posee un nivel de cleptomanía `int` entre 5 y 10. Si esta criatura esta satisfecha al comienzo del día, entregará Sickles a su dueño, en el caso contrario, le robará. La cantidad a entregar o robra es:

$$
  \text{nivel\_cleptomania} \times 2
$$

#### DCCriatura Erkling

Las criaturas más peligrosas de todas. Con un parecido a los elfos, suelen parecer desapercibidos, pero son violentos.

- Su nivel mágico varia entre 30 y 45
- Su probabilidad de escaparse es 0.5
- Su probabilidad de enfermase es 0.3
- Sus puntos de salud oscilan entre 50 y 60
- Pasa de satisfecha a hambrienta en 2 días
- Su nivel de agresividad es peligrosa
- Especial: si la criatura está hambrienta al comienzo del día robará cualquier alimento y pasará a estar satisfecha. Si el dueño no tiene alimentos, no hace nada

### Alimentos

#### Atributo Alimentos

- [ ] **Efecto de salud** `int` cantidad de puntos que aumentará la salud de la DDCriatura al consumirla

#### Alimento Tarta de Maleza

Alimento muy apetecido por los Magizoólogos para dárselos a las DCCriaturas, pues posee buenas propiedades respecto al resto de los alimentos.

- Efecto de salud de 15
- Si es consumido por un Niffler, existe una probabilidad de 0.15 en que la agresividad pase de arisca a inofensiva de manera permanente

#### Alimento Hígado de Dragon

Conocido por ser un alimento con propiedades medicinales.

- Efecto de salud de 10
- Si la DCCriatura está enferma, se sanará

#### Alimento Buñuelo de Gusarajo

Es el alimento menos costoso.

- Efecto de salud de 5
- Existe una probabilidad de 0.35 que la criatura rechace el alimento y este se pierda.

### DCC

institución más seria y respetable del mundo mágico. Permite fiscalizar Magizoólogos y aplicarles multas en el caso de que incurran en una falta,Además controlan el nivel de aprobación de los Magizoólogos, pudiendo quitarles la licencia.

#### Métodos DCC

- [ ] **Calcular nivel de aprobación**: se calcula el nivel de aprobación con la formula:

$$
  \min\left(100, \max\left(0, \left[\dfrac{\text{n\_criaturas\_sanas} + \text{n\_criaturas\_retenidas}}{2 \times \text{n\_criaturas\_totales}}\right]\times 100\right)\right)
$$
Si es menor que 60, se quita la licencia al Magizoólogo.

- [ ] **Pagar a los Magizoólogos**: La cantidad a pagar es:

$$
  \text{n\_aprobación}\times4+\text{cantidad\_alimento}\times15+\text{nivel\_magico\_magizoologo}\times3
$$

- [ ] **Fiscalizar a los Magizoólogos**: Las posibles multas son:
  - El escape de una criatura: 50 Sickles con probabilidad de 0.5
  - La enfermedad de una criatura: 70 Sickles con probabilidad de 0.7
  - La salud de una criatura: 150 Sickles, sin excepción

Si no se posee dinero, no se cobrará la multa pero el Magizoólogo perderá la licencia.

- [ ] **Vender criatura a Magizoólogo**: un Magizoólogo puede adquirir una criatura si posee una licencia, los costos son:
  - Augurey: 75 Sickles
  - Niffler: 100 Sickles
  - Erkling: 125 Sickles

- [ ] **Vender alimento a Magizoólogo**: un Magizoólogo puede adquirir alimentos, cuyos costos son:
  - Tarta de Melaza: 10 Sickles
  - Hígado de Dragón: 15 Sickles
  - Buñuelos de Gusarajo: Sickles

- [ ] **Mostrar estado de Magizoólogo y DCCriaturas**: se muestra en la pantalla todos los valores de atributos relevantes del usuario Magizoólogo. Debe mostrar:
  - Nombre
  - Sickles
  - Energía actual
  - Licencia
  - Nivel de aprobación
  - Nivel mágico
  - Destreza
  - Responsabilidad
  - Lista de los alimentos
    - Tipos
    - Efectos a la salud
  - Lista de DCCriaturas
    - Nombre
    - Nivel mágico
    - Puntos de salud actual
    - Estado de salud
    - Nivel de hambre
    - Nivel de agresividad

## Archivos

### `magizoologos.csv`

| Nombre | Tipo | Descripción |
| -: | :-: | :- |
| Nombre   | `str` | Nombre del Magizoólogo |
| Tipo | `str` | Tipo de Magizoólogo |
| Sickles | `int` | Dinero del Magizoólogo |
| Criaturas | `list` | Nombres de criaturas separadas por `;` |
| Alimentos | `list` | Alimentos separados por `;` |
| Licencia | `bool` | Si el Magizoólogo posee la licencia |
| NivelMag | `int` | Nivel mágico |
| Destreza | `int` | Destreza |
| Energía | `int` | Energía total |
| Responsabilidad | `int` | Responsabilidad |
| HabEspecial | `bool` | Si ha realizado o no su habilidad especial |

### `criaturas.csv`

| Nombre | Tipo | Descripción |
| -: | :-: | :- |
| Nombre   | `str` | Nombre de la DCCriatura |
| Tipo | `str` | Tipo de DCCriatura |
| NivelMag | `int` | Nivel mágico |
| ProbEsc | `float` | Probabilidad de escaparse |
| ProbEnf | `float` | Probabilidad de enfermarse |
| Enferma | `bool` | Si se enfermó |
| Escapado | `bool` | Si se escapó |
| PtsSaludTot | `int` | Salud máxima |
| PtsSaludAct | `int` | Salud total |
| NivelHam | `str` | Nivel de hambre |
| NivelAgr | `str` | Nivel de agresividad |
| DiasSinCom | `str` | Días sin comer |
| NivelClep | `str` | Nivel de cleptomanía |

### `parametros.py`

**Nota**: en la T0 no pude utilizar variables globales (que eran parámetros que no cambiaban) por ser consideradas _malas practicas_, pero esto me va a ayudar :sweat_smile:

Son variables escritas completamente en mayúscula (`PARAMETRO_ESPECIAL`) que no se modifican.

## _Bonus_ del programa :tada:

Solo aplicable si la nota es igual o superior a 4.0 y si se completa en su totalidad.

### Super Mágizoólogo DocencioTareaHíbrido (3 décimas)

Se debe implementar la nueva (y poderosa) clase Mágizoólogo DocencioTareaHíbrido, la cual **hereda de Mágizoólogo Docencio, Mágizoólogo Tareo y Mágizoólogo Híbrido**, de modo que tendrá los siguientes beneficios:

- 0.7 de probabilidad que al alimentar una criatura esta recupere toda su salud
- al alimentar una criatura, esta recupera inmediatamente 10 puntos
- al capturar una criatura, está no pierde la salud.

Si un Mágizoólogo alcanza el nivel de aprobación de 100, entonces se convertirá en uno, notificando al usuario.

El nuevo Mágizoólogo DocencioTareaHíbrido debe conservar sus atributos anteriores.

El tipo en el archivo `magizoologo.csv` es "super".

### Peleas entre DCCriaturas (5 décimas)

En el menú _"cuidar"_ DCCriaturas se debe añadir la acción Peleas
entre DCCriaturas, el el que se mostraran un listado de todas las criaturas que estén al cuidado del Magizoólogo (Si es que existen al menos 2), para luego elegir dos criaturas: una que represente al usuario y otra que represente al DCC.

Se apuesta 30 Sickles antes de empezar.

La batalla se realizará entre turnos, donde se notifica que:

- Una DCCriatura está atacando a otra
- El daño que recibe la DCCriatura o si esquivo el ataque
- Puntos de salud restantes de la criatura atacada
- Si una criatura queda con 1 punto de salud, termina el combate

El daño de la criatura está modelada con la siguiente función:

$$
  \text{daño} = \begin{cases}
    \text{criatura.nivel\_magico} \times 0.25 & \text{si el atacante es "inofensiva"}\\
    \text{criatura.nivel\_magico} \times 0.3  & \text{si el atacante es "arisca"}\\
    \text{criatura.nivel\_magico} \times 0.35 & \text{si el atacante es "peligrosa"}\\
  \end{cases}
$$

La probabilidad de esquivar el ataque esta fado por la función:

$$\left(1 - \text{criatura.prop\_escapar}\right)\times 0.5$$

Si la criatura representando al usuario gana, el usuario se lleva el doble de Sickles apostados, en el caso contrario, el DCC se queda con el dinero.

Al terminar la batalla, las DCCriaturas restaurarán su salud que tenían antes de la batalla.

## _Bonus_ de la entrega

### Bonus avance (2 décimas)

Entregar una versión preliminar del diagrama de clases, en PDF o imagen, para brindar un _feedback_. Les permitirá optar por hasta 2 décimas adicionales.

Debe contener:

- Clases con atributos y métodos
- Contener las relaciones de agregación, composición y herencia

Este debe ser enviado junto al README

### Bonus README?
