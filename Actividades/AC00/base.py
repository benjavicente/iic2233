class Cuadrado(object):
    def __init__(self, coordenadas):
        # coordenadas es una lista de las coordenadas de los 4 vertices
        self.coordenadas = coordenadas

    def calcular_vertice(self):
        # Asumo que es un cuadrado, en consecuencia,
        # calculo solo la longitud de uno de los lados
        # Esto es escalable a multiples dimenciones
        distancias_cuadradas = list()
        for indice in range(len(self.coordenadas[0])):
            delta = self.coordenadas[0][indice] - self.coordenadas[0][indice]
            distancias_cuadradas.append(delta ** 2)
        return sum(distancias_cuadradas) ** 0.5

    def calcular_area(self):
        return self.calcular_vertice() ** 2

    def calcular_perimetro(self):
        return self.calcular_vertice() * 4

    def __str__(self):
        return str(f"Cuadrado de "
                   f"perímetro {self.calcular_perimetro()} "
                   f"y area {self.calcular_area()}")


class Triangulo(object):
    def __init__(self, coordenadas):
        # Completar método y borrar pass
        pass
    # Agregar métodos


if __name__ == '__main__':
    cuadrado_2d = Cuadrado([[0, 0], [0, 1], [1, 1], [1, 0]])
    print(cuadrado_2d)

    cuadrado_3d = Cuadrado([0, 0, 0], [])
