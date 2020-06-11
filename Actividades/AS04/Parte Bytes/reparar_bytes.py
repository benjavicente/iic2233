def reparar_imagen(ruta):
    with open(ruta, 'rb') as file:
        content = bytearray(file.read())
    image = bytearray()
    for i in range(0, len(content), 32):
        inverted = content[i]
        new_content = content[i+1:i+17]
        if inverted == 1:
            new_content.reverse()
        image += new_content
    with open(R'Parte bytes\user_info.bmp', 'wb') as file:
        file.write(image)




if __name__ == '__main__':
    try:
        # Problema de VSCode, elimar el path relativo
        reparar_imagen(R'Parte bytes\imagen_danada.xyz')
        print("Contraseña reparada")
    except Exception as error:
        print(f'Error: {error}')
        print("No has podido obtener la información del Ayudante!")  