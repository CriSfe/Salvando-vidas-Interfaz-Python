import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque


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
    