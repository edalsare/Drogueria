##http://mundogeek.net/archivos/2008/09/23/distribuir-aplicaciones-python/
from gi.repository import Gtk
import gettext
from os.path import abspath, dirname, join, exists
import locale
from drogueria_ctl import Drogueria,Producto, Vendedor, Cliente, Factura, Facpro
import os, datetime

APP_NAME = "ventana"
WHERE_AM_I = abspath(dirname(__file__))
LOCALE_DIR = join(WHERE_AM_I, 'locale')

try:
	locale.setlocale(locale.LC_ALL, '')
	locale.bindtextdomain(APP_NAME, LOCALE_DIR)
except:
	pass
if not exists(LOCALE_DIR):
	LOCALE_DIR = '/usr/share/locale'
	
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
gettext.textdomain(APP_NAME)
_ = gettext.gettext

class Drogueria_ctl:
	def __init__(self):
		gui = Gtk.Builder()
		gui.set_translation_domain(APP_NAME)
		gui.add_from_file("gui_farmacia.glade")
		eventos ={"on_window1_delete_event": Gtk.main_quit,
				  "on_act_cer_activate": Gtk.main_quit,
				  "on_act_abr_activate": self.__Nuevo_Cargar_activate,
				  "on_act_nue_activate": self.__Nuevo_Cargar_activate,
				  "on_imi_about_activate": self.__on_imi_about_activate,
                  "on_about_dro_delete_event": self.__about_dlg,
                  
                  "on_btn_add_pro_clicked": self.__on_btn_add_pro,
                  "on_cbxt_cod_pro_changed": self.__on_cbxt_cod_pro_changed,
                  "on_ent_nom_pro_focus_in_event":self.__barra_pro,
                  "on_ent_pre_pro_focus_in_event":self.__barra_pro,
                  "on_ent_can_pro_focus_in_event":self.__barra_pro,
                  
                  "on_btn_add_ven_clicked": self.__on_btn_add_ven,
                  "on_ent_cod_ven_focus_in_event":self.__barra_pro,
                  "on_ent_nom_ven_focus_in_event":self.__barra_pro,
                  "on_ent_tel_ven_focus_in_event":self.__barra_pro,
                  "on_ent_email_ven_focus_in_event":self.__barra_pro,
                  
                  "on_btn_add_cli_clicked":self.__add_cliente,
                  "on_cbxt_ide_cli_changed":self.__on_cbxt_ide_cli_changed,
                  "on_btn_acep_cli_clicked":self.__on_btn_acep_cli_clicked,
                  
                  "on_cbx_codv_fac_changed":self.__on_cbx_codv_fac_changed, 
                  "on_ent_fec_fac_icon_press":self.__fecha_factura,
                  "on_ent_num_fac_icon_press":self.__numero_factura,
                  "on_btn_todop_fac_clicked":self.__on_btn_todop_fac_clicked,
                  "on_btn_busp_fac_clicked":self.__on_btn_busp_fac_clicked,
                  "on_trv_pro_fac_row_activated":self.__anadir_a_factura,
                  
                  "on_btn_can_clicked":self.__on_btn_can_clicked,
                  "on_btn_cancel_clicked":self.__on_btn_can_clicked,
                  
                  "on_btn_guar_fac_clicked":self.__on_btn_guar_fac_clicked,
                  "on_trv_fac_row_activated":self.__sacar_producto,
                  "on_btn_remove_clicked":self.__on_btn_remove_clicked,
                  "on_btn_can_fac_clicked":self.__on_btn_can_fac_clicked
                  
                  }
		
		gui.connect_signals(eventos)
		self.mi_base= None
		self.Ventana = gui.get_object("window1")
		self.Ventana.set_title(_("Pharmacy - 2014"))
		
		self.lstS_codp = Gtk.ListStore(str)
		self.lstS_idec = Gtk.ListStore(str)
		self.lstS_codv = Gtk.ListStore(str)
		self.label =""
		self.aux=None
		self.sacar = None
		
		self.cbxt_cod_pro = gui.get_object("cbxt_cod_pro")
		self.ent_cbx_pro = gui.get_object("ent_cbx_pro")
		self.cbxt_cod_pro.set_model(self.lstS_codp)
		self.ent_nom_pro = gui.get_object("ent_nom_pro")
		self.ent_pre_pro = gui.get_object("ent_pre_pro")
		self.ent_can_pro = gui.get_object("ent_can_pro")
		self.btn_add_pro = gui.get_object("btn_add_pro")
		self.pro_var_pro = gui.get_object("pro_var_pro")
		
		
		
		self.ent_cod_ven = gui.get_object("ent_cod_ven")
		self.ent_nom_ven = gui.get_object("ent_nom_ven")
		self.ent_tel_ven = gui.get_object("ent_tel_ven")
		self.ent_email_ven = gui.get_object("ent_email_ven")
		self.btn_add_ven = gui.get_object("btn_add_ven")
		self.pro_var_ven = gui.get_object("pro_var_ven")
		
		self.cbxt_ide_cli = gui.get_object("cbxt_ide_cli")
		self.ent_cbx_cli = gui.get_object("ent_cbx_cli")
		self.cbxt_ide_cli.set_model(self.lstS_idec)
		self.ent_nom_cli = gui.get_object("ent_nom_cli")
		self.ent_tel_cli = gui.get_object("ent_tel_cli")
		self.btn_add_cli = gui.get_object("btn_add_cli")
		self.btn_acep_cli = gui.get_object("btn_acep_cli")
		
		self.ent_num_fac = gui.get_object("ent_num_fac")
		self.ent_fec_fac = gui.get_object("ent_fec_fac")
		self.ent_nomc_fac = gui.get_object("ent_nomc_fac")
		self.ent_idec_fac = gui.get_object("ent_idec_fac")
		self.ent_telc_fac = gui.get_object("ent_telc_fac")
		self.trv_fac = gui.get_object("trv_fac")
		self.cbx_codv_fac = gui.get_object("cbx_codv_fac")
		self.cbx_codv_fac.set_model(self.lstS_codv)
		self.cbx_codv_fac.set_entry_text_column(0)
		
		self.ent_nomv_fac = gui.get_object("ent_nomv_fac")
		self.ent_iva_fac = gui.get_object("ent_iva_fac")
		self.ent_tot_fac = gui.get_object("ent_tot_fac")
		self.btn_guar_fac = gui.get_object("btn_guar_fac")
		
		self.ent_nomp_fac = gui.get_object("ent_nomp_fac")
		self.ent_codp_fac = gui.get_object("ent_codp_fac")
		self.btn_busp_fac = gui.get_object("btn_busp_fac")
		self.btn_todop_fac = gui.get_object("btn_todop_fac")
		self.trv_pro_fac = gui.get_object("trv_pro_fac")
		
		
		self.listS_profac = gui.get_object("listS_profac")
		self.listS_prod = gui.get_object("listS_prod")
		self.about_dro = gui.get_object("about_dro")
		self.ent_Codigop = gui.get_object("ent_Codigop")
		self.ent_Codigop.set_model(self.lstS_codp)
		self.ent_Codigop.set_text_column(0)
		self.ent_idec = gui.get_object("ent_idec")
		self.ent_idec.set_model(self.lstS_idec)
		self.ent_idec.set_text_column(0)
		tre_pre = gui.get_object("tre_pre")
		cel_pre = gui.get_object("cel_pre")
		tre_pre.set_cell_data_func(cel_pre, self.__func_render_pre)
		tre_uni = gui.get_object("tre_uni")
		cell_uni = gui.get_object("cell_uni")
		tre_uni.set_cell_data_func(cell_uni, self.__func_render_pre)
		tre_iva = gui.get_object("tre_iva")
		cell_iva = gui.get_object("cell_iva")
		tre_iva.set_cell_data_func(cell_iva, self.__func_render_pre)
		tre_tot = gui.get_object("tre_tot")
		cell_tot = gui.get_object("cell_tot")
		tre_tot.set_cell_data_func(cell_tot, self.__func_render_pre)
		
		self.dlg_num_pro = gui.get_object("dlg_num_pro")
		self.ent_can = gui.get_object("ent_can")
		self.btn_can = gui.get_object("btn_can")
		self.btn_cancel = gui.get_object("btn_cancel")
		self.btn_remove = gui.get_object("btn_remove")
        
		
		
		self.Ventana.show
		
	def __Nuevo_Cargar_activate(self, widget):

		if widget.get_name() == "act_nue":
			fcd_inventario = Gtk.FileChooserDialog(_("New Database Drugstore"),
                                                   self.Ventana,
                                                   Gtk.FileChooserAction.SAVE,
                                                   (Gtk.STOCK_CANCEL,
                                                    Gtk.ResponseType.CANCEL,
                                                    Gtk.STOCK_SAVE,
                                                    Gtk.ResponseType.OK))
			"""# Se coloca un nombre de archivo por defecto para guardar"""
			fcd_inventario.set_current_name(_("new base.db"))
			"""
            # Se activa la opcion que en el caso de que se seleccione un
            # archivo existente, se muestra un mensaje de confirmacion de
            # sobre-escritura
            """
			Gtk.FileChooser.set_do_overwrite_confirmation(fcd_inventario, True)
		else:
			fcd_inventario = Gtk.FileChooserDialog(
                _("Select Database"),
                self.Ventana,
                Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL,
                 Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN,
                 Gtk.ResponseType.OK)
            )

		fcd_inventario.add_filter(self.__add_filtro_inv())
		fcd_inventario.set_current_folder("Archivos/")

		respuesta = fcd_inventario.run()
		if respuesta == Gtk.ResponseType.OK:
			ruta_archivo = fcd_inventario.get_filename()

            # Si el widget que lanzo la senal corresponde a la accion
            # "act_Nuevo" y el archivo correspondiente para guardar YA EXISTE,
            # se coloca la variable bandera "self.bSobre_escribir" a True y se
            # coloca la variable "color" a un tono Azul claro
			if (widget.get_name() == "act_nue" and
                    os.path.exists(ruta_archivo)):
				self.bSobre_escribir = True

            # Se crea un objeto Inventario con el archivo correspondiente
			self.mi_inventario = Drogueria(ruta_archivo)

		fcd_inventario.destroy()
		if widget.get_name() == "act_nue":
			self.mi_inventario.nue_base()
		self.mi_inventario.completar(self.lstS_codp, self.lstS_idec, self.lstS_codv)
	
	
	def __func_render_pre(self, column, cell, model, iter, user_data):
		str_pvp = cell.get_property('text')
		strTofloat = float(str_pvp.replace(',', '.'))
		floatTostr_2_decimales = "$ %.2f" % strTofloat
		cell.set_property('text', floatTostr_2_decimales)
	
	def __add_filtro_inv(self):

		fft_iventario = Gtk.FileFilter()
		fft_iventario.set_name(_("base de datos"))
		fft_iventario.add_pattern("*.db")
		return fft_iventario
	
	def __on_imi_about_activate(self, widget):
		self.about_dro.run()
        
        
	def __about_dlg(self,widget,otro):
		self.about_dro.hide()
         
	def __on_btn_add_pro(self, widget):
		"""
		metodo que maneja  la senal del boton anadir producto
		"""	
		codpro = self.cbxt_cod_pro.get_active_text()
		nompro = self.ent_nom_pro.get_text()
		precio = self.ent_pre_pro.get_text()
		canpro = self.ent_can_pro.get_text()
		d = self.ent_pre_pro.get_can_focus()
		
		if codpro == "":
			self.__mensaje(None, _("The product code field can not be empty"))
			return
		
		if nompro == "":
			self.__mensaje(None, _("The Product Name field can not be empty"))
			return

		
		try:
			nue_pro= Producto(codpro,nompro,float(precio),int(canpro))
		except ValueError:
			self.__mensaje(None,_("Verify that price and quantity data must be numerical") )
			
			return
		if int(canpro) <=0:
			self.__mensaje(None, _("enter amounts greater than zero"))
			return
		
		self.mi_inventario.add_producto(nue_pro,self.label)
		self.lstS_codp.append([codpro])
		self.__reiniciar_campos(widget)
		
	def __on_btn_add_ven(self, widget):
		"""
		metodo que controla la senal de anadir un vendedor
		"""
		ban = None
		codven = self.ent_cod_ven.get_text()
		nomven = self.ent_nom_ven.get_text()
		telven = self.ent_tel_ven.get_text()
		email = self.ent_email_ven.get_text()
		
		if codven == "" or nomven =="" or telven == "" or email == "":
			self.__mensaje(None, _("verify that all fields are complete"))
			return
			
		nue_ven = Vendedor(codven, nomven, telven, email)
		ban = self.mi_inventario.add_vendedor(nue_ven)
		if ban == "No":
			return
		self.lstS_codv.append([codven])
		self.__reiniciar_campos(widget)

    
	def __reiniciar_campos(self, widget):
		if widget.get_name() == "add_pro":
			self.cbxt_cod_pro.set_active(-1)
			self.ent_cbx_pro.set_text("")
			self.ent_nom_pro.set_text("") 
			self.ent_pre_pro.set_text("")
			self.ent_can_pro.set_text("")
			self.ent_can_pro.set_placeholder_text("")
			self.pro_var_pro.set_fraction(0)
		elif widget.get_name() == "add_ven":
			self.ent_cod_ven.set_text("")
			self.ent_nom_ven.set_text("")
			self.ent_tel_ven.set_text("")
			self.ent_email_ven.set_text("")
			self.pro_var_ven.set_fraction(0) 
		elif widget.get_name() == "addcli" or widget.get_name() == "cbxide" or widget.get_name() == "acecli":
			if widget.get_name() == "addcli" or widget.get_name() == "acecli":
				self.cbxt_ide_cli.set_active(-1)
				self.ent_cbx_cli.set_text("")
			self.ent_nom_cli.set_text("")
			self.ent_tel_cli.set_text("")
		else:	
			#~ self.cbxt_cod_pro.set_active(-1)
			 
			self.ent_nom_pro.set_text("") 
			self.ent_pre_pro.set_text("")
			self.ent_can_pro.set_text("")
			self.ent_can_pro.set_placeholder_text("")
			self.pro_var_pro.set_fraction(0) 
			
	# controla la senal de combo box de productos		
	def __on_cbxt_cod_pro_changed(self, widget):
		self.__barra_pro(None,None)
		cod = widget.get_child().get_text()
		self.__reiniciar_campos(widget)
		reg = self.mi_inventario.buscar(cod,1)
		if reg != None:
			can =""
				
			self.btn_add_pro.set_label(_("Update"))
			self.ent_nom_pro.set_text(reg[1])
			self.ent_pre_pro.set_text(str(reg[2]))
			self.ent_can_pro.set_placeholder_text(str(reg[3]))
			self.ent_nom_pro.set_can_focus(False)
			self.ent_pre_pro.set_can_focus(False)
			
			self.label = "Ok"

		else:
			self.ent_nom_pro.set_can_focus(True)
			self.ent_pre_pro.set_can_focus(True)
			t=self.btn_add_pro.set_label(_("Add"))
			self.label = "No"
	# metodo q contro la accion de la barras de progreso de prooductos y vendedores
	def __barra_pro(self, widget, otro):
		mas = 0
		try:
			if widget.get_name() =="nompro" or widget.get_name() =="prepro" or widget.get_name() =="canpro":
				cod = self.cbxt_cod_pro.get_active_text()
				nom = self.ent_nom_pro.get_text()
				pre = self.ent_pre_pro.get_text()
				can = self.ent_can_pro.get_text()
			else:
				cod = self.ent_cod_ven.get_text()
				nom = self.ent_nom_ven.get_text()
				pre = self.ent_tel_ven.get_text()
				can = self.ent_email_ven.get_text()
			
			if cod != "":
				mas = mas+0.25

			if nom != "":
				mas = mas+0.25

			if pre != "":
				mas = mas+0.25

			if can != "":
				mas = mas+0.25

		except AttributeError:
			None
		

		try:
			if widget.get_name() =="nompro" or widget.get_name() =="prepro" or widget.get_name() =="canpro":
				self.pro_var_pro.set_fraction(mas)
			else:
				self.pro_var_ven.set_fraction(mas)
		except AttributeError:
			None
	
	
	def __add_cliente(self, widget):
		"""
		metodo que controla la senal del boton anadir un cliente
		"""
		ide = self.cbxt_ide_cli.get_active_text()
		nom = self.ent_nom_cli.get_text()
		tel = self.ent_tel_cli.get_text()
		
		if ide =="" or nom =="" or tel == "":
			self.__mensaje(None, _("verify that all fields are complete"))
			return
			
		nue_cli = Cliente(ide, nom, tel)
		ban = self.mi_inventario.add_cliente(nue_cli)
		if ban == "No":
			return
		
		self.ent_nomc_fac.set_text(nom)
		self.ent_idec_fac.set_text(ide)
		self.ent_telc_fac.set_text(tel)
		self.lstS_idec.append([ide])
		self.__reiniciar_campos(widget)
		
	def __on_cbxt_ide_cli_changed(self, widget):
		"""
		metodo que controla la senal changed del combo box
		de cliente para activar o desactivar los botones de 
		anadir y aceptar.
		"""
		ide = widget.get_child().get_text()
		self.__reiniciar_campos(widget)
		reg = self.mi_inventario.buscar(ide,2)
		if reg != None:
			self.btn_acep_cli.set_sensitive(True)
			self.btn_add_cli.set_sensitive(False)
			self.ent_nom_cli.set_text(reg[1])
			self.ent_tel_cli.set_text(reg[2])
			self.ent_tel_cli.set_can_focus(False)
			self.ent_nom_cli.set_can_focus(False)
		else:
			self.btn_acep_cli.set_sensitive(False)
			self.btn_add_cli.set_sensitive(True)
			self.ent_tel_cli.set_can_focus(True)
			self.ent_nom_cli.set_can_focus(True)
	
	def __on_btn_acep_cli_clicked(self,  widget):
		"""
		metodo que controla la senal del boton aceptar
		en cliente para aadir lod datos de este a la factura
		"""
		ide = self.cbxt_ide_cli.get_active_text()
		nom = self.ent_nom_cli.get_text()
		tel = self.ent_tel_cli.get_text()
		
		self.ent_nomc_fac.set_text(nom)
		self.ent_idec_fac.set_text(ide)
		self.ent_telc_fac.set_text(tel)
		self.btn_acep_cli.set_sensitive(False)
		self.__reiniciar_campos(widget)
		
	def __on_cbx_codv_fac_changed(self, widget):
		"""
		metodo que controla la senal changed del combo box
		del codigo del vendedor en la factura para posteriormente
		adicionar el nombre de este
		"""
		cod = self.cbx_codv_fac.get_active_text()
		reg = self.mi_inventario.buscar(cod,3)
		
		self.ent_nomv_fac.set_text(reg)
		
	def __fecha_factura(self, widget, event_btn, icon_pos):
		"""
		metodo que controla la senal icon press del boton de estock
		de la entrada dela fecha en la factura
		para asi agrgar la fecha del dia correspondiente
		"""
		x = datetime.datetime.now()
		fecha = ("%s-%s-%s"%(x.day,x.month,x.year))
		self.ent_fec_fac.set_text(fecha)
			
	
	def __numero_factura(self, widget, event_btn, icon_pos):
		"""
		metodo que controla la senal icon press del boton stock
		de la entrada del numero de la factura
		asignandola automticamente
		"""
		num = "d"
		reg = self.mi_inventario.buscar(num,4)
		reg = "NumFac" + str(reg)
		self.ent_num_fac.set_text(reg)
	
	def __on_btn_todop_fac_clicked(self, widget):
		""" metodo que controla la senal cliked a la hora de mostrar
		todos los productos en el treeview
		"""
		try:
			reg = self.mi_inventario.buscar_pro(None, None, self.listS_prod)
		except AttributeError:
			pass
		
	def __on_btn_busp_fac_clicked(self,widget):
		try:
			nom = self.ent_nomp_fac.get_text()
			cod = self.ent_codp_fac.get_text()
			self.mi_inventario.buscar_pro(cod, nom, self.listS_prod)
		except AttributeError:
			pass
	
	def __anadir_a_factura(self, treeview, patch, view_column):
		"""
		metodo que controla la senal doble click en el treeview
		"""
		self.aux = None
		model = self.trv_pro_fac.get_model()
		titer = model.get_iter(patch)
		
		codigo = model.get_value(titer, 0)
		for reg in model:
			cod, nom, can, pre = reg
			if cod == codigo:
				break
		if can >0:
			self.dlg_num_pro.run()
			if self.aux != None:
				try:
					if int(self.aux) > 0 and int(self.aux)<=can:
						self.mi_inventario.adicionar_treview_factura(self.aux,reg, self.listS_profac)
					elif int(self.aux)>can:
						self.__mensaje(None, _("income exceeds the amount that the actual amount of products"))
					else:
						self.__mensaje(None, _("enter only numbers that is positive"))
				except ValueError:
					self.__mensaje(None, _("Only enter numbers greater than zero"))		
			self.ent_can.set_text("")
			
			self.total_iva()
		else:
			self.__mensaje(None, _("This product is out for now"))
		self.aux = None
		
	def __on_btn_can_clicked(self, widget):
		""" 
		metodo que extrae la cantidad del cuadro de dialogo
		numero de productos
		"""
		if widget.get_name() == "adicionar":
			self.aux = self.ent_can.get_text()
			self.dlg_num_pro.hide()
		elif widget.get_name()== "cancelar":
			self.dlg_num_pro.hide()
		
	def total_iva(self):
		"""
		metodo que calcula el iva total  y el total a pagar
		en la factura, agregandolos a sus respectivos campos
		"""
		total = 0.0
		iva = 0.0
		for lista in self.listS_profac:
			total = total + lista[5]
			iva = iva + lista[4]
			
		total = ("$ %.2f"% total)
		iva = ("$ %.2f"% iva)
		self.ent_iva_fac.set_text(str(iva))
		self.ent_tot_fac.set_text(str(total))
	
	def __on_btn_guar_fac_clicked(self, widget):
		codp = []
		canP = []
		numfac = self.ent_num_fac.get_text()
		fec_fac =self.ent_fec_fac.get_text()
		idec = self.ent_idec_fac.get_text()
		codv = self.cbx_codv_fac.get_active_text()
		ivaf = self.ent_iva_fac.get_text()
		try:
			fec_fac = datetime.datetime.strptime(fec_fac, "%d-%m-%Y")
		except ValueError:
			self.__mensaje(None, _("Enter the date"))
		if idec == "" or numfac == "" or ivaf == "":
			self.__mensaje(None, _("verify that all fields are complete"))
			return
		nue_fac = Factura(numfac, codv, idec, fec_fac)
		self.mi_inventario.add_factura(nue_fac)
		
		for lista in self.listS_profac:
			facpro = Facpro(numfac, lista[0], lista[2])
			self.mi_inventario.pro_fac(facpro)
		self.__sacar_cantidad()	
		self.__reiniciar_factura()	
	
	def __sacar_cantidad(self):
		"""
		metodo que resta las cantidades para actualizar la base
		"""
		for lista in self.listS_profac:
			cod, nom, can, val, iva, tot = lista
			self.mi_inventario.actualizar_productos(can,cod)
		self.__on_btn_todop_fac_clicked(None)
	
	
	def __reiniciar_factura(self):
		self.listS_profac.clear()
		self.ent_num_fac.set_text("")
		self.ent_fec_fac.set_text("")
		self.ent_idec_fac.set_text("")
		self.cbx_codv_fac.set_active(-1)
		self.ent_iva_fac.set_text("")
		self.ent_tot_fac.set_text("")
		self.ent_nomv_fac.set_text("")
		self.ent_nomc_fac.set_text("")
		self.ent_telc_fac.set_text("")
		self.ent_idec_fac.set_text("")
		
	
	def __sacar_producto(self, treeview, patch, view_column):
		"""
		metodo que controla la senal doble click del treevie
		de la factura en caso de q se dese retirar un producto o sierta cantidad
		"""
		self.aux = None
		sacar = self.listS_profac.get_iter(patch)
		self.sacar = sacar
		codigo = self.listS_profac.get_value(sacar, 0)
		for reg in self.listS_profac:
			cod, nom, can, val, iva, tot = reg
			if cod == codigo:
				break
		self.btn_remove.set_sensitive(True)
		self.dlg_num_pro.run()
		if self.aux != None:
			
			ncan = 0
			ncan = int(can) - int(self.aux)
			iva1 = (float(val) * 0.16)
			iva1 = (float(iva1) * float(ncan))
			print(iva1)
			total = (float(ncan) * float(val)) + iva1
			self.listS_profac.set_value(sacar, 2, ncan)
			self.listS_profac.set_value(sacar, 4, iva1)
			self.listS_profac.set_value(sacar, 5, total)
			if ncan == 0:
				self.listS_profac.remove(sacar)
					
		
		self.total_iva()
		self.btn_remove.set_sensitive(False)
		self.ent_can.set_text("")
		
	def __on_btn_can_fac_clicked(self, widget):
			self.__reiniciar_factura()
	
	def __on_btn_remove_clicked(self, widget):
		self.listS_profac.remove(self.sacar)
		self.dlg_num_pro.hide()
		self.total_iva()
		
	def __mensaje(self, widget, mensaje):
		flags = Gtk.DialogFlags.DESTROY_WITH_PARENT | Gtk.DialogFlags.MODAL
		dialogo = Gtk.MessageDialog(
			widget, flags, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, mensaje)
		dialogo.run()
		dialogo.destroy()	
		
if __name__ =='__main__':
	Drogueria_ctl()
	Gtk.main()
