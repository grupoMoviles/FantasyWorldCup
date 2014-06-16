import baseCouch as bc
from flask import jsonify
base = bc.base
#Jugadores
def obtenerJugadores():
    lista = []    
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        lista.append(row.key)
    return jsonify( { 'player': lista })

def obtenerJugadores2():
    lista = []    
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        player = dict(name=row.key['name'],team=row.key['team'],position=row.key['position'],totalPoints=row.key['totalPoints'],price = row.key['price'])
        lista.append(player)
    return jsonify( { 'player': lista })

def obtenerJuadoresEquipo(equipo):
    lista = []
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['team'] == equipo:
            lista.append(row.key)
    return jsonify({'player':lista})

