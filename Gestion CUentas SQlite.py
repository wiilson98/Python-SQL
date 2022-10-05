import sqlite3 as lite
from contextlib import closing

class CuentaDesconocidaError(Exception):
    pass
class ClienteDesconocidoError(Exception):
    pass
class CuentaDuplicadaError(Exception):
    pass
class ClienteDuplicadoError(Exception):
    pass
class saldoError(Exception):
    pass
class interesError(Exception):
    pass
class saldoInsuficienteError(Exception):
    pass
class bonificacionError(Exception):
    pass

BANCO_DB = "banco.db"
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
        
##funcion independiente que retorna una la lista de dnis 
def lista_dnis():
    db = None
    try:
        objeto = None
        lista = []
        db = database(BANCO_DB)
        datos = db.consultar("SELECT DNI,NOMBRE,DIRECCION,TELEFONO,EMAIL FROM CLIENTES", ())
        for dato in datos:
            objeto = Cliente(dato['DNI'],dato['NOMBRE'],dato['DIRECCION'],dato['TELEFONO'],dato['EMAIL'])
            lista.append(objeto.dni)
        return lista    
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()
##funcion independiente que retorna una la lista de n_cuentas
def lista_n_cuentas():
    db = None
    try:
        objeto = None
        lista = []
        db = database(BANCO_DB)
        datos = db.consultar("SELECT N_CUENTA,SALDO,INTERESES,BONIFICACION,DNI_CLIENTE FROM CUENTAS", ())
        for dato in datos:
            objeto = Cuenta(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['DNI_CLIENTE'])
            lista.append(objeto.ncuenta)
        return lista    
    except Exception as ex:
        raise ex
    finally:
        if db:
            db.cerrar()

class Cliente:
    def __init__(self, dni: str, nombre: str, direccion: str, telefono: str, email: str):
        self.dni = dni
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
                
    def eliminar(self):
        db = None
        try:
            db = database(BANCO_DB)
            regs = db.actualizar('''DELETE FROM CLIENTES WHERE DNI = ?''', (self.dni,))
            db.confirmar()
            return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()    

    def __str__(self):
        return f'DNI: {self.dni} NOMBRE: {self.nombre} ADRESS: {self.direccion} EMAIL: {self.email})'

class Cuenta:
    def __init__(self, ncuenta: int, saldo: float, interes: float, dni_cliente:str):
        self.ncuenta = ncuenta
        self.saldo = saldo
        self.interes = interes
        self.dni_cliente = dni_cliente
        
    def actualizar(self):
        db = None
        try:
            db = database(BANCO_DB)
            regs = db.actualizar('''UPDATE CUENTAS SET SALDO = ? WHERE N_CUENTA = ?''', (self.saldo, self.ncuenta))
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
            db = database(BANCO_DB)
            regs = db.actualizar('''DELETE FROM CUENTAS WHERE N_CUENTA = ?''', (self.ncuenta,))
            db.confirmar()
            return regs
        except Exception as ex:
            db.deshacer()
            raise ex
        finally:
            if db:
                db.cerrar()   

    def __str__(self):
        return f'Cuenta: {self.ncuenta} Saldo: {self.saldo} Interes: {self.interes}'


class CuentaBonificada(Cuenta):
    def __init__(self, ncuenta: int, saldo: float, interes: float, bonificacion: float, dni_cliente: str):
        Cuenta.__init__(self, ncuenta, saldo, interes, dni_cliente)
        self.bonificacion = bonificacion

    def __str__(self):
        return f'{Cuenta.__str__(self)} Bonificacion: {self.bonificacion}'

