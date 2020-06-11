DATA = bytearray()

for i in range(1, 10):
    with open(f'secuencia_{i}', 'rb') as file:
        DATA += bytearray(file.read())

with open('clave.py', 'wb') as archivo:
    archivo.write(bytearray(filter(lambda b: 10 <= b <= 195, DATA)))
