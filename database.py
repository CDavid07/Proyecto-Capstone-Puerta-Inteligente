import mysql.connector as db
from datetime import datetime

#Función que inserta datos de adminitrador nuevo
def registerUser(nom, psw):   

    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql='''INSERT INTO user (idSU,name, password) 
        VALUES(1,'{}', '{}')'''.format(nom, psw)
        cur.execute(sql)
        con.commit()
            
    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()

#Función que inserta datos de nuevo usuario
def insertUser(asig,nom):   
    fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql='''INSERT INTO permiso (idU, name, acceso) 
        VALUES('{}', '{}',1)'''.format(asig,nom )
        cur.execute(sql)
        con.commit()
            
    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        setChanges(asig,fecha,nom,1,0)
        if con.is_connected():
            cur.close()
            con.close()

#Función que se le pasa como parametro el id de adminitrador
#regresa una lista de usuarios que tienen acceso
def getUsers(n):
    
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql = "SELECT * FROM `permiso` WHERE idU = %s"
        cur.execute(sql, (n,))
        datos = cur.fetchall()   
        
    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()

    return datos

#Función que se le pasa como parametro el id de smartgate
#regresa una lista de administradores registrados
def getAdmins(n):
    
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql = "SELECT * FROM `user` WHERE idSU = %s"
        cur.execute(sql, (n,))
        datos = cur.fetchall()   
        
    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()

    return datos

#Función que se le pasa como parametros el id de administrador, fecha en que se realizo
#el nombre a quien se esta agregando y/o eleminando, la opcion de agregar y la opcion de eliminar
#segun sea el caso
def setChanges(id,fecha,name,op,cl):
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql='''INSERT INTO bitacora (idU,fecha, name, agregar,eliminar) 
        VALUES('{}','{}', '{}','{}','{}')'''.format(id,fecha,name,op,cl)
        cur.execute(sql)
        con.commit()
            
    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()

#Función que se le pasa como parametro el id de smartgate
#regresa una lista de los datos registrados sobre los movimientos que realizan los administradores
def getChanges():
    
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql = "SELECT * FROM `bitacora` "
        cur.execute(sql)
        datos = cur.fetchall()   
        
    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()

    return datos

#Función que se le pasa como parametros nombre y contraseña 
#regresa el id y nombre de segun sea el dato haya encontrado ya sea administrador o smartgate
def getUser(nam,passw):
    id= 0
    idSU =0
    name = ""
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        #revisa en la tabla de administradores 
        sql = "SELECT * FROM `user` WHERE name = %s AND password = %s"
        cur.execute(sql, (nam,passw))
        datos = cur.fetchone()

        #si no se encuentra el valor buscado entonces se realiza la busqueda en la tabla de smartgate
        if datos is None:
            sql = "SELECT * FROM `superuser` WHERE name = %s AND password = %s"
            cur.execute(sql, (nam,passw))
            datos = cur.fetchone()
            if datos is None:
                id= 0
                idSU =0
                name = ""
            else:
                id = datos[0]
                name = datos[1]
                idSU= 1
        #en otro caso se refresa los valores de administrador
        else:
            id = datos[0]
            name = datos[2]

    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()

    return {"idSU": idSU, "id": id, "name": name}

#Función que elimina datos de usuario en la base de datos pasando id de usuario que selecciona a eliminar  
def removeUser(idUser,id,nom) :
    fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql="DELETE FROM `permiso` WHERE id = %s"
        
        cur.execute(sql,(id,))
        con.commit()

    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        setChanges(idUser,fecha,nom,0,1)
        if con.is_connected():
            cur.close()
            con.close()

#Función que elimina a administrador de la base de datos pasando id de usuario que selecciona a eliminar  
def removeAdmin(id) :
    try:
        con = db.connect(host="127.0.0.1", user="admin", password="codigoIOT", database="proyectoIOTSM")
        cur = con.cursor()
        sql="DELETE FROM `user` WHERE id = %s"
        
        cur.execute(sql,(id,))
        con.commit()

    except db.Error as e:
        print(f"Error de conexión: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()
