import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo: str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


# EJERCICIO 1
def colocar_minas(filas: int, columnas: int, minas: int) -> list[list[int]]:
    """
    Crea un tablero de posiciones vacias (0) basandose en la cantidad de filas y columnas para determinar su dimension.
    Coloca la cantidad de minas (-1) solicitadas, en posiciones al azar del tablero.

    Args:
        filas (int): Cantidad de filas que debe tener el tablero.
        columnas (int): Cantidad de columnas que debe tener el tablero.
        minas (int):  Cantidad de minas que debe tener el tablero.
            
    Returns:
        list[list[int]]:
                        tablero: Tablero armado con la cantidad de filas, columnas y minas que entraron como parametro.
    """
    tablero : list[list[int]] = []

    for i in range (filas):
        fila : list[int] = []
        for j in range (columnas):
            fila.append(0)
        tablero.append(fila)

    minas_colocadas : int = 0
    while minas_colocadas < minas:
        pos_fila : int = random.randint(0, filas - 1)
        pos_columna : int = random.randint(0, columnas - 1)

        if tablero[pos_fila][pos_columna] != -1:
            tablero[pos_fila][pos_columna] = -1
            minas_colocadas += 1

    return tablero


def es_matriz(matriz: list[list[int]]) -> bool:
    """
    Analiza si la matriz pasada por parametro tiene la dimension correcta, cantidad de filas y columnas mayor a cero y cada fila con la misma longitud de cada columna.

    Args:
        matriz (list[list[int]]): Matriz a analizar.

    Returns:
        bool:
            res = True: Si la matriz pasada por parametro tiene la dimension correcta para ser una matriz. \n
            res = False: Si la cantidad de filas o de columnas es igual a 0. \n
            res = False: Si el tamaño de las filas de la matriz es distinto al tamaño de las columnas.
    """
    res : bool = True

    if len(matriz) == 0 or len(matriz[0]) == 0:
        res = False

    for i in range (len(matriz)):
        if len(matriz[i]) != len(matriz[0]):
            res = False

    return res


# EJERCICIO 2
def calcular_numeros(tablero: list[list[int]]) -> None:
    """
    Modifica el tablero agregando la cantidad de minas adyacentes que tiene cada posicion del tablero donde no haya una mina.

    Args:
        tablero (list[list[int]]): Tablero que se va a modificar.

    Returns:
            None:
    """
    for i in range (len(tablero)):
        for j in range (len(tablero[0])):
            if tablero[i][j] != -1:
                tablero[i][j] = contar_minas_adyacentes(tablero, i, j)


def contar_minas_adyacentes(tablero: list[list[int]], fila: int, col: int) -> int:
    """
    Recorre cada posicion del tablero recibida como parametro y analiza sus posiciones adyacentes.
    Determina cuantas minas hay en sus posiciones adyacentes y las cuenta para cada posicion del tablero donde no haya una mina.

    Args:
        tablero (list[list[int]]): Tablero a recorrer posición a posición.
        fila (int): Posicion de la fila donde se contarán las minas.
        col (int):  Posicion de la columna donde se contarán las minas.
            
    Returns:
        int:
            contado_minas: Cantidad de minas que hay alrededor de una posicion, entre 0 y 8.
    """
    contador_minas : int = 0

    for indice_fila in [-1, 0, 1]:
        for indice_columna in [-1, 0, 1]:
            if indice_fila != 0 or indice_columna != 0:
                pos_fila : int = fila + indice_fila
                pos_columna : int = col + indice_columna

                if 0 <= pos_fila < len(tablero) and 0 <= pos_columna < len(tablero[0]) and tablero[pos_fila][pos_columna] == -1:
                    contador_minas += 1

    return contador_minas


