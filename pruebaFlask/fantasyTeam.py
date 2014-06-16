from flask import jsonify
import baseCouch as bc
import hashlib
base = bc.base
#FANTASY
    #
    
def obtenerMatriz(mat):
    lista = []
    while mat!= ']':
        matTemp = mat[1:mat.find("]")+1][1:-1].split(",")
        mat = mat[mat.find("]")+1:len(mat)]
        lista.append(matTemp)
    return lista

def obtenerPosicionPrecioT(listaJugadores,pJugador,pEquipo):
    for item in listaJugadores:
        for jugador in item:          
            if str(jugador['player']['name']) == pJugador and str(jugador['player']['team'])==pEquipo:
                return [jugador['player']['position'],jugador['player']['price']]
    return -1

def obtenerPosicionPrecioB(listaJugadores,pJugador,pEquipo):    
    for jugador in listaJugadores:      
        if str(jugador['player']['name']) == pJugador and str(jugador['player']['team'])==pEquipo:
            return [jugador['player']['position'],jugador['player']['price']]
    return -1

#METODOS USABLES
def establecerEquipo(password,jugadores,equipos,jugadoresBanca,equiposBanca):
    equipos = equipos[1:-1].split(',')
    jugadores = obtenerMatriz(jugadores)
    keyHash = hashlib.md5(password)       
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():
            respuesta = []
            doc = base[row.key['_id']]
            cont = 0
            equipoIndex = 0
            titulares = doc['fantasyTeam']['startingPlayers']
            banca = doc['fantasyTeam']['bench']
            while cont < len(jugadores):
                temp = []
                for i in range(0,len(jugadores[cont])):
                    dato = []
                    esTitular = obtenerPosicionPrecioT(titulares,jugadores[cont][i],equipos[equipoIndex])
                    esBanca = obtenerPosicionPrecioB(banca,jugadores[cont][i],equipos[equipoIndex])
                    if esTitular != -1:
                        dato = esTitular
                    elif esBanca != -1:
                        dato = esBanca
                    else:
                        dato = obtenerPosicionPrecio(jugadores[cont][i],equipos[equipoIndex])
                    temp.append(dict(player=dict(position=dato[0],price=dato[1],name=jugadores[cont][i],team=equipos[equipoIndex])))
                    equipoIndex+=1
                respuesta.append(temp)
                cont += 1
            establecerBancas(jugadoresBanca,equiposBanca,doc)
            doc['fantasyTeam']['startingPlayers'] = respuesta
            #print(titulares)
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def establecerBancas(jugadores,equipos,doc):
    equipos = equipos[1:-1].split(',')
    jugadores = jugadores[1:-1].split(',')    
    cont = 0
    titulares = doc['fantasyTeam']['startingPlayers']
    banca = doc['fantasyTeam']['bench']
    bancas = []
    while cont < len(jugadores):
        dato = []
        esTitular = obtenerPosicionPrecioT(titulares,jugadores[cont],equipos[cont])
        esBanca = obtenerPosicionPrecioB(banca,jugadores[cont],equipos[cont])
        if esTitular != -1:
            dato = esTitular
        elif esBanca != -1:
            dato = esBanca
        else:
            dato = obtenerPosicionPrecio(jugadores[cont],equipos[cont])
        bancas.append(dict(player=dict(position=dato[0],price=dato[1],name=jugadores[cont],team=equipos[cont])))
        cont += 1
    doc['fantasyTeam']['bench'] = bancas
    base.save(doc)
    #return jsonify({'success':'0'})
    

def transferencia(password,jugador1,equipo1,jugador2,equipo2):
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():            
            doc = base[row.key['_id']]
            if jugador1 == "VACIO":
                return transferenciaVacio(jugador2,equipo2,doc)            
            if obtenerPosicionPrecioB(doc['fantasyTeam']['bench'],jugador1,equipo1) != -1:
                return transferenciaBanca(jugador1,equipo1,jugador2,equipo2,doc)
            iniciales = doc['fantasyTeam']['startingPlayers']
            dato = obtenerPosicionPrecio(jugador2,equipo2)
            salir = False
            for i in range(0,len(iniciales)):
                if salir:
                    break
                for jugador in range(0,len(iniciales[i])):
                    print(iniciales)
                    if iniciales[i][jugador]['player']['name']==jugador1 and iniciales[i][jugador]['player']['team']==equipo1:                        
                        iniciales[i][jugador] = dict(player=dict(position=dato[0],price=dato[1],name=jugador2,team=equipo2))
                        salir = True
                        break
            doc['fantasyTeam']['startingPlayers'] = iniciales
            doc['fantasyTeam']['transfers'] += obtenerPosicionPrecio(jugador1,equipo1)[1]
            doc['fantasyTeam']['transfers'] -= dato[1]
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})


def transferenciaBanca(jugador1,equipo1,jugador2,equipo2,doc):
    bancas = doc['fantasyTeam']['bench']
    dato = obtenerPosicionPrecio(jugador2,equipo2)
    for i in range(0,len(bancas)):
        if bancas[i]['player']['name'] == jugador1 and bancas[i]['player']['team'] == equipo1:
            bancas[i] = dict(player=dict(position=dato[0],price=dato[1],name=jugador2,team=equipo2))
            break
    doc['fantasyTeam']['bench'] = bancas
    doc['fantasyTeam']['transfers'] += obtenerPosicionPrecio(jugador1,equipo1)[1]
    doc['fantasyTeam']['transfers'] -= dato[1]
    base.save(doc)
    return jsonify({'success':'0'})

def transferenciaVacio(jugador,equipo,doc):
    dato = obtenerPosicionPrecio(jugador,equipo)
    titulares = doc['fantasyTeam']['startingPlayers']
    posiciones = dict(Goalkeeper=0,Defender=1,Midfielder=2,Forward=3)
    pos = posiciones[dato[0]]
    for i in range(0,len(titulares[pos])):
        if titulares[pos][i]['player']['name'] == "VACIO":
            titulares[pos][i] = dict(player=dict(position=dato[0],price=dato[1],name=jugador,team=equipo))
            doc['fantasyTeam']['startingPlayers'] = titulares
            doc['fantasyTeam']['transfers'] -= dato[1]
            base.save(doc)
            return jsonify({'success':'0'})
    banca = doc['fantasyTeam']['bench']
    for i in range(0,len(banca)):
        if banca[i]['player']['position'] == dato[0] and banca[i]['player']['name'] == "VACIO":
            banca[i] = dict(player=dict(position=dato[0],price=dato[1],name=jugador,team=equipo))
            doc['fantasyTeam']['bench'] = banca
            doc['fantasyTeam']['transfers'] -= dato[1]
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def obtenerTransfers(password):
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():            
            return jsonify({'transfers':row.key['fantasyTeam']['transfers']})
    return jsonify({'error':'1'})

def establecerCantidadTransferencias(password,monto):
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():
            doc = base[row.key['_id']]
            doc['fantasyTeam']['transfers'] = monto
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def cambiarCapitan(password,captain,captainTeam):
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():
            doc = base[row.key['_id']]
            if existeJugador(doc['fantasyTeam']['startingPlayers'],captain,captainTeam):
                doc['fantasyTeam']['captain'] = dict(player=dict(name=captain,team=captainTeam))
                base.save(doc)
                return jsonify({'success':'0'})
            else:
                return jsonify({'error':'1'})
    return jsonify({'error':'1'})

def registrarNombreFantasy(password,name):
    usuario = None
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():
            usuario = row.key
        elif row.key['fantasyTeam'].get('name') == name:            
            return jsonify({'error':'1'})
    doc = base[usuario['_id']]
    doc['fantasyTeam']['name'] = name
    base.save(doc)
    return jsonify({'success':'0'})

