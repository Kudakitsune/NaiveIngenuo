from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import DoubleVar
from tkinter import Canvas
from tkinter import IntVar
from tkinter import Label
from tkinter import Entry
from tkinter import Menu
from tkinter import Tk
from tkinter import simpledialog
import numpy as np
from numpy import matrix
import matplotlib.pyplot as plt
import pandas as pd

ventana = Tk()
ancho = 300#w
alto = 250#h
extraAncho=ventana.winfo_screenwidth() - ancho
extraAlto=ventana.winfo_screenheight() - alto
ventana.geometry("%dx%d%+d%+d" % (ancho, alto, extraAncho / 2, extraAlto / 2))

canvas = Canvas(ventana, width=300, height=250)
canvas.pack()

ventana.title("Interfaz")
entrada=StringVar()
Entry(ventana, textvariable = entrada, width = 47).place(x=5, y=65)
Label(text = "Ingrese los Patrones delimiatados por comas", font= ("Arial",11)).place(x=0, y=20)

#Funciones----------------------------------------------

def Abrir():
    ventana.filename = filedialog.askopenfilename(title = "Elige tu archivo:")
    ruta=ventana.filename

    Matriz=[]
    enca=[]

    with open(ruta,'r') as archivo:
        lineas=archivo.read().splitlines()
        enca=lineas[0]
        lineas.pop(0)#sacamos el encavezado
        
        for i in lineas:
            linea=i.split(',')
            Matriz.append(linea)
            pass#final de for i
        
        #print(Matriz)
        pass#final de with
    #hay que separar por numero de clases, para eso la MatrizClases
    MatrizAux=Separa(Matriz)
    #print(len(MatrizAux))#prueba para saber si jaló la estructura
    #print(MatrizAux[0][0])#prueba para ver si si tiene datos la estructura.

    patron=str(entrada.get())#el patron sin delimitar
    clasi=patron.split(',')#el patron ya delimitado por comas.
    
    #prueba=['lluvia', 'templado','normal','si']
    #prueba=['nublado', 'calor','alta','no']
    Clasificar(clasi,MatrizAux)


    pass#final de Abrir

def Separa(Matriz):
    Matriz2=[]#será una matriz de matrices
    clases=0
    vectorAuxiliarRepetidos=[]
    vectorAuxiliarUnicos=[]
    #print(len(Matriz))#para saber cuantos registros hay.
    for i in range(len(Matriz)):
        #print(Matriz[i][0])#primer columna
        vectorAuxiliarRepetidos.append(Matriz[i][0])
        pass
    #print(vectorAuxiliarRepetidos)
    vectorAux = set(vectorAuxiliarRepetidos)#set es un conjunto de elementos UNICOS e irrepetibles (como tabla hash) pero que es inalterable
    #se le pueden aplicar operaciones pero es complicado.
    vectorAuxiliarUnicos = list(vectorAux)#transformamos el set en una lista, la cual si se manejar, para eso es list()
    vectorAuxiliarUnicos.sort()#esto fue por que por alguna razon a veces cambiaba el orden de entrada, no se por que, pero ordenado
    #alfabeticamente ya mantiene un orden. Nota: investigar por que no jala esta madre sin el sort.
    print("Clases:\n")
    print(vectorAuxiliarUnicos)
    #ya tenemos un vector con las clases unicas, para contarlas solo hace falta usar el len()

    for i in range(len(vectorAuxiliarUnicos)):#aqui vamos de 0 a la cantidad de clases que hay
        MatrizAux=[]#para ser una lista temporal para cada clase que se guardará en Matriz2
        print("Clase: "+str(i+1))
        for j in range(len(Matriz)):#aqui ya vamos a recorrer las filas de la matriz original.
            print(Matriz[j][0])#este es para saber cuales con las filas y columnas en la matriz, el primer elemento son filas, luego columnas.
            if vectorAuxiliarUnicos[i] == Matriz[j][0]:
                MatrizAux.append(Matriz[j])
                print(Matriz[j])#para saber que estoy metiendo              
                pass#fin if
            pass#fin for j
        Matriz2.append(MatrizAux)#guardamos una matriz temporal en la matriz2 y asi a la siguiente iteracion ya se refresca la temporal pero se
        #mantuvo la anterior resguardada en matriz2.
        pass#fin for i
    
    #ahora matriz2 es una matriz de matrices.
    return Matriz2#ahora regresamos el objeto.
    pass