class Gestion:
##  
    def __init__(self):
        self.__clientes =  lista_dnis()                          
        self.__cuentas = lista_n_cuentas()    

    def altaCliente(self, cliente: Cliente) -> None:
        if cliente.dni not in self.__clientes:
            db = None
            try:
                db = database(BANCO_DB)
                regs = db.actualizar("INSERT INTO CLIENTES(DNI,NOMBRE,DIRECCION,TELEFONO,EMAIL) VALUES(?,?,?,?,?)",(cliente.dni,cliente.nombre,cliente.direccion,cliente.telefono,cliente.email))
                db.confirmar()
                return regs
            except Exception as ex:
                db.deshacer()
                raise ex
            finally:
                if db:
                    db.cerrar()      
        else:
            raise ClienteDuplicadoError()

    def bajaCliente(self, dni: str) -> None:
        if dni in self.__clientes:
            cliente = self.obtenerCliente(dni)
            cliente.eliminar()
        else:
            raise ClienteDesconocidoError()
        
    def ver_cliente(self, dni:str)->Cliente:
        if dni in self.__clientes:
            cliente = self.obtenerCliente(dni)
            return cliente
        else:
            raise ClienteDesconocidoError()
        
    def obtenerCliente(self, dni: str) -> Cliente:     
        if dni in self.__clientes:
            db = None
            try:
                resultado = None
                db = database(BANCO_DB)
                datos = db.consultar('''SELECT DNI,NOMBRE,DIRECCION,TELEFONO,EMAIL FROM CLIENTES WHERE DNI = ?''', (dni,))
                dato = datos[0]
                cliente = Cliente(dato['DNI'],dato['NOMBRE'],dato['DIRECCION'],dato['TELEFONO'],dato['EMAIL'])
                return cliente
            except Exception as ex:
                raise ex
            finally:
                if db:
                    db.cerrar()
        else:
            raise ClienteDesconocidoError() 

    def listarClientes(self)->list:
        db = None
        try:
            lista_clientes = []
            db = database(BANCO_DB)
            datos = db.consultar("SELECT DNI,NOMBRE,DIRECCION,TELEFONO,EMAIL FROM CLIENTES", ())
            for dato in datos:
                lista_clientes.append(Cliente(dato['DNI'],dato['NOMBRE'],dato['DIRECCION'],dato['TELEFONO'],dato['EMAIL']))            
            return lista_clientes
        except Exception as ex:
            raise ex
        finally:
            if db:
                db.cerrar()

    def altaCuenta(self, cuenta: Cuenta, opcion:int):
        if cuenta.ncuenta not in self.__cuentas:
            if opcion == 1:
                db = None
                try:
                    db = database(BANCO_DB)
                    regs = db.actualizar("INSERT INTO CUENTAS(N_CUENTA,SALDO,INTERESES,DNI_CLIENTE) VALUES(?,?,?,?)",(cuenta.ncuenta,cuenta.saldo,cuenta.interes,cuenta.dni_cliente))
                    db.confirmar()
                    return regs
                except Exception as ex:
                    db.deshacer()
                    raise ex
                finally:
                    if db:
                        db.cerrar()
            elif opcion == 2:
                db = None
                try:
                    db = database(BANCO_DB)
                    regs = db.actualizar("INSERT INTO CUENTAS(N_CUENTA,SALDO,INTERESES,BONIFICACION,DNI_CLIENTE) VALUES(?,?,?,?,?)",(cuenta.ncuenta,cuenta.saldo,cuenta.interes,cuenta.bonificacion,cuenta.dni_cliente))
                    db.confirmar()
                    return regs
                except Exception as ex:
                    db.deshacer()
                    raise ex
                finally:
                    if db:
                        db.cerrar()                
        else:
            raise CuentaDuplicadaError()

    def bajaCuenta(self, ncuenta: int) -> None:
        if ncuenta in self.__cuentas:
            cuenta = self.obtenerCuenta(ncuenta)
            cuenta.eliminar()
        else:
            raise CuentaDesconocidaError()

    def obtenerCuenta(self, ncuenta: int) -> Cuenta:    # Se retorna el objeto Cuenta con el NCUENTA indicado
        if ncuenta in self.__cuentas:
            db = None
            try:
                cuenta = None
                db = database(BANCO_DB)
                datos = db.consultar("SELECT N_CUENTA,SALDO,INTERESES,BONIFICACION,DNI_CLIENTE FROM CUENTAS WHERE N_CUENTA = ?", (ncuenta,))
                dato = datos[0]
                if dato[3] is not None:
                    return CuentaBonificada(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['BONIFICACION'],dato['DNI_CLIENTE'])
                else:
                    return Cuenta(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['DNI_CLIENTE'])
            except Exception as ex:
                raise ex
            finally:
                if db:
                    db.cerrar()              
        else:
            raise CuentaDesconocidaError()

    def listarCuentasCliente(self, dni: str) -> list:
        if dni in self.__clientes:                      
            lista_cuentas = []
            db = database(BANCO_DB)
            datos = db.consultar("SELECT N_CUENTA,SALDO,INTERESES,BONIFICACION,DNI_CLIENTE FROM CUENTAS WHERE DNI_CLIENTE = ?", (dni,))
            for dato in datos:
                if dato[3] is not None:
                    lista_cuentas.append(CuentaBonificada(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['BONIFICACION'],dato['DNI_CLIENTE']))
                else:
                    lista_cuentas.append(Cuenta(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['DNI_CLIENTE']))
            return lista_cuentas   
        else:
            raise ClienteDesconocidoError()

    def saldoCuentasCliente(self, dni: str) -> float:    # Retorno decimal como el saldo
        if dni in self.__clientes:
            # Obtencion de las cuentas del cliente
            cuentas_cliente = self.listarCuentasCliente(dni)
            # Retorno del sumatorio del saldo de las cuentas obtenidas
            return sum( map(lambda cuenta: cuenta.saldo, cuentas_cliente))
        else:
            raise ClienteDesconocidoError()

    def cuentas_bonificadas(self, dni: str)->list:
        if dni in self.__clientes:                      
            lista_cuentas = []
            db = database(BANCO_DB)
            datos = db.consultar("SELECT N_CUENTA,SALDO,INTERESES,BONIFICACION,DNI_CLIENTE FROM CUENTAS WHERE DNI_CLIENTE = ?", (dni,))
            for dato in datos:
                if dato[3] is not None:
                    lista_cuentas.append(CuentaBonificada(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['BONIFICACION'],dato['DNI_CLIENTE']))
            return lista_cuentas   
        else:
            raise ClienteDesconocidoError()

    def cuentas_normales(self, dni: str)->list:
        if dni in self.__clientes:                      
            lista_cuentas = []
            db = database(BANCO_DB)
            datos = db.consultar("SELECT N_CUENTA,SALDO,INTERESES,BONIFICACION,DNI_CLIENTE FROM CUENTAS WHERE DNI_CLIENTE = ?", (dni,))
            for dato in datos:
                if dato[3] is None:
                    lista_cuentas.append(Cuenta(dato['N_CUENTA'],dato['SALDO'],dato['INTERESES'],dato['DNI_CLIENTE']))
            return lista_cuentas   
        else:
            raise ClienteDesconocidoError()

    def ingreso(self,valor:float, ncuenta:int)->None:
        if ncuenta in self.__cuentas:
            if valor > 0:
                cuenta = self.obtenerCuenta(ncuenta)
                cuenta.saldo += valor
                cuenta.actualizar()
            else:
                raise saldoError()
        else:
            raise CuentaDesconocidaError()

    def retirar(self,valor:float, ncuenta:int)->None:
        if ncuenta in self.__cuentas:
            if valor > 0:
                cuenta = self.obtenerCuenta(ncuenta)
                if cuenta.saldo < valor:
                    raise saldoInsuficienteError()
                else:
                    cuenta.actualizar()
            else:
                raise saldoError()
        else:
            raise CuentaDesconocidaError()        

