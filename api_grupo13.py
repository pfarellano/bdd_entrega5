from flask import Flask, jsonify, abort, request
from pymongo import MongoClient, TEXT
import sys

# Se recomienda descargar el json de requests para postman, 
# e importarlo en postman para probar las funciones.

app = Flask(__name__)
# MONGODATABASE corresponde al nombre de su base de datos
MONGODATABASE = "entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017

# instanciar el cliente de pymongo para realizar consultas a la base de datos
client = MongoClient(MONGOSERVER, MONGOPORT)


# Decorador defiene la ruta. 
@app.route('/')
def hello_world():
    # Funcion retorna una json en base de su request
    # Se recomienda usar jsonify de Flask para manejar la creacion de json
    # Para hacer un print, necesitan hacerlo de la siguiente manera:
    print(123, file=sys.stdout)
    return jsonify({"status": "ok"})


# Decorador para ruta con metodo GET, solo puede recibir requests tipo GET
# También recibe un variable user como int, para poder usarlo en la función
# Ejemplo: GET a "localhost:5000/sender/2" retorna los mensajes mandados por el usuario 2




@app.route('/id_mensaje/<string:string_id>', methods=['GET'])
def id(string_id):
    # Se conecta el cliente de pymongo a la base de datos
    mongodb = client[MONGODATABASE]
    # Se define un "cursor" para la tabla ayudantia de la base de datos
    collection = mongodb.mensajes
    output = []
    for m in collection.find():
        if string_id == str(m['_id']):
            m['_id'] = str(m['_id'])
            output.append(m)
            break
    # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
    # Si la consulta resulta ser vacia, se retorna código HTTP 404,
    # para decir que no se encontró ningún mensaje mandado por el usuario.
    if len(output) == 0:
        return jsonify(), 404
    # Retorna los mensajes
    else:
        return jsonify(output), 200



@app.route('/id_usuario/<int:string_id>', methods=['GET'])
def id_usuario(string_id):
    # Se conecta el cliente de pymongo a la base de datos
    mongodb = client[MONGODATABASE]
    # Se define un "cursor" para la tabla ayudantia de la base de datos
    collection = mongodb.usuarios
    output = []
    print(string_id)
    for m in collection.find({"id_usuario": str(string_id)},{"_id":0}):
            output.append(m)


    # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
    # Si la consulta resulta ser vacia, se retorna código HTTP 404,
    # para decir que no se encontró ningún mensaje mandado por el usuario.
    if len(output) == 0:
        return jsonify(), 404
    # Retorna los mensajes
    else:
        return jsonify(output), 200



@app.route('/dos_usuarios/<string:usuarios>', methods=['GET'])
def dos_usuarios(usuarios):

    # Se conecta el cliente de pymongo a la base de datos
    mongodb = client[MONGODATABASE]
    # Se define un "cursor" para la tabla ayudantia de la base de datos
    collection = mongodb.mensajes

    lista_usuarios=usuarios.split(",")
    usuario1=lista_usuarios[0]
    usuario2=lista_usuarios[1]


    output=[]


    for s in collection.find({ "$and": [{"sender": int(usuario1)}, {"receptant": int(usuario2)}]}, {"_id":0}):
        output.append(s)

    for f in collection.find({"$and": [{"sender": int(usuario2)}, {"receptant": int(usuario1)}]}, {"_id": 0}):
        output.append(f)


        #print(s["receptant"])
        #enviados_por_1.append(s)




    #for m in collection.find({"id_usuario": str(string_id)},{"_id":0}):
           # output.append(m)


    # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
    # Si la consulta resulta ser vacia, se retorna código HTTP 404,
    # para decir que no se encontró ningún mensaje mandado por el usuario.
    if len(output) == 0:
        return jsonify(), 404
    # Retorna los mensajes
    else:
        return jsonify(output), 200


@app.route('/buscar_frases/<string:frases>', methods=['GET'])
def buscar_frases(frases):
    lista = list(frases)
    buscadas = "".join(lista)
    mongodb = client[MONGODATABASE]

    collection = mongodb.mensajes
    collection.create_index([('message', TEXT)], name='search_index')
    output = []

    if "-" in buscadas:
        lista = buscadas.split('-')
        user = int(lista[0])
        buscadas = lista[1]
        buscadas = buscadas.split(';')
        lista = []

        for frase in buscadas:
            frase2 = '\"' + frase + '\"'
            lista.append(frase2)
        # Se conecta el cliente de pymongo a la base de datos
        frases = "".join(lista)

        for s in collection.find({"$and": [{"sender": user}, {"$text": {
            "$search": frases}}]}, {"_id": 0}):
            s['message'] += "                                                                                      " \
                            "                                                                                      " \
                            "                                                 "
            output.append(s['message'])
        # Si la consulta resulta ser vacia, se retorna código HTTP 404,
        # para decir que no se encontró ningún mensaje mandado por el usuario.
    else:
        buscadas = buscadas.split(';')
        lista = []
        for frase in buscadas:
            frase2 = '\"' + frase + '\"'
            lista.append(frase2)
        # Se conecta el cliente de pymongo a la base de datos
        frases = "".join(lista)
        print(frases)

        # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
        for s in collection.find({"$text": {"$search": frases}}, {"_id": 0}):
            s['message'] += "                                                                                      " \
                            "                                                                                      " \
                            "                                                 "
            output.append(s['message'])
    if len(output) == 0:
        return jsonify(), 404
    # Retorna los mensajes
    else:
        return jsonify(output), 200




