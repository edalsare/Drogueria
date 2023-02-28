import sqlite3
from gi.repository import Gtk


class Producto:
    def __init__(self,codigop,nombrep,preciop,cantidadp):
        self.codigop = codigop
        self.nombrep = nombrep
        self.preciop = preciop
        self.cantidadp = cantidadp

class Vendedor:
    def __init__(self,codven,nomven,emailven,telven):
        self.codven = codven
        self.nomven = nomven
        self.emailven = emailven
        self.telven = telven

class Cliente:
    def __init__(self,idecli,nomcli,telcli):
        self.idecli = idecli
        self.nomcli = nomcli
        self.telcli = telcli
        
class Factura:
    def __init__(self,codfac,codve, idecli,fecha):
        self.codfac = codfac
        self.codv = codve
        self.idecli = idecli
        self.fecha = fecha
        
class Facpro:
	def __init__(self,codfac,codpro,can):
		self.codfac = codfac
		self.codpro = codpro
		self.can = can
	

        
class Drogueria:
    
    def __init__(self, nom_base):
        self.nom_base = nom_base

        
    def nue_base(self):
        base = sqlite3.connect(self.nom_base)
        cursor = base.cursor()
        cursor.executescript("create table Productos(Codigo text primary key, Nombre text);"
							 "alter table Productos add Precio float;"
							 "alter table productos add Cantidad int;"
							 "create table Vendedor(Codigo text primary key );"
							 "alter table Vendedor add Nombre text;"
							 "alter table Vendedor add Email text;"
							 "alter table Vendedor add Telefono text;"
							 "create table Clientes (Identificacion text primary key );"
							 "alter table Clientes add Nombre text;"
							 "alter table Clientes add Telefono text;"
							 "create table Factura (Codigo text primary key );"
							 "alter table Factura add Cod_Vendedor text;"
							 "alter table Factura add Cod_Cliente text;"
							 "alter table Factura add Fecha date;"
							 "create table Fac_pro(codfac text, codpro text, Cantidad int, foreign key (codfac) references Factura(Codigo), foreign key (codpro) references Productos(Codigo))")
							 
        base.commit()
        base.close()

    
    def completar(self,listp,listc,listv):
        listp.clear()
        listc.clear()
        listv.clear()
        base = sqlite3.connect(self.nom_base)
        
        cursor = base.execute("select Codigo from Productos")
        for registro in cursor:
            codigop = registro
            listp.append([codigop[0]])
            
        cursor = base.execute("select Identificacion from Clientes")
        for registro in cursor:
            idecli = registro
            listc.append([idecli[0]])
            
        cursor = base.execute("select Codigo from Vendedor")
        for registro in cursor:
            codven = registro
            listv.append([codven[0]])
        
        base.close()
			
    def buscar(self, codigo,otro):
        aux = None
        aux2 = None
        aux3 = None
        aux4 = 0
        base = sqlite3.connect(self.nom_base)
        
        cursor = base.execute("select * from Productos")
        for reg in cursor:
            codigop, nombrep, preciop, cantidadp = reg 
            if str(codigop) == str(codigo):
                aux = reg
                break
        
        cursor = base.execute("select * from Clientes")
        for reg in cursor:
            idecli, nomcli, telcli = reg 
            if str(idecli) == str(codigo):
                aux2 = reg
                break
        
        cursor = base.execute("select * from Vendedor")
        for reg in cursor:
            codven, nomven, emailven, telven = reg 
            if str(codven) == str(codigo):
                codven, nomven, emailven, telven = reg
                break
        
        cursor = base.execute("select * from Factura")
        for reg in cursor:
            aux4 +=1
       
        if otro == 1:
            return aux
        elif otro == 2:
            return aux2
        elif otro == 3:
            return codven
        else:
            return aux4
        base.close()
    
    def buscar_pro(self, codigo, nombre, lstS):
        lstS.clear()
        base = sqlite3.connect(self.nom_base)
        cursor = base.execute("select * from Productos")
        for reg in cursor:
            codigop, nombrep, preciop, cantidadp = reg
            if codigo == "" and nombre == nombrep:
                lstS.clear()
                lstS.append([reg[0], reg[1], reg[3], reg[2]])
                break
            elif codigo == codigop and nombre == "":
                lstS.clear()
                lstS.append([reg[0], reg[1], reg[3], reg[2]])
                break
            elif codigo == codigop and nombre == nombrep:
                lstS.clear()
                lstS.append([reg[0], reg[1], reg[3], reg[2]])
                break
            elif codigo == None and nombre == None:
                lstS.append([reg[0], reg[1], reg[3], reg[2]])
                
        
    
    def add_producto(self, producto, label):
        base = sqlite3.connect(self.nom_base)
        cursor = base.cursor()
        if label == "Ok":
            can = 0
            reg = self.buscar(producto.codigop,1)
            can = reg[3] + producto.cantidadp
            cursor.execute("update Productos set Cantidad = ? where Codigo = ?", (can, producto.codigop))

        else:
            cursor.execute("insert into Productos(Codigo, Nombre, Precio, Cantidad) values (?,?,?,?)", 
                           (producto.codigop, producto.nombrep, producto.preciop, producto.cantidadp))
        base.commit()
        base.close()
 
    def add_vendedor(self, vendedor):
        base = sqlite3.connect(self.nom_base)
        cursor = base.cursor()
        try:
            cursor.execute("insert into Vendedor(Codigo, Nombre, Telefono, Email) values (?,?,?,?)",
                           (vendedor.codven, vendedor.nomven, vendedor.telven, vendedor.emailven))
            base.commit()
            base.close()
        
        except sqlite3.IntegrityError:
            Mensaje.mensaje(None, None, "No pueden existir mas de un vendedor con el mismo codigo")
            return "No"
        
        
    
    def add_cliente(self, cliente):
        base = sqlite3.connect(self.nom_base)
        cursor = base.cursor()
        try:
            cursor.execute("insert into Clientes(Identificacion, Nombre, Telefono) values (?,?,?)",
                           (cliente.idecli, cliente.nomcli, cliente.telcli))
            base.commit()
            base.close()
        
        except sqlite3.IntegrityError:
            Mensaje.mensaje(None, None, "No pueden existir mas de un Cliente con el mismo codigo")
            return "No"
    
    def adicionar_treview_factura(self, cant, reg, lstS):
        can = 0
        total = 0.0
        iva = 0.0
        base = sqlite3.connect(self.nom_base)
        cursor = base.execute("select * from Productos")
        for lista in cursor:
            codigop, nombrep, preciop, cantidadp = lista
            if reg[0] == codigop:
                break
        iva = (float(preciop) * 0.16)
        iva = (float(cant) * iva)
        total = (float(cant) * float(preciop)) + iva
        lstS.append([codigop, nombrep, int(cant), preciop, iva, total])
        
        can = int(cantidadp) - int(cant)
        
        
        base.commit()
        base.close()
        
    def actualizar_productos(self, can, codigo):
        base = sqlite3.connect(self.nom_base)
        cursor = base.execute("select * from Productos")
        for lista in cursor:
            codigop, nombrep, preciop, cantidadp = lista
            if codigo == codigop:
                can1 = cantidadp - can
        cursor.execute("update Productos set Cantidad = ? where Codigo = ?", (can1, codigo))
        base.commit()
        base.close()
    
    def add_factura(self, factura):
        base = sqlite3.connect(self.nom_base)
        cursor = base.cursor()
        cursor.execute("insert into Factura(Codigo, Cod_Vendedor, Cod_cliente, Fecha) values (?,?,?,?)",
                           (factura.codfac, factura.codv, factura.idecli, factura.fecha))
        base.commit()
        base.close()
        
    def pro_fac(self, profac):
        base = sqlite3.connect(self.nom_base)
        cursor = base.cursor()
        cursor.execute("insert into Fac_pro(codfac, codpro, Cantidad) values (?,?,?)",
                           (profac.codfac, profac.codpro, profac.can))
        base.commit()
        base.close()
        
        
        
class Mensaje:
    def mensaje(self, widget, mensaje):
        flags = Gtk.DialogFlags.DESTROY_WITH_PARENT | Gtk.DialogFlags.MODAL
        dialogo = Gtk.MessageDialog(
			widget, flags, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, mensaje)
        dialogo.run()
        dialogo.destroy()
        

         
