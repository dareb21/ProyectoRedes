#lIBRERIAS NECESARIAS PARA ESTO pip install requests paramiko psutil speedtest-cli matplotlib PyQt5 PyQtWebEngine

import tkinter as tk
from tkinter import messagebox, BooleanVar, Checkbutton, Frame
import requests
import time
import paramiko
import psutil
import speedtest
import matplotlib.pyplot as plt
import threading
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


#Inicio de ROOT
app = None
web = None
container = None
root=tk.Tk()
root.geometry('800x500')
root.title("Monitoreo de Red y Navegacion Privada")

#extras NO TOCAR, Si es necesario preguntar a Carlos
response = requests.get("https://api.ipify.org")
ip=response.text
My_Ip=tk.StringVar()
My_Ip.set(ip)
Vps_ip="161.97.134.102"
Vps_user="root"
Vps_pass="ArquitecturaEnRedes1"
monitoreo = True
ConsumoINarray = []
keywords = ["Download", "Upload","ms"]
chk_state=BooleanVar()
chk_state.set(False)
chk=Checkbutton(root,text="",variable=chk_state)


#Zona de funciones
def Browser():
    global app, web, container

    if app is None:
        app = QApplication(sys.argv)  # Crea la aplicación solo una vez
        web = QWebEngineView()  # Crea la vista web
        web.setUrl(QUrl("https://google.com"))  # Establece la URL

        # Crear el contenedor y asignar la vista web
        container = QWidget()
        container.setLayout(QVBoxLayout())
        container.layout().addWidget(web)
        container.setGeometry(0, 0, 1024, 800)
        container.show()

        # Ejecutar el ciclo de eventos de PyQt en un hilo separado
        def run_app():
            app.exec_()

        # Crear un hilo para la aplicación PyQt
        threading.Thread(target=run_app, daemon=True).start()

    else:
        # Si la aplicación ya está corriendo, solo mostrarla
        container.show()


def PrenderVpn():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(Vps_ip, username=Vps_user, password=Vps_pass)
        stdin, stdout, stderr = client.exec_command('curl https://api.ipify.org')
        time.sleep(1)
        output=stdout.read().decode('utf-8')
        use_thisip=output
        My_Ip.set(use_thisip)
        chk_state.set(True)
        print(My_Ip.get())
    except Exception as e:
            print(e)
    finally:
        client.close()
    return chk_state, use_thisip
def PrenderVpnHilo():
    PrenderVPN_hilo=threading.Thread(target=PrenderVpn)
    PrenderVPN_hilo.start()

def ApagarVpn():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        My_Ip.set(ip)
        chk_state.set(False)
        print(ip)
    except requests.RequestException as e:
        print(e)
    return chk_state
def ApagarVpnHilo():
    ApagarVPN_hilo=threading.Thread(target=ApagarVpn)
    ApagarVPN_hilo.start()

def Monitoreo():
    global monitoreo
    global ConsumoINarray
    byteIN_inicio = psutil.net_io_counters().bytes_recv

    while monitoreo:
        time.sleep(1)
        byteIn_Final = psutil.net_io_counters().bytes_recv
        consumoIN = (byteIn_Final - byteIN_inicio) / (1024 * 1024)
        print(f"Consumo Realizado: {consumoIN:.2f} MB")
        ConsumoINarray.append(consumoIN)
        byteIN_inicio = byteIn_Final

def MonitoreoHilo():
    Monitoreo_hilo=threading.Thread(target=Monitoreo)
    Monitoreo_hilo.start()

def Monitoreofin():
    global ConsumoINarray
    global monitoreo
    monitoreo = False
    time.sleep(1)
    tiempo=range(len(ConsumoINarray))
    graf=input("Desea graficar los resultados: (s/n)")
    if graf=="s":
        fig, axs = plt.subplots()
        axs.plot(tiempo, ConsumoINarray)
        axs.set(xlabel='tiempo (segundos)', ylabel='consumo (Mb)', title='Consumo')
        axs.grid()
        plt.savefig("consumo_red.png")
        plt.show()
    else:
        ConsumoINarray = []
    print("Monitoreo Finalizado")

def MonitoreofinHilo():
    Monitoreofin_hilo = threading.Thread(target=Monitoreofin)
    Monitoreofin_hilo.start()

