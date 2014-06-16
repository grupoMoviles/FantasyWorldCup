
import os
from flask import Flask, jsonify
import couchdb
from flask import request
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import couchConn as conn
import hashlib
import jugadores
import fantasyTeam as ft
import team
import ligas
import admin
import users
app = Flask(__name__)
##########################################################################################
#CROSS DOMAIN
##########################################################################################

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

##########################################################################################
#FIN DEL CROSS DOMAIN
##########################################################################################

#####################################################################################
#CROSS DOMAIN

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']


    return resp
##########################################################################################
##################################METODOS HTTP############################################

#JUGADORES
@app.route('/players', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def get_player():
    return jugadores.obtenerJugadores()

@app.route('/players2', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def get_player2():
    return jugadores.obtenerJugadores2()

@app.route('/playersTeam', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def players_team():
    return jugadores.obtenerJuadoresEquipo(request.args.get('team'))

##########################################################################################
#EQUIPOS

@app.route('/teams', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def get_teams():
    return team.obtenerEquipos()

##########################################################################################
#USUARIOS

#Registra al usuario
@app.route('/registerUser', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def register_user():
    correo = request.form['email']
    password = request.form['password']
    pais = request.form['country']
    return users.registrarUsuario(correo,password,pais)

@app.route('/registerUserFacebook', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def register_userFacebook():
    correo = request.form['email']
    password = request.form['password']
    pais = request.form['country']
    return users.registrarUsuarioFacebook(correo,password,pais)

#Hace el log in
@app.route('/logIn', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def log_In():
    return users.logIn(request.args.get('password'))

##########################################################################################
#FANTASY

#Registra el nombre del equipo del fantast
@app.route('/fantasy/registerName', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def registrar_nombreFantasy():
    name = request.form['name']
    password = request.form['password']
    return ft.registrarNombreFantasy(password,name)

#Registra la cantidad de transferencias
@app.route('/fantasy/transfers', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def obtener_transfersFantasy():
    password = request.form['password']
    return ft.obtenerTransfers(password)

#Guarda la formacion del equipo
@app.route('/fantasy/guardarFormacion', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def guardar_formacion():
    password = request.form['password']
    defenders = request.form['defenders']
    midfielders = request.form['midfielders']
    forwards = request.form['forwards']
    return ft.saveFormation(email,password,[defenders,midfielders,forwards])

#Agrega un jugador al equipo
@app.route('/agregarJugador', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_Jugador():
    email = request.form['email']
    player = request.form['player']
    team = request.form['team']
    active = request.form['active']
    return ft.agregarJugador(email,player,team,active)

#Cambia los titulares
@app.route('/agregarTitulares', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_JugadoresTitulares():
    email = request.form['email']
    players = request.form['player']
    team = request.form['team']
    return ft.agregarJugadoresTitulares(email,players,team)

#Cambia la 
@app.route('/agregarBancas', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_JugadoresBancas():
    email = request.form['email']
    players = request.form['player']
    team = request.form['team']
    return ft.agregarJugadoresBancas(email,players,team)

@app.route('/establecerEquipo', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def establecer_equipo():
    password = request.form['password']
    titulares = request.form['startingPlayers']
    bancas = request.form['benchPlayers']
    equipoTitulares = request.form['startingTeams']
    equipoBancas = request.form['benchTeams']
    return ft.establecerEquipo(password,titulares,equipoTitulares,bancas,equipoBancas)

@app.route('/transferencia', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def establecer_transferencia():
    password = request.form['password']
    player1 = request.form['player1']
    player2 = request.form['player2']
    team1 = request.form['team1']
    team2 = request.form['team2']
    return ft.transferencia(password,player1,team1,player2,team2)

@app.route('/bancaTitular', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def banca_titular():
    email = request.form['email']
    startingPlayer = request.form['startingPlayer']
    benchPlayer = request.form['benchPlayer']
    startingPlayerTeam = request.form['startingPlayerTeam']
    benchPlayerTeam = request.form['benchPlayerTeam']
    return ft.bancaTitular(email,startingPlayer,benchPlayer,startingPlayerTeam,benchPlayerTeam)

@app.route('/establecerCantidadTransferencias', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def establecer_cantidad_transferencias():
    password = request.form['password']
    monto = request.form['amount']
    return ft.establecerCantidadTransferencias(password,int(monto))

@app.route('/cambiarCapitan', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def cambiar_capitan():
    email = request.form['email']
    password = request.form['password']
    captain = request.form['captain']  
    captainTeam = request.form['captainTeam']
    return ft.cambiarCapitan(email,password,captain,captainTeam)

@app.route('/actualizarPuntos', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def actualizar_puntos():
    puntos = request.form['points']
    password = request.form['password']
    return ft.actualizarPuntos(password,puntos)

##########################################################################################
#LIGAS
@app.route('/crearLiga', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def crear_liga():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    return ligas.crearLiga(email,password,name)

@app.route('/agregarUsuarioLiga', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_usuario_liga():
    name = request.form['name']
    password = request.form['password']
    newUser = request.form['newUser']
    return ligas.agregarUsuarioLiga(password,name,newUser)

@app.route('/obtenerLigasUsuario', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def obtener_usuario_ligas():   
    return ligas.obtenerLigasUsuario(request.args.get('email'),request.args.get('password'))

@app.route('/obtenerInfoLiga', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def obtener_info_ligas():   
    return ligas.obtenerInfoLiga(request.args.get('password'),request.args.get('name'))
##########################################################################################
#ADMINISTRADOR
@app.route('/admin/logIn', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def admin_log_In():
    return admin.logIn(request.args.get('username'),request.args.get('password'))

@app.route('/admin/agregarJugador', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_JugadorAdmin():
    name = request.form['name']
    price = request.form['price']
    position = request.form['position']
    team = request.form['team']
    clave = request.form['clave']
    return admin.agregarJugador(name,team,position,price,clave)

@app.route('/admin/borrarJugador', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_JugadorAdmin():
    name = request.form['name']
    team = request.form['team']
    clave = request.form['clave']
    return admin.borrarJugador(name,team,clave)

@app.route('/admin/editarJugador', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def editar_JugadorAdmin():
    name = request.form['name']
    team = request.form['team']
    price = request.form['price']
    position = request.form['position']
    clave = request.form['clave']
    return admin.editarJugador(name,team,position,price,clave)

@app.route('/admin/registrarUsuario', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def registrar_UsuarioAdmin():
    correo = request.form['email']
    password = request.form['password']
    pais = request.form['country']
    clave = request.form['clave']
    return admin.registrarUsuario(correo,password,pais,clave)

@app.route('/admin/obtenerUsuarios', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def obtener_UsuarioAdmin():
    return admin.obtenerUsuarios(request.args.get('clave'))

@app.route('/admin/borrarUsuario', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_UsuarioAdmin():
    email = request.form['email']
    clave = request.form['clave']
    return admin.borrarUsuario(email,clave)

@app.route('/admin/agregarEquipo', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_EquipoAdmin():
    name = request.form['name']
    abreviation = request.form['abreviation']
    clave = request.form['clave']
    return admin.agregarEquipo(name,abreviation,clave)

@app.route('/admin/borrarEquipo', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_EquipoAdmin():
    name = request.form['name']
    clave = request.form['clave']
    return admin.borrarEquipo(name,clave)

@app.route('/admin/borrarFantasy', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_FantasyAdmin():
    name = request.form['name']
    clave = request.form['clave']
    return admin.borrarFantasy(name,clave)

@app.route('/admin/ligas', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def obtener_LigasAdmin():
    return admin.obtenerLigas(request.args.get('clave'))

@app.route('/admin/borrarLiga', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_LigaAdmin():
    name = request.form['name']
    clave = request.form['clave']
    return admin.borrarLiga(name,clave)

@app.route('/admin/agregarFecha', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_FechaAdmin():
    number = request.form['number']
    state = request.form['state']
    clave = request.form['clave']
    return admin.agregarFecha(number,state,clave)

@app.route('/admin/fechas', methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def obtener_FechasAdmin():
    return admin.obtenerFechas(request.args.get('clave'))

@app.route('/admin/editarFecha', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def editar_FechaAdmin():
    number = request.form['number']
    state = request.form['state']
    clave = request.form['clave']
    return admin.editarFecha(number,state,clave)

@app.route('/admin/borrarFecha', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_FechaAdmin():
    number = request.form['number']
    clave = request.form['clave']
    return admin.borrarFecha(number,clave)

@app.route('/admin/agregarPartido', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def agregar_PartidoAdmin():
    numberFixture = request.form['numberFixture']
    state = request.form['state']
    team1 = request.form['team1']
    team2 = request.form['team2']
    score1 = request.form['score1']
    score2 = request.form['score2']
    clave = request.form['clave']
    return admin.agregarPartido(numberFixture,state,team1,team2,score1,score2,clave)

@app.route('/admin/editarPartido', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def editar_PartidoAdmin():
    numberFixture = request.form['numberFixture']
    lastTeam = request.form['lastTeam']
    state = request.form['state']
    team1 = request.form['team1']
    team2 = request.form['team2']
    score1 = request.form['score1']
    score2 = request.form['score2']
    clave = request.form['clave']
    return admin.editarPartido(numberFixture,state,team1,team2,score1,score2,lastTeam,clave)

@app.route('/admin/borrarPartido', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_PartidoAdmin():
    numberFixture = request.form['numberFixture']
    team1 = request.form['team1']   
    clave = request.form['clave']
    return admin.borrarPartido(numberFixture,team1,clave)

@app.route('/admin/editarEstadisticas', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def editar_EstadisticasAdmin():
    fecha = request.form['numberFixture']
    equipo = request.form['team']   
    clave = request.form['clave']
    minutos = request.form['minutesPlayed']
    nombre = request.form['name']
    amarillas = request.form['yellows']
    rojas = request.form['reds']
    asistencias = request.form['assists']
    goles = request.form['goals']
    puntos = request.form['points']
    return admin.editarEstadisticasJugador(nombre,equipo,fecha,amarillas,rojas,asistencias,goles,minutos,puntos,clave)

@app.route('/admin/borrarEstadisticas', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def borrar_EstadisticasAdmin():
    fecha = request.form['numberFixture']
    equipo = request.form['team']   
    clave = request.form['clave']
    nombre = request.form['name']    
    return admin.borrarEstadisticasJugador(nombre,equipo,fecha,clave)

if __name__ == '__main__':
   app.run(debug = True)

