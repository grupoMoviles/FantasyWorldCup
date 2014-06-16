import baseCouch
from flask import jsonify
import hashlib
base = baseCouch.base

def logIn(usuario,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['usuario'] == usuario and row.key['clave'] == keyHash.hexdigest():
            return jsonify({'event':'0'})
    return jsonify({'event':'1'})

def agregarJugador(nombre,equipo,posicion,precio,clave):  
    sePuedeAgregar = True
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name'] == nombre and row.key['team'] == equipo:
            sePuedeAgregar = False
            break
    if sePuedeAgregar:
        jugador = dict(totalPoints=0,stats=[],team=equipo,price=int(precio),type="player",name=nombre,position=posicion)
        base.save(jugador)
        return jsonify({'result':'1'})
    return jsonify({'result':'0'})

def borrarJugador(nombre,equipo,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name'] == nombre and row.key['team'] == equipo:
            doc = base[row.key['_id']]
            base.delete(doc)
            break   
    return jsonify({'result':'1'})

def editarJugador(nombre,equipo,posicion,precio,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name'] == nombre and row.key['team'] == equipo:            
            doc = base[row.key['_id']]
            break
    doc['price'] = precio
    doc['position'] = posicion    
    base.save(doc)
    return jsonify({'result':'1'})

def registrarUsuario(correo,password,pais,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == correo:
            return jsonify({'result':'0'})
    keyHash = hashlib.md5(password)
    fantasy = dict(formation=[],startingPlayers=[],bench=[],name="",transfers=16,captain={},totalPoints=0,fixtures=[])
    base.save({'type':'user','players':[],'email':correo,'facebook':'false',
               'google':'false','country':pais,'password':keyHash.hexdigest(),'fantasyTeam':fantasy})
    return jsonify({'result':'1'})

def obtenerUsuarios(clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    lista = []
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        lista.append(row.key)
    return jsonify({'user':lista})

def borrarUsuario(email,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == email:
            doc = base[row.key['_id']]
            base.delete(doc)
            break   
    return jsonify({'result':'1'})

def agregarEquipo(name,abreviation,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_equipos_fun/obtener_equipos_fun'):
        if row.key['name'] == name:
            return jsonify({'result':'0'})
    equipo = dict(name=name,abbreviation=abreviation,type='team')
    base.save(equipo)
    return jsonify({'result':'1'})

def borrarEquipo(name,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_equipos_fun/obtener_equipos_fun'):
        if row.key['name'] == name:
            doc = base[row.key['_id']]
            base.delete(doc)
            break   
    return jsonify({'result':'1'})

def llenarTitulares():
    titulares = []
    titulares.append([dict(player=dict(position="Goalkeeper",price=0,name="VACIO",team="VACIO"))])
    posicion = []
    for i in range(0,4):
        posicion.append(dict(player=dict(position="Defender",price=0,name="VACIO",team="VACIO")))
    titulares.append(posicion)
    posicion = []
    for i in range(0,4):
        posicion.append(dict(player=dict(position="Midfielder",price=0,name="VACIO",team="VACIO")))
    titulares.append(posicion)
    posicion = []
    for i in range(0,2):
        posicion.append(dict(player=dict(position="Forward",price=0,name="VACIO",team="VACIO")))
    titulares.append(posicion)
    return titulares

def llenarBanca():
    titulares = []
    titulares.append(dict(player=dict(position="Goalkeeper",price=0,name="VACIO",team="VACIO")))
    titulares.append(dict(player=dict(position="Defender",price=0,name="VACIO",team="VACIO")))
    titulares.append(dict(player=dict(position="Midfielder",price=0,name="VACIO",team="VACIO")))
    titulares.append(dict(player=dict(position="Forward",price=0,name="VACIO",team="VACIO")))    
    return titulares


def borrarFantasy(name,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == name:
            doc = base[row.key['_id']]
            fantasy = dict(formation=[],startingPlayers=llenarTitulares(),bench=llenarBanca(),name="",transfers=120,captain={},totalPoints=0,fixtures=[])
            doc['fantasyTeam'] = fantasy
            base.save(doc)
            break   
    return jsonify({'result':'1'})


def obtenerLigas(clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    lista = []
    for row in base.view('obtener_ligas/obtener_ligas'):
        lista.append(row.key)
    return jsonify({'liga':lista})

def borrarLiga(name,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_ligas/obtener_ligas'):
        if row.key['name'] == name:
            doc = base[row.key['_id']]
            base.delete(doc)
            break   
    return jsonify({'result':'1'})

def obtenerFechas(clave):
    lista = []
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        lista.append(row.key)
    return jsonify({'fixture':lista})

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
    return jsonify({'result':'1'})

def editarFecha(number,state,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        if row.key['number'] == number:
            doc = base[row.key['_id']]
            doc['state'] = state
            base.save(doc)
            return jsonify({'result':'1'})
    return jsonify({'result':'0'})

def borrarFecha(number,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        if row.key['number'] == number:
            doc = base[row.key['_id']]
            base.delete(doc)
            return jsonify({'result':'1'})
    return jsonify({'result':'0'})

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
            return jsonify({'result':'1'})
    return jsonify({'result':'0'})

def borrarPartido(numberFixture,team1,clave):
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})    
    for row in base.view('obtener_fechas/obtener_fechas'):
        if row.key['number'] == numberFixture:
            lista = []
            for item in row.key['matches']:
                if item['team1'] != team1:
                    lista.append(item)            
            doc = base[row.key['_id']]
            doc['matches'] = lista
            base.save(doc)
            return jsonify({'result':'1'})
    return jsonify({'result':'0'})

def editarPartido(numberFixture,state,team1,team2,score1,score2,lastTeam,clave):
    borrarPartido(numberFixture,lastTeam,clave)
    return agregarPartido(numberFixture,state,team1,team2,score1,score2,clave)

def editarEstadisticasJugador(nombre,equipo,fecha,amarillas,rojas,asistencias,goles,minutos,puntos,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name'] == nombre and row.key['team'] == equipo:            
            doc = base[row.key['_id']]
            break
    estadisticas = []
    puntosTotales = doc['totalPoints']
    for elem in doc['stats']:
        if elem['fixture'] != fecha:
            estadisticas.append(elem)
    stat = dict(yellows=amarillas,reds=rojas,assists=asistencias,goals=goles,minutesPlayed=minutos,points=puntos,fixture=fecha)
    estadisticas.append(stat)
    puntosTotales+=int(puntos)
    doc['stats'] = estadisticas
    doc['totalPoints'] = puntosTotales
    base.save(doc)
    return jsonify({'result':'1'})

def borrarEstadisticasJugador(nombre,equipo,fecha,clave):  
    for row in base.view('obtener_admin/obtener_admin'):
        keyHash = hashlib.md5(clave)
        if row.key['clave'] != keyHash.hexdigest():
            return jsonify({'result':'0'})
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['name'] == nombre and row.key['team'] == equipo:            
            doc = base[row.key['_id']]
            break
    puntosFecha = 0
    estadisticas = []
    puntosTotales = doc['totalPoints']
    for elem in doc['stats']:
        if elem['fixture'] != fecha:
            estadisticas.append(elem)
        else:
            puntosFecha = elem['points']
    puntosTotales-=int(puntosFecha)
    doc['stats'] = estadisticas
    doc['totalPoints'] = puntosTotales
    base.save(doc)
    return jsonify({'result':'1'})
