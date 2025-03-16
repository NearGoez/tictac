import random 
import pickle
import os 
import regex as re
import time

if os.path.exists('data.pkl'):
    with open('data.pkl', 'rb') as f:
        Q_table = pickle.load(f)
else:
    Q_table = {}

alpha = 0.1
gamma = 0.9
r = 1

def revisar_ganador(tablero):
    tablero = "".join(tablero)

    # Convertir lista a string para facilitar la búsqueda de patrones
    tablero_str = "".join(tablero)
    
    # Revisar filas
    for i in range(0, 9, 3):
        if tablero[i] == tablero[i+1] == tablero[i+2] != ' ':
            return tablero[i]
    
    # Revisar columnas
    for i in range(3):
        if tablero[i] == tablero[i+3] == tablero[i+6] != ' ':
            return tablero[i]
    
    # Revisar diagonales
    if tablero[0] == tablero[4] == tablero[8] != ' ':
        return tablero[0]
    if tablero[2] == tablero[4] == tablero[6] != ' ':
        return tablero[2]
    
    # Revisar empate
    if ' ' not in tablero:
        return 'Empate'
    

def mostrar_tablero(lista_tablero):
    for i in range(3):
        print(lista_tablero[(i*3):(i*3 + 3)])
    print()

def jugar(qtable, params, mostrar=False):

    alpha, gamma, epsilon = params
    tablero = [' ' for _ in range(9)]
    players = ['X', 'O']

    ganador = None
    jugadas_O = []
    jugadas_X = []

    while not ganador:

        for player in players:
            #print('turno de', player)
            state = player + '-' + ''.join(''.join(fila) for fila in tablero)

            #determinar la mejor jugada

            casillas_vacias = [i for i in range(len(tablero)) if tablero[i] == ' ']

            if state not in qtable.keys():
                #en caso de que el estado sea nuevo
                qtable[state] = [0 for _ in range(9)] #se crea el estado nuevo

                jugada = random.choice(casillas_vacias)

            elif random.random() < epsilon:
                jugada = random.choice(casillas_vacias)
            else:
                valores_temp = qtable[state].copy()
                for i in range(9):
                    if i not in casillas_vacias:
                        valores_temp[i] = -float('inf')

                jugada = valores_temp.index(max(valores_temp))

            if player == 'X':
                jugadas_X.append((state, jugada))
            else:
                jugadas_O.append((state, jugada))

            tablero[jugada] = player

            ganador = revisar_ganador(tablero)
            if ganador:
                break
            
            if mostrar:
                mostrar_tablero(tablero)


    if mostrar:
        mostrar_tablero(tablero)
        print('El ganador es', ganador)

    if ganador == 'O':
        r_O = 1.0
        r_X = -1.0
    elif ganador == 'X':
        r_O = -1.0
        r_X = 1.0
    else:
        r_O, r_X = 0.1, 0.1

    for i in range(len(jugadas_X)-1, -1, -1):
        estado, accion = jugadas_X[i]
        if i == len(jugadas_X)-1:
            print(f"Actualizacion: {estado}[{accion}] | {qtable[estado][accion]} -> ", end='')
            qtable[estado][accion] += alpha * (r_X - qtable[estado][accion])

            print(qtable[estado][accion])
        else:
            print(f"Actualizacion: {estado}[{accion}] | {qtable[estado][accion]} -> ", end='')

            siguiente_estado = jugadas_X[i+1][0]
            mejor_siguiente = max(qtable[siguiente_estado]) if siguiente_estado in qtable else 0
            qtable[estado][accion] += alpha * (gamma * mejor_siguiente - qtable[estado][accion])

            print(qtable[estado][accion])

    for i in range(len(jugadas_O)-1, -1, -1):
        estado, accion = jugadas_O[i]
        if i == len(jugadas_O)-1:
            print(f"Actualizacion: {estado}[{accion}] | {qtable[estado][accion]} -> ", end='')

            qtable[estado][accion] += alpha * (r_O - qtable[estado][accion])

            print(qtable[estado][accion])
        else:
            print(f"Actualizacion: {estado}[{accion}] | {qtable[estado][accion]} -> ", end='')

            siguiente_estado = jugadas_O[i+1][0]
            mejor_siguiente = max(qtable[siguiente_estado]) if siguiente_estado in qtable else 0
            qtable[estado][accion] += alpha * (gamma * mejor_siguiente - qtable[estado][accion])

            print(qtable[estado][accion])
    


for _ in range(1):
    jugar(Q_table, (0.1, 0.9, 0.001), mostrar=True)


print(len(Q_table.items()))
with open('data.pkl', 'wb') as f:
    pickle.dump(Q_table, f)