#EJERCICIO 3
def crear_juego(filas: int, columnas: int, minas: int) -> EstadoJuego:
    """
    Crea un juego/estado con las filas, columnas y minas pasadas por parametro.
    Usando la funcion colocar_minas se crea el tablero y con calcular_numeros se agrega la cantidad de minas por celda.
    Se crea un tablero_visible con el valor VACIO en todas sus posiciones.
    Se crea el estado de juego_terminado como falso.

    Args:
        filas (int): Cantidad de filas que debe tener el tablero.
        columnas (int): Cantidad de columnas que debe tener el tablero.
        minas (int):  Cantidad de minas que debe tener el tablero.
            
    Returns:
        EstadoJuego:
                    estado: {estado['filas'] = filas \n
                             estado['columnas'] = columnas \n
                             estado['minas'] = minas \n
                             estado['tablero'] = crea un tablero con colocar_minas y se modifica con calcular_numeros. \n
                             estado['tablero_visible'] = tablero con el valor VACIO en todas sus posiciones. \n
                             estado['juego_terminado'] = False}
    """
    estado : EstadoJuego = {}
    estado['filas'] = filas 
    estado['columnas'] = columnas
    estado['minas'] = minas 
    estado['tablero'] = colocar_minas(filas, columnas, minas)

    calcular_numeros(estado['tablero'])
    
    tablero_visible : list[list[str]] = []
    for i in range (filas):
        fila : list[str]= []
        for j in range (columnas):
            fila.append(VACIO)
        tablero_visible.append(fila)

    estado['tablero_visible'] = tablero_visible
    estado['juego_terminado'] = False

    return estado 


def son_matriz_y_misma_dimension(t1: list[list[Any]], t2: list[list[Any]]) -> bool:
    """
    Analiza si las dos matrices pasadas por parametro son matrices individualmente usando la funcion es_matriz 
    y luego compara si en ambas coinciden en cantidad de filas y columnas.

    Args:
        t1 (list[list[Any]]): Primera matriz a comparar.
        t2 (list[list[Any]]): Segunda matriz a comparar.
            
    Returns:
        bool:
            res = True: Si ambas matrices son validas y si tienen la misma cantidad de filas y columnas. \n
            res = False: Si t1 no es matriz. \n
            res = False: Si t2 no es matriz. \n
            res = False: Si la cantidad de filas son distintas entre las dos matrices. \n
            res = False: Si la cantidad de columnas son distintas entre las dos matrices.
    """
    res: bool = True

    if not es_matriz(t1) or not es_matriz(t2) or len(t1) != len(t2) or len(t1[0]) != len(t2[0]):
        res = False

    return res


def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:   
    """
    Analiza posicion a posicion el tablero y compara el valor de dicha posicion con el tablero visible para ver si los valores coinciden,
    si no hay una mina en tablero, en ambos tableros debe haber un numero entre 0 y 8. En caso de que haya una mina, esa posicion debe ser VACIO o BANDERA.

    Args:
        tablero (list[list[int]]): Tablero a reorrer para corroborar cada celda.
        tablero_visible (list[list[str]]): Tablero visible a recorrer para corroborar que cada celda coincida.
            
    Returns:
        bool:
            res = True: Todas las posiciones del tablero donde no haya una mina están descubiertas. \n
            res = False: Si en una posicion del tablero donde no haya una mina, no coincida el contenido de la celda entre los dos tableros. \n
            res = False: Si en una posicion del tablero donde hay una mina, en tablero_visible no hay ni VACIO ni BANDERA.
    """  
    res : bool = True

    for i in range (len(tablero)):
        for j in range (len(tablero[0])):
            if tablero[i][j] != -1:
                if tablero_visible[i][j] != str(tablero[i][j]):
                    res = False
            else:
                if tablero_visible[i][j] != VACIO and tablero_visible[i][j] != BANDERA:
                    res = False

    return res


# EJERCICIO 4
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """
    Crea una copia del tablero visible.

    Args:
        estado (EstadoJuego): Estado del que se saca el tablero visible para copiarlo.
            
    Returns:
        list[list[str]]:
                        copia_tablero_visible: Copia del tablero visible.
    """
    tablero_visible : list[list[str]] = estado['tablero_visible']
    copia_tablero_visible : list[list[str]] = []

    for i in range (len(tablero_visible)):
        copia_lista : list[str] = tablero_visible[i].copy()
        copia_tablero_visible.append(copia_lista)

    return copia_tablero_visible


