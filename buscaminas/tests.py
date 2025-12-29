import os
import unittest
from buscaminas import (existe_archivo, crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)


'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero: 
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True



class colocar_minasTest(unittest.TestCase):
    def test_una_mina(self):
        filas = 3
        columnas = 3
        minas = 1
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        self.assertTrue(dimension_correcta(tablero, filas, columnas))
        

    def test_muchas_minas(self):
        filas = 3
        columnas = 3
        minas = 8 
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        self.assertTrue(dimension_correcta(tablero, filas, columnas))



class calcular_numerosTest(unittest.TestCase):
    def test_todos_uno(self):

        tablero = [[0,-1,0],
                   [0, 0,0]]
        filas = len(tablero)
        columnas = len(tablero[0])

        calcular_numeros(tablero)

        self.assertTrue(dimension_correcta(tablero, filas, columnas))
        self.assertEqual(tablero, [[1,-1,1],
                                   [1, 1,1]])
        

    def test_hay_ceros(self):   
        tablero = [[-1,0,0],
                   [0, 0,0]]
        filas = len(tablero)
        columnas = len(tablero[0])

        calcular_numeros(tablero)

        self.assertTrue(dimension_correcta(tablero, filas, columnas))
        self.assertEqual(tablero, [[-1,1,0],
                                   [1, 1,0]]) 


    def test_varias_minas(self):   
        tablero = [[-1, 0, 0],
                   [ 0,-1,-1],
                   [-1, 0, 0]]
        filas = len(tablero)
        columnas = len(tablero[0])

        calcular_numeros(tablero)

        self.assertTrue(dimension_correcta(tablero, filas, columnas))
        self.assertEqual(tablero, [[-1, 3, 2],
                                   [ 3,-1,-1],
                                   [-1, 3, 2]]) 

        

