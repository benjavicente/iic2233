# Tarea 00: DCCahuín :eyes:

## Consideraciones

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

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es  `menu.py`.

El módulo `postmanager.py` debe encontrarse en el mismo directorio que `menu.py`.

Si los archivos `posts.csv`, `seguidores.csv` y `usuarios.csv` no son proporcionados en la carpeta `data`, se deben crear estos en dicha carpeta.

---

### Características implementadas

**Todo lo pedido fue implementado**.
A continuación se encuentra todos los puntos considerados de la pauta y enunciado, además de otras características adicionales que mejoran la experiencia del usuario.

#### Menú de usuarios

* El menú de inicio contiene las opciones:
  * [X] Iniciar sesión
  * [X] Registro de Usuario
  * [X] Salir
* El menu principal contiene las opciones:
  * [X] Menú de PrograPosts
  * [X] Menú de Seguidos y Seguidores
  * [X] Cerrar sesión
* Cuando se inicia sesión:
  * [X] Se verifica que el nombre exista en `usuarios.csv`
* Cuando se registra un nuevo usuario:
  * [X] Se verifica que el nombre elegido no esté ocupado, contiene mínimo 8 caracteres, tiene por lo menos una letra y un número, y es alfanumérico
  * [X] **Adicional**: Se limita el nombre de usuario hasta 32 caracteres
  * [X] Se crea el usuario en `usuarios.csv` y `seguidores.csv`
* Cuando se quiere salir del programa:
  * [X] La opción `0` vuelve al menú anterior hasta llegar a el menú de inicio, donde `0` cierra el programa

#### Menú de Posts

* El menú de PrograPosts contiene las opciones:
  * [X] Ver tu Muro
  * [X] Ver tus publicaciones
  * [X] Crear un PrograPost
  * [X] Eliminar un PrograPost
  * [X] Volver
* Cuando se ven los PrograPosts:
  * [X] Se muestra el Muro (PrograPosts de usuarios seguidos)
  * [X] Se muestran los PrograPost propios
  * [X] Se entrega la opción de ver post ordenados de más nuevo a más antiguo y viceversa
  * [X] **Adicional**: Los post son mostrados en *contenedores*
* Cuando se crea un PrograPost:
  * [X] Si supera los 140 caracteres, se avisa al usuario que el mensaje es muy largo
  * [X] Se guarda en `posts.csv` con el mensaje elegido, el nombre de usuario y la fecha actual
  * [X] **Adicional**: Al publicar el PrograPost, se muestra
  * [X] Se agrega el post a `post.csv`
* Cuando se elimina un PrograPost:
  * [X] Se permite elegit el PrograPost a eliminar
  * [X] **Adicional**: Si el usuario solo tiene un PrograPost, se selecciona este automáticamente
  * [X] **Adicional**: Luego de elegir cual eliminar, se muestra el PrograPost y se confirma la acción
  * [X] Se elimina el post en `post.csv`
* La fecha del PrograPost se encuentra en el formato pedido:
  * [X] Se muestra la fecha en formato `YYYY/MM/DD` en los PrograPosts

#### Menú de Seguidos y Seguidores

* El menú contiene las opciones:
  * [X] Seguir a un usuario
  * [X] Dejar de seguir a un usuario
  * [X] **Adicional**: Ver usuario seguidos
  * [X] **Adicional**: Ver seguidores
  * [X] Volver
* Cuando se sigue a un usuario:
  * [X] Se verifica que el usuario a seguir no es sí mismo y se avisa si es el caso
  * [X] Se verifica que el usuario exista y se avisa si es el caso
  * [X] Si el usuario existe y no es sí mismo, se sigue y modifica `seguidores.csv`
* Cuando se deja de seguir a un usuario
  * [X] Se verifica que el usuario existe, si es el caso, se avisa
  * [X] Se verifica que el usuario es sí mismo, si es el caso, se avisa
  * [X] Se deja de seguir al usuario y se modifica el archivo `seguidores`

---

## Librerías :books:

### Librerías externas utilizadas

La lista de librerías externas y sus funciones que utilicé fueron las siguientes:

1. **`os`**
   * Función `path.join()`
        Une los *paths* relativos de los archivos. Permite compativilidad con multiples sistemas operativos
2. **`operator`**
   * Función `attrgetter()`
        Crea una llave para sortear los PrograPosts por sus atributos
3. **`datetime`**
     * Método `today()` de la clase `date`
        Obtiene la fecha actual para la creación de PrograPosts

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

1. **`usermanager`**
   * Administra la información los usuarios y los PrograPosts. Puede considerase el *"back-end"* del programa

### Código externo utilizado

*No considero las recomendaciones o documentación, pero donde se utilizo guiás o tips se comentó en el código.*

* `not usuario.upper().isupper()`, que retorna `True` si hay una letra en el string. Es utilizado para verificar que el usuario contiene una letra es su nombre
  * Obtenido de [stack overflow](https://stackoverflow.com/a/47453486)

## Supuestos y consideraciones adicionales :thinking:

Los supuestos que realicé durante la tarea son los siguientes:

1. **Asumo que los archivos** `posts.csv` y `usuarios.csv` **terminan con una linea vacía**, es decir, que cada fila esta compuesta por sus campos y el carácter de nueva linea. Si no es correcto esto, el primer dato ingresado en cada archivo no será ingresado correctamente.

2. **Asumo que todos los PrograPosts son distintos**. Se pueden publicar dos o más PrograPost iguales (mismo usuario, fecha y mensaje), pero si se intenta eliminar uno de ellos, se eliminan todos estos.