@app.route('/palabras_deseadas/<string:palabras>', methods=['GET'])
def palabras_deseadas(palabras):
    # Se conecta el cliente de pymongo a la base de datos
    mongodb = client[MONGODATABASE]
    # Se define un "cursor" para la tabla ayudantia de la base de datos
    collection = mongodb.mensajes
    output = []

    if "," in palabras:
        lista = palabras.split(',')
        user = int(lista[0])
        palabras = lista[1]
        lista = list(palabras)
        deseadas = "".join(lista)
        deseadas = deseadas.split(' ')

        # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
        for s in collection.find({"sender": user}, {"_id": 0}):
            incluido = 0
            mensaje = s['message']
            testeo = mensaje.replace(".", "").replace(":", "").replace(
                "!", "").replace("?", "").replace(",", "").split(" ")
            lista_palabras = list(testeo)
            for palabra in lista_palabras:
                if palabra in deseadas:
                    if incluido == 0:
                        s[
                            'message'] += "                                                                                      " \
                                          "                                                                                      " \
                                          "                                                 "
                        output.append(s['message'])
                        incluido = 1

    else:
        lista = list(palabras)
        deseadas = "".join(lista)
        deseadas = deseadas.split(' ')

        # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
        for s in collection.find():
            incluido = 0
            mensaje = s['message']
            testeo = mensaje.replace(".", "").replace(":", "").replace(
                "!", "").replace("?", "").replace(",", "").split(" ")
            lista_palabras = list(testeo)
            for palabra in lista_palabras:
                if palabra in deseadas:
                    if incluido == 0:
                        s['message'] += "                                                                                      " \
                                          "                                                                                      " \
                                          "                                                 "
                        output.append(s['message'])
                        incluido = 1

    # Si la consulta resulta ser vacia, se retorna código HTTP 404,
    # para decir que no se encontró ningún mensaje mandado por el usuario.
    if len(output) == 0:
        return jsonify(), 404
    # Retorna los mensajes
    else:
        return jsonify(output), 200




@app.route('/prohibir_palabras/<string:palabras>', methods=['GET'])
def prohibir_palabras(palabras):
    # Se conecta el cliente de pymongo a la base de datos
    mongodb = client[MONGODATABASE]
    # Se define un "cursor" para la tabla ayudantia de la base de datos
    collection = mongodb.mensajes
    collection.create_index([('message', TEXT)], name='searcher_index')
    output = []
    if "," in palabras:
        lista = palabras.split(',')
        user = int(lista[0])
        palabras = lista[1]
        prohibidas = palabras.split(" ")
        prohibidas2 = prohibidas
        prohibidas = "-" + " -".join(prohibidas)
        for t in collection.find():
            seguro = t['message'].replace(".", "").replace(":", "").replace("!", "").replace("?", "").replace(",", "").split(" ")
            seguro2 = None
            for i in seguro:
                if i not in prohibidas2:
                    seguro2 = i
                    break
            for s in collection.find({"$and": [{"sender": user},
                                               {"$text": {"$search": seguro2 + " " + prohibidas}}]}, {"_id": 0}):
                s['message'] += "                                                                                      " \
                                "                                                                                      " \
                                "                                                 "
                output.append(s['message'])

    else:
        lista = list(palabras)
        prohibidas = "".join(lista)
        prohibidas = prohibidas.split(' ')
        prohibidas2 = prohibidas
        prohibidas = "-" + " -".join(prohibidas)
        for t in collection.find():
            seguro = t['message'].replace(".", "").replace(":", "").replace("!", "").replace("?", "").replace(",", "").split(" ")
            print(seguro)
            print(prohibidas2)
            seguro2 = None
            for i in seguro:
                if i not in prohibidas2:
                    seguro2 = i
                    break
            for s in collection.find({"$text": {"$search": seguro2 + " " + prohibidas}}, {"_id": 0}):
                s['message'] += "                                                                                      " \
                                "                                                                                      " \
                                "                                                 "
                output.append(s['message'])

    if len(output) == 0:
        return jsonify(), 404
    else:
        return jsonify(output), 200



# La función recibe una json con los parametros de la insercion,
# No es necesario agregar variables dentro del URL
@app.route('/add_message/', methods=['POST'])
def add_message():
    mongodb = client[MONGODATABASE]
    collection = mongodb.ayudantia
    # Guarda el json en el variable data
    data = request.get_json()
    # Se inserta un nuevo item a la colección de mongo con los
    #  parámetros definidos en el json
    inserted_message = collection.insert_one({
        'message': data["message"],
        'sender': data["sender"],
        'receptant': data["receptant"],
        'date':data["date"],
    })
    # insert_one retorna None si no pudo insertar
    if inserted_message is None:
        return jsonify(), 404
    # Retorna el id del elemento insertado
    else:
        return jsonify({"id": str(inserted_message.inserted_id)}), 200







@app.route('/remove_message/<string:string_id>', methods=['GET', 'DELETE'])
def remove_message(string_id):
    mongodb = client[MONGODATABASE]
    messages = mongodb.mensajes
    eliminado = 0
    for m in messages.find():
        if string_id == str(m['_id']):
            result = messages.delete_one(m)
            eliminado = 1
            break
    if eliminado == 0:
        return jsonify('No existe un mensaje con ese id'), 404
    else:
        return jsonify("Eliminado"), 200


if __name__ == '__main__':
    # Pueden definir su puerto para correr la aplicación
    app.run(port=5000)
