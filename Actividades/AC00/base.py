"""
Actividad 0
Realizada tarde porque no pude acceder al repositorio personal antes :(
Contiene clases de Cuadrado y Triangulo, donde ambas contienen
el atributo "coordenadas" con las coordenadas de cada vertice
Se asume que las coordenadas crear la figura del método
"""


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
            delta = self.coordenadas[0][indice] - self.coordenadas[1][indice]
            distancias_cuadradas.append(delta ** 2)
        return sum(distancias_cuadradas) ** 0.5

    def calcular_area(self):
        return self.calcular_vertice() ** 2

    def calcular_perimetro(self):
        return self.calcular_vertice() * 4

    def __str__(self):
        return str(f"Cuadrado de "
                   f"perímetro {self.calcular_perimetro():.2f} "
                   f"y area {self.calcular_area():.2f}")


class Triangulo(object):
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas

    # Esto se podria simplificar a futuro,
    # ya que en Cuadrado tambien se usan métodos similares

    def calcular_vertices(self):
        lista_vertices = list()
        for n_vertice in range(3):
            distancias_cuadradas = list()
            for indice in range(len(self.coordenadas[0])):
                delta = float(self.coordenadas[(n_vertice + 1) % 3][indice]
                              - self.coordenadas[n_vertice][indice])
                distancias_cuadradas.append(delta ** 2)
            lista_vertices.append(sum(distancias_cuadradas) ** 0.5)
        return lista_vertices

    def es_equilatero(self):
        # si es equilatero tiene todos los lados igales
        vertices = self.calcular_vertices()
        for i_vertice in range(len(vertices)):
            if vertices[i_vertice] != vertices[(i_vertice+1) % 3]:
                return False
        return True

    def calcular_area(self):
        if self.es_equilatero():
            return self.calcular_vertices()[0] ** 2 * (3 ** 2)/4
        else:
            # Uso el metodo de crear tres triangulos rectangulos alrededor del
            # triangulo inicial para crear un rectangulo, y luego calcular la
            # diferencia entre el area del rectangulo y
            # de los triangulos rectangulos

            lista_distancias = list()
            area_triangulos = 0
            # i_comp = indice comparación
            for i_comp in range(3):
                sub_distancias = list()
                for dim in range(len(self.coordenadas[0])):
                    sub_distancias.append(
                        abs(self.coordenadas[i_comp][dim] -
                            self.coordenadas[(i_comp + 1) % 3][dim]))
                # veo el area de el triangulo de la comparación
                area_triangulo_actual = 1 / len(sub_distancias)
                for valor in sub_distancias:
                    area_triangulo_actual *= valor
                area_triangulos += area_triangulo_actual
                # agrego las distancias para el calculo del rectangulo
                lista_distancias.append(sub_distancias)

            # veo distancias del rectangulo
            # NOTA: debería añadir un atributo de dimenciones para simplificar
            #       parte del código (ej: len(self.coordenadas[0]) )
            lista_maximos = [0] * len(self.coordenadas[0])
            for distancias in lista_distancias:
                for coord_dist in range(len(lista_maximos)):
                    if lista_maximos[coord_dist] < distancias[coord_dist]:
                        lista_maximos[coord_dist] = distancias[coord_dist]
            area_rectangulo = 1  # variable temporal
            for valor in lista_maximos:
                area_rectangulo *= valor
            return area_rectangulo - area_triangulos

    def calcular_perimetro(self):
        return sum(self.calcular_vertices())

    def __str__(self):
        return str(f"Triángulo {'equilatero ' if self.es_equilatero() else ''}"
                   f"de perímetro {self.calcular_perimetro():.2f} "
                   f"y area {self.calcular_area():.2f}")


if __name__ == '__main__':
    cuadrado_2d = Cuadrado([[0, 0], [0, 1], [1, 1], [1, 0]])
    print(cuadrado_2d)

    cuadrado_3d = Cuadrado([[1, 0, 0], [0, 1, 0],
                            [1, 0, 2 ** 0.5], [0, 1, 2 ** 0.5]])
    print(cuadrado_3d)

    triangulo_2d = Triangulo([[0, 0], [1, 0], [0, 1]])
    print(triangulo_2d)

    triangulo_3d = Triangulo([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    print(triangulo_3d)
