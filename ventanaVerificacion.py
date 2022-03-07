from tkinter import *
from tkinter import ttk
import database as db
from tkinter import messagebox
from ventanaMenu import *

#Clase definida que hace la creacion de interfaz ventana de verificación
class VentanaVerificacion(Frame):
    
    #Parametros inicales
    def __init__(self, master=None):
        super().__init__(master,width=500, height=300)
        self.master = master
        self.pack()
    
    #Función para guardar usuario nuevo
    def fGuardar(self): 
        #Función para registrar administrador nuevo en la base de datos
        db.registerUser(self.txtNombre.get(), self.txtContraseña.get())  
        self.destroy   
        messagebox.showinfo("Exito", 'Usuario agregado correctamente.')
        
    #Función donde se verifican datos ingresados en la base de datos, regresa la ventana segun los datos
    #si es administrador o smartgate mostrara su respectiva ventana
    def fBuscar(self): 
             
        datos = db.getUser(self.txtNombreI.get(),self.txtContraseñaI.get())

        if datos["id"] > 0:
            if datos["idSU"] >0:
                root3 = Tk()
                root3.title("Bienvenido "+ datos["name"])
                #Crea la ventana menu 
                app = VentanaMenu(root3)  
                app.idusuario = datos["id"]
                #Crea los componentes para smartgate
                app.create_widgetsSU()
                #Funcion que trae los administradores registrados
                app.llenaDatosT1()
                app.llenaDatosB()
                
            else:
                root3 = Tk()
                root3.title("Bienvenido "+ datos["name"])
                app = VentanaMenu(root3) 
                app.idusuario = datos["id"]
                #Crea los componentes para administrador
                app.create_widgets()
                #Funcion que trae los usuarios registrados que tengan acceso
                app.llenaDatos()
        else:
            messagebox.showinfo("Error", 'Datos invalidos.')
        self.master.destroy()

    #Funcion que crea los componentes de la ventana verificación
    def create_login(self):
        
        frame2 = Frame(self,bg="#bfdaff" )
        frame2.place(x=0,y=0,width=500, height=300)                        
        lbl1 = Label(frame2,text="Nombre de usuario: ", font=("arial",14),bg="#bfdaff")
        lbl1.place(x=175,y=30)        
        self.txtNombreI=Entry(frame2)
        self.txtNombreI.place(x=200,y=65,width=100, height=25)                
        lbl2 = Label(frame2,text="Contraseña: ", font=("arial",14),bg="#bfdaff")
        lbl2.place(x=200,y=105)        
        self.txtContraseñaI=Entry(frame2,show='*')
        self.txtContraseñaI.place(x=200,y=135,width=100, height=25) 
                      
        self.btnGuardar=Button(frame2,text="Ingresar", command=self.fBuscar, bg="green", fg="white")
        self.btnGuardar.place(x=190,y=210,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.master.destroy, bg="red", fg="white")
        self.btnCancelar.place(x=260,y=210,width=60, height=30) 