# EJERCICIO 5
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Si el juego ya termino o se pisó una mina no se hace ningun cambio.
    Modifica el tablero visible de un estado con una posicion en la fila y otra en la columna, si en la posicion hay VACIO, se cambia a BANDERA y viceversa.

    Args:
        estado (EstadoJuego): Estado del que se consigue el tablero visible para modificar con una BANDERA o VACIO.
        fila (int): Posicion en fila de la celda a marcar.
        columna (int): Posicion en columna de la celda a marcar.
            
    Returns:
        None:
    """
    res : bool = True
    tablero_visible : list[list[str]] = estado['tablero_visible']
    juego_terminado : bool = estado['juego_terminado']

    if juego_terminado == True or (tablero_visible[fila][columna] != VACIO and tablero_visible[fila][columna] != BANDERA):
        res = False
    
    if res == True:
        if tablero_visible[fila][columna] == VACIO:
            tablero_visible[fila][columna] = BANDERA

        else:
            tablero_visible[fila][columna] = VACIO


# EJERCICIO 6
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Si el juego terminó, se descubren todas las bombas en sus posiciones correspondientes.
    Si el juego no terminó, se descubren las celdas desde la posicion de las coordenadas pasadas por parametros hasta que haya al menos una mina adyacente a la posicion,
    recorriendo todos los caminos posibles conseguidos en caminos_descubiertos y por cada celda descubierta se muestra su valor en tablero.

    Args:
        estado (EstadoJuego): Estado al cual se le deben encontrar los caminos y descubrir las celdas.
        fila (int): Posicion en fila de la celda a descubrir.
        columna (int): Posicion en columna de la celda a descubrir.
            
    Returns:
        None:
    """
    res : bool = True
    tablero : list[list[int]] = estado['tablero']
    tablero_visible : list[list[str]] = estado['tablero_visible']

    if estado['juego_terminado'] == True:
        res = False

    if tablero[fila][columna] == -1:
        estado['juego_terminado'] = True
        for i in range (len(tablero)):
            for j in range (len(tablero[0])):
                if tablero[i][j] == -1:
                    tablero_visible[i][j] = BOMBA
        res = False

    if res == True:
        caminos : list[list[tuple[int, int]]] = caminos_descubiertos(tablero, tablero_visible, fila, columna)
        for camino in caminos:
            for posicion in camino:
                fila_actual : int = posicion[0]
                columna_actual : int = posicion[1]
                if tablero_visible[fila_actual][columna_actual] != BANDERA:
                    tablero_visible[fila_actual][columna_actual] = str(tablero[fila_actual][columna_actual])
        
    if todas_celdas_seguras_descubiertas(tablero, tablero_visible):
        estado['juego_terminado'] = True


def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[tuple[int, int]]]:
    """
    Devuelve todos los posibles caminos descubiertos desde la posicion (f, c) como primer posicion del camino.
    Analiza las celdas que ya fueron procesadas con visitados y agrega los distintos caminos en la lista caminos que tiene dentro la lista de posiciones camino
    Mientras haya caminos por procesar, se crea un camino desde la celda (f,c) tomando la lista camino_actual y analizando su ultima celda, 
    si fue visitada sigue de largo y sino la marca como visitada y guarda ese camino en caminos.
    Si la celda tiene minas alrededor no se expande más, sino busca las celdas vecinas con valor VACIO y expande el camino con esas nuevas posiciones

    Args:
        tablero (list[list[int]]): Tablero donde se harán los caminos.
        tablero_visible (list[list[str]]): Tablero visible donde se buscará que la celda a descubrir en el camino sea VACIO.
        f (int): Posicion en fila de la celda desde donde se buscan los caminos.
        c (int): Posicion en columna  de la celda desde donde se buscan los caminos.
            
    Returns:
        list[list[tuple[int, int]]]:
            caminos: Lista con distintos caminos representados con listas de tuplas con cada tupla siendo una posicion en tablero.
    """
    caminos : list[list[tuple[int, int]]]= []

    visitados : list[list[bool]] = []
    for i in range (len(tablero)):
        fila : list[bool] = []
        for j in range (len(tablero[0])):
            fila.append(False)
        visitados.append(fila)


    camino : list[list[tuple[int, int]]] = []
    camino_inicial : list[tuple[int, int]] = [(f, c)]
    camino.append(camino_inicial)

    while len(camino) > 0:
        camino_actual : list[tuple[int, int]] = camino.pop()
        ultima_posicion : tuple[int, int] = camino_actual[-1]
        ultima_fila : int = ultima_posicion[0]
        ultima_columna : int = ultima_posicion[1]

        if visitados[ultima_fila][ultima_columna] == True:
            continue

        visitados[ultima_fila][ultima_columna] = True

        caminos.append(camino_actual)

        minas_alrededor = contar_minas_adyacentes(tablero, ultima_fila, ultima_columna)
        if minas_alrededor > 0:
            continue

        for indice_fila in [-1, 0, 1]:
            for indice_columna in [-1, 0, 1]:
                if indice_fila != 0 or indice_columna != 0:
                    nueva_fila : int = ultima_fila + indice_fila
                    nueva_columna : int = ultima_columna + indice_columna
                    
                    if 0 <= nueva_fila < len(tablero) and 0 <= nueva_columna < len(tablero[0]):
                        if not visitados[nueva_fila][nueva_columna] and tablero_visible[nueva_fila][nueva_columna] == VACIO:
                            nuevo_camino : list[tuple[int, int]] = []
                            for pos in camino_actual:
                                nuevo_camino.append(pos)
                            nuevo_camino.append((nueva_fila, nueva_columna))
                            camino.append(nuevo_camino)

    return caminos