class crear_juegoTest(unittest.TestCase):
    def test_chico(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    

    def test_mediano(self):
        filas = 4
        columnas = 4
        minas = 3
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        self.assertTrue(dimension_correcta(estado["tablero"], filas, columnas))
        self.assertTrue(dimension_correcta(estado["tablero_visible"], filas, columnas))
        for fila in estado["tablero_visible"]:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        self.assertEqual(estado["filas"], filas)
        self.assertEqual(estado["columnas"], columnas)
        self.assertEqual(estado["minas"], minas)
        self.assertFalse(estado["juego_terminado"])
        self.assertEqual(cant_minas_en_tablero(estado["tablero"]), minas)


    def test_grande(self):
        filas = 10
        columnas = 10
        minas = 20
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        self.assertTrue(dimension_correcta(estado["tablero"], filas, columnas))
        self.assertTrue(dimension_correcta(estado["tablero_visible"], filas, columnas))
        for fila in estado["tablero_visible"]:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        self.assertEqual(estado["filas"], filas)
        self.assertEqual(estado["columnas"], columnas)
        self.assertEqual(estado["minas"], minas)
        self.assertFalse(estado["juego_terminado"])
        self.assertEqual(cant_minas_en_tablero(estado["tablero"]), minas)



class obtener_estado_tableroTest(unittest.TestCase):
    def test_una_mina(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 1,
            'tablero' : [[-1, 1],
                        [ 1, 1]],

            'tablero_visible' : [[VACIO, "1"],
                                [VACIO, VACIO]],

            'juego_terminado' : False}

        self.assertEqual(obtener_estado_tablero_visible(estado), [[VACIO, "1"],
                                                                  [VACIO, VACIO]])

        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1, 1]])
        
        self.assertEqual(estado['tablero_visible'], [[VACIO, "1"],
                                                     [VACIO, VACIO]])
        
        self.assertFalse(estado['juego_terminado'])


    def test_todo_vacio(self):
        estado: EstadoJuego = {
            "filas" : 2,
            "columnas" : 2,
            "minas" : 1,
            "tablero" : [[-1, 1],
                         [ 1, 1]],
            'tablero_visible': [[VACIO, VACIO],
                                [VACIO, VACIO]],
            'juego_terminado': False
        }

        copia = obtener_estado_tablero_visible(estado)
        
        self.assertEqual(copia, estado['tablero_visible'])

        self.assertEqual(estado["filas"], 2)
        self.assertEqual(estado["columnas"], 2)
        self.assertEqual(estado["minas"], 1)
        self.assertEqual(estado["tablero"], [[-1, 1],
                                             [ 1, 1]])
        self.assertEqual(estado["tablero_visible"], [[VACIO, VACIO],
                                                     [VACIO, VACIO]])
        self.assertFalse(estado["juego_terminado"])


    def test_con_bandera(self):
        estado: EstadoJuego = {
            "filas" : 2,
            "columnas" : 2,
            "minas" : 1,
            "tablero" :  [[-1, 1],
                          [ 1, 1] ],
            'tablero_visible': [[BANDERA, "1"],
                                [VACIO, VACIO]],
            'juego_terminado': False
        }

        copia = obtener_estado_tablero_visible(estado)
        
        self.assertEqual(copia, estado['tablero_visible'])

        self.assertEqual(estado["filas"], 2)
        self.assertEqual(estado["columnas"], 2)
        self.assertEqual(estado["minas"], 1)
        self.assertEqual(estado["tablero"], [[-1, 1],
                                             [1, 1]])
        self.assertEqual(estado["tablero_visible"], [[BANDERA, "1"],
                                                     [VACIO, VACIO]])
        self.assertFalse(estado["juego_terminado"])


    def test_terminado(self):
        estado: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 4,
            "tablero" :  [[-1, 3,-1],
                          [ 3,-1, 2],
                          [-1, 2, 1]],
            'tablero_visible': [[BANDERA, "3", BANDERA],
                                ["3", BANDERA, "2"],
                                [VACIO,"2", "1"]],
            'juego_terminado': True
        }

        copia = obtener_estado_tablero_visible(estado)
        
        self.assertEqual(copia, estado['tablero_visible'])

        self.assertEqual(estado["filas"], 3)
        self.assertEqual(estado["columnas"], 3)
        self.assertEqual(estado["minas"], 4)
        self.assertEqual(estado["tablero"], [[-1, 3,-1],
                                             [ 3,-1, 2],
                                             [-1, 2, 1]])
        self.assertEqual(estado["tablero_visible"], [[BANDERA, "3", BANDERA],
                                                     ["3", BANDERA, "2"],
                                                     [VACIO,"2", "1"]])
        self.assertTrue(estado["juego_terminado"])



class marcar_celdaTest(unittest.TestCase):
    def test_colocar_bandera(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 1,
            'tablero' : [[-1, 1],
                         [ 1, 1]],
            'tablero_visible' : [[VACIO, VACIO],
                                [VACIO, VACIO]],

            'juego_terminado' : False
        }

        marcar_celda(estado, 0, 0) 

        self.assertEqual(estado['tablero_visible'], [[BANDERA, VACIO],
                                                     [VACIO, VACIO]])
        
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1, 1]])
        
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)


    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 1,
            'tablero' : [[-1, 1],
                         [ 1, 1]],
            'tablero_visible' : [[VACIO, VACIO],
                                 [VACIO, VACIO]],

            'juego_terminado': True
        }
         
        marcar_celda(estado, 0, 0)

        self.assertTrue(estado['juego_terminado'])


    def test_colocar_vacio(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 2,
            'tablero' : [[-1,-1],
                        [ 1, 1]],
            'tablero_visible' : [[VACIO, BANDERA],
                                [VACIO, VACIO]],
            'juego_terminado' : False
        }

        marcar_celda(estado, 0, 1) 

        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],
                                                     [VACIO, VACIO]])
        
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1,-1],
                                             [ 1, 1]])
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        


