def reparar_usuario(ruta):
    image = bytearray()
    # Se lee el contenido en bytes
    with open(ruta, 'rb') as file:
        content = bytearray(file.read())
    # Se separan los bytes
    for i in range(0, len(content), 32):
        inverted = content[i]
        # Se porcesa el segmento
        new_content = content[i+1:i+17]
        if inverted == 1:
            new_content.reverse()
        # Se concatena los segmentos
        image += new_content
    # Se escribe el archivo resultante
    with open(R'user_info.bmp', 'wb') as file:
        file.write(image)


if __name__ == '__main__':
    reparar_usuario('imagen_danada.xyz')
    print("Contraseña reparada, ver 'user_info.bmp'")
