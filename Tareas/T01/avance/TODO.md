# TODO

Mezcla de "Resumen" del enunciado y notas.

- [X] Falta añadir nuevos métodos y atributos al diagrama de clases (la estructura está bien)
- [X] Ver los parámetros
- [X] Ver como guardar y cargar las los datos de las clases, y como utilizar **valores predeterminados**
- [X] Crear un esquema para los menús
- [ ] Hacer [README](../README.md)
- [X] Crear los procesos en [ZoologicoMagico](../ZoologicoMagico.py)
- [X] Completar DCC
- [ ] Completar DCCriaturas
- [ ] Ver los nombres de los archivos, variables y métodos
- [ ] Testear

**Notas generales**:
Cambie el nombre de _puntos de salud_ a _puntos de vida_ para evitar la confusión con _estado de salud_.

## Menús

### General

- [X] A prueba de errores de usuario
- [X] Opción de volver atrás
- [X] Opción de salir

### Menús de inicio

Menú de entrada al programa

- [X] Crear Magizoólogo
  - [X] Nombres alfanuméricos
  - [X] Nombres únicos (no importa las mayúsculas, Al == al)
  - [X] Al ser no válido:
    - [X] Se indica el error
    - [X] Volver a intentarlo
    - [X] Volver atrás
    - [X] Salir
  - [X] Al ser válido:
    - [X] Elegir entre Docencio, Tarea o Híbrido
    - [X] Desplegar una lista de especies de DCCriaturas
    - [X] Elegir DCCriatura con nombre único alfanumérico
    - [X] Volver a intentarlo
    - [X] Volver atrás
    - [X] Salir
- [X] Cargar Magizoólogo
- [X] Salir

### Menú de acciones

Menu principal, donde se accede iniciar sesión o crear un nuevo Magizoólogo

- [X] Menú cuidar DCCriaturas
- [X] Menú DCC
- [X] Pasar al día siguiente
- [X] Volver atrás
- [X] Salir

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
- [X] Volver atrás
- [X] Salir

### Menú DCC

Las acciones Adoptar y Comprar tienen un costo monetario. Si no se posee fondos, se avisa.

- [X] Adoptar DCCriaturas
  - [X] Opción de adoptar una criatura por Sickles.
- [X] Comprar alimentos
  - [X] Opción de comprar alimentos por Sickles.
- [X] Ver estado de Magizoólogo
  - [X] Imprime los datos del Magizoólogo
- [X] DCCriaturas
  - [X] Imprime los datos de las DCCriaturas
- [X] Volver atrás
- [X] Salir

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

- [X] **Nombre** `str`: nombre elegido y único.
- [X] **Sickles** `int`: inicialmente 500, no puede ser negativo.
- [X] **Criaturas** `list`: inicialmente una criatura elegida.
- [X] **Alimentos** `list`: inicialmente 1 alimento aleatorio.
- [X] **Licencia** `bool`: inicialmente True.
- [X] **Nivel mágico** `int`.
- [X] **Destreza** `int`.
- [X] **Energía total** `int`.
- [X] **Responsabilidad** `int`.
- [X] **Energía actual** `int`: Entre 0 y un valor máximo. Su valor inicial y máximo dependen del tipo de Magizoólogo.
- [X] **Nivel de aprobación** `int`: entre 0 y 100, si es menor que 60 se pierde la licencia.

#### Métodos Magizoólogos

- [X] **Adoptar DCCriaturas al DCC**: Se adopta una criatura si se posee licencia y dinero suficiente.
- [X] **Comprar alimentos al DCC**: Se compra alimentos si posee suficiente dinero.
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

- [X] **Nombre** `str`: identificador de cada criatura.
- [X] **Nivel mágico** `int`.
- [X] **Puntos de salud total** `int`.
- [X] **Puntos de salud actual** `int`: mínimo 1.
- [X] **Probabilidad de escape** `float`: entre 0 y 1.
- [X] **Probabilidad de enfermarse** `float`: entre 0 y 1.
- [X] **Estado de salud** `bool`: si es false, pierde 7 de salud.
- [X] **Nivel de hambre** `str`: es `"satisfecha"` o `"hambrienta"`, si esta hambrienta, pierde 3 de salud.
- [X] **Días sin comer** `int`.
- [X] **Nivel de agresividad** `str`: es `"inofensiva"`, `"arisca"`  o `"peligrosa"`

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

#### Alimento Tarta de Melaza

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

- [X] **Mostrar estado de Magizoólogo y DCCriaturas**: se muestra en la pantalla todos los valores de atributos relevantes del usuario Magizoólogo. Debe mostrar:
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