class descubrir_celdaTest(unittest.TestCase):
    def test_caminos(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 3,
            'tablero' : [[2, -1, 1],
                         [-1, 3, 1],
                         [-1, 2, 0]],

            'tablero_visible' : [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado' : False}

        descubrir_celda(estado, 2, 2)

        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO, VACIO],
                                                     [VACIO, "3", "1"],
                                                     [VACIO, "2", "0"]])

        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[2, -1, 1],
                                             [-1, 3, 1],
                                             [-1, 2, 0]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])


    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 3,
            'tablero' : [[2, -1, 1],
                         [-1, 3, 1],
                         [-1, 2, 0]],

            'tablero_visible' : [[VACIO, VACIO, VACIO],
                                [VACIO, VACIO, VACIO],
                                [VACIO, VACIO, VACIO]],

            'juego_terminado' : True}
        
        descubrir_celda(estado, 2, 2)
        
        self.assertTrue(estado['juego_terminado'])


    def test_hay_mina(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 3,
            'tablero' : [[2, -1, 1],
                         [-1, 3, 1],
                         [-1, 2, 0]],

            'tablero_visible' : [[VACIO, VACIO, VACIO],
                                [VACIO, "3", "1"],
                                [VACIO, "2", "0"]],

            'juego_terminado' : False}
        
        descubrir_celda(estado, 0, 1)

        self.assertEqual(estado['tablero_visible'], [[VACIO, BOMBA, VACIO],
                                                     [BOMBA, "3", "1"],
                                                     [BOMBA, "2", "0"]])

        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[2, -1, 1],
                                             [-1, 3, 1],
                                             [-1, 2, 0]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertTrue(estado['juego_terminado'])


    def test_ganado(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 3,
            'tablero' : [[2, -1, 1],
                         [-1, 3, 1],
                         [-1, 2, 0]],

            'tablero_visible' : [[VACIO, VACIO, "1"],
                                 [VACIO, "3", "1"],
                                 [VACIO, "2", "0"]],

            'juego_terminado' : False}
        
        descubrir_celda(estado, 0, 0)

        self.assertEqual(estado['tablero_visible'], [["2", VACIO, "1"],
                                                     [VACIO, "3", "1"],
                                                     [VACIO, "2", "0"]])

        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[2, -1, 1],
                                             [-1, 3, 1],
                                             [-1, 2, 0]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertTrue(estado['juego_terminado'])


    def test_repite_camino(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 1,
            'tablero' : [[0, 0, 0],
                         [0, 1, 1],
                         [0, 1, -1]],

            'tablero_visible' : [[VACIO, VACIO, VACIO],
                                 [VACIO, VACIO, VACIO],
                                 [VACIO, VACIO, VACIO]],

            'juego_terminado' : False}

        descubrir_celda(estado, 0, 0)

        self.assertEqual(estado['tablero_visible'], [["0", "0", "0"],
                                                     ["0", "1", "1"],
                                                     ["0", "1", VACIO]])

        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[0, 0, 0],
                                             [0, 1, 1],
                                             [0, 1,-1]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertTrue(estado['juego_terminado'])


    def test_con_bandera(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 1,
            'tablero' : [[0, 0, 0],
                         [0, 1, 1],
                         [0, 1, -1]],

            'tablero_visible' : [[VACIO, BANDERA, VACIO],
                                 [VACIO, VACIO, VACIO],
                                 [VACIO, VACIO, VACIO]],

            'juego_terminado' : False}

        descubrir_celda(estado, 0, 0)

        self.assertEqual(estado['tablero_visible'], [["0", BANDERA, VACIO],
                                                     ["0", "1", VACIO],
                                                     ["0", "1", VACIO]])

        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[0, 0, 0],
                                             [0, 1, 1],
                                             [0, 1,-1]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertFalse(estado['juego_terminado'])


    def test_sobre_bandera(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 1,
            'tablero' : [[0, 0, 0],
                         [0, 1, 1],
                         [0, 1, -1]],

            'tablero_visible' : [[VACIO, VACIO, VACIO],
                                 [VACIO, BANDERA, VACIO],
                                 [VACIO, VACIO, VACIO]],

            'juego_terminado' : False}

        descubrir_celda(estado, 1, 1)

        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO, VACIO],
                                                     [VACIO, BANDERA, VACIO],
                                                     [VACIO, VACIO, VACIO]])

        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[0, 0, 0],
                                             [0, 1, 1],
                                             [0, 1,-1]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertFalse(estado['juego_terminado'])