def saveFormation(password,formation):
    defenders = int(formation[0])
    midfielders = int(formation[1])
    forwards = int(formation[2])
    formation = [defenders,midfielders,forwards]
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():
            usuario = row.key
            doc = base[row.key['_id']]
            doc['fantasyTeam']['formation'] = formation
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def actualizarPuntos(password,puntos):
    keyHash = hashlib.md5(password)
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['password'] == keyHash.hexdigest():
            doc = base[row.key['_id']]
            doc['fantasyTeam']['totalPoints'] = puntos
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

#FIN METODOS USABLES
#active = 0,1
def agregarJugador(correo,jugador,equipo,active):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == correo:
            titulares = row.key['fantasyTeam']['startingPlayers'] 
            banca = row.key['fantasyTeam']['bench']
            lista = titulares + banca
            if existeJugador(lista,jugador,equipo):
                return jsonify({'error':'1'})
            doc = base[row.key['_id']]
            if int(active):
                titulares.append(dict(player=dict(name=jugador,team=equipo)))
                doc['fantasyTeam']['startingPlayers'] = titulares
            else:
                banca.append(dict(player=dict(name=jugador,team=equipo)))
                doc['fantasyTeam']['bench'] = banca

            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def agregarJugadoresTitulares(correo,jugadores,equipos):
    equipos = equipos[1:-1].split(',')
    jugadores = jugadores[1:-1].split(',')
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == correo:
            titulares = row.key['fantasyTeam']['startingPlayers'] 
            banca = row.key['fantasyTeam']['bench']
            lista = titulares + banca
            cont = 0
            while cont < len(jugadores):         
                if existeJugador(lista,jugadores[cont],equipos[cont]):
                    return jsonify({'error':'1'})
                cont += 1
            doc = base[row.key['_id']]
            cont = 0
            while cont < len(jugadores):
                titulares.append(dict(player=dict(name=jugadores[cont],team=equipos[cont])))
                cont += 1
            doc['fantasyTeam']['startingPlayers'] = titulares
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def agregarJugadoresBancas(correo,jugadores,equipos):
    equipos = equipos[1:-1].split(',')
    jugadores = jugadores[1:-1].split(',')
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == correo:
            titulares = row.key['fantasyTeam']['startingPlayers'] 
            banca = row.key['fantasyTeam']['bench']
            lista = titulares + banca
            cont = 0
            while cont < len(jugadores):         
                if existeJugador(lista,jugadores[cont],equipos[cont]):
                    return jsonify({'error':'1'})
                cont += 1
            doc = base[row.key['_id']]
            cont = 0
            while cont < len(jugadores):
                banca.append(dict(player=dict(name=jugadores[cont],team=equipos[cont])))
                cont+=1
            doc['fantasyTeam']['bench'] = banca
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def bancaTitular(email,startingPlayer,benchPlayer,startingPlayerTeam,benchPlayerTeam): 
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == email:
            bancas = row.key['fantasyTeam']['bench']
            titulares = row.key['fantasyTeam']['startingPlayers']
            bancaTemp = bancas[obtenerPosicionJugador(benchPlayer,benchPlayerTeam,bancas)]
            bancas[obtenerPosicionJugador(benchPlayer,benchPlayerTeam,bancas)] = titulares[obtenerPosicionJugador(startingPlayer,startingPlayerTeam,titulares)]
            titulares[obtenerPosicionJugador(startingPlayer,startingPlayerTeam,titulares)] = bancaTemp 
            doc = base[row.key['_id']]           
            doc['fantasyTeam']['bench'] = bancas
            doc['fantasyTeam']['startingPlayers'] = titulares
            base.save(doc)
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def obtenerPosicionPrecio(nombre,equipo):
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['team'] == equipo and row.key['name'] == nombre:
            return [row.key['position'],row.key['price']]



def obtenerPosicionJugador(nombre,equipo,lista):
    cont = 0
    while cont < len(lista):
        if lista[cont]['player']['name']==nombre and lista[cont]['player']['team']==equipo:
            return cont
    return -1

def existeJugador(lista,jugador,equipo):
    for item in lista:
        if item.get('player').get('name') == jugador and item.get('player').get('team') == equipo:
            return True
    return False
