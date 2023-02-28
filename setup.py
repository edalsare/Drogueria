from cx_Freeze import setup, Executable

setup(name="Ventana",
	version="0.1",
	description="drogueria",
	executables=[Executable("ctl_ventana.py")],)
