import sqlite3
from typing import Optional
import random
from fastapi import FastAPI
import secrets

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
#conexion = sqlite3.connect("Registro")
#cursor = conexion.cursor()
#into = "DROP table secretos"
#into = "delete from usuarios where nombre = 'marcos'"
#into="create table usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre varchar(30) not null, correo varchar(30) not null, clave varchar(20) not null, token varchar(25) null);"
#into = "create table secretos(id INTEGER PRIMARY KEY AUTOINCREMENT, titulo varchar(30) not null, descripcion varchar(200) not null, valor varchar(20) not null, fecha varchar(20) not null, lugar varchar(100) not null, LatLng varchar(50) not null, token varchar(50) not null, correo varchar(30) null);"
#cursor.execute(into)
#conexion.commit()

@app.get("/api/registrar/{nombre}/{corre}/{clav}")
def Registro(nombre: str, corre: str, clav: str):
    try:
        correo=""
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        cursor.execute("SELECT correo FROM usuarios WHERE correo = '"+corre+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            correo = i[0]
        if correo == corre:
            return "EL usuario ya existe"
            
        else:
            conexion = sqlite3.connect("Registro")
            cursor = conexion.cursor()
            into = "INSERT INTO usuarios ('nombre','correo','clave', 'token') VALUES('"+nombre+"','"+corre+"','"+clav+"', '000000');"
            cursor.execute(into)
            conexion.commit()
            return {"Registro":"Los datos fuero registrados exitosamente"}
            
    except:
        return "No se pudieron registrar los datos"

@app.get("/api/regSecretos/{titulo}/{descripcion}/{valor}/{fecha}/{lugar}/{LatLng}/{keton}/{correo}")
def regSecretos(titulo: str, descripcion: str, valor: str, fecha: str, lugar: str, LatLng: str, keton:str, correo:str):
    try:
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        into = "INSERT INTO secretos ('titulo','descripcion','valor', 'fecha','lugar','LatLng', 'token','correo') VALUES('"+titulo+"','"+descripcion+"','"+valor+"','"+fecha+"','"+lugar+"','"+LatLng+"', '"+keton+"','"+correo+"');"
        cursor.execute(into)
        conexion.commit()
        return {"respuesta":"Los datos fueros registrados exitosamente"}
        conexion.close()
    except:
        return {"respuesta":"No se pudieron registrar los datos"}

@app.get("/api/iniciar/{corre}/{clav}")
def inicio(corre: str, clav: str):
    try:
        correo = ""
        clave = ""
        titulo = ""
        descripcion = ""
        fecha=""
        LatLng =""
        valor =""
        lugar=""
        toke = secrets.token_hex(20);
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        carga = "UPDATE secretos SET token ='"+str(toke)+"' WHERE correo = '"+corre+"'"
        cursor.execute(carga)
        token = "UPDATE usuarios SET token ='"+str(toke)+"' WHERE correo = '"+corre+"' and clave = '"+clav+"'"
        cursor.execute(token)
        conexion.commit()
        cursor.execute("SELECT id, correo, clave, nombre, token FROM usuarios WHERE correo = '"+corre+"' and clave = '"+clav+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            correo = i[1]
            clave = i[2]
            nombre = i[3]
            tok = i[4]
        if corre == correo and clav == clave:
            conexio = sqlite3.connect("Registro")
            curso = conexio.cursor()
            curso.execute("SELECT titulo,descripcion,valor, fecha,lugar,LatLng FROM secretos WHERE token = '"+tok+"'")
            contenid = curso.fetchall()
            conexio.commit()
            for s in contenid:
                titulo = s[0]
                descripcion = s[1]
                valor = s[2]
                fecha = s[3]
                lugar = s[4]
                LatLng = s[5]
                mensaje = { "iniciadoSesion": nombre ,"Titulo": titulo, "Descripcion": descripcion, "key":tok, "correo":correo, "ValorMonetario": valor, "Fecha": fecha, "Lugar": lugar, "LongitudYLatitud": LatLng}
            inici = {"key":tok, "correo": correo, "iniciadoSesion":nombre,"Titulo":titulo}
            if titulo == "" or descripcion =="" or LatLng == "":
                return inici
            else:
                return mensaje
        else:
            return "Las credenciales son incorrectas"
    except TypeError:
        return "No se pudieron estraer los datos"

@app.get("/api/modificar/{nombre}/{correo}/{token}")
def modificar(nombre: str, correo: str, token: str):
    try:
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        update = "UPDATE usuarios SET nombre = '"+nombre+"', correo = '"+correo+"' WHERE token = '"+token+"'"
        cursor.execute(update)
        conexion.commit()
        return {"respuesta":"Se modificaron los datos"}
    except TypeError:
        return {"respuesta":"No se pudieron modificar los datos"}

@app.get("/api/ModClave/{clave_old}/{token}/{nuw_clave}")
def modClave(new_clave: str, clave_old: str, token: str):
    try:
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        updat = "UPDATE usuarios SET clave ='"+new_clave+"' WHERE clave = '"+clave_old+"' and token ='"+token+"'"
        cursor.execute(updat)
        conexion.commit()
        return {"respuesta":"Se modificaron los datos"}
    except TypeError:
        return {"respuesta":"No se pudieron modificar los datos"}

@app.get("/api/Eliminar/{eliminar}")
def eliminar(eliminar: str):
    try:
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        delete = "delete from secretos where token = '"+eliminar+"'"
        cursor.execute(delete)
        conexion.commit()
        return {"respuesta":"Se eliminaron los datos"}
        conexion.close()
    except TypeError:
        return {"respuesta":"No se pudieron eliminar los datos"}

@app.get("/api/salir/{salir}")
def salir(salir: str):
    try:
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        ex = "UPDATE usuarios SET token = 'null' WHERE token ='"+salir+"'"
        cursor.execute(ex)
        conexion.commit()
        conexion.close()
        return "Has salido del sistema"
    except TypeError:
        return "No se a podido cerrar la sesion"




@app.get("/api/NotRemmenver/{remenber}")
def NotRemmenver(remenber: str):
    try:
        conexion = sqlite3.connect("Registro")
        cursor = conexion.cursor()
        cursor.execute("select clave from usuarios WHERE correo ='"+remenber+"'")
        re = cursor.fetchall()
        conexion.commit()
        for d in re:
            con = d[0]
        return {"pass": "Tu contraseña es: " +con+""}
    except TypeError:
        return "Error"