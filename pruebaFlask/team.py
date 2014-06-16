import baseCouch
from flask import jsonify
base = baseCouch.base

def obtenerEquipos():
    lista = []
    for row in base.view('obtener_equipos_fun/obtener_equipos_fun'):
        lista.append(row.key)
    return jsonify( { 'team': lista })
