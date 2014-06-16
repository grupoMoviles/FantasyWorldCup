import random
import couchdb
import funBase
couch = couchdb.Server('https://app25620887.heroku:guqMR0FiTQqqw5O8cgG27n7U@app25620887.heroku.cloudant.com')
base = couch['fantasydb']

#Agregar Fechas

class Equipo:
    def __init__(self,grupo,nombre):
        self.grupo = grupo
        self.puntos = 0
        self.nombre = nombre

class Jugador:
    def __init__(self,nombre,equipo,posicion,precio,id):
        self.nombre = nombre
        self.equipo = equipo
        self.amarillas = 0
        self.rojas = 0
        self.minutos = 0
        self.goles = 0
        self.asistencias = 0
        self.puntos = 0
        self.posicion = posicion
        self.precio = precio
        self.id = str(id)

listaNombres = ["Brazil","Croatia","Mexico","Cameroon","Spain","Netherlands","Chile","Australia","Colombia","Greece","Ivory Coast","Japan","Uruguay","Costa Rica","England","Italy","Switzerland","Ecuador","France","Honduras","Argentina","Bosnia-Herzegovina","Iran","Nigeria","Germany","Portugal","Ghana","United States","Belgium","Algeria","Russia","South Korea"]
listaEquipos = []
gruposNombres = ["A","B","C","D","E","F","G","H"]
grupos = []
octavos = []

def obtenerPuntosJugadores(jugador,golesEnContra):
    puntos = 2
    puntosGoles = dict(Goalkeeper=6,Defender=6,Midfielder=5,Forward=4)
    puntosGolesContra = dict(Goalkeeper=4,Defender=4,Midfielder=1,Forward=0)
    puntos += jugador.goles*puntosGoles[jugador.posicion]
    puntos += jugador.amarillas*-1
    puntos += jugador.rojas*-3
    puntos += jugador.asistencias*3
    if golesEnContra == 0:
        puntos+= puntosGolesContra[jugador.posicion]
    return puntos

def guardarEstadisticasJugadores(listaJugadores,golesEnContra,numFecha):
    for posicion in listaJugadores[0]:
        for jugador in posicion:
            jugador.minutos = 60
            jugador.puntos = obtenerPuntosJugadores(jugador,golesEnContra)
            funBase.agregarEstadisticasJugador2(jugador.id,jugador.nombre,jugador.equipo,numFecha,jugador.amarillas,jugador.rojas,jugador.asistencias,jugador.goles,jugador.minutos,jugador.puntos,"clave")


