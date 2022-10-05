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

class Empleados:
    def __init__(self, dni, nombre,apellidos, edad, ciudad, email, cod_depto, sueldo):
        self.dni = dni
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = edad
        self.ciudad = ciudad
        self.email = email
        self.cod_depto = cod_depto
        self.sueldo = sueldo
## Recibe una opcion y segun esta cambia el parametro deseado.Retorna el numero de columnas modificadas = 1. 
    def actualizar(self,opcion):
        db = None
        try:
            db = database(EMPRESA_DB)
            if opcion == 1:
                regs = db.actualizar("UPDATE EMPLEADOS SET NOMBRE= ? WHERE DNI = ?",(self.nombre,self.dni))
                db.confirmar()
                return regs
            if opcion == 2:
                regs = db.actualizar("UPDATE EMPLEADOS SET APELLIDOS= ? WHERE DNI = ?",(self.apellidos,self.dni))
                db.confirmar()
                return regs
            if opcion == 3:
                regs = db.actualizar("UPDATE EMPLEADOS SET EDAD= ? WHERE DNI = ?",(self.edad,self.dni))
                db.confirmar()
                return regs
            if opcion == 4:
                regs = db.actualizar("UPDATE EMPLEADOS SET CIUDAD= ? WHERE DNI = ?",(self.ciudad,self.dni))
                db.confirmar()
                return regs
            if opcion == 5:
                regs = db.actualizar("UPDATE EMPLEADOS SET EMAIL= ? WHERE DNI = ?",(self.email,self.dni))
                db.confirmar()
                return regs
            if opcion == 6:
                regs = db.actualizar("UPDATE EMPLEADOS SET SUELDO= ? WHERE DNI = ?",(self.sueldo,self.dni))
                db.confirmar()
                return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()
    def eliminar(self):
        db = None
        try:
            db = database(EMPRESA_DB)
            regs = db.actualizar('''DELETE FROM EMPLEADOS WHERE DNI = ?''', (self.dni,))
            db.confirmar()
            return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()
##  CAMBIA EL CODIGO DE DEPARTAMENTO. Y RETORNA EL NUMERO DE COLUMNAS MODIFICADAS = 1.             
    def trasladar(self):
        db = None
        try:
            db = database(EMPRESA_DB)
            regs = db.actualizar('''UPDATE EMPLEADOS SET COD_DEPTO = ? WHERE DNI = ?''', (self.cod_depto,self.dni))
            db.confirmar()
            return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()
                        
        

    def __str__(self):
        return "DNI: {:s} NOMBRE: {:s} APELLDIOS: {:s} EDAD: {:d} CIUDAD: {:s} EMAIL: {:s} COD_DEPTO: {:d} SUELDO: {:f} ".format(self.dni, self.nombre,self.apellidos,self.edad,self.ciudad,self.email,self.cod_depto,self.sueldo)

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
            print("----------------")
            print("5.- Mostrar todos empleados")
            print("6.- Obtener todos los empleados de un departamento")
            print("7.- Eliminar un empleado")
            print("8.- Insertar un empleado")
            print("9.- Modificar un empleado")
            print("10.- Trasladar de departamento a un empleado")
            print("0.- Salir")
            opcion = int(input("Opcion (0 - 10) ?: "))
            if opcion >= 0 and opcion <= 10:
                print("")
                return opcion
            else:
                print("Opcion no válida")
        except ValueError:
            print("Opcion incorrecta")

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
def obtenerDepartamento(ide):
    db = None
    try:
        resultado = None
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT COD_DEPTO, DEPARTAMENTO FROM DEPARTAMENTOS WHERE COD_DEPTO = ?''', (ide,))
        if len(datos) > 0:
            dato = datos[0]
            resultado = departamento(dato['DEPARTAMENTO'], dato['COD_DEPTO'])
        return resultado
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()
## recibe el codigo del departamento y devuelve el departamento al que pertenece
def obtener_Departamento_Empleado(ide):
    db = None
    try:
        resultado = None
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT COD_DEPTO, DEPARTAMENTO FROM DEPARTAMENTOS WHERE COD_DEPTO = ?''', (ide,))
        if len(datos) > 0:
            dato = datos[0]
            resultado = departamento(dato['DEPARTAMENTO'], dato['COD_DEPTO'])
        return resultado.departamento
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
##Recibe un empleado y lo inserta.        
def insertarEmpleado(emp):
    db = None
    try:
        db = database(EMPRESA_DB)
        regs = db.actualizar("INSERT INTO EMPLEADOS(DNI,NOMBRE,APELLIDOS,EDAD,CIUDAD,EMAIL,COD_DEPTO,SUELDO) VALUES(?,?,?,?,?,?,?,?)",(emp.dni,emp.nombre,emp.apellidos,emp.edad,emp.ciudad,emp.email,emp.cod_depto,emp.sueldo,))
        db.confirmar()
        return regs
    except Exception as ex:
        db.deshacer()
        raise ex
    finally:
        if db:
            db.cerrar()
