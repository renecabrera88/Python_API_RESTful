'''from pickle import FALSE'''
from asyncio import all_tasks
from pickle import PUT
from flask import Flask
"""importo request"""
from flask import request
"""jsonify sirve para responder en formato json"""
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
    
    """recibido por request y lo asigno a variables. para obtener 
    los datos atributos del json en el request, se debe sacar con corchetes cuadratos"""
    title = request.json['title']
    description = request.json['description']

    """envio las variables a la classe Task"""
    new_task = Task(title,description)
    """agrego la data a la BD"""
    db.session.add(new_task)
    """hago commit para terminar con la operacion"""
    db.session.commit()

    """siempre las funciones deben devolver algo en este caso retorno
    new_task, que es el registro nuesvo creado """
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

"""Esta ruta recibe dentro de la url un id"""
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    """se hace la consulta con el id"""
    task = Task.query.get(id)
    """se duvuelve el resultado de la consulta en json"""
    return task_schema.jsonify(task)
    

"""actualizar registros"""
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)
    

"""borra registro"""
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_taks(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    
    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'name' : 'Welcome to my APIrestul'})




if __name__ == '__main__':
    app.run(debug=True)
    


