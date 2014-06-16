import baseCouch
from flask import jsonify
import hashlib
base = baseCouch.base

def registrarUsuario(correo,password,pais):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == correo:
            return jsonify({'error':'1'})
    keyHash = hashlib.md5(correo+password)
    fantasy = dict(formation=[],startingPlayers=llenarTitulares(),bench=llenarBanca(),name="",transfers=120,captain={},totalPoints=0,fixtures=[])
    base.save({'type':'user','players':[],'email':correo,'facebook':'false',
               'google':'false','country':pais,'password':keyHash.hexdigest(),'fantasyTeam':fantasy})
    return jsonify({'success':'0'})

def registrarUsuarioFacebook(correo,password,pais):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == correo:
            return logIn(correo+password)
    keyHash = hashlib.md5(correo+password)
    fantasy = dict(formation=[],startingPlayers=llenarTitulares(),bench=llenarBanca(),name="",transfers=120,captain={},totalPoints=0,fixtures=[])
    base.save({'type':'user','players':[],'email':correo,'facebook':'false',
               'google':'false','country':pais,'password':keyHash.hexdigest(),'fantasyTeam':fantasy})
    return logIn(correo+password)

def logIn(password):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        keyHash = hashlib.md5(password)
        if row.key['password'] == keyHash.hexdigest():
            return jsonify({'user':row.key})
    return jsonify({'error':'1'})

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
                     
            
