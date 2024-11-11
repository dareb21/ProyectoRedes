import tkinter as tk
from PIL import Image, ImageTk

greenColor = (76,229,100)

# Crear ventana
root = tk.Tk()
root.title("GhostVPN")
root.geometry("1600x900")
root.configure(background='white')

# Crear canvas
canvas = tk.Canvas(root, width=1400, height=900, bg='white')
canvas.pack()

img_boton2 = Image.open("off.png")  # Reemplaza por imagen
img_boton2 = img_boton2.resize((200, 200))
img_boton_tk2 = ImageTk.PhotoImage(img_boton2)

    
# Función para el botón
def boton1():
    print("Botón presionado") #Cambiar a proceso de encender
    def boton2def():
        print("Boton 2 presionado")
        boton2.destroy()
    boton2 = tk.Button(root, borderwidth=0, bg='white', image=img_boton_tk2, command=boton2def)
    boton2.place(x=1180, y=300)


# Cargar y colocar imagen central (900x400)
img_central = Image.open("mapa_mundi_blanco.png")  # Reemplaza por imagen
img_central = img_central.resize((1600, 900), Image.LANCZOS)
img_central_tk = ImageTk.PhotoImage(img_central)
canvas.create_image(700, 600, image=img_central_tk)  # Colocar la imagen al centro

# Texto Nombre App
label_trafico = tk.Label(root, bg='white', text="VPN", font=("Myriad Pro", 20))
label_trafico.place(x=700, y=50)

# Texto "Tráfico de red"

k = "Trafico de Datos" #Variable para el flujo de datos actualizable
label_trafico = tk.Label(root, bg="white", text=k, font=("Myriad Pro", 20), fg="#4CE664") #Color letra en hexadecimal
label_trafico.place(x=1100, y=200)

# Cargar imagen para el botón (200x200)
img_boton = Image.open("on.png")  # Reemplaza por imagen
img_boton = img_boton.resize((200, 200))
img_boton_tk = ImageTk.PhotoImage(img_boton)

# Crear botón con imagen
boton = tk.Button(root, borderwidth=0, bg='white', image=img_boton_tk, command=boton1)
boton.place(x=1180, y=300)

# Iniciar la aplicación
root.mainloop()
