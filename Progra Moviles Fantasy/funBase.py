import couchdb
import hashlib
couch = couchdb.Server('https://app25620887.heroku:guqMR0FiTQqqw5O8cgG27n7U@app25620887.heroku.cloudant.com')
base = couch['fantasydb']

#Agrega las fechas
def agregarFecha(number,state,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'2'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        if row.key['number'] == number:
            return jsonify({'result':'0'})
    fecha = dict(state=state,matches=[],type='fixture',number=number)
    base.save(fecha)

def obtenerUsuarios(clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    lista = []
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        lista.append(row.key)
    return lista

#Borra partidos de una fecha
def borrarPartidos(number,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        if row.key['number'] == number:
            doc = base[row.key['_id']]
            doc['matches'] = []
            base.save(doc)
            return 1
        
#Agrega Partido a una fecha
def agregarPartido(numberFixture,state,team1,team2,score1,score2,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        if row.key['number'] == numberFixture:
            doc = base[row.key['_id']]
            matches = doc['matches']
            matches.append(dict(team1=team1,team2=team2,state=state,score=[score1,score2]))
            doc['matches'] = matches
            base.save(doc)
            return 1
    return 0

#Agrega estadisticas por fecha
def agregarEstadisticasJugador(nombre,equipo,fecha,amarillas,rojas,asistencias,goles,minutos,puntos,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return 0
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name'] == nombre and row.key['team'] == equipo:            
            doc = base[row.key['_id']]
            break
    estadisticas = []
    puntosTotales = doc['totalPoints']
    for elem in doc['stats']:
        if elem['fixture'] != fecha:
            estadisticas.append(elem)
    stat = dict(yellows=amarillas,reds=rojas,assists=asistencias,goals=goles,minutesPlayed=minutos,points=puntos,fixture=str(fecha))
    estadisticas.append(stat)
    puntosTotales+=int(puntos)
    doc['stats'] = estadisticas
    doc['totalPoints'] = puntosTotales
    base.save(doc)
    return 1

def agregarEstadisticasJugador2(id,nombre,equipo,fecha,amarillas,rojas,asistencias,goles,minutos,puntos,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return 0
    doc = base[id]
    estadisticas = []
    puntosTotales = doc['totalPoints']
    for elem in doc['stats']:
        if elem['fixture'] != fecha:
            estadisticas.append(elem)
    stat = dict(yellows=amarillas,reds=rojas,assists=asistencias,goals=goles,minutesPlayed=minutos,points=puntos,fixture=str(fecha))
    estadisticas.append(stat)
    puntosTotales+=int(puntos)
    doc['stats'] = estadisticas
    doc['totalPoints'] = puntosTotales
    base.save(doc)
    return 1

#Borrar Estadisticas de todos los jugadores
def borrarEstadisticasJugadores(clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return 0
    i=0
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        doc = base[row.key['_id']]            
        doc['stats'] = []
        doc['totalPoints'] = 0
        base.save(doc)
        i+=1
    return 1

def encontrarPuntosJugador(nombre,equipo,numFecha):
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name']==nombre and row.key['team']==equipo:
            for item in row.key['stats']:
                if item['fixture'] == numFecha:
                    return item['points']
    return 0

def actualizarUsuarios(numFecha):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
            puntosJugador = 0
            for item in row.key['fantasyTeam']['startingPlayers']:
                    for jugador in item:
                            #print(str(jugador['player']['name']),str(jugador['player']['team']))
                            puntosJugador += encontrarPuntosJugador(str(jugador['player']['name']),str(jugador['player']['team']), numFecha)
            points = row.key['fantasyTeam']['totalPoints']
            if puntosJugador > 0:
                print(puntosJugador)
                doc = base[row.key['_id']]
                doc['fantasyTeam']['totalPoints'] = points+puntosJugador
                base.save(doc)

def borrarPuntosUsuarios():
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        doc = base[row.key['_id']]
        doc['fantasyTeam']['totalPoints'] = 0
        base.save(doc)
    
           

    
