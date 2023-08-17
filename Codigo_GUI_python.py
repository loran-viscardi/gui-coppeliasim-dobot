#Importa as librarys utilizadas
from tkinter import *
from tkinter import messagebox
import sim
import time
import math
#Atribui à GUI_Host, funções para controle/programa da GUI
GUI_Host = Tk()
#Cria a classe para a GUI
class GUI(Frame):
    scales_l = []
    labels_l = []
    handles = []
    boolConnect = False
    clientID = -1
    base = 'Dobot_motor'
    #Define a inicialação da GUI
    def __init__(gui):
        super().__init__()
        gui.initUI()
    #Específica todos parâmetros de exibição da GUI
    def initUI(gui):
        gui.master.title("Controle Dobot Magician")
        gui.master.configure(bg='green')
        fonte=('Comic_Sans', 8, 'bold')
        for i in range(4):
            tit = "Junta"+str(i+1)
            w_label = Label(gui.master, text=tit, font=fonte, fg='white', bg='green').grid(row=i, column=0, pady=4, padx = 4)
            w_label = Label(gui.master, text="IFSP Catanduva - Loran Viscardi", font=fonte, fg='white', bg='green').grid(row=10,column=1,pady=4,padx=4)
            win = Scale(gui.master, from_=-100, to=100, tickinterval= 20, orient=HORIZONTAL, resolution=1, length=450, command=lambda value, name=i: gui.onScale(name, value), fg='white', bg='green', highlightbackground='white')
            win.set(0)
            win.grid(row=i, column=1)

            gui.scales_l.append(win)
            gui.labels_l.append(w_label)

        gui.conectar = Button(gui.master, text ="Conectar", command = gui.onConnect, fg='white', bg='green', font=fonte)
        gui.conectar.grid(row=8,column=1)
                
    def onScale(gui, name,value):
        if(gui.clientID != -1):
            print("{} : {}".format(name, value))
            obj = gui.handles[int(name)]
            ang = float(value)*math.pi/180
            sim.simxSetJointTargetPosition(gui.clientID, obj ,ang ,sim.simx_opmode_oneshot)


    def onConnect(gui):
        if gui.clientID != -1:
            return
            
        gui.clientID = sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        if gui.clientID == -1:
            messagebox.showinfo( "Não foi possível se conectar ao servidor")
        else:

            for i in range(4):
                j = i + 1
                nome = gui.base + str(j)
                _, handle=sim.simxGetObjectHandle(gui.clientID, nome, sim.simx_opmode_oneshot_wait)
                gui.handles.append(handle)
            time.sleep(1)
            print("Conectado! Enviando comandos ao robô")

def close_window():
  print("Fecha todas conexões")
  sim.simxFinish(-1) 
  GUI_Host.destroy()

def main():
    GUI_Host.protocol("WM_DELETE_WINDOW", close_window)
    ex = GUI()
    GUI_Host.geometry("550x300")
    GUI_Host.mainloop()


if __name__ == '__main__':
    main()