## retorna una lista con todos los empleados de la empresa.
def listar_Empleados():
    db = None
    try:
        resultados = []
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT DNI,NOMBRE,APELLIDOS,EDAD,CIUDAD,EMAIL,COD_DEPTO,SUELDO FROM EMPLEADOS''', ())
        for dato in datos:
            resultados.append(Empleados(dato['DNI'],dato['NOMBRE'],dato['APELLIDOS'],dato['EDAD'],dato['CIUDAD'],dato['EMAIL'],dato['COD_DEPTO'],dato['SUELDO']))            
        return resultados
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()
## retorna una lista con los DNIS de todos los empleados.
def comprobar_empleado():
    db = None
    try:
        objeto = None
        lista_dnis = []
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT DNI,NOMBRE,APELLIDOS,EDAD,CIUDAD,EMAIL,COD_DEPTO,SUELDO FROM EMPLEADOS''', ())
        for dato in datos:
            objeto = Empleados(dato['DNI'],dato['NOMBRE'],dato['APELLIDOS'],dato['EDAD'],dato['CIUDAD'],dato['EMAIL'],dato['COD_DEPTO'],dato['SUELDO'])
            lista_dnis.append(objeto.dni)
        return lista_dnis    
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()
## recibe un codigo del departamento y retorna una lista con los trabajadores de este departamento.           
def obtener_empleados_departamento(ide):
    db = None
    try:
        resultado = []
        db = database(EMPRESA_DB)
        datos = db.consultar('''SELECT DNI,NOMBRE,APELLIDOS,EDAD,CIUDAD,EMAIL,COD_DEPTO,SUELDO FROM EMPLEADOS WHERE COD_DEPTO = ?''', (ide,))
        for dato in datos:
            resultado.append(Empleados(dato['DNI'],dato['NOMBRE'],dato['APELLIDOS'],dato['EDAD'],dato['CIUDAD'],dato['EMAIL'],dato['COD_DEPTO'],dato['SUELDO']))
        return resultado
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()    
        
# Muestra lista de departamentos.
def listarDepartamentos( lista ):
    if len(lista)>0:
        print("Lista de departamentos: ")
        print("{:s}\t\t{:s}".format("ID", "DEPARTAMENTO"))
        for d in lista:
            print(d.id,"\t\t", d.departamento)
    else:
        print("No hay departamentos registrados")
        
# Solicita identificador de departamento.
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
## Recibe una lista de empleados y mediante el dni devuelve los datos del empleado
def obtener_empleado(lista):
    try:
        dni = input("Indica el dni del empleado: ")
        for emp in lista:
            if emp.dni == dni:
                return emp
        print("Empleado no registrado") 
    except ValueError:
            print("Valor incorrecto")
## Recibe una lista de empleados y la muestra            
def listarEmpleados(lista):
    if len(lista)>0:
        print("Lista de empleados:")
        print("DNI\t  NOMBRE\tAPELLIDOS\tEDAD\tCIUDAD\tEMAIl\tCOD_DEPTO\tSUELDO\tDEPARTAMENTO")
        for emp in lista:
            print(emp.dni, emp.nombre,"\t", emp.apellidos,"\t", emp.edad,"\t", emp.ciudad,"\t", emp.email,"\t", emp.cod_depto,"\t\t", emp.sueldo,"\t", obtener_Departamento_Empleado(emp.cod_depto))
    else:
        print("No hay empleados registrados")
        
## Solicito que parametro se desea cambiar y retorno una opcion
def modificar_empleado(empleado):
    print(empleado)
    print("")
    print("PARAMETROS A CAMBIAR")
    print("1.-NOMBRE")
    print("2.-APELLIDOS")
    print("3.- EDAD")
    print("4.-CIUDAD")
    print("5.- EMAIL")
    print("6.- SUELDO")
    opcion = int(input("Elija una opcion(1-6): "))
    if opcion == 1:
        nombre = input("Introduzca el nuevo nombre: ")
        if len(nombre) > 0:
            empleado.nombre = nombre
            return opcion
        else:
            print("El nuevo nombre no puede ser nulo.")    
    elif opcion == 2:
        apellidos = input("Introduzca los nuevos apellidos: ")
        if len(apellidos) > 0:
            empleado.apellidos = apellidos
            return opcion
        else:
            print("El nuevo apellido no puede ser nulo.")            
    elif opcion == 3:
        edad = int(input("Introduzca la nueva edad: "))
        if edad is not None:
            empleado.edad = edad
            return opcion
        else:
            print("La nueva edad no puede ser nula.")    
    elif opcion == 4:
        ciudad = input("Introduzca la nueva ciduad: ")
        if len(ciudad) > 0:
            empleado.ciudad = ciudad
            return opcion
        else:
            print("La nueva ciudad no puede ser nula.")    
    elif opcion == 5:
        email = input("Introduzca el nuevmo email: ")
        empleado.email = email
        return opcion
         
    elif opcion == 6:    
        sueldo = float(input("Introduzca el nuevo sueldo: "))
        if sueldo > 0:
            empleado.sueldo = sueldo
            return opcion
        else:
            print("El nuevo sueldo no puede ser nulo.")            
    else:
        print("Valor no váildo.")