# EJERCICIO 7
def verificar_victoria(estado: EstadoJuego) -> bool:
    """
    Verifica si el juego terminó con la funcion todas_celdas_seguras_descubiertas.

    Args:
        estado (EstadoJuego): Estado a analizar.
            
    Returns:
        bool:
            res = True: Si todas_celdas_seguras_descubiertas es verdadero. \n
            res = False: Si todas_celdas_seguras_descubiertas es falso.
    """
    res : bool = False
    if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
        res = True

    return res


# EJERCICIO 8
def reiniciar_juego(estado: EstadoJuego) -> None:
    """
    Reinicia el juego creando un nuevo estado con la funcion crear_juego con las mismas dimensiones y minas que antes,
    pero con nuevos tableros y cambiando el juego_terminado a False.
    En caso de que el tablero reiniciado tenga las minas en las mismas posiciones que el anterior, se reinicia de vuelta el tablero hasta que sea diferente.

    Args:
        estado (EstadoJuego): Estado a reiniciar.
            
    Returns:
        None:
    """
    nuevo_estado : EstadoJuego = crear_juego(estado['filas'], estado['columnas'], estado['minas'])

    while not tableros_distintos(estado['tablero'], nuevo_estado['tablero']):
        nuevo_estado = crear_juego(estado['filas'], estado['columnas'], estado['minas'])

    estado['tablero_visible'] = nuevo_estado['tablero_visible']
    estado['juego_terminado'] = nuevo_estado['juego_terminado']
    estado['tablero'] = nuevo_estado['tablero']


def tableros_distintos(t1 : list[list[int]], t2: list[list[int]]) -> bool:
    """
    Guarda las posiciones donde hay una mina de ambos tableros pasados por parametros y analiza si las posiciones de ambos tableros son las mismas.

    Args:
        t1 (list[list[int]]): Primer tablero a analizar.
        t2 (list[list[int]]): Segundo tablero a analizar.
            
    Returns:
        bool:
            res = True: Si la cantidad de posiciones donde coinciden las minas en ambos tableros es menor a la cantidad total de posiciones donde hay una mina. \n
            res = False: Si en todas las posiciones donde hay una mina en t1, tambien hay una mina en t2.
    """
    res : bool = False
    posiciones : list[tuple[int, int]] = []
    posiciones_nuevas : list[tuple[int, int]] = []

    for i in range (len(t1)):
        for j in range (len(t1[0])):
            if t1[i][j] == -1:
                posiciones.append((i, j))

    for f in range (len(t2)):
        for c in range (len(t2[0])):
            if t2[f][c] == -1:
                posiciones_nuevas.append((f, c))

    contador : int = 0
    for posicion_1 in posiciones:
        for posicion_2 in posiciones_nuevas:
            if posicion_1 == posicion_2:
                contador += 1

    if contador < len(posiciones):
        res = True

    return res


