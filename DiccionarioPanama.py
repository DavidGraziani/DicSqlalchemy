from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


eng = create_engine('sqlite:///diccionario.db')
Session = sessionmaker(bind=eng)
session = Session()
Base = declarative_base()

class Diccionario(Base):
    __tablename__ = 'Diccionario'

    id = Column(Integer, primary_key=True)
    palabra = Column(String)
    significado = Column(String)

def principal():
    Diccionario()
    menu = """
a) Escribe la palabra panameña
b) Edita la palabra existente
c) Eliminar palabra 
d) Ver la lista de palabras
e) Buscar significado de una palabra
f) Salir
Elige: """
    eleccion = ""
    while eleccion != "f":
        eleccion = input(menu)
        if eleccion == "a":
            palabra = input("Escribe la palabra panameña: ")
            posible_significado = buscar_significado_palabra(palabra)
            if posible_significado:
                print(f"esta palabra '{palabra}' ya esta anotada")
            else:
                significado = input("Ingresa su significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra a sido registrada")
        
        if eleccion == "b":
            palabra = input("Ingresa la palabra que quieres editar: ")
            nuevo_significado = input("Ingresa el nuevo significado: ")
            editar_palabra(palabra, nuevo_significado)
            print("Palabra actualizada")
        
        if eleccion == "c":
            palabra = input("Ingresa la palabra a eliminar: ")
            eliminar_palabra(palabra)
        
        if eleccion == "d":
            palabras = obtener_palabras()
            print("=== Lista de palabras ===")
            for palabra in palabras:
                print(palabra[0])
        
        if eleccion == "e":
            palabra = input(
                "escribe la palabra que quieres saber su significado: ")
            significado = buscar_significado_palabra(palabra)
            if significado:
                print(f"El significado de '{palabra}' es:\n{significado[0]}")
            else:
                print(f"Esta palabra '{palabra}' no esta en el diccionario")


def agregar_palabra(palabra, significado):
    conexion = Diccionario()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO diccionario(palabra, significado) VALUES (?, ?)"
    cursor.execute(sentencia, [palabra, significado])
    conexion.commit()


def editar_palabra(palabra, nuevo_significado):
    conexion = Diccionario()
    cursor = conexion.cursor()
    sentencia = "UPDATE diccionario SET significado = ? WHERE palabra = ?"
    cursor.execute(sentencia, [nuevo_significado, palabra])
    conexion.commit()


def eliminar_palabra(palabra):
    conexion = Diccionario()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM diccionario WHERE palabra = ?"
    cursor.execute(sentencia, [palabra])
    conexion.commit()


def obtener_palabras():
    conexion = Diccionario()
    cursor = conexion.cursor()
    consulta = "SELECT palabra FROM diccionario"
    cursor.execute(consulta)
    return cursor.fetchall()


def buscar_significado_palabra(palabra):
    conexion = Diccionario()
    cursor = conexion.cursor()
    consulta = "SELECT significado FROM diccionario WHERE palabra = ?"
    cursor.execute(consulta, [palabra])
    return cursor.fetchone()


if __name__ == '__main__':
    principal()
