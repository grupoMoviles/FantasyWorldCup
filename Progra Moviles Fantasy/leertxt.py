import json
import urllib2
import couchdb

couch = couchdb.Server('https://app25620887.heroku:guqMR0FiTQqqw5O8cgG27n7U@app25620887.heroku.cloudant.com')
base = couch['fantasydb']

def rest():
    mat = []
    data = json.load(urllib2.urlopen('http://footballdb.herokuapp.com/api/v1/event/world.2014/teams'))
    for i in range(0,len(data['teams'])):
        elem = data['teams'][i]
        if i == 14:
            elem['title'] = u'Ivory Coast'
        mat+=[[elem['title'].encode("ascii"),elem['code'].encode("ascii")]]
    return mat
        
def leer():
    ar = open('C:\Users\Victor\Desktop\jugadores.txt','r')
    global lista2
    lista2=ar.read()
    lista2=eval(lista2)
    ar.close()
    return lista2

def reemplazarEquipos(lista):
    for row in base.view('obtener_equipos_fun/obtener_equipos_fun'):
        doc = base[row.key['_id']]
        base.delete(doc)
    for elem in lista:
        equipo = dict(name=elem[0],abbreviation=elem[1],type="team")
        base.save(equipo)

def reemplazarJugadores(lista):
    posiciones = [" ","Goalkeeper","Defender","Midfielder","Forward"]
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        doc = base[row.key['_id']]
        base.delete(doc)
    for elem in lista:
        equipo = elem[0]
        print("Equipo",equipo)
        for i in range(1,len(elem)):
            for j in range(0,len(elem[i])):
                datos = elem[i][j]
                jugador = dict(totalPoints=0,stats=[],team=equipo,price=datos[1],type="player",name=datos[0],position=posiciones[i])
                base.save(jugador)

