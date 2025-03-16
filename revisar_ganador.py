import re


tablero = 'EXXXEEEOO'


ganador = 'none'
for patron in ['X..X..X',  'X...X...X', ]:
    if re.search(patron, tablero) :
        ganador = 'X'

for patron in ['XXX', 'X.X.X']:
    if re.search(patron, tablero) and tablero.index(patron)%3 != 1:
        print(tablero.index(patron))
        ganador = 'X'
print(ganador)

