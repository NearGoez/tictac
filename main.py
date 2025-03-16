import random 
import pickle
import os 
import regex as re
import time

if os.path.exists('data.pkl'):
    with open('data.pkl', 'rb') as f:
        Q_table = pickle.load(f)

Q_table = {}
alpha = 0.1
gamma = 0.9
r = 1

def revisar_ganador(tablero):
    tablero = "".join(tablero)
    ganador = None
    if 'E' not in tablero:
        return 'Empate'

    for patron in ['X..X..X', 'X...X...X']:
        if re.search(patron, tablero):
            return 'X'
    for patron in ['XXX', 'X.X.X']:
        if re.search(patron, tablero) and tablero.index(patron)%3 != 1:
            return 'X'
        
    for patron in ['O..O..O', 'OOO', 'O...O...O', 'O.O.O']:
        if re.search(patron, tablero):
            return 'O'

    for patron in ['OOO', 'O.O.O']:
        if re.search(patron, tablero) and tablero.index(patron)%3 != 1:
            return 'O'
    return
def mostrar_tablero(lista_tablero):
    lista = []
    for i in range(3):
        print(lista_tablero[(i*3):(i*3 + 3)])
    print()

def jugar(qtable, params):

    alpha, gamma, r = params
    tablero = ['E' for _ in range(9)]
    players = ['X', 'O']

    ganador = None
    jugadas_O = []
    jugadas_X = []

    while not ganador:

        for player in players:
            #print('turno de', player)
            state = player + '-' + ''.join(''.join(fila) for fila in tablero)

            #determinar la mejor jugada

            casillas_vacias = [i for i in range(len(tablero)) if tablero[i] == 'E']

            if state not in qtable.keys():
                #en caso de que el estado sea nuevo

                qtable[state] = [0 for _ in range(9)] #se crea el estado nuevo
                #se revisa si hay algun potencial estado siguiente conocido 
                jugada = random.choice(casillas_vacias)
            else:
               jugada = qtable[state].index(max(qtable[state]))

            if player == 'X':
                jugadas_X.append((state, jugada))
            else:
                jugadas_O.append((state, jugada))

            tablero[jugada] = player
            mostrar_tablero(tablero)

            ganador = revisar_ganador(tablero)
            if ganador:
                break


    print('El ganador es', ganador)
    print(jugadas_O)
    print(jugadas_X)

    if ganador == 'O':
        r_O = r
        r_X = -r
    elif ganador == 'X':
        r_O = -r
        r_X = r
    else:
        r_O, r_X = 0, 0

    for i in range(0, len(jugadas_O), -1):
        print(i)

    for i in range(0, len(jugadas_X), -1):
        pass

        
jugar(Q_table, (0.1, 0.9, 1))

with open('data.pkl', 'wb') as f:
    pickle.dump(Q_table, f)