def Clasificar(patron, MatrizClases):
    #encabezados=encavezado.split(',')
    #encabezados.pop(0)
    #recordar que patron no tiene id, entonces el saltarnos el id puede darnos error
    MatrizAtributos=[]
    for i in range(len(MatrizClases)):#for para recorrer las clases.
        #print("clase "+str(i+1))
        MatrizAux=[]
        for j in range(1,len(MatrizClases[i][0])):#ahora vamos por columnas en lugar de filas. el 1 antes de "len" es para saltar la columna "id"
            contador=0
            for k in range(len(MatrizClases[i])):
                #print(MatrizClases[i][k][j])
                if MatrizClases[i][k][j] == patron[j-1]:
                    contador=contador+1
                    pass                           
                pass#fin for k
            #print(str(patron[j-1])+": "+str(contador)+"/"+str(len(MatrizClases[i])))#para saber si los numeros concuerdan
            MatrizAux.append((contador/len(MatrizClases[i])))
            pass#fin for j
        MatrizAtributos.append(np.asarray(MatrizAux,dtype=float))
        pass#fin for i

    TotalElementos=0
    for i in range(len(MatrizClases)):
        TotalElementos=TotalElementos+len(MatrizClases[i])
        pass
    
    Operaciones(MatrizAtributos,TotalElementos,MatrizClases)

    pass

def Operaciones(MatrizATRIB,ElementosTotales,MatrizClass):
    numeradores=[]
    denominador=0
    for i in range(len(MatrizATRIB)):
        #print(MatrizClases[i])
        auxiliar=1
        for j in range(len(MatrizATRIB[i])):
            auxiliar=auxiliar*MatrizATRIB[i][j]
            pass#fin for j
        #print(auxiliar)
        numeradores.append( ( (len(MatrizClass[i]))/ElementosTotales ) * auxiliar )
        pass#fin for i

    for i in range(len(numeradores)):
        denominador=denominador+numeradores[i]
        pass#fin for i
    #print(denominador)
    
    #------segmento para saber las clases por que don pendejo se le olvidó jalarlo desde hace tres metodos
    vectorAuxiliarUnicos=[]
    for i in range(len(MatrizClass)):
        vectorAuxiliarUnicos.append(MatrizClass[i][0][0])
        pass
    vectorAuxiliarUnicos.sort()
    print("Clases: ")
    print(vectorAuxiliarUnicos)
    #------------------------------------------------------------------------------------------------------
    
    Pertenencia=[]

    for i in range(len(numeradores)):
        Pertenencia.append( (numeradores[i]/denominador)*100 )
        pass
    print(Pertenencia)
    menorIndice=Pertenencia.index(max(Pertenencia))
    print(menorIndice)
    print("El vector pertenece a la clase: "+str(vectorAuxiliarUnicos[menorIndice]))

    pass

#menus--------------------------------------------------
barraMenu = Menu(ventana)
mnuU1 = Menu(barraMenu,tearoff=0)#menu de archivos.
#creacion de los elementos de los menus-------------------------
mnuU1.add_command(label = "abrir archivo", command = Abrir)#me falta el comand
mnuU1.add_separator()
mnuU1.add_command(label = "Salir", command = ventana.destroy)
#asignacion de menus en una barra-------------------------------
barraMenu.add_cascade(label = "Archivo", menu = mnuU1)#menu base
#------------------

ventana.config(menu = barraMenu)
ventana.mainloop()