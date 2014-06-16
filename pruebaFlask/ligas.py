import baseCouch
from flask import jsonify
import hashlib
base = baseCouch.base

def crearLiga(email,password,name):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        keyHash = hashlib.md5(password)
        if row.key['email'] == email and row.key['password'] == keyHash.hexdigest():
            for row in base.view('obtener_ligas/obtener_ligas'):
                if row.key['name'] == name:
                    return jsonify({'error':'1'})
            base.save({'name':name,'owner':email,'users':[email],'type':'league'})
            return jsonify({'success':'0'})
    return jsonify({'error':'1'})

def existeEmail(email):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        if row.key['email'] == email:
            return True
    return False

def agregarUsuarioLiga(password,name,newUser):
    if existeEmail(newUser):
        for row in base.view('obtener_usuarios/obtener_usuarios'):
            keyHash = hashlib.md5(password)
            if row.key['password'] == keyHash.hexdigest():
                for row in base.view('obtener_ligas/obtener_ligas'):
                    if row.key['name'] == name:
                        lista = row.key['users']
                        if newUser in lista:
                            return jsonify({'error':'1'})
                        doc = base[row.key['_id']]
                        lista.append(newUser)
                        doc['users'] = lista
                        base.save(doc)
                        return jsonify({'success':'0'})
                return jsonify({'error':'1'})
        return jsonify({'error':'1'})
    else:
        return jsonify({'error':'1'})

def obtenerLigasUsuario(email,password):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        keyHash = hashlib.md5(password)
        ligas = []
        if row.key['email'] == email and row.key['password'] == keyHash.hexdigest():
            for row in base.view('obtener_ligas/obtener_ligas'):
                lista = row.key['users']
                if email in lista:
                    ligas.append(row.key)
            return jsonify({'liga':ligas})
    return jsonify({'liga':[]})

def obtenerPuntosUsuario(email):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        ligas = []
        if row.key['email'] == email:
                return row.key['fantasyTeam']['totalPoints']
    return 0

def obtenerPaisUsuario(email):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        ligas = []
        if row.key['email'] == email:
                return row.key['country']
    return 0

def obtenerInfoLiga(password,name):
    for row in base.view('obtener_usuarios/obtener_usuarios'):
        keyHash = hashlib.md5(password)
        usuarios = []
        if row.key['password'] == keyHash.hexdigest():
            for row in base.view('obtener_ligas/obtener_ligas'):
                if name == row.key['name']:
                    lista = row.key['users']
                    for elem in lista:
                        usuarios.append(dict(email=elem,totalPoints=obtenerPuntosUsuario(elem),country=obtenerPaisUsuario(elem)))
                    return jsonify({'user':usuarios})
    return jsonify({'user':[]})
    
    
