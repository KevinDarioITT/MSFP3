# Práctica tres: Modelado y control del sistema musculoesquelético

# Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
# Tecnológico Nacional de México [TecNM - Tijuana]
# Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

# Nombre del alumno: Kevin Dario De La Cruz Bojorquez
# Número de control: 20210777
# Correo institucional: l20210777@tijuana.tecnm.mx

# Asignatura: Modelado de Sistemas Fisiológicos
# Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx

# Instalar librerias en consola
# pip install numpy control matplotlib

# Librerias
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulacion
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
F = np.zeros(N); F[round(1/dt):round(2/dt)] = 1    

# Parametros del circuito Control y Caso
alpha = 0.25
Cs,Cp = 10E-6, 100E-6
R_control, R_caso = 100, 10E3

# Funcion de transferencia:
def planta(R,Cs,Cp,alpha):
    num = [Cs*R, 1-alpha]
    den = [R*(Cp+Cs), 1]
    return ctrl.tf(num,den)

sysControl = planta(R_control,Cs,Cp,alpha)
sysCaso = planta(R_caso,Cs,Cp,alpha)
print(f"Funcion de transferencia (Control): {sysControl}\n")
print(f"Funcion de transferencia (Caso): {sysCaso}\n")

# Parametros del controlador PID 
kP,kI,kD,Nf = 0.223904745099563, 3558.19126457357, 0, 100
numPID = [kP,kI]                 
denPID = [1,0]
PID = ctrl.tf(numPID,denPID)      
print(f"Ganancia proporcional kP: {kP}\n")
print(f"Ganancia integral kI: {kI}\n")

# Sistema de control en lazo cerrado (planta: Caso)
sysPID = ctrl.feedback(ctrl.series(PID,sysCaso),1,sign = -1)
print(f"Funcion de transferencia en lazo cerrado: {sysPID}\n")

# Colores
clr1 = np.array([0,114,189])/255
clr2 = np.array([237,177,32])/255
clr3 = np.array([34,139,34])/255
clr4 = np.array([0.5,0.5,0.5])/255

# Funciones de respuesta
def respuesta(t,sys,u):
    _,y = ctrl.forced_response(sys,t,u,x0)
    return y

# Respuestas: Simulaciones numericas
Fs_control = respuesta(t,sysControl,F)              
Fs_caso = respuesta(t,sysCaso,F)                     
PIDu = respuesta(t,sysPID,Fs_control)                

fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,F,'-',linewidth=0.75,color=clr1,label=r'$F(t)$')
plt.plot(t,Fs_control,'--',linewidth=0.75,color=clr2,label=r'$F_s(t):Control$')
plt.plot(t,Fs_caso,'--',linewidth=0.75,color=clr3,label=r'$F_s(t):Caso$')
plt.plot(t,PIDu,':',linewidth=1.5,color=clr4,label=r'$PID(t):Tratamiento$')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.round(np.arange(-0.1,1.2,0.1),1))
plt.tick_params(direction='in',top=True,right=True)
plt.xlabel(r'$t$ [s]')
plt.ylabel(r'$F(t)$ [V]')
plt.legend(bbox_to_anchor=(0.5,1.08),loc='center',ncol=4,frameon=False)
fg.savefig('Respuestas_python.pdf',bbox_inches='tight')
plt.show()