## Obtengo la lista de departamentos y saco los ID en una lista. Solicito el dni mediante otra funcion, obtengo el empleado(objeto), muestro su departamento. Muestro la lista de departamentos con los ID y solicito...
## que indique el nuevo departamento, comprobando que se elija un codigo de departamento existente y que no sea al que ya pertenece.
def trasladar_empleado():
    lista_id = []
    lista_empleados = listar_Empleados()
    empleado = obtener_empleado(lista_empleados)
    if empleado is not None:
        print("")
        deps = listar_Departamentos()
        listarDepartamentos(deps)
        print("")
        print(f"Departamento al que pertenece: {obtener_Departamento_Empleado(empleado.cod_depto)}")    
        print("")
        opcion = int(input("A que departamento(ID)desea trasladar el empleado: "))
        for departamento in deps:
            lista_id.append(departamento.id)
        if opcion in lista_id:
            for departamento in deps:
                if departamento.id == opcion :
                    print("Error. Este empleado ya pertenece a este departamento.")
                    empleado = None
                    return empleado
                else:
                    empleado.cod_depto = opcion
                    return empleado
        else:
            print("El departamento que ha escogido no existe.")
    
## Creo el empleado y compruevo si este no se encuentra ya registrado mediante el dni.   
def nuevoEmpleado():
    try:
        dni = input("Introudzca el DNI (9 digitos): ")
        while len(dni) != 9:
            print("Error dni vacio o sin 9 digitos.")
            dni = input("Introudzca el DNI (9 digitos): ")
        lista_dnis = comprobar_empleado()
        if dni not in lista_dnis:
            nombre = input("Introduzca el nombre: ")
            while len(nombre)==0:
                print("El campo no puede etsra vacío.")
                nombre = input("Introduzca el nombre: ")
            apellidos = input("Introduzca los apellidos: ")
            while len(apellidos)==0:
                print("El campo no puede etsra vacío.")
                apellidos = input("Introduzca los apellidos: ")
            edad = int(input("Introduzca la edad: "))
            while edad <=0 :
                print("La edad tiene que ser un numéro y no puede ser negativa.")
                edad = int(input("Introduzca la edad: "))
            ciudad = input("Introduzca la ciudad: ")
            while len(ciudad)==0:
                print("El campo no puede estar vacío.")
                ciudad = input("Introduzca la ciudad: ")
            email = input("Introduzca el email: ")
            deps = listar_Departamentos()
            listarDepartamentos(deps)
            cod_depto = int(input("Introduzca el ID del departamento: "))
            while cod_depto<=0:
                print("El campo no puede estar vacío.")
                cod_depto = int(input("Introduzca el ID del departamento: "))
                
            sueldo = float(input("Introduzca el sueldo: "))
            while sueldo<=0 :
                print("El campo no puede estar vacío.")
                sueldo = float(input("Introduzca el sueldo: "))    
            nuevo_empleado = Empleados(dni,nombre,apellidos,edad,ciudad,email,cod_depto,sueldo)
            return nuevo_empleado          
        else:        
            print("Error. Empleado ya registrado.")
    except Exception as ex:
        raise ex
        
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
            ## Muestro todos los empleados        
            elif opcion == 5:
                lista_empleados = listar_Empleados()
                listarEmpleados(lista_empleados)
            ## Muestro los empleados de un departamento    
            elif opcion ==6:
                deps = listar_Departamentos()
                listarDepartamentos(deps)
                ide = int(input("Introduzca el id del departamento: "))
                lista = obtener_empleados_departamento(ide)
                listarEmpleados(lista)
            ## Elimino un empleado
            elif opcion == 7:
                lista_empleados = listar_Empleados()
                if len(lista_empleados) > 0:
                    empleado = obtener_empleado(lista_empleados)
                    if empleado is not None:
                        if empleado.eliminar() == 1:
                            print("Empleado eliminado")
                else:
                    print("No hay empleados registrados.")                
            ## Inserto un empleado    
            elif opcion == 8:
                empleado = nuevoEmpleado()
                if insertarEmpleado(empleado) == 1:
                    print("Empleado añadido.")
            ## Modifico un empleado
            elif opcion == 9:
                lista_empleados = listar_Empleados()
                empleado = obtener_empleado(lista_empleados)
                if empleado is not None:
                    opcion = modificar_empleado(empleado)
                    if empleado.actualizar(opcion) == 1:
                        print("Empleado actualizado.")
            ## Traslado un empleado            
            elif opcion == 10:                
                empleado = trasladar_empleado()
                if empleado is not None:
                    if empleado.trasladar() == 1:
                        print("Empleado trasladado correctamente.")
            
            elif opcion == 0:
                print("Fin de programa.")
                break
        except Exception as ex:
            print(ex)
        
if __name__ == "__main__":
    main()
