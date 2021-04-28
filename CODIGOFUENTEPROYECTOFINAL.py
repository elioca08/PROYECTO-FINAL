#Integrantes del Proyecto:
#Carlos Gonzalez Carranza: 305190688
#Luis Enrique Jimenez: AT456762
#Valeria Diaz: 086253824
#Annie Williams: 4-757-1087
#Elio Camarena: 4-807-1816

from flask import Flask,request, jsonify,Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin

app = Flask(_name_)
app.config['MONGO_URI']='mongodb://localhost/citas'
mongo = PyMongo(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




#Crea una cita

@app.route('/api/citas',methods=['POST'])
@cross_origin()
def Crearcitas():
    #Guarda las citas
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    edad=request.json['edad']
    telefono=request.json['telefono']
    motivo=request.json['motivo']
    descripcion=request.json['descripcion']
    fecha=request.json['fecha']
    hora=request.json['hora']

    #verifica si la fecha que el usuario ingreso ya habia sido registrada
    encontrar_fecha = mongo.db.citas.find_one({'fecha':fecha})
    
    ##Si la fecha habia sido registrada
    if (encontrar_fecha):
        ##verifica si la hora ya habia sido registrada
        encontrar_hora = mongo.db.citas.find_one({'hora':hora})
        
        ## si habia una fecha registrada y una hora en el mismo dia, no permite crear la cita por choque de horas
        if (encontrar_hora):
            response = jsonify( {'message':'La fecha de la cita ya existe'})
            response.status_code = 400
            return response
    
        
        
        ## verifica que todos los datos hayan sido enviadaos
       
    if nombre and apellido and edad and telefono and motivo and descripcion and fecha and hora:
        #lo guarda en la bae de datos
        id = mongo.db.citas.insert(
                
                {
                    'nombre':nombre,
                    'apellido':apellido,
                    'edad':edad,
                    'telefono':telefono,
                    'motivo':motivo,
                    'descripcion':descripcion,
                    'fecha':fecha,
                    'hora':hora,
                }
                
            )
        #se crea una respuesta para la api
        response = {
            'nombre':nombre,
            'apellido':apellido,
            'fecha':fecha,
            'hora':hora
        }
            
        return response
    
    return {'message':'Error'}



# trae todas las citas
@app.route('/api/citas',methods=['GET'])
@cross_origin()
def traer_citas():
    #metodo para traer todas las citas
    citas = mongo.db.citas.find()
    response = json_util.dumps(citas)
    return Response(response,mimetype='application/json')

#Trae una cita por id
@app.route('/api/citas/<id>',methods=['GET'])
@cross_origin()
def traer_una_cita(id):

    #veritifca si la cita existe
    citas =  mongo.db.citas.find_one({'_id':ObjectId(id)})
 
    ## si el metodo anterior viene vacio significa que la cita a no existe asi que retorna un mensaje de error con codigo 400
    if (not citas):
        response = jsonify( {'message':'La cita no exite'})
        response.status_code = 400
        return response
    response = json_util.dumps(citas)
    return Response(response,mimetype="application/json")


#Elimina una cita
@app.route('/api/citas/<id>',methods=['DELETE'])
@cross_origin()
def borrar_una_cita(id):

    #verifica si la cita no  existe igual que en el metodo anterior, si no exite manda un error 400
    cita =  mongo.db.citas.find_one({'_id':ObjectId(id)})
    if (not cita):
        response = jsonify( {'message':'La cita no exite'})
        response.status_code = 400
        return response
    
    #Elimina la cita
    mongo.db.citas.delete_one({'_id':ObjectId(id)})
    return jsonify({'message':'La cita fue eliminada exitosamente'})

#si la ruta no existe manda este error
@app.errorhandler(404)
@cross_origin()
def not_found(error=None):
    response = jsonify( {
        
        'message':'Recurso no encontrado',
        'status':404
    })
    response.status_code = 404
    return response

if _name_ == "_main_":
    app.run(debug=True)
