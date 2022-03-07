from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import database as db
import facial_recognition as rf

#Clase definida que hace la creacion de interfaz ventana de menu
class VentanaMenu(Frame):

    #Parametros inicales    
    def __init__(self, master=None):
        super().__init__(master,width=500, height=300)
        self.master = master
        self.pack()
        self.idusuario = 0
        self.selected = IntVar() 
        self.selected.set(0) 

    #Función de administrador que limpia tabla, lo realiza cuando hay una actualización
    def limpiaGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)
    
    #Funcion de administrador que trae los usuarios registrados que tengan acceso 
    #y los pone en la tabla de administrador
    def llenaDatos(self):
       
        datos = db.getUsers(self.idusuario)  
              
        for row in datos:            
            self.grid.insert("",END,text=row[0], values=(row[2]))
        
        if len(self.grid.get_children()) > 0:
            self.grid.selection_set( self.grid.get_children()[0] )

    #Funcion de smartgate que trae los administradores registrados
    def llenaDatosT1(self):
       
        datos = db.getAdmins(self.idusuario)  
              
        for row in datos:            
            self.grid.insert("",END,text=row[0], values=(row[2]))
        
        if len(self.grid.get_children()) > 0:
            self.grid.selection_set( self.grid.get_children()[0] )

    #Funcion de smartgate que trae los registros de que realiza el usuario
    def llenaDatosB(self):
       
        datos = db.getChanges()  
        print(datos)
        for row in datos:
            if row[4] == 1 :           
                self.gridSu.insert("",END,text=row[0], values=("Administrador "+str(row[1])+" agrego usuario nuevo llamado "+row[3],row[2]))
        
        if len(self.gridSu.get_children()) > 0:
            self.gridSu.selection_set( self.gridSu.get_children()[0] )

    #Función que tiene administrador, realiza la captura de usuario nuevo
    #se realiza una verificaión de que tipo de imagen se va tomar para la captura de rostro(cubrebocas, lentes o normal)
    def inicia(self):
        if self.selected.get()==1:
            db.insertUser(self.idusuario,self.txtNombreN.get())
            rf.register_capture(self,self.txtNombreN.get(),300)
            self.limpiaGrid()
            self.llenaDatos()
        else:
            if self.selected.get()==2:
                db.insertUser(self.idusuario,self.txtNombreN.get())
                rf.register_capture(self,self.txtNombreN.get(),300)
                self.limpiaGrid()
                self.llenaDatos()
            else:
                db.insertUser(self.idusuario,self.txtNombreN.get())
                rf.register_capture(self,self.txtNombreN.get(),200)
                self.limpiaGrid()
                self.llenaDatos()

    #Función de administrador crea la ventana para agregar usuario      
    def fNuevo(self):     
        self.nuevo = Toplevel()    
        self.nuevo.geometry("400x200")
        self.nuevo.title("Agregar nuevo")
        frame1 = Frame(self.nuevo, bg="#bfdaff")
        frame1.place(x=0,y=0,width=400, height=200)                        
        lbl1 = Label(frame1,text="Nombre: ", font=("arial",14),bg="#bfdaff")
        lbl1.place(x=3,y=55)        
        self.txtNombreN=Entry(frame1)
        self.txtNombreN.place(x=110,y=55,width=100, height=25)  
        self.opc1 = Radiobutton(frame1,text='Cubrebocas', variable=self.selected, value=1,bg="#bfdaff")
        self.opc1.place(x=250,y=55,width=110, height=50)
        self.opc2 = Radiobutton(frame1,text='Lentes', variable=self.selected,value=2,bg="#bfdaff")
        self.opc2.place(x=235,y=95,width=100, height=50)
        self.btnGuardar=Button(frame1,text="Capturar rostro", command=self.inicia, bg="#ec6e00", fg="white")
        self.btnGuardar.place(x=10,y=110,width=200, height=40)                 

    #Función de smartgate crea la ventana para agregar nuevo adminstrador  
    def fNuevoA(self):
        self.nuevoA = Toplevel()
        self.nuevoA.geometry("500x300")
        self.nuevoA.title("Agregar nuevo")
        frame2 = Frame(self.nuevoA,bg="#bfdaff" )
        frame2.place(x=0,y=0,width=500, height=300)                        
        lbl1 = Label(frame2,text="Nombre del administrador: ", font=("arial",14),bg="#bfdaff")
        lbl1.place(x=175,y=30)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=200,y=65,width=100, height=25)                
        lbl2 = Label(frame2,text="Contraseña: ", font=("arial",14),bg="#bfdaff")
        lbl2.place(x=200,y=105)        
        self.txtContraseña=Entry(frame2)
        self.txtContraseña.place(x=200,y=135,width=100, height=25) 
        self.btnGuardar=Button(frame2,text="Registrar", command=lambda:[self.fGuardarA(), self.nuevoA.destroy()], bg="green", fg="white")
        self.btnGuardar.place(x=190,y=210,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.nuevoA.destroy, bg="red", fg="white")
        self.btnCancelar.place(x=260,y=210,width=60, height=30) 

    #Función de administrador, realiza el monitoreo de reconocimiento facial
    #se crea frame dando imagen de ESP32CAM y checando cuando una persona quiere entrar        
    def fMonitorear(self):        
        rf.login_capture(self)

    #Función de administrador que elimina a usuario seleccionado                                  
    def fEliminar(self):
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            valores = self.grid.item(selected,'values')
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n")            
            if r == messagebox.YES:
                db.removeUser(clave,valores[0])
                messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                self.limpiaGrid()
                self.llenaDatos()
            else:
                messagebox.showwarning("Eliminar", 'No fue posible eliminar el elemento.')

    #Función de smartgate que elimina a administrador seleccionado 
    def fEliminarA(self):
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n")            
            if r == messagebox.YES:
                db.removeAdmin(clave)
                messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                self.limpiaGrid()
                self.llenaDatosT1()
            else:
                messagebox.showwarning("Eliminar", 'No fue posible eliminar el elemento.')

    #Función de smartgate que guarda en la base de datos al administrador nuevo
    def fGuardarA(self): 
        db.insertUser(self.txtNombre.get(), self.txtContraseña.get())  
        messagebox.showinfo("Exito", 'Usuario agregado correctamente.')

    #Crea los componentes para administrador
    def create_widgets(self):
        
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=150, height=300)        
        self.btnNuevo=Button(frame1,text="Agregar", command=self.fNuevo, bg="green", fg="white")
        self.btnNuevo.place(x=30,y=50,width=80, height=30 )                        
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="red", fg="white")
        self.btnEliminar.place(x=30,y=90,width=80, height=30)   
        self.btnModificar=Button(frame1,text="Monitorear", command=self.fMonitorear, bg="#ec6e00", fg="white")
        self.btnModificar.place(x=30,y=130,width=80, height=30) 

        frame3 = Frame(self,bg="#bfdaff" )
        frame3.place(x=152,y=0,width=350, height=300)     
        #Creación de tabla usuarios registrados                
        self.grid = ttk.Treeview(frame3, columns=("col1"))        
        self.grid.column("#0",width=60)
        self.grid.column("col1",width=200, anchor=CENTER)     
        self.grid.heading("#0", text="Id", anchor=CENTER)
        self.grid.heading("col1", text="Nombre", anchor=CENTER)
        self.grid.pack(side=LEFT,fill = Y)        
        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)
        self.grid['selectmode']='browse'   
    
    #Crea los componentes para smartgate
    def create_widgetsSU(self):

        self.master.geometry("1050x300")
        frame1 = Frame(self.master, bg="#bfdaff")
        frame1.place(x=0,y=0,width=150, height=300)        
        self.btnNuevo=Button(frame1,text="Agregar", command=self.fNuevoA, bg="green", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )                        
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminarA, bg="red", fg="white")
        self.btnEliminar.place(x=5,y=90,width=80, height=30)   
        frame3 = Frame(self.master,bg="#bfdaff" )
        frame3.place(x=152,y=0,width=350, height=300)  

        #Creación de tabla para administradores          
        self.grid = ttk.Treeview(frame3, columns=("col1"))        
        self.grid.column("#0",width=60)
        self.grid.column("col1",width=200, anchor=CENTER)     
        self.grid.heading("#0", text="Id", anchor=CENTER)
        self.grid.heading("col1", text="Nombre", anchor=CENTER)
        self.grid.pack(side=LEFT,fill = Y)        
        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        sb.place(x=265,y=0,height=300)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)
        self.grid['selectmode']='browse'  

        frame4 = Frame(self.master,bg="#bfdaff" )
        frame4.place(x=485,y=0,width=590, height=300)
        #Creación de tabla para registros de lo que realizan los administradores                      
        self.gridSu = ttk.Treeview(frame4, columns=("col1","col2"))        
        self.gridSu.column("#0",width=50)
        self.gridSu.column("col1",width=375, anchor=CENTER)  
        self.gridSu.column("col2",width=130, anchor=CENTER)
        self.gridSu.heading("#0", text="Id", anchor=CENTER)
        self.gridSu.heading("col1", text="Descripción", anchor=CENTER)
        self.gridSu.heading("col2", text="Fecha", anchor=CENTER)
        self.gridSu.pack(side=LEFT,fill = Y)        
        sb2 = Scrollbar(frame4, orient=VERTICAL)
        sb2.pack(side=RIGHT, fill = Y)
        self.gridSu.config(yscrollcommand=sb2.set)
        sb2.config(command=self.gridSu.yview)
        self.gridSu['selectmode']='browse'       