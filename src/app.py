'''from pickle import FALSE'''
#from asyncio import all_tasks
#from pickle import PUT
from flask import Flask
"""importo request"""
from flask import request
"""jsonify sirve para responder en formato json"""
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

"""============== Config =============================== Config ==============================="""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123@localhost/revisiontecnica'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)


"""============== Modelos =============================== Modelos ==============================="""

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    identificacion = db.Column(db.String(70))
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))


    def __init__(self, identificacion, nombre, apellido):
        self.identificacion = identificacion
        self.nombre = nombre
        self.apellido = apellido

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    marca = db.Column(db.String(20))
    modelo = db.Column(db.String(20))
    patente = db.Column(db.String(10))
    anio = db.Column(db.String(10))
    personaid = db.Column(db.Integer, db.ForeignKey(Persona.id), comment='Dueño del Vehiculo')


    def __init__(self, marca, modelo, patente, anio, personaid):
        self.marca = marca
        self.modelo = modelo
        self.patente = patente
        self.anio = anio
        self.personaid = personaid

class Revision(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    vehiculoid = db.Column(db.Integer, db.ForeignKey(Vehiculo.id), comment='id del vehiculo')
    aprobado = db.Column(db.String(10))
    observaciones = db.Column(db.String(100))
    personaiden = db.Column(db.Integer, db.ForeignKey(Persona.id), comment='Encargado de la Revision')
    fecharevision = db.Column(db.String(10))

    def __init__(self, vehiculoid, aprobado, observaciones, personaiden, fecharevision):
        self.vehiculoid = vehiculoid
        self.aprobado = aprobado
        self.observaciones = observaciones
        self.personaiden = personaiden
        self.fecharevision = fecharevision        

class Tiporevision(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nombretipo = db.Column(db.String(20), unique=True)
    
    def __init__(self, nombretipo):
        self.nombretipo = nombretipo

class Inspeccion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    revisionid = db.Column(db.Integer, db.ForeignKey(Revision.id), comment='Tabla Revision')
    tipoinspeccionid = db.Column(db.Integer, db.ForeignKey(Tiporevision.id), comment='Tipo de revision')
    observaciones = db.Column(db.String(100))
    estado = db.Column(db.String(20))
    personaiden = db.Column(db.Integer, db.ForeignKey(Persona.id), comment='Persona encargada')

    def __init__(self, revisionid, tipoinspeccionid, observaciones, estado, personaiden):
        self.revisionid = revisionid
        self.tipoinspeccionid = tipoinspeccionid
        self.observaciones = observaciones
        self.estado = estado
        self.personaiden = personaiden

db.create_all()

"""============== Schemas =============================== Schemas ==============================="""

class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'identificacion', 'nombre', 'apellido')

persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True)

class VehiculoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'marca', 'modelo', 'patente', 'anio', 'personaid')

vehiculo_schema = VehiculoSchema()
vehiculos_schema = VehiculoSchema(many=True)

class RevisionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'vehiculoid', 'aprobado', 'observaciones', 'personaiden', 'fecharevision')

revision_schema = RevisionSchema()
revisiones_schema = RevisionSchema(many=True)

class TiporevisionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombretipo')

tiporevision_schema = TiporevisionSchema()
tiporevisiones_schema = TiporevisionSchema(many=True)

class InspeccionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'revisionid', 'tipoinspeccionid', 'observaciones', 'estado', 'personaiden')

inspeccion_schema = InspeccionSchema()
inspecciones_schema = InspeccionSchema(many=True)

"""============== Routes =============================== Routes ==============================="""

@app.route('/ingreso_vehiculo', methods=['POST'])
def post_ingreso():
    try:
        ##fields = ('id', 'marca', 'modelo', 'patente', 'anio', 'personaid')
        """recibido atributos del json en el request"""
        marca = request.json['marca']
        modelo = request.json['modelo']
        patente = request.json['patente']
        anio = request.json['anio']
        personaid = request.json['personaid']
        
        """envio las variables a la classe Vehiculo """
        nuevo_vehiculo = Vehiculo(marca, modelo, patente, anio, personaid)
        """agrego la data a la BD"""
        db.session.add(nuevo_vehiculo)
        """hago commit para terminar con la operacion"""
        db.session.commit()
        
        """siempre las funciones deben devolver algo en este caso retorno
        new_task, que es el registro nuesvo creado """
        return vehiculo_schema.jsonify(nuevo_vehiculo)

    except Exception as errorRamdom:
        #imprime el error por consola
        print(errorRamdom)
        #manda mensaje que hubo un error en formato json
        return jsonify({"Mesaage": "Hubo un error inesperado al grabar vehiculo"})

@app.route('/ingreso_persona', methods=['POST'])
def post_persona():
    try:
        #identificacion, nombre, apellido
        identificacion = request.json['identificacion']
        nombre = request.json['nombre']
        apellido = request.json['apellido']
  
        nueva_persona = Persona(identificacion, nombre, apellido)
        db.session.add(nueva_persona)
        db.session.commit()

        return persona_schema.jsonify(nueva_persona)

    except Exception as errorRamdom:
        print(errorRamdom)
        return jsonify({"Mesaage": "Hubo un error inesperado al grabar persona"})

@app.route('/ingreso_revision', methods=['POST'])
def post_revision():
    try:
        #vehiculoid, aprobado, observaciones, personaiden, fecharevision
        vehiculoid = request.json['vehiculoid']
        aprobado = request.json['aprobado']
        observaciones = request.json['observaciones']
        personaiden = request.json['personaiden']
        fecharevision = request.json['fecharevision']
  
        nueva_revision = Revision(vehiculoid, aprobado, observaciones, personaiden, fecharevision)
        db.session.add(nueva_revision)
        db.session.commit()

        return revision_schema.jsonify(nueva_revision)

    except Exception as errorRamdom:
        print(errorRamdom)
        return jsonify({"Mesaage": "Hubo un error inesperado al grabar la revision"})

@app.route('/tipo_revision', methods=['POST'])
def post_tipo_revision():
    try:
        #nombretipo
        nombretipo = request.json['nombretipo']
        tipo_revision = Tiporevision(nombretipo)
        db.session.add(tipo_revision)
        db.session.commit()
        return tiporevision_schema.jsonify(tipo_revision)
    
    except Exception as errorRamdom:
        print(errorRamdom)
        return jsonify({"Mesaage": "Hubo un error inesperado al grabar tipo de revision"})

@app.route('/ingreso_inspeccion', methods=['POST'])
def post_inspeccion():
    try:
        #fields = ('id', 'revisionid', 'tipoinspeccionid', 'observaciones', 'estado', 'personaiden')
        revisionid = request.json['revisionid']
        tipoinspeccionid = request.json['tipoinspeccionid']
        observaciones = request.json['observaciones']
        estado = request.json['estado']
        personaiden = request.json['personaiden']
  
        nueva_inspeccion = Inspeccion(revisionid, tipoinspeccionid, observaciones, estado, personaiden)
        db.session.add(nueva_inspeccion)
        db.session.commit()

        return inspeccion_schema.jsonify(nueva_inspeccion)

    except Exception as errorRamdom:
        print(errorRamdom)
        return jsonify({"Mesaage": "Hubo un error inesperado al grabar la inspeccion"})

@app.route('/borrar_inspeccion/<id>', methods=['DELETE'])
def delete_inspeccion(id):
    try:
        inspeccion = Inspeccion.query.get(id)
        #valida si es true inspeccion, sino 
        if inspeccion:
            db.session.delete(inspeccion)
            db.session.commit()
            return inspeccion_schema.jsonify(inspeccion)

        return jsonify({"messages": "No existe la inspeccion con ese ID"})

    except Exception as errorRamdom:
        print(errorRamdom)
        return jsonify({"Mesaage": "Hubo un error inesperado al borrar la inspeccion"})
 
@app.route('/consulta_revision/<id>', methods=['GET'])
def get_revision(id):
    try:
        """se hace la consulta con el id"""
        revision_por_patente = (db.session.query(Revision)
                                .join(Vehiculo)
                                .filter(Vehiculo.id == id)
                                ).all()
        #valida si la consulta tuvo resultados                        
        if revision_por_patente:
            db.session.commit()
            return revisiones_schema.jsonify(revision_por_patente)

        return jsonify({"messages": "Codigo de vehiculo no existe"})

    except Exception as errorRamdom:
        print(errorRamdom)
        return jsonify({"Mesaage": "Hubo un error inesperado al consultar por las revisiones"})

"""============== Server =============================== Server ==============================="""
if __name__ == '__main__':
    app.run(debug=True)
    