# EJERCICIO 9
from typing import TextIO
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """
    Se guarda en ruta_directorio los archivos tablero.txt y tablero_visible.txt.
    Ambos archivos tienen los elementos de su tablero de juego correspondiente separados por comas, sin espacios y con saltos de linea en cada fila.
    Ademas de que en tablero_visible.txt se reemplaza BANDERA por '*' y VACIO por '?'.

    Args:
        estado (EstadoJuego): Estado del cual se van a guardar los tableros.
        ruta_directorio (str): Ruta donde se van a guardar los archivos tablero.txt y tablero_visible.txt
            
    Returns:
        None:
    """
    ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
    ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

    tablero : list[list[int]] = estado['tablero']
    tablero_visible : list[list[str]] = estado['tablero_visible']

    f_tablero : TextIO = open(ruta_tablero, 'w', encoding='utf-8')
    
    for i in range (len(tablero)):
        linea_tablero : str = ""
        for j in range (len(tablero[0])):
            linea_tablero += str(tablero[i][j])

        texto_tablero : str = agregar_comas(linea_tablero)
        f_tablero.write(texto_tablero + '\n')

    f_tablero.close()

    f_tablero_visible : TextIO = open(ruta_tablero_visible, 'w', encoding='utf-8')

    for i in range (len(tablero_visible)):
        linea_tablero_visible : str = ""
        for j in range (len(tablero_visible[0])):
            if tablero_visible[i][j] == BANDERA:
                linea_tablero_visible += '*'
            elif tablero_visible[i][j] == VACIO:
                linea_tablero_visible += '?'
            else:
                linea_tablero_visible += str(tablero_visible[i][j])

        texto_tablero_visible : str = agregar_comas(linea_tablero_visible)
        f_tablero_visible.write(texto_tablero_visible + '\n')

    f_tablero_visible.close()


def agregar_comas(linea: str) -> str:
    """
    Agrega comas entre cada caracter de una linea de texto sin contar los '-' para poder poner los -1 en las lineas.

    Args:
        linea (str): Linea de texto pasada por parametro a la cual se le van a agregar las comas.
            
    Returns:
        str:
            linea_comas: Linea de texto con las comas agregadas.
    """
    linea_comas : str = ""
    linea_sin_espacios : str = sin_espacios_y_saltos(linea) 

    for i in range (len(linea_sin_espacios)):
        linea_comas += linea_sin_espacios[i]
        if linea_sin_espacios[i] != '-':
            if i < len(linea_sin_espacios) - 1:
                linea_comas += ','

    return linea_comas


def sin_espacios_y_saltos(linea : str) -> str:
    """
    Saca los espacios y saltos de linea de una linea de texto.

    Args:
        linea (str): Linea de texto pasada por parametro a la cual se le van a sacar los espacios y los saltos de linea.
            
    Returns:
        str:
            linea_nueva: Linea de texto sin espacios ni saltos de linea.
    """
    linea_nueva : str = ""

    for i in range (len(linea)):
        if linea[i] != " " and linea[i] != "\n":
            linea_nueva += str(linea[i])

    return linea_nueva