class verificar_victoriaTest(unittest.TestCase):
    def test_ganado(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 1,
            'tablero' : [[-1, 1],
                         [ 1, 1]],

            'tablero_visible' : [[VACIO, "1"],
                                 ["1", "1"]],

            'juego_terminado' : True}
        
        self.assertTrue(verificar_victoria(estado))

        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1, 1]])

        self.assertEqual(estado['tablero_visible'], [[VACIO, "1"],
                                                     ["1", "1"]])
        
        self.assertTrue(estado['juego_terminado'])


    def test_perdido(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 1,
            'tablero' : [[-1, 1],
                         [ 1, 1]],

            'tablero_visible' : [[BOMBA, VACIO],
                                 ["1", "1"]],

            'juego_terminado' : True}

        self.assertFalse(verificar_victoria(estado))

        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1, 1]])
        
        self.assertEqual(estado['tablero_visible'], [[BOMBA, VACIO],
                                                     ["1", "1"]])
        
        self.assertTrue(estado['juego_terminado'])
        


class reiniciar_juegoTest(unittest.TestCase):
    def test_reiniciado(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 2,
            'minas' : 1,
            'tablero' : [[-1, 1],
                         [ 1, 1]],

            'tablero_visible': [[VACIO, "1"],
                                [VACIO, VACIO]],

            'juego_terminado': False}
        
        reiniciar_juego(estado)

        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],
                                                     [VACIO, VACIO]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])

        self.assertNotEqual(estado['tablero'], [[-1, 1],
                                                [ 1, 1]])


    def test_reinicio_repetido(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 1,
            'minas' : 1,
            'tablero' : [[-1],
                         [ 1]],

            'tablero_visible': [[VACIO],
                                [VACIO]],

            'juego_terminado': False}
        
        reiniciar_juego(estado)

        self.assertEqual(estado['tablero_visible'], [[VACIO],
                                                     [VACIO]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 1)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 1)
        self.assertFalse(estado['juego_terminado'])

        self.assertNotEqual(estado['tablero'], [[-1],
                                                [ 1]])


    def test_segundo_reinicio_repetido(self):
        estado: EstadoJuego = {
            'filas' : 2,
            'columnas' : 1,
            'minas' : 1,
            'tablero' : [[ 1],
                         [-1]],

            'tablero_visible': [[VACIO],
                                [VACIO]],

            'juego_terminado': False}
        
        reiniciar_juego(estado)

        self.assertEqual(estado['tablero_visible'], [[VACIO],
                                                     [VACIO]])

        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 1)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 1)
        self.assertFalse(estado['juego_terminado'])

        self.assertNotEqual(estado['tablero'], [[ 1],
                                                [-1]])
        


class guardar_estadoTest(unittest.TestCase):
    def test_guardado_correcto (self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 2,
            'tablero' : [[-1, 2, 1],
                         [ 1, 2,-1],
                         [ 0, 1, 1]],

            'tablero_visible' : [[VACIO, VACIO, "1"],
                                 [VACIO, VACIO,BANDERA],
                                 [VACIO, "1", "1"]],

            'juego_terminado' : False}
        
        ruta_directorio = 'GUARDAR'

        guardar_estado(estado, ruta_directorio)
        self.assertTrue(existe_archivo(ruta_directorio, 'tablero.txt'))
        self.assertTrue(existe_archivo(ruta_directorio, 'tablero_visible.txt'))


    def test_lineas_correctas(self):
        estado: EstadoJuego = {
            'filas' : 3,
            'columnas' : 3,
            'minas' : 4,
            'tablero' : [[-1, 3, 1],
                         [-1, 4,-1],
                         [ 2,-1, 2]],

            'tablero_visible' : [[VACIO, VACIO, VACIO],
                                 [VACIO, "4",BANDERA],
                                 [VACIO, BANDERA, "2"]],

            'juego_terminado' : False}
        
        ruta_directorio = 'GUARDAR'

        guardar_estado(estado, ruta_directorio)

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')


        f_tablero = open(ruta_tablero, 'r', encoding='utf-8')

        lineas_tablero : list[str] = f_tablero.readlines()
        self.assertEqual(len(lineas_tablero), estado['filas'])

        for linea in lineas_tablero:
            comas_tablero = 0
            for c in linea:
                if c == ',':
                    comas_tablero += 1
            self.assertEqual(comas_tablero, estado['columnas'] - 1)

        f_tablero.close()


        f_tablero_visible = open(ruta_tablero_visible, 'r', encoding='utf-8')

        lineas_tablero_visible : list[str] = f_tablero_visible.readlines()
        self.assertEqual(len(lineas_tablero_visible), estado['filas'])

        for linea in lineas_tablero_visible:
            comas_tablero_visible = 0
            for c in linea:
                if c == ',':
                    comas_tablero_visible += 1
            self.assertEqual(comas_tablero_visible, estado['columnas'] - 1)

        f_tablero_visible.close()



class cargar_estadoTest(unittest.TestCase):
    def test_cargar_valido(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,2,1\n")
        archivo_tablero.write("1,2,-1\n")
        archivo_tablero.write("0,1,1\n")
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?, ?,1\n")
        archivo_tablero_visible.write("?, ?,*\n")
        archivo_tablero_visible.write("?,1,1\n")
        archivo_tablero_visible.close()


        self.assertTrue(cargar_estado(estado, ruta_directorio))
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, 2, 1],
                                            [ 1, 2,-1],
                                            [ 0, 1, 1]])
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO, "1"],
                                                    [VACIO, VACIO, BANDERA],
                                                    [VACIO, "1", "1"]])
        self.assertFalse(estado['juego_terminado'])


    def test_archivo_invalido(self):
        estado = {}

        ruta_directorio = 'RUTA_VACIA' 

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_tableros_vacios(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("")
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_lineas_disparejas(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1\n")
        archivo_tablero.write("1,1\n")  
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("?,?,?\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_mas_comas_en_tablero(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1,,\n")
        archivo_tablero.write("1,1\n")  
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_mas_comas_en_tablero_visible(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1\n")
        archivo_tablero.write("1,1\n")  
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("?,,?\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_valor_de_tablero_incorrecto(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1\n")
        archivo_tablero.write("1,1\n")  
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("?,10\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_tableros_distintos(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1\n")
        archivo_tablero.write("1,1\n")  
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("2,1\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_cantidad_de_minas_incorrectas(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,2\n")
        archivo_tablero.write("1,1\n")  
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,?\n")
        archivo_tablero_visible.write("1,1\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_sin_minas(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("0,0\n")
        archivo_tablero.write("0,0\n")
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("0,0\n") 
        archivo_tablero_visible.write("0,0\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_mas_minas(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1\n")
        archivo_tablero.write(" 1,1\n")
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,2\n") 
        archivo_tablero_visible.write("?,2\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))


    def test_sin_vacios(self):
        estado = {}

        ruta_directorio = 'CARGAR'

        ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

        archivo_tablero = open(ruta_tablero, "w", encoding="utf-8")
        archivo_tablero.write("-1,1\n")
        archivo_tablero.write("1,1\n")
        archivo_tablero.close()

        archivo_tablero_visible = open(ruta_tablero_visible, "w", encoding="utf-8")
        archivo_tablero_visible.write("?,1\n") 
        archivo_tablero_visible.write("1,1\n")
        archivo_tablero_visible.close()

        self.assertFalse(cargar_estado(estado, ruta_directorio))



"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""



if __name__ == '__main__':
    unittest.main(verbosity=2)