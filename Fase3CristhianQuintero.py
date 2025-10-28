import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque
import json


#----- Clase para las estructuras de datos -----

class Pila:
    #--- Implementación de una pila (LIFO) ---
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
class Cola:
    #--- Implementación de una cola(FIFO) ---
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

class Nodo:
    #--- Nodo para la lista enlazada ---
    def __init__(self,dato):
        self.dato = dato
        self.siguiente = None

class Lista:
    #--- Implementación de la lista ----
    def __init__(self):
        self.cabeza = None
    
    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_todos(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado
    
    def buscar(self, id_paciente):
        actual = self.cabeza
        while actual:
            if actual.dato.ge('id_numero') == id_paciente:
                return actual.dato
            actual = actual.siguiente
        return None
    

#----- Clases para la gestión de pacientes -----
class Paciente:
    #--- Datos de los copagos ---
    copago_medicina_general = [
        {"Estrato": "1", "Valor Del Copago": 0},
        {"Estrato": "2", "Valor Del Copago": 0},
        {"Estrato": "3", "Valor Del Copago": 10000},
        {"Estrato": "4", "Valor Del Copago": 15000},
        {"Estrato": "5", "Valor Del Copago": 20000},
        {"Estrato": "6", "Valor Del Copago": 30000}
    ]
    copago_laboratorio = [
        {"Estrato": "1", "Valor Del Copago": 0},
        {"Estrato": "2", "Valor Del Copago": 0},
        {"Estrato": "3", "Valor Del Copago": 0},
        {"Estrato": "4", "Valor Del Copago": 5000},
        {"Estrato": "5", "Valor Del Copago": 10000},
        {"Estrato": "6", "Valor Del Copago": 20000}
    ]

    def __init__ (self, tipo_id, numero_id, nombre, edad, estrato, tipo_atencion, fecha_ingreso):
        self.tipo_id = tipo_id
        self.numero_id = numero_id
        self.nombre = nombre
        self.edad = edad
        self.estrato = estrato
        self.tipo_atencion = tipo_atencion
        self.copago = self.calcular_copago()
        self.fecha_ingreso = fecha_ingreso 

    def calcular_copago(self):
        if self.tipo_atencion == "Medicina General":
            tabla_copago = Paciente.copago_medicina_general
        elif self.tipo_atencion == "Laboratorio":
            tabla_copago = Paciente.copago_laboratorio
        else:
            return 0
        
        for item in tabla_copago:
            if item["Estrato"] == self.estrato:
                return item["Valor del Copago"]
        return 0

#-- Convertir al paciente en diccionario

    def to_diccio(self):
        return {
            'tipo_id': self.tipo_id,
            'id_numero': self.numero_id,
            'nombre': self.nombre,
            'edad': self.edad,
            'estrato': self.estrato,
            'tipo_atencion': self.tipo_atencion,
            'copago': self.copago,
            'fecha_ingreso': self.fecha_ingreso
        }

#--- Clase para gestionar los pacientes de acuerdo a la estructura de dato ----
class GestorPacientes:
    def __init__(self):
        self.lista_pacientes = Lista()
        self.pila_operaciones = Pila()
        self.cola_espera = Cola() 

    def agregarPaciente(self, paciente):
        self.lista_pacientes.insertar(paciente.to_diccio())
        self.pila_operaciones.push(('agregar', paciente.numero_id))
        self.cola_espera.enqueue(paciente.numero_id)

    def obtenerPaciente(self):
        self.lista_pacientes.obtener_todos()

    def buscarPaciente(self, numero_id):
        self.lista_pacientes.buscar(numero_id)

    def deshacerUltimaOperacion(self):
        if not self.pila_operaciones.is_empty():
            return self.pila_operaciones.pop()
        return None
    

#-------------Clase para las ventanas de la interfaz----------------------#

class VentanaLogin(tk.Tk):
    #-----Inicio de la ventana de Login----#
    def __init__(self):
        super().__init__()
        self.title("Login - EPS Salvando Vidas")
        self.geometry("500x300")
        self.configure(bg="#f0f0f07f")
        self.resizable(False, False)

        self.crearinterfaz()
    
    def crear_interfaz(self):
        