# EJERCICIO 10 
def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    """
    Carga los tableros que hay en ruta directorio, tomando cada uno de esos archivos y leyendo las lineas de cada uno,
    Compara que los elementos de ambos tableros coincidan y crea un estado con los elementos de tablero.txt y tablero_visible.txt
    Toma las lineas de ambos tableros, separa los elementos por comas y analiza.
    Compara la cantidad de filas, columnas, minas y la cantidad de minas adyacentes en el resto de celdas.    
    En tablero hay valores entre -1 y 8, y en tablero visible solo puede haber valores entre 0 y 8, '*' que es BANDERA y '?' que es VACIO. \n
    estado = {
            estado['filas'] = cantidad de lineas en tablero.txt \n
            estado['columnas'] = 1 + cantidad de comas por linea en tablero.txt \n
            estado['minas'] = cantidad de -1 en tablero.txt. \n
            estado['tablero'] = es igual, posicion a posicion, a los valores en tablero.txt \n
            estado['tablero_visible'] = es igual, posicion a posicion, a los valores en tablero_visible.txt, cambiando '*' por BANDERA y '?' por VACIO. \n
            estado['juego_terminado'] = False} \n
    
    Args:
        estado (EstadoJuego): Estado que se va a limpiar y agregar los valores correspondientes de los archivos de la ruta.
        ruta_directorio (str): Ruta de donde se van a cargar los archivos tablero.txt y tablero_visible.txt
            
    Returns:
        bool:
            res = True: Si se cumplen todas las condiciones. \n
            res = False: Si alguno de los archivos no existe. \n
            res = False: Si la cantidad de lineas de ambos tableros son distintas, osea si sus dimensiones son distintas. \n
            res = False: Si la cantidad de comas de alguna linea de las lineas del tablero o del tablero visible es diferente a las demas. \n
            res = False: Si hay valores incorrectos en tablero visible. \n
            res = False: Si algun numero de alguna posicion del tablero no coincide con su valor al contar la cantidad de minas en las posiciones adyacentes. \n
            res = False: Si en tablero visible hay un numero entre 0 y 8 que no coincide con el valor de la misma posicion en tablero. \n
            res = False: Si no hay minas en el tablero. \n
            res = False: Si no existe ninguna posicion en el tablero donde haya un numero mayor a 0 y en esa misma posicion del tablero visible haya un VACIO.
    """
    estado.clear()
    ruta_tablero = os.path.join(ruta_directorio, 'tablero.txt')
    ruta_tablero_visible = os.path.join(ruta_directorio, 'tablero_visible.txt')

    res : bool = True

    if not existe_archivo(ruta_directorio, 'tablero.txt') or not existe_archivo(ruta_directorio, 'tablero_visible.txt'):
        return False

    f_tablero : TextIO = open(ruta_tablero, 'r', encoding='utf-8')
    lineas_tablero : list[str] = f_tablero.readlines()
    f_tablero.close()

    f_tablero_visible : TextIO = open(ruta_tablero_visible, 'r', encoding='utf-8')
    lineas_tablero_visible : list[str] = f_tablero_visible.readlines()
    f_tablero_visible.close()


    tablero : list[list[int]] = crear_tablero(lineas_tablero)
    tablero_visible : list[list[str]] = crear_tablero_visible(lineas_tablero_visible)

    if tablero_visible == []:
        return False

    if not son_matriz_y_misma_dimension(tablero, tablero_visible):
        return False
    

    cantidad_comas : int = contar_comas(lineas_tablero[0])

    for linea in lineas_tablero:
        if contar_comas(linea) != cantidad_comas:
            res = False
        
    for linea in lineas_tablero_visible:
        if contar_comas(linea) != cantidad_comas:
            res = False


    minas : int = contar_minas(tablero)
    if minas == 0:
        res = False


    if not tableros_iguales(tablero, tablero_visible):
        res = False


    if not hay_vacio(tablero, tablero_visible):
        res = False


    if res == True:
        estado['filas'] = len(lineas_tablero)
        estado['columnas'] = 1 + contar_comas(lineas_tablero[0])
        estado['minas'] = minas
        estado['tablero'] = tablero
        estado['tablero_visible'] = tablero_visible
        estado['juego_terminado'] = False

    return res


def crear_tablero(lineas_tablero: list[str]) -> list[list[int]]:
    """
    Crea un tablero con una lista de string que funcionan como las filas del tablero,
    y analiza que los valores de dichas lineas correspondan a valores permitidos, que son los numeros entre -1 y 8.

    Args:
        lineas_tablero (list[str]): Lista de lineas de texto pasada por parametro con la que se va a crear el tablero.
            
    Returns:
        list[list[int]]:
                    tablero: Tablero nuevo creado con las lineas de la lista pasada por parametro, tomando solo los valores entre -1 y 8.
    """
    validos : list[str] = ['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8']
    tablero : list[list[int]] = []

    for linea in lineas_tablero:
        valores : list[str] = split(linea, ',')
        fila : list[int] = []

        for elem in valores:
            if elem in validos:
                if elem == '-1':
                    fila.append(-1)
                else:
                    fila.append(int(elem))
        tablero.append(fila)

    return tablero


