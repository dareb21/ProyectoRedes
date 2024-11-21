import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox

greenColor = (76, 229, 100)


# # Crear ventana
# root = tk.Tk()
# root.title("GhostVPN")
# root.geometry("1300x600")
# root.configure(background='white')
# root.resizable(False, False)

# # Crear canvas
# canvas = tk.Canvas(root, width=1300, height=600, bg='white')
# canvas.pack()

def centrar_ventana(ventana, ancho, alto):
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    # Calcular la posición x, y para centrar
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    # Aplicar la geometría centrada
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Crear la ventana principal
root = tk.Tk()
root.title("GhostVPN")
root.configure(background='white')
root.resizable(False, False)

# Dimensiones de la ventana
ancho_ventana = 1300
alto_ventana = 600
# Centrar la ventana
centrar_ventana(root, ancho_ventana, alto_ventana)

# Crear canvas
canvas = tk.Canvas(root, width=ancho_ventana, height=alto_ventana, bg='white')
canvas.pack()

# BOTON OFF
img_boton2 = Image.open("./SWITCH_APAGADO.png")
img_boton2 = img_boton2.resize((125, 140))
img_boton_tk2 = ImageTk.PhotoImage(img_boton2)

vpn_connected = False  # Variable global para verificar si la VPN está conectada

def connect_vpn():
    global vpn_connected
    try:
        # Ruta al ejecutable de OpenVPN GUI
        openvpn_gui_path = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
        # Nombre del perfil que ya está importado en OpenVPN GUI
        profile_name = "RedesUsap" # Cambia esto por el nombre exacto de tu perfil
        process = subprocess.run(
            [openvpn_gui_path, "--connect", profile_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Verificar si hubo algún error
        if process.returncode != 0:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la VPN. Error: {process.stderr}")
        else:
            vpn_connected = True
            messagebox.showinfo("Conexión VPN", "La VPN se ha conectado correctamente.")
            obtener_linea_base()  # Establecer la línea base al conectar la VPN
            reset_traffic_counters()  # Resetear contadores de tráfico
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró OpenVPN GUI. Verifica tu instalación.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

def disconnect_vpn():
    global vpn_connected
    try:
        # Ruta al ejecutable de OpenVPN GUI
        openvpn_gui_path = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
        # Nombre del perfil que ya está importado en OpenVPN GUI
        profile_name = "RedesUsap" # Cambia esto por el nombre exacto de tu perfil
        command = f'"{openvpn_gui_path}" --command disconnect "{profile_name}"'

        # Ejecutar OpenVPN GUI para desconectar el perfil
        process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Verificar si hubo algún error
        if process.returncode != 0:
            messagebox.showerror("Error de Desconexión", f"No se pudo desconectar la VPN. Error: {process.stderr}")
        else:
            vpn_connected = False
            messagebox.showinfo("Desconexión VPN", "La VPN se ha desconectado correctamente.")
            reset_traffic_counters()  # Reiniciar contadores de tráfico al desconectar
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró OpenVPN GUI. Verifica tu instalación.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
    finally:
        reset_traffic_counters()  # Asegurarse que siempre se reinicien los contadores

def reset_traffic_counters():
    global base_enviados, base_recibidos
    base_enviados = 0
    base_recibidos = 0
    label_trafico.config(text="Trafico de Datos\nEnviados: 0.00 MB\nRecibidos: 0.00 MB")

boton1_creado = None

# Función para el botón de encender
def boton1():
    global boton1_creado
    print("Botón ON presionado")
    delete_imgledonH()
    create_imgledoffH()
    delete_imgledoffA()
    create_imgledonA()
    if boton1_creado:
        boton1_creado.destroy()
    boton1_creado = boton
    connect_vpn()
    boton.destroy()

    def boton2def():
        print("Boton OFF presionado")
        boton2.destroy()
        delete_imgledoffH()
        create_imgledonH()
        delete_imgledonA()
        create_imgledoffA()
        boton12 = tk.Button(root, borderwidth=0, bg='black', image=img_boton_tk, command=boton1)
        boton12.place(x=973, y=405)
        global boton1_creado
        boton1_creado = boton12
        disconnect_vpn()

    boton2 = tk.Button(root, borderwidth=0, bg='black', image=img_boton_tk2, command=boton2def)
    boton2.place(x=1136, y=405)

# INFO DE TRÁFICO DE RED
label_trafico = tk.Label(root, bg="black", text="Trafico de Datos\nEnviados: 0.00 MB\nRecibidos: 0.00 MB", font=("Myriad Pro", 20), fg="white")
label_trafico.place(x=990, y=170)

# Variables para guardar la línea base
base_enviados = 0
base_recibidos = 0
linea_base_enviados = 0
linea_base_recibidos = 0

# Función para obtener la línea base
def bytes_a_mb(bytes_val):
    return f"{bytes_val / 1024 ** 2:.2f} MB"


# Función para obtener la línea base
def obtener_linea_base():
    global linea_base_enviados, linea_base_recibidos
    try:
        # Ejecutar el comando OpenVPN para obtener estadísticas iniciales
        command = 'netstat -e'
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            # Extraer estadísticas relevantes
            output = result.stdout
            for line in output.splitlines():
                if "Bytes" in line:
                    partes = line.split()
                    linea_base_enviados = int(partes[-2])
                    linea_base_recibidos = int(partes[-1])
                    break
    except Exception as e:
        print(f"Error al obtener línea base: {e}")

# Función para actualizar tráfico
def actualizar_trafico():
    global base_enviados, base_recibidos
    if vpn_connected:  # Verificar si la VPN está conectada
        try:
            # Ejecutar el comando OpenVPN para obtener estadísticas actuales
            command = 'netstat -e'
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            if result.returncode != 0:
                label_trafico.config(text="Error al obtener tráfico")
            else:
                output = result.stdout
                for line in output.splitlines():
                    if "Bytes" in line:
                        partes = line.split()
                        base_enviados = int(partes[-2]) - linea_base_enviados
                        base_recibidos = int(partes[-1]) - linea_base_recibidos
                        label_trafico.config(
                            text=f"Trafico de Datos\nEnviados: {bytes_a_mb(base_enviados)}\nRecibidos: {bytes_a_mb(base_recibidos)}"
                        )
                        break
        except Exception as e:
            label_trafico.config(text=f"Error al leer el tráfico: {e}")
    else:
        reset_traffic_counters()  # Reiniciar contadores si la VPN está desconectada

    # Actualizar tráfico cada 5 segundos
    root.after(5000, actualizar_trafico)

# Establecer línea base y actualizar tráfico
obtener_linea_base()
actualizar_trafico()

# MAPA CENTRAL
img_central = Image.open("./Mapa_mundi_Final.png")
img_central = img_central.resize((1300, 600), Image.LANCZOS)
img_central_tk = ImageTk.PhotoImage(img_central)
canvas.create_image(0, 0, anchor="nw", image=img_central_tk)

# TITULO NOMBRE APP
img_titulo = Image.open("./TITULO.png")
img_titulo = img_titulo.resize((230, 100))
img_titulotk = ImageTk.PhotoImage(img_titulo)
canvas.create_image(140, 70, image=img_titulotk)

# INFO TRAFICO DE RED
img_info = Image.open("./VPN_INFO.png")
img_info = img_info.resize((340, 293))
img_infotk = ImageTk.PhotoImage(img_info)
canvas.create_image(1120, 200, image=img_infotk)

#MARCO SWITCH BOTONES
img_sw = Image.open("./SWITCH_MARCO.png")
img_sw = img_sw.resize((360, 280))
img_sw_tk = ImageTk.PhotoImage(img_sw)
ksw = canvas.create_image(1120, 480, image=img_sw_tk)

#BOTON ON
img_boton = Image.open("./SWITCH_ENCENDIDO.png")
img_boton = img_boton.resize((125, 140))
img_boton_tk = ImageTk.PhotoImage(img_boton)
boton = tk.Button(root, borderwidth=0, bg='black', image=img_boton_tk, command=boton1)
boton.place(x=973, y=405)

#IMAGEN LED ON HONDURAS
img_ledontk = None
kledon = None
def create_imgledonH():
    global img_ledontk, kledon
    img_ledon = Image.open("./VPN_ENCENDIDO_LED.png")
    img_ledon = img_ledon.resize((31, 34))
    img_ledontk = ImageTk.PhotoImage(img_ledon)
    kledon = canvas.create_image(210, 350, image=img_ledontk)

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
    img_ledoff = Image.open("./VPN_APAGADO_LED.png")
    img_ledoff = img_ledoff.resize((31, 34))
    img_ledofftk = ImageTk.PhotoImage(img_ledoff)
    kledoff = canvas.create_image(210, 350, image=img_ledofftk)

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
    img_ledonA = Image.open("./VPN_ENCENDIDO_LED.png")
    img_ledonA = img_ledonA.resize((31, 34))
    img_ledonAtk = ImageTk.PhotoImage(img_ledonA)
    kledonA = canvas.create_image(480, 240, image=img_ledonAtk)

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
    img_ledoffA = Image.open("./VPN_APAGADO_LED.png")
    img_ledoffA = img_ledoffA.resize((31, 34))
    img_ledoffAtk = ImageTk.PhotoImage(img_ledoffA)
    kledoffA = canvas.create_image(480, 240, image=img_ledoffAtk)

def delete_imgledoffA():
    global kledoffA
    if kledoffA is not None:
        canvas.delete(kledoffA)
        kledoffA = None

create_imgledonH()
create_imgledoffA()

root.mainloop()
