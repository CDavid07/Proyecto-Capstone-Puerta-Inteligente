#12 de febrero del 2022
#Integrantes:
#David Arturo Castellanos Guzmán 
#Merle Yuridia Meza Nava
#Andy Mitchell Torres Martínez

from tkinter import *
from ventanaMenu import *
from ventanaVerificacion import *

#Declaracion de variables para interfaz
txt_login = "Iniciar Sesión"
txt_register = "Registrarse"
color_white = "#101010" 
color_black = "#f4f5f4" 
color_orange2 = "#FF9933"

color_btn = "#ec6e00" #naranja
color_background = "#f4f5f4"

font_label = "Candara"
size_screen = "500x300"

#Inicio sesion
def login():

    root2 = Toplevel()
    root2.title("Iniciar sesion")
    #Llamamos la clase ventana de verificacion
    app = VentanaVerificacion(root2) 
    app.create_login()
 
#Creación de ventana inicial
root = Tk()
root.geometry(size_screen)
root.title("CodigoIOT")
root.configure(bg=color_background)
Label(text="¡Bienvenido(a)!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

Label(root, text="", bg=color_background).pack()
Label(root, text="", bg=color_background).pack()
Label(root, text="", bg=color_background).pack()
root.x =Button(root,text=txt_login, fg=color_white, bg=color_btn, activebackground=color_orange2, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()


root.mainloop()