def crear_tablero_visible(lineas_tablero_visible: list[str]) -> list[list[str]]:
    """
    Crea un tablero visible con una lista de string que funcionan como las filas del tablero visible,
    y analiza que los valores de dichas lineas correspondan a valores permitidos, que son los numeros entre -1 y 8, ? y *.
    En caso contrario, devuelve la matriz vacía.

    Args:
        lineas_tablero_visible (list[str]): Lista de lineas de texto pasada por parametro con la que se va a crear el tablero visible.
            
    Returns:
        list[list[int]]:
                    tablero_visible: Tablero nuevo creado con las lineas de la lista pasada por parametro, tomando solo los valores entre -1 y 8.
    """
    validos : list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '*', '?']
    tablero_visible_valido : bool = True
    tablero_visible : list[list[str]] = []

    for linea in lineas_tablero_visible:
        valores_visibles : list[str] = split(linea, ',')
        fila_visible : list[str] = []

        for elem in valores_visibles:
            if elem in validos:
                if elem == '?':
                    fila_visible.append(VACIO)
                elif elem == '*':
                    fila_visible.append(BANDERA)
                else:
                    fila_visible.append(elem)
            else:
                tablero_visible_valido = False
        tablero_visible.append(fila_visible)

    if not tablero_visible_valido:
        tablero_visible = []

    return tablero_visible


def contar_minas(tablero: list[list[int]]) -> int:
    """
    Cuenta la cantidad de minas que hay en un tablero, recorriendolo y contando cada aparicion de un -1.

    Args:
        tablero (list[list[int]]): Tablero a recorrer para contar minas.
            
    Returns:
        int:
            minas: cantidad de minas que hay en el tablero pasado por parametro.
    """
    minas : int = 0

    for i in range (len(tablero)):
        for j in range (len(tablero[0])):
            if tablero[i][j] == -1:
                minas += 1

    return minas


def tableros_iguales(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """
    Recorre el tablero y compara cada celda con la misma posicion en el tablero visible para ver que coincidan,
    y luego analiza si el valor de esa posicion es el correcto usando la funcion contar_minas_adyacentes.

    Args:
        tablero (list[list[int]]): Tablero a recorrer para anlizar sus elementos.
        tablero_visible (list[list[str]]): Tablero visible para comparar sus valores con los del tablero.
            
    Returns:
        bool:
            res = True: Si todas las posiciones de tablero y tablero visible coinciden y tienen el valor correspondiente. \n
            res = False: Si el valor de alguna celda de tablero es distinto al de tablero visible. \n
            res = False: Si algun valor de alguna celda del tablero no tiene el valor correcto al contar las minas adyacentes.
    """
    res : bool = True
    numeros : list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] != -1:
                if contar_minas_adyacentes(tablero, i, j) != tablero[i][j]:
                    res = False
            if tablero_visible[i][j] in numeros:
                if tablero[i][j] != int(tablero_visible[i][j]):
                    res = False
                
    return res


def hay_vacio(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """
    Recorre el tablero del estado y analiza si hay posiciones con minas adyacentes que sean VACIO en el tablero visbile.

    Args:
        estado (EstadoJuego): estado del cual se analizaran el tablero y el tablero visible.
            
    Returns:
        bool:
            res = True: Si en alguna poscion del tablero donde haya alguna mina adyacente, en tablero visible es VACIO. \n
            res = False: Si no hay ninguna posicion con VACIO en todo el tablero visible.
    """
    res : bool = False

    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] > 0 and tablero_visible[i][j] == VACIO:
                res = True

    return res


def contar_comas (linea : str) -> int:
    """
    Cuenta la cantidad de comas que tiene una linea de texto.

    Args:
        linea (str): Linea de texto pasada por parametro a la cual se le van a contar las comas que tiene.
            
    Returns:
        int:
            contador_comas: Cantidad de comas de una linea.
    """
    contador_comas : int = 0

    for elem in linea:
        if elem == ',':
            contador_comas += 1

    return contador_comas


def split(linea: str, separador: str) -> list[str]:
    """
    Crea una lista con los caracteres de la linea de texto pasada por parametro, los elementos de la lista son los que estan a los lados de un separador.

    Args:
        linea (str): Linea de texto pasada por parametro que se va a recorrer para agregar sus caracteres, distintos del separador, a una lista.
        separador (str): Caracter que se toma como referencia para dividir la linea.
            
    Returns:
        list[str]:
                res: Lista con los caracteres de la linea de texto que se encuentran entre el separador.
    """
    linea_modificada : str = sin_espacios_y_saltos(linea)
    res : list[str] = []
    letra_actual : str = ""

    for letra in linea_modificada:
        if letra == separador:
            res.append(letra_actual)
            letra_actual = ""
        else:
            letra_actual += letra
    res.append(letra_actual)

    return res