def menu():
    while True:
        print("OPCIONES")
        print("1.- ALTA CLIENTE")
        print("2.- BAJA CLIENTE")
        print("3.- VER CLIENTE")
        print("4.- LISTA DE CLIENTES")
        print("5.- ALTA DE CUENTA")
        print("6.- BAJA DE CUENTA")
        print("7.- OBTENER CUENTA")
        print("8.- LISTA CUENTAS CLIENTES")
        print("9.- SALDO CUENTAS CLIENTE")
        print("10.- CATEGORIAS DE LAS CUENTAS")
        print("11.- INGRESAR A UNA CUENTA")
        print("12.- RETIRAR DE UNA CUENTA")
        print("0.- SALIR")
        try:
            opcion = int(input("Indica una opcion: "))
            if 0 <= opcion <= 12:                                       
                return opcion
            else:
                print("Opcion incorrecta.")
        except ValueError:
            print("Valor no valido.")

def main():
    gestor = Gestion()
    while True:
        try:
            opcion = menu()

            if opcion == 1:
                print("ALTA DE CLIENTE\n")
                dni = input("Introduzca el dni: ")
                nombre = input("Introduzca el nombre: ")
                direccion = input("Introduzca la direccion : ")
                telefono = input("Introduzca el telefono: ")
                email = input("Introduzca el email: ")
                cliente = Cliente(dni, nombre, direccion, telefono, email)
                gestor.altaCliente(cliente)
                print("Cliente registrado correctamente.\n")

            elif opcion == 2:
                print("BAJA DE CLIENTE\n")
                dni = input("Introduzca el dni: ")
                gestor.bajaCliente(dni)
                print("Cliente dado de baja correctamente.\n")

            elif opcion == 3:
                print("OBTENER DATOS DE UN CLIENTE\n")
                dni = input("Introduzca el dni: ")
                cliente = gestor.ver_cliente(dni)
                print(cliente)
                print("Fin datos cliente.\n")

            elif opcion == 4:
                print("LISTA DE CLIENTES\n")
                clientes=gestor.listarClientes()
                for cliente in clientes:
                    print(cliente)
##                print(list(map(str, clientes)))
                print("Fin lista clientes.\n")

            elif opcion == 5:
                print("ALTA DE CUENTA\n")
                dni = input("Introduzca el dni: ")
                ncuenta = int(input("Introduzca el número de cuenta: "))
                saldo = float(input("Introduzca el saldo: "))
                if saldo < 0:
                    raise saldoError()
                interes = float(input("Introduzca el interés: "))
                if interes < 0.05 or interes > 5.0:
                    raise interesError()
                pregunta = input("Desea que le cuenta sea bonificada?(s/n): ").lower()
                if pregunta == "n":
                    opc = 1
                    cuenta = Cuenta(ncuenta, saldo, interes,dni)
                else:
                    opc = 2
                    bonificacion = float(input("Introduzca la bonifiacion: "))
                    if bonificacion < 10 or bonificacion > 100:
                        raise bonificacionError()
                    cuenta = CuentaBonificada(ncuenta,saldo, interes, bonificacion,dni)
                gestor.altaCuenta(cuenta,opc)       
                print("Cuenta con cliente regitrada correctamente.\n")

            elif opcion == 6:
                print("BAJA DE CUENTA\n")
                ncuenta = int(input("Introduzca el número de cuenta: "))
                gestor.bajaCuenta(ncuenta)
                print("Cuenta dada de baja correctamente.\n")

            elif opcion == 7:
                print("OBTENER DATOS DE UNA CUENTA")
                ncuenta = int(input("Introduzca el nùmero de cuenta: "))
                cuenta = gestor.obtenerCuenta(ncuenta)
                print(cuenta)
                print("Fin datos cuenta.")

            elif opcion == 8:
                print("LISTA DE CUENTAS DE CLIENTE")
                dni = input("Introduzca el dni: ")
                cuentas = gestor.listarCuentasCliente(dni)
                for cuenta in cuentas:
                    print(cuenta)
##                print(list(map(str, cuentas)))
                print("Fin cuentas cliente.")

            elif opcion == 9:
                print("SUMA SALDOS CLIENTE.")
                dni = input("Introudzca el dni: ")
                suma_saldos = gestor.saldoCuentasCliente(dni)
                print(f"La suma de saldos de las cuentas con el numero de dni {dni} es de: {suma_saldos} $.")
                
            elif opcion == 10:
                print("CATEGORIAS.")
                dni = input("Introudzca el dni: ")
                print("")
                cuentas_norm = gestor.cuentas_normales(dni)
                print("Cuentas SIN bonificacion:")
                for cuenta in cuentas_norm:
                    print(cuenta)
                print("")
                cuentas_bonif = gestor.cuentas_bonificadas(dni)
                print("Cuentas CON bonificacion: ")
                for cuenta in cuentas_bonif:
                    print(cuenta)
                    
            elif opcion == 11:
                print("INGRESO")
                ncuenta = int(input("Introduzca el número de cuenta: "))
                valor = int(input("Introduzca la cantidad a ingresar: "))
                gestor.ingreso(valor,ncuenta)
                print("Ingreso realizado correctamente.")

            elif opcion == 12:
                print("RETIRO")
                ncuenta = int(input("Introduzca el número de cuenta: "))
                valor = int(input("Introduzca la cantidad a retirar: "))
                gestor.retirar(valor,ncuenta)
                print("Retirada realizada correctamente.")
                
            else:
                print("adios")
                break

        except CuentaDesconocidaError:
            print("Error. Cuenta no existente.\n")
        except ClienteDesconocidoError:
            print("Error. Cliente no existente.\n")
        except CuentaDuplicadaError:
            print("Error. Este número de cuenta ya está registrado.\n")
        except ClienteDuplicadoError:
            print("Error. Cliente con DNI ya registrado.\n")
        except saldoError:
            print("Error saldo insuficiente o valor negativo o fuera de rango.\n")
        except interesError:
            print("Error. Ineteres negativo o fuera de rango.\n")
        except saldoInsuficienteError:
            print("Error. Valor superior al saldo de la cuenta.\n")
        except bonificacionError:
            print("Error. Bonificacion negativa o fuera de rango.\n")

if __name__ == "__main__":
    main()