def asignarGrupos():
    for i in range(0,32):       
        listaEquipos.append(Equipo(gruposNombres[i//4], listaNombres[i]))        
    
def formarMatrix():
    grupo = []
    for i in range(0,32):
        if i != 0 and i%4==0:
            grupos.append(grupo)
            grupo = []
        grupo.append(listaEquipos[i])
    grupos.append(grupo)

fechas = [[0,1,2,3,],[0,2,1,3],[0,3,2,1]]

def obtenerJugadoresEquipo(equipo):
    print("Empieza obtener jugadores")
    lista = []
    for row in base.view('obtener_jugadores_fun/obtener_jugadores_fun'):
        if row.key['team'] == equipo:
            lista.append(row.key)
    print("Termina obtener jugadores")
    return lista

def traerJugadores(nombre):
    jugadores = obtenerJugadoresEquipo(nombre)
    listaJugadores = []
    for i in range(0,len(jugadores)):
        listaJugadores.append(Jugador(str(jugadores[i]['name']),nombre,str(jugadores[i]['position']),jugadores[i]['price'],jugadores[i]['_id']))
    return listaJugadores

def ordenarPosiciones(listaJugadores):
    alineacion = []
    posiciones = ["Goalkeeper","Defender","Midfielder","Forward"]
    for i in range(0,len(posiciones)):
        posicion = []
        for j in range(0,len(listaJugadores)):
            if listaJugadores[j].posicion == posiciones[i]:
                posicion.append(listaJugadores[j])
        alineacion.append(posicion)
    return alineacion

formaciones = [[4,3,3],[5,4,2],[5,5,1],[3,4,3],[4,5,2]]

def imprimirJugadores(listaJugadores):
    for i in range(0,len(listaJugadores)):
        print(listaJugadores[i].nombre)

def imprimirPosiciones(listaJugadores):
    for i in range(0,len(listaJugadores)):
        print("-----")
        for j in range(0,len(listaJugadores[i])):
            print(listaJugadores[i][j].nombre)

def eliminarEscogido(numero,ruleta):
    respuesta = []
    for i in range(0,len(ruleta)):
        if ruleta[i] !=  numero:
            respuesta.append(ruleta[i])
    return respuesta

def escogerBanca(ruleta,listaJugadores):
    banca = []
    for i in range(0,len(listaJugadores)):
        if i in ruleta:
            banca.append(listaJugadores[i])
    return banca

def escogerTitulares(listaJugadores,cantidad):
    ruleta = []
    for i in range(0,len(listaJugadores)):
        for  j in range(0,listaJugadores[i].precio):
            ruleta.append(i)
    titulares = []
    banca = []
    for i in range(0,cantidad):
        jugador = ruleta[random.randint(0,len(ruleta)-1)]
        titulares.append(listaJugadores[jugador])
        ruleta = eliminarEscogido(jugador,ruleta)
    return [titulares,escogerBanca(ruleta,listaJugadores)]


def imprimirAlineacion(alineacion):
    for i in range(0,len(alineacion)):
        print("++++++")
        for j in range(0,len(alineacion[i])):
            print("----")
            for k in range(0,len(alineacion[i][j])):
                print(alineacion[i][j][k].nombre)

def escogerFormacion(defensas,medios,delanteros):
    formacion = formaciones[random.randint(0,len(formaciones)-1)]
    while formacion[0] > defensas or formacion[1] > medios or formacion[2] > delanteros:
        formacion = formaciones[random.randint(0,len(formaciones)-1)]
    return formacion
                
def crearAlineacion(listaJugadores):
    posicion = []
    formacion = escogerFormacion(len(listaJugadores[1]),len(listaJugadores[2]),len(listaJugadores[3]))
    porteros = escogerTitulares(listaJugadores[0],1)
    alineacion =  [[porteros[0]],[porteros[1]]]
    for i in range(0,len(formacion)):
        linea = escogerTitulares(listaJugadores[i+1],formacion[i])
        alineacion[0].append(linea[0])
        alineacion[1].append(linea[1])
    return alineacion

def tuvoAmarilla():
    return tuvoTarjeta(10)

def tuvoRoja():
    return tuvoTarjeta(1)

def tuvoGol(valor,precio):
    if random.randint(0,100) < valor+precio//3:
        return True
    return False

def tuvoTarjeta(porcentaje):
    if random.randint(0,200) < porcentaje:
        return True
    else:
        return False

def asignarAsistencia(jugador,listaJugadores):
    i = random.randint(0,100)
    posPosicion = random.randint(1,len(listaJugadores[0])-1)
    posJugador = random.randint(0,len(listaJugadores[0][posPosicion])-1)    
    listaJugadores[0][posPosicion][posJugador].asistencias+=1
    return listaJugadores

def calcularEstadisticasEquipo(listaJugadores):
    valoresGoles = dict(Defender=2,Midfielder=4,Forward=5)
    for i in range(1,len(listaJugadores[0])):
            #print("----")
            for k in range(0,len(listaJugadores[0][i])):
                #Aqui se van calculando los puntos
                if tuvoAmarilla():
                    listaJugadores[0][i][k].amarillas+=1
                if tuvoRoja():
                    listaJugadores[0][i][k].rojas+=1
                if tuvoGol(valoresGoles[listaJugadores[0][i][k].posicion],listaJugadores[0][i][k].precio):
                    listaJugadores[0][i][k].goles+=1
                    listaJugadores = asignarAsistencia(listaJugadores[0][i][k],listaJugadores)
                #print("Jugador: " + str(listaJugadores[0][i][k].nombre) + " Amarillas: " + str(listaJugadores[0][i][k].amarillas) + " Rojas: " + str(listaJugadores[0][i][k].rojas) + " Goles: " + str(listaJugadores[0][i][k].goles)) 
                            
    return listaJugadores

def devolverPuntos(jugadores):
    golesEquipo = 0
    for i in range(0,len(jugadores[0])):
            #print("----")
            for k in range(0,len(jugadores[0][i])):
                golesEquipo+=jugadores[0][i][k].goles
    return golesEquipo

def determinarGanador(jugadores1,jugadores2,equipo1,equipo2,numFecha):
    golesEquipo1 = devolverPuntos(jugadores1)
    golesEquipo2 = devolverPuntos(jugadores2)
    posEquipo1 = listaNombres.index(equipo1)
    posEquipo2 = listaNombres.index(equipo2)
    #Guarda Estadisticas Jugador
    print("Empieza guardar estadisticas 1")
    guardarEstadisticasJugadores(jugadores1,golesEquipo2,numFecha)
    print("Termino Guardar estadisticas 1")
    print("Empieza Guardar estadisticas 2")
    guardarEstadisticasJugadores(jugadores2,golesEquipo1,numFecha)
    print("Termino Guardar estadisticas 2")
    print("Empieza a guardar partido")
    print(funBase.agregarPartido(str(numFecha),"Inactivo",equipo1,equipo2,golesEquipo1,golesEquipo2,"clave"))
    print("Termina de guardar partido")
    ##actualizarFechaPartido(team1,team2,score,fecha)
    if golesEquipo1 > golesEquipo2:
        grupos[posEquipo1//4][posEquipo1%4].puntos+=3
        #print("Gano: " + equipo1)
    elif golesEquipo1 < golesEquipo2:
        grupos[posEquipo2//4][posEquipo2%4].puntos+=3
        #print("Gano: " + equipo2)
    else:
        grupos[posEquipo1//4][posEquipo1%4].puntos+=1
        grupos[posEquipo2//4][posEquipo2%4].puntos+=1
        #print("Empate")

def ordenarGrupo(lista):
    for i in range(1, len(lista)):
        j = i
        while j > 0 and lista[j - 1].puntos < lista[j].puntos:
            lista[j - 1], lista[j] = lista[j], lista[j - 1]
            j -= 1
    return lista

#Lista de Jugadores con datos modificados
def simularPartidoGrupos(equipo1,equipo2,numFecha):
    #print(equipo1,equipo2)
    jugadoresEquipo1 = calcularEstadisticasEquipo(crearAlineacion(ordenarPosiciones(traerJugadores(equipo1))))
    jugadoresEquipo2 = calcularEstadisticasEquipo(crearAlineacion(ordenarPosiciones(traerJugadores(equipo2))))
    determinarGanador(jugadoresEquipo1,jugadoresEquipo2,equipo1,equipo2,numFecha)


def jugarFechas(fechaInicio,fechaFin):
    for j in range(fechaInicio,fechaFin):
        for i in range(0,8):
            print("Partido: " + str(i))
            simularPartidoGrupos(grupos[i][fechas[j][0]].nombre,grupos[i][fechas[j][1]].nombre,j)
            simularPartidoGrupos(grupos[i][fechas[j][2]].nombre,grupos[i][fechas[j][3]].nombre,j)
        funBase.actualizarUsuarios(str(j))
        ##actualizarUsuario() -> Buscar jugadores y sumar puntos -> establecer nuevo puntaje
        ##
def faseGrupos(fechaInicio,fechaFin):
    jugarFechas(fechaInicio,fechaFin)
    for i in range(0,len(grupos)):
        grupos[i] = ordenarGrupo(grupos[i])
    imprimirGrupos()

def imprimirGrupos():
    for elem in grupos:
        print("-----")
        for equipo in elem:
            print("Nombre :" + str(equipo.nombre) + " Puntos: " + str(equipo.puntos))
        
def simularGrupos(fechaInicio,fechaFin):
    asignarGrupos()
    formarMatrix()
    faseGrupos(fechaInicio,fechaFin)

#####################################################################
#OCTAVOS DE FINAL
def imprimirOctavos(lista):
    for elem in lista:
        print("Equipo1: " + str(elem[0].nombre) + " Equipo2: " + str(elem[1].nombre))

def asignarOctavos():
    lista = []
    for i in range(0,len(grupos),2):
        lista.append([grupos[i][0],grupos[i+1][1]])        
        lista.append([grupos[i][1],grupos[i+1][0]])
    imprimirOctavos(lista)
    return lista


def ganadorFase(jugadores1,jugadores2,equipo1,equipo2):
    golesEquipo1 = devolverPuntos(jugadores1)
    golesEquipo2 = devolverPuntos(jugadores2)
    ##
    ##guardarPartido(equipo1,equipo2,marc1,marc2,fecha)
    ##guardarJugadores
    if golesEquipo1 > golesEquipo2:
        return 0
    elif golesEquipo1 < golesEquipo2:
        return 1
    else:
        return random.randint(0,1)

def simularPartidoOctavos(equipo1,equipo2):
    #print(equipo1,equipo2)
    jugadoresEquipo1 = calcularEstadisticasEquipo(crearAlineacion(ordenarPosiciones(traerJugadores(equipo1))))
    jugadoresEquipo2 = calcularEstadisticasEquipo(crearAlineacion(ordenarPosiciones(traerJugadores(equipo2))))
    ganador = ganadorFase(jugadoresEquipo1,jugadoresEquipo2,equipo1,equipo2)    
    return ganador

cuartos = []
semis = []
final = []
def simularOctavos(listaVieja,numFecha):
    print("Largo lista",len(listaVieja))
    listaNueva = []
    for i in range(0,len(listaVieja),2):
        ganador1 = simularPartidoOctavos(listaVieja[i][0].nombre,listaVieja[i][1].nombre)
        ganador2 = simularPartidoOctavos(listaVieja[i+1][0].nombre,listaVieja[i+1][1].nombre)
        if ganador1 == 0:
            ganador1 = listaVieja[i][0]
        else :
            ganador1 = listaVieja[i][1]
        if ganador2 == 0:
            ganador2 = listaVieja[i+1][0]
        else:
            ganador2 = listaVieja[i+1][1]
        listaNueva.append([ganador1,ganador2])
    imprimirOctavos(listaNueva)
    return listaNueva
    #return cuartos

def simularMuerteSubita():
    listaVieja = []
    for i in range(0,3):
        print("I",i)
        if i==0:
            listaVieja = asignarOctavos()
            listaVieja = simularOctavos(listaVieja,i+3)
        elif i==1:
            listaVieja = simularOctavos(listaVieja,i+3)
        elif i==2:
            listaVieja=simularOctavos(listaVieja,i+3)
        ###
        ###actualizarUsuario()
        ###
    print("Final",len(listaVieja))
    
    
    

           
        

