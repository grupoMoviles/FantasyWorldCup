#Se establece la conexion con la base de datos
import couchdb
couch = couchdb.Server('https://app25620887.heroku:guqMR0FiTQqqw5O8cgG27n7U@app25620887.heroku.cloudant.com')
base = couch['fantasydb']
