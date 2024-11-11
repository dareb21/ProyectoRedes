import tkinter as tk
from PIL import Image, ImageTk

greenColor = (76,229,100)

# Crear ventana
root = tk.Tk()
root.title("GhostVPN")
root.geometry("1600x900")
root.configure(background='white')
root.resizable(False,False)

# Crear canvas
canvas = tk.Canvas(root, width=1600, height=900, bg='white')
canvas.pack()

#BOTON OFF
img_boton2 = Image.open("VPN Interfaz/SWITCH_APAGADO.png")  # Reemplaza por imagen
img_boton2 = img_boton2.resize((135, 155))
img_boton_tk2 = ImageTk.PhotoImage(img_boton2)

boton1_creado = None
# Función para el botón de encender
#ACA SE DEBE AGREGAR TODO LO QUE SEA CORRESPONDIENTE A ENCENDER LA VPN
#LOS DATOS DE TRANSFERENCIA Y ESO
def boton1():
    global boton1_creado
    print("Botón ON presionado") #ESTE PRINT ESTA PARA VERIFICAR, ESTO SE DEBE QUITAR Y PONER LOS SERVICIOS CORRESPONDIENTES
    delete_imgledonH() #borro encendido en H
    create_imgledoffH() #creo apagado en H
    delete_imgledoffA() #borro apagado en A
    create_imgledonA() #creo encendido en A
    if boton1_creado:
        boton1_creado.destroy()

    boton1_creado = boton    

    boton.destroy()
    def boton2def(): #ESTE BOTON ES PARA APAGAR EL VPN, ACA SE DEBE DESACTIVAR LOS SERVICIOS DEL VPN
        print("Boton OFF presionado")#ESTE PRINT ESTA PARA VERIFICAR, ESTO SE DEBE QUITAR Y PONER LOS SERVICIOS CORRESPONDIENTES
        boton2.destroy()
        delete_imgledoffH() #borro apagado en H
        create_imgledonH() #creo encendido en H
        delete_imgledonA() #borro encendido en A
        create_imgledoffA() #creo apagado en 
        boton12 = tk.Button(root, borderwidth=0, bg='black', image=img_boton_tk, command=boton1)
        boton12.place(x=1209, y=417)

        global boton1_creado
        boton1_creado = boton12
    boton2 = tk.Button(root, borderwidth=0, bg='black', image=img_boton_tk2, command=boton2def)
    boton2.place(x=1390, y=417)
    
    


#MAPA CENTRAL
img_central = Image.open("VPN Interfaz/Mapa_mundi_Final.png")
img_central = img_central.resize((1600, 900), Image.LANCZOS)
img_central_tk = ImageTk.PhotoImage(img_central)
canvas.create_image(0, 0, anchor="nw", image=img_central_tk)

#TITULO NOMBRE APP
img_titulo = Image.open("VPN Interfaz/TITULO.png")
img_titulo = img_titulo.resize((330, 130))
img_titulotk = ImageTk.PhotoImage(img_titulo)
canvas.create_image(190,70, image=img_titulotk)

#INFO TRAFICO DE RED
k = "Trafico de Datos" #Variable para el flujo de datos actualizable
label_trafico = tk.Label(root, bg="black", text=k, font=("Myriad Pro", 20), fg="white") #Color letra en hexadecimal #4CE664
label_trafico.place(x=1230, y=170)

#MARCO INFO DE VPN
img_info = Image.open("VPN Interfaz/VPN_INFO.png")
img_info = img_info.resize((372, 293))
img_infotk = ImageTk.PhotoImage(img_info)
canvas.create_image(1370,200, image=img_infotk)

#MARCO SWITCH BOTONES
img_sw = Image.open("VPN Interfaz/SWITCH_MARCO.png")
img_sw = img_sw.resize((400, 300))
img_sw_tk = ImageTk.PhotoImage(img_sw)
ksw = canvas.create_image(1370, 500, image=img_sw_tk)

#BOTON ON
img_boton = Image.open("VPN Interfaz/SWITCH_ENCENDIDO.png")
img_boton = img_boton.resize((135, 155))
img_boton_tk = ImageTk.PhotoImage(img_boton)
boton = tk.Button(root, borderwidth=0, bg='black', image=img_boton_tk, command=boton1)
boton.place(x=1209, y=417)

#IMAGEN LED ON HONDURAS
img_ledontk = None
kledon = None
def create_imgledonH():
    global img_ledontk, kledon 
    img_ledon = Image.open("VPN Interfaz/VPN_ENCENDIDO_LED.png")
    img_ledon = img_ledon.resize((31, 34))
    img_ledontk = ImageTk.PhotoImage(img_ledon)
    kledon = canvas.create_image(260, 530, image=img_ledontk)

def delete_imgledonH():
    global kledon
    if kledon is not None:
        canvas.delete(kledon)
        kledon = None

#IMAGEN LED OFF HONDURAS
img_ledofftk = None
kledoff = None
def create_imgledoffH():
    global img_ledofftk, kledoff 
    img_ledoff = Image.open("VPN Interfaz/VPN_APAGADO_LED.png")
    img_ledoff = img_ledoff.resize((31, 34))
    img_ledofftk = ImageTk.PhotoImage(img_ledoff)
    kledoff = canvas.create_image(260, 530, image=img_ledofftk)

def delete_imgledoffH():
    global kledoff
    if kledoff is not None:
        canvas.delete(kledoff)
        kledoff = None


#IMAGEN LED ON ALEMANIA
img_ledonAtk = None
kledonA = None
def create_imgledonA():
    global img_ledonAtk, kledonA
    img_ledonA = Image.open("VPN Interfaz/VPN_ENCENDIDO_LED.png")
    img_ledonA = img_ledonA.resize((31, 34))
    img_ledonAtk = ImageTk.PhotoImage(img_ledonA)
    kledonA = canvas.create_image(590, 360, image=img_ledonAtk)

def delete_imgledonA():
    global kledonA
    if kledonA is not None:
        canvas.delete(kledonA)
        kledonA = None

#IMAGEN LED OFF ALEMANIA
img_ledoffAtk = None
kledoffA = None
def create_imgledoffA():
    global img_ledoffAtk, kledoffA
    img_ledoffA = Image.open("VPN Interfaz/VPN_APAGADO_LED.png")
    img_ledoffA = img_ledoffA.resize((31, 34))
    img_ledoffAtk = ImageTk.PhotoImage(img_ledoffA)
    kledoffA = canvas.create_image(590, 360, image=img_ledoffAtk)

def delete_imgledoffA():
    global kledoffA
    if kledoffA is not None:
        canvas.delete(kledoffA)
        kledoffA = None


create_imgledonH()
create_imgledoffA()


# Iniciar la aplicación
root.mainloop()