def VelocidadRecursive():
    if chk_state.get() == False:
        st = speedtest.Speedtest()
        st.get_best_server()
        Vdown = st.download() / (1024 * 1024)
        Vup = st.upload() / (1024 * 1024)
        Lag = st.results.ping
        label_ST.config(text=f"Descarga: {Vdown:.2f} MB/s\nSubida: {Vup:.2f} MB/s\nLatencia: {Lag} ms")
        root.after(60000, VelocidadRecursive)
def VelocidadRecursiveHilo():
    VelocidadRecursive_hilo = threading.Thread(target=VelocidadRecursive)
    VelocidadRecursive_hilo.start()

###Esta funcion se usara solo si se implemeta el boton Test de velocidad (y en caso de usarla, usar el hilo), sino solo usar la recursiva
def Velocidad():
    if chk_state.get() == True:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(Vps_ip, username=Vps_user, password=Vps_pass)
        stdin, stdout, stderr = client.exec_command('speedtest-cli')
        time.sleep(1)
        output = stdout.read().decode('utf-8')
        print(output)
        client.close()
        filtered_output = [line for line in output.split('\n') if any(keyword in line for keyword in keywords)]
        for line in filtered_output:
            print(line)
    else:
        st = speedtest.Speedtest()
        st.get_best_server()
        Vdown = st.download() / (1024 * 1024)
        Vup = st.upload() / (1024 * 1024)
        Lag = st.results.ping
        label_ST.config(text=f"Descarga: {Vdown:.2f} MB/s\nSubida: {Vup:.2f} MB/s\nLatencia: {Lag} ms")
    return output
def MostrarVelocidad():
    Vdown, Vup, Lag = Velocidad()
    label_ST.config(text=f"Descarga: {Vdown:.2f} MB/s\nSubida: {Vup:.2f} MB/s\nLatencia: {Lag} ms")


def Navegacion():
    if chk_state.get() == True:
        try:
            #curl = f"curl https://www.{nav}.com"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(Vps_ip, username=Vps_user, password=Vps_pass)
            #stdin, stdout, stderr = client.exec_command(curl)
            time.sleep(1)
            #output = stdout.read().decode('utf-8')
            #print(output)
        except paramiko.SSHException as e:
            print(e)
        finally:
            client.close()
    else:
        Browser()


#Zona de labels
labelTitulo=tk.Label(root, text="Monitoreo de Red y Navegacion Privada", font=("Arial", 20, "bold"))
labelTitulo.place(x=150, y=0)
labelTextIp=tk.Label(root, text="Ip Actual: ", font=("Arial", 12, "bold"))
labelTextIp.place(x=10, y=50)
labelIp=tk.Label(root,textvariable=My_Ip, font=("Arial", 12))
labelIp.place(x=100, y=50)
label_ST=tk.Label()
label_ST.place(x=150, y=300)

#Zona de botones
Btn_PrenderVPN=tk.Button(root, text="Prender VPN",bg="green",fg="white",font=("Arial", 12), command=PrenderVpnHilo)
Btn_PrenderVPN.place(x=250, y=50)
Btn_ApagarVPN=tk.Button(root, text="Apagar VPN",bg="red",fg="white",font=("Arial", 12),command=ApagarVpnHilo)
Btn_ApagarVPN.place(x=390, y=50)
Btn_Monitoreo=tk.Button(root, text="Realizar Monitoreo en tiempo real",font=("Arial", 12,"bold"),command=MonitoreoHilo)
Btn_Monitoreo.place(x=10, y=100)
Btn_MonitoreoFin=tk.Button(root, text="Terminar Monitoreo en tiempo real",font=("Arial", 12,"bold"),command=MonitoreofinHilo)
Btn_MonitoreoFin.place(x=150, y=100)
Btn_Velocidad=tk.Button(root, text="Test de velocdidad de conexion",font=("Arial", 12,"bold"), command=Velocidad)
Btn_Velocidad.place(x=10, y=150)
Btn_Navegacion=tk.Button(root, text="Navegacion",font=("Arial", 12,"bold"),command=Navegacion)
Btn_Navegacion.place(x=10, y=200)

VelocidadRecursiveHilo()

root.mainloop()
