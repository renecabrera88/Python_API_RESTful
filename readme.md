1.- Hacer correr la aplicacion en virtualenv
2.- Crear una BD llamada "revisiontecnica"
3.- colocar la configuracion de la BD en la siguiente linea:
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://usuario:pass@localhost/revisiontecnica'
4.- intalar requirement.txt con siguiiente comando: pip install -r requirements.txt
