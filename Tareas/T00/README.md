# Tarea 00: DCCahuín :eyes:

```txt
                                         _____
Bienvenid@ a                            / ... \
  _____   _____ _____      _           / _____/
 |  __ \ / ____/ ____|    | |         /_/
 | |  | | |   | |     __ _| |__  _   _ _ _ __
 | |  | | |   | |    / _` | '_ \| | | | | '_ \
 | |__| | |___| |___| (_| | | | | |_| | | | | |
 |_____/ \_____\_____\__,_|_| |_|\__,_|_|_| |_|
```

- [Tarea 00: DCCahuín :eyes:](#tarea-00-dccahu%c3%adn-eyes)
  - [Ejecución :computer:](#ejecuci%c3%b3n-computer)
  - [Características implementadas :wrench:](#caracter%c3%adsticas-implementadas-wrench)
      - [Menú de usuarios :bust_in_silhouette:](#men%c3%ba-de-usuarios-bustinsilhouette)
      - [Menú de Posts :speech_balloon:](#men%c3%ba-de-posts-speechballoon)
      - [Menú de Seguidos y Seguidores :busts_in_silhouette:](#men%c3%ba-de-seguidos-y-seguidores-bustsinsilhouette)
  - [Librerías :books:](#librer%c3%adas-books)
    - [Librerías externas utilizadas :clipboard:](#librer%c3%adas-externas-utilizadas-clipboard)
    - [Librerías propias :pencil:](#librer%c3%adas-propias-pencil)
  - [Supuestos y consideraciones :thinking:](#supuestos-y-consideraciones-thinking)
  - [Código externo utilizado :package:](#c%c3%b3digo-externo-utilizado-package)
  - [Notas adicionales :octocat:](#notas-adicionales-octocat)

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es  `menu.py`.

El módulo `postmanager.py` debe encontrarse en el mismo directorio que `menu.py`.

Los archivos `posts.csv`, `seguidores.csv` y `usuarios.csv` deben encontrarse en una carpeta llamada `data`. Deben terminar con una linea vacía.

---

## Características implementadas :wrench:

**Todo lo pedido fue implementado**.
A continuación se encuentra todos los puntos considerados de la [pauta](https://docs.google.com/spreadsheets/d/1SgQlv1EL57C-DoC0ldShzXupAgMnnLkaDnUwStjjRd4/edit#gid=0) y [enunciado](https://github.com/IIC2233/syllabus/blob/master/Tareas/T00/Enunciado.pdf), además de otras características adicionales que mejoran la experiencia del usuario.

#### Menú de usuarios :bust_in_silhouette:

- El menú de inicio contiene las opciones:
  - [X] Iniciar sesión
  - [X] Registro de Usuario
  - [X] Salir
- El menu principal contiene las opciones:
  - [X] Menú de PrograPosts
  - [X] Menú de Seguidos y Seguidores
  - [X] Cerrar sesión
- Cuando se inicia sesión:
  - [X] Se verifica que el nombre exista en `usuarios.csv`
- Cuando se registra un nuevo usuario:
  - [X] Se verifica que el nombre elegido no esté ocupado, contiene mínimo 8 caracteres, tiene por lo menos una letra y un número, y es alfanumérico
  - [X] **Adicional**: Se limita el nombre de usuario hasta 32 caracteres
  - [X] Se crea el usuario en `usuarios.csv` y `seguidores.csv`
- Cuando se quiere salir del programa:
  - [X] La opción `0` vuelve al menú anterior hasta llegar a el menú de inicio, donde `0` cierra el programa. Si el usuario esta realizando una acción, dejar el campo vacío volverá al menú anterior.

#### Menú de Posts :speech_balloon:

- El menú de PrograPosts contiene las opciones:
  - [X] Ver tu Muro
  - [X] Ver tus publicaciones
  - [X] Crear un PrograPost
  - [X] Eliminar un PrograPost
  - [X] Volver
- Cuando se ven los PrograPosts:
  - [X] Se muestra el Muro (PrograPosts de usuarios seguidos)
  - [X] Se muestran los PrograPost propios
  - [X] Se entrega la opción de ver post ordenados de más nuevo a más antiguo y viceversa
  - [X] **Adicional**: Los post son mostrados en *contenedores*
- Cuando se crea un PrograPost:
  - [X] Si supera los 140 caracteres, se avisa al usuario que el mensaje es muy largo
  - [X] Se guarda en `posts.csv` con el mensaje elegido, el nombre de usuario y la fecha actual
  - [X] **Adicional**: Al publicar el PrograPost, se muestra
  - [X] Se agrega el post a `post.csv`
- Cuando se elimina un PrograPost:
  - [X] Se permite elegit el PrograPost a eliminar
  - [X] **Adicional**: Si el usuario solo tiene un PrograPost, se selecciona este automáticamente
  - [X] **Adicional**: Luego de elegir cual eliminar, se muestra el PrograPost y se confirma la acción
  - [X] Se elimina el post en `post.csv`
- La fecha del PrograPost se encuentra en el formato pedido:
  - [X] Se muestra la fecha en formato `YYYY/MM/DD` en los PrograPosts

#### Menú de Seguidos y Seguidores :busts_in_silhouette:

- El menú contiene las opciones:
  - [X] Seguir a un usuario
  - [X] Dejar de seguir a un usuario
  - [X] **Adicional**: Ver usuario seguidos
  - [X] **Adicional**: Ver seguidores
  - [X] Volver
- Cuando se sigue a un usuario:
  - [X] Se verifica que el usuario a seguir no es sí mismo y se avisa si es el caso
  - [X] Se verifica que el usuario exista y se avisa si es el caso
  - [X] Si el usuario existe y no es sí mismo, se sigue y modifica `seguidores.csv`
- Cuando se deja de seguir a un usuario
  - [X] Se verifica que el usuario existe, si es el caso, se avisa
  - [X] Se verifica que el usuario es sí mismo, si es el caso, se avisa
  - [X] Se deja de seguir al usuario y se modifica el archivo `seguidores`

---

## Librerías :books:

### Librerías externas utilizadas :clipboard:

La lista de librerías externas y sus funciones que utilicé fueron las siguientes:

1. **`os`**
   - Función `path.join()`
        Une los *paths- relativos de los archivos. Permite compatibilidad con multiples sistemas operativos
2. **`operator`**
   - Función `attrgetter()`
        Crea una llave para sortear los PrograPosts por sus atributos
3. **`datetime`**
     - Método `today()` de la clase `date`
        Obtiene la fecha actual para la creación de PrograPosts

Ninguna de estas debe instalarse.

### Librerías propias :pencil:

Por otro lado, los módulos que fueron creados fueron los siguientes:

1. **`usermanager`**
   - Administra la información los usuarios y los PrograPosts. Puede considerase el *"back-end"* del programa

## Supuestos y consideraciones :thinking:

Los supuestos que realicé durante la tarea son los siguientes:

1. **Asumo que los archivos** `posts.csv` y `usuarios.csv` **terminan con una linea vacía**, es decir, que cada fila esta compuesta por sus campos y el carácter de nueva linea. Si no es correcto esto, el primer dato ingresado en cada archivo no será ingresado correctamente.

2. **Asumo que todos los PrograPosts son distintos**. Se pueden publicar dos o más PrograPost iguales (mismo usuario, fecha y mensaje), pero si se intenta eliminar uno de ellos, se eliminan los iguales.

## Código externo utilizado :package:

*No considero las recomendaciones o la documentación, pero donde se utilizo guiás o tips se comentó en el código.*

- `not usuario.upper().isupper()`, que retorna `True` si hay una letra en el string. Es utilizado para verificar que el usuario contiene una letra es su nombre
  - Obtenido de [stack overflow](https://stackoverflow.com/a/47453486)

## Notas adicionales :octocat:

- Se omitió el uso de variables globales que (*según preferencia personal*) permitían adaptar mejor el programa y mejoraban la legibilidad. Esto se debe a que están consideradas como [malas practicas](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md#malas-pr%C3%A1cticas-5-d%C3%A9cimas-x). Estas eran `ancho_ui`, `usuario_actual` y variables que almacenaban los *paths*. Hasta el commit `333087be05b5909fe4648d3eddde7ee36ecca877` se pueden ver completamente presentes.
