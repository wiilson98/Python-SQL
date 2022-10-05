import sqlite3 as lite
from contextlib import closing

class database:
    # Constructor -> recibe la ruta al fichero de base de datos SQLite
    def __init__(self, db_file):
        self.con = lite.connect(db_file)
        self.con.row_factory = lite.Row
    # Ejecuta consulta a partir de comando SQL y tupla de valores
    def consultar(self, comando, valores ):
        with closing(self.con.cursor()) as cur:
            cur.execute(comando, valores)
            datos = cur.fetchall()
            return datos
    # Ejecuta actualización a partir de comando SQL y tupla de valores
    # retorna nº de registros modificados
    def actualizar( self, comando, valores):
        with closing(self.con.cursor()) as cur:
            cur.execute(comando, valores)
            return cur.rowcount
    # Confirma las modificaciones ejecutados
    def confirmar(self):
        self.con.commit()
    # Deshace las modificaciones pendientes
    def deshacer(self):
        self.con.rollback()
    # Cierra la conexion con la base de datos
    def cerrar(self):
        self.con.close()

EMPRESA_DB = 'empresa.db'
# Obtiene listado de departamentos
def listar_Departamentos():
    db = None
    try:
        resultados = []
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT COD_DEPTO, DEPARTAMENTO FROM DEPARTAMENTOS''', ())
        for dato in datos:
            resultados.append(departamento(dato['DEPARTAMENTO'],dato['COD_DEPTO']))
        return resultados
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()
            
# Obtiene departamento
def obtenerDepartamento(id):
    db = None
    try:
        resultado = None
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT COD_DEPTO, DEPARTAMENTO FROM DEPARTAMENTOS WHERE COD_DEPTO = ?''', (id,))
        if len(datos) > 0:
            dato = datos[0]
            resultado = departamento(dato['DEPARTAMENTO'], dato['COD_DEPTO'])
        return resultado
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()
            
# Inserta un nuevo departamento
def insertarDepartamento(dep):
    db = None
    try:
        db = database(EMPRESA_DB)
        regs = db.actualizar('''INSERT INTO DEPARTAMENTOS(DEPARTAMENTO) VALUES(?)''', (dep.departamento,))
        db.confirmar()
        return regs
    except Exception as ex:
        db.deshacer()
        raise ex
    finally:
        if db:
            db.cerrar()
        
# Clase departamento
class departamento:
    def __init__( self, _departamento, _id = 0):
        self.id = _id
        self.departamento = _departamento
        
    # Actualiza el departamento
    def actualizar(self):
        db = None
        try:
            db = database(EMPRESA_DB)
            regs = db.actualizar('''UPDATE DEPARTAMENTOS SET DEPARTAMENTO = ? WHERE COD_DEPTO = ?''', (self.departamento, self.id))
            db.confirmar()
            return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()
                
    # Elimina el departamento
    def eliminar(self):
        db = None
        try:
            db = database(EMPRESA_DB)
            regs = db.actualizar('''DELETE FROM DEPARTAMENTOS WHERE COD_DEPTO = ?''', (self.id,))
            db.confirmar()
            return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()
                
    def __str__(self):
        return "COD_DEPTO: {:d} DEPARTAMENTO: {:s}".format(self.id, self.departamento)


# Muestra menu de opciones y solicita opcion
def mostrarMenu():
    while(True):
        try:
            print("")
            print("Menu de opciones: ")
            print("1.- Listar departamentos")
            print("2.- Modificar departamento")
            print("3.- Eliminar departamento")
            print("4.- Insertar departamento")
            print("0.- Salir")
            opcion = int(input("Opcion (1 - 4) ?: "))
            if opcion >= 0 and opcion <= 4:
                print("")
                return opcion
            else:
                print("Opcion no válida")
        except ValueError:
            print("Opcion incorrecta")


# Muestra lista de departamentos
def listarDepartamentos( lista ):
    if len(lista)>0:
        print("Lista de departamentos: ")
        print("{:s}\t\t{:s}".format("ID", "DEPARTAMENTO"))
        for d in lista:
            print(d.id, d.departamento)
    else:
        print("No hay departamentos registrados")
        
# Solicita identificador de departamento
def solicitarIdDepartamento( lista ):
    while(True):
        try:
            listarDepartamentos(lista)
            ide = int(input("Indica ID de departamento: "))
            #if any( d.ide == id for d in lista)
            for dep in lista:
                if dep.id == ide:
                    return dep
            print("Valor no valido")
        except ValueError:
            print("Valor incorrecto")
            
# Solicita nombre para nuevo departamento
def nuevoDepartamento():
    while(True):
        nombre = input("Indica el nombre del nuevo departamento: ")
        if len(nombre) > 0:
            return nombre
        else:
            print("Debes indicar un nombre.")
            
# Modifica nombre de departamento existente
def modificarDepartamento( dep ):
    print("Nombre actual departamento: {:s}".format(dep.departamento))
    while(True):
        nuevo = input("Indica nombre nuevo: ")
        if len(nuevo) > 0:
            dep.departamento = nuevo
            return
        else:
            print("El nuevo nombre no puede ser nulo.")




def main():
    while(True):
        try:
            # Mostrar menu de opciones
            opcion = mostrarMenu()
            # Mostrar lista de departamentos
            if opcion == 1:
                deps = listar_Departamentos()
                listarDepartamentos(deps)
            # Modificar nombre de departamento
            elif opcion == 2:
                deps = listar_Departamentos()
                if len(deps) > 0:
                    dep = solicitarIdDepartamento(deps)
                    modificarDepartamento(dep)
                    if dep.actualizar() == 1:
                        print("Departamento actualizado.")
                else:
                    print("No hay departamentos registrados.")
            # Eliminar un departamento
            elif opcion == 3:
                deps = listar_Departamentos()
                if len(deps) > 0:
                    dep = solicitarIdDepartamento(deps)
                    if dep.eliminar() == 1:
                        print("Departamento eliminado.")
                else:
                    print("No hay departamentos registrados.")
            # Insertar un departamento
            elif opcion == 4:
                nombre = nuevoDepartamento()
                nuevo_departamento = departamento(nombre)
                if insertarDepartamento(nuevo_departamento) == 1:
                    print("Departamento creado.")
            elif opcion == 0:
                print("Fin de programa.")
                break
        except Exception as ex:
            print(ex)
        
if __name__ == "__main__":
    main()
