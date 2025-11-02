import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque
from tkcalendar import DateEntry



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
    
    def is_empty(self):
        return len(self.items) == 0
    
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
            if actual.dato.get('id_numero') == id_paciente:
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
                return item["Valor Del Copago"]
        return 0

#-- Convertir los datos del paciente en diccionario

    def to_dict(self):
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

#--- Clase para gestionar los pacientes de acuerdo a la estructura de datos ----
class GestorPacientes:
    def __init__(self):
        self.lista_pacientes = Lista()
        self.pila_pacientes = Pila()
        self.cola_pacientes = Cola()
        self.pila_operaciones = Pila()  #Para deshacer las operaciones
        self.estructura_actual = "Lista Enlazada" #Estructura por defecto

    def agregarPaciente(self, paciente, estructura):

        paciente_dict = paciente.to_dict()

        if estructura == "Lista Enlazada":
            self.lista_pacientes.insertar(paciente_dict)
        elif estructura == "Pila":
            self.pila_pacientes.push(paciente_dict)
        elif estructura == "Cola":
            self.cola_pacientes.enqueue(paciente_dict)
        
        self.estructura_actual = estructura
        self.pila_operaciones.push(('agregar', paciente.numero_id))

    def obtenerPacientes(self, estructura=None):
        #-------Obtiene todos los pacientes según la estructura
        if estructura is None:
            estructura = self.estructura_actual
        
        if estructura == "Lista Enlazada":
            return self.lista_pacientes.obtener_todos()
        elif estructura == "Pila":
            return list(reversed(self.pila_pacientes.items))
        elif estructura == "Cola":
            return list(self.cola_pacientes.items)
        return []

    def buscarPaciente(self, numero_id):
        self.lista_pacientes.buscar(numero_id)

    def deshacerUltimaOperacion(self):
        if not self.pila_operaciones.is_empty():
            return self.pila_operaciones.pop()
        return None
    

#-------------Clases para las ventanas de la interfaz----------------------#

#-------------Ventana PopUp Acerca de------------------#

class VentanaAcercaDe(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acerca de")
        self.geometry("400x300")
        self.configure(bg="#e8f4f8")
        self.resizable(False, False)

        #Centrar la ventana
        self.transient(parent)
        self.grab_set()

        self.crear_interfaz()

    def crear_interfaz(self):
        #Crear el frame principal
        frame_principal = ttk.Frame(self, padding="30")
        frame_principal.pack(expand=True, fill=tk.BOTH)

        #Titulo de la aplicación
        titulo = tk.Label(frame_principal, text="EPS SALVANDO VIDAS", font=("Arial", 18, "bold"), bg="#e8f4f8", fg="#2c5aa0")
        titulo.pack(pady=(0,20))

        #Separador
        separador = ttk.Separator(frame_principal, orient='horizontal')
        separador.pack(fill=tk.X, pady=10)

        #Informacion de creador
        tk.Label(frame_principal,
                text="Estudiante:",
                font=("Arial", 10, "bold"),
                bg='#e8f4f8',
                fg='#555555').pack(pady=(10, 5))
        
        tk.Label(frame_principal,
                text="Cristhian Fernando Quintero Holguín",
                font=("Arial", 12),
                bg='#e8f4f8',
                fg='#2c5aa0').pack()
        
        tk.Label(frame_principal,
                text="Grupo:",
                font=("Arial", 12),
                bg='#e8f4f8',
                fg='#2c5aa0').pack()

        tk.Label(frame_principal,
                text="114",
                font=("Arial", 12),
                bg='#e8f4f8',
                fg='#2c5aa0').pack()
        
        #Salir de la ventana
        ttk.Button(frame_principal, text="Cerrar", command=self.destroy).pack(pady=(10, 0))


#-----Inicio de la ventana de Login----#
class VentanaLogin(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Login - EPS Salvando Vidas")
        self.geometry("500x350")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        self.crear_interfaz()
    
    def crear_interfaz(self):
        #frame principal
        frame_principal = ttk.Frame(self, padding="20")
        frame_principal.pack(expand=True)

        #Título
        titulo = ttk.Label(frame_principal, text="Ingresar - EPS Salvando Vidas", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)

        #Boton de Acerca de (falta la ventana popup)
        acerca_de = ttk.Button(frame_principal, command=self.abrir_acerca_de, text="Acerca de")
        acerca_de.pack(pady=20)

        #Contraseña
        ttk.Label(frame_principal, text="Contraseña:").pack(anchor='w', pady=(20,0))
        self.entrada_contrasena = ttk.Entry(frame_principal, width=30, show="*")
        self.entrada_contrasena.pack(pady=5)

        #Botones
        frame_botones = ttk.Frame(frame_principal)        
        frame_botones.pack(pady=30)

        ttk.Button(frame_botones, text="Ingresar", command=self.validar_login).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Salir", command=self.quit).pack(side = tk.LEFT, padx=5)

    #metodo para abrir la clase VentanaAcercaDe
    def abrir_acerca_de(self):
        VentanaAcercaDe(self)
        

    #Validar las credenciales
    def validar_login(self):
        contrasena = self.entrada_contrasena.get()

        if contrasena == "unad":
            gestor = GestorPacientes()
            ventana_control = VentanaControlUsuario(self, gestor)
            self.withdraw() 
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
            self.entrada_contrasena.delete(0, tk.END)
            self.entrada_contrasena.focus()


#------------------Clase de la ventana principal----------------#
class VentanaControlUsuario(tk.Toplevel):
    def __init__(self, parent, gestor):
        super().__init__(parent)
        self.parent = parent
        self.gestor = gestor
        self.estructura_seleccionada = "Lista Enlazada"
        self.title("Control de Usuarios")
        self.geometry("1200x800")
        self.configure(bg='#f0f0f0')

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame superior - Formulario
        frame_formulario = ttk.LabelFrame(self, text="Formulario de Ingreso de Paciente", 
                                         padding="10")
        frame_formulario.pack(fill=tk.X, padx=10, pady=10)
        
        self.crear_formulario(frame_formulario)

        
        # Frame de control de las estructuras y la visualización
        frame_control = ttk.Frame(self)
        frame_control.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_control, text="Ver estructura:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.combo_ver_estructura = ttk.Combobox(frame_control, values=["Lista Enlazada", "Pila", "Cola"], state='readonly', width=18)
        self.combo_ver_estructura.bind('<<ComboboxSelected>>', self.cambiar_visualizacion)
        self.combo_ver_estructura.pack(side=tk.LEFT, padx=5)
        self.combo_ver_estructura.set(self.estructura_seleccionada)

        ttk.Label(frame_control, text="Estructura activa:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(30, 5))

        self.label_estructura = ttk.Label(frame_control, text=self.estructura_seleccionada, foreground= "blue", font=("Arial", 10, "bold"))
        self.label_estructura.pack(side=tk.LEFT, padx= 5)
        
        # Botones de acción
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="Actualizar Tabla", command=self.actualizar_tabla).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Deshacer", command=self.deshacer_operacion).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Salir", command=self.salir_aplicacion).pack(side=tk.LEFT, padx=5)
    

        #Frame inferior - Tabla
        frame_tabla = ttk.LabelFrame(self, text="Registro de Paciente", padding="10")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.crear_tabla(frame_tabla)

        
    def crear_formulario(self, parent):
        #Escoger la estructura
        ttk.Label(parent, text="Estructura:").grid(row=0, column=0, sticky='w', padx=(20,0))
        self.combo_estructura = ttk.Combobox(parent, values=["Lista Enlazada", "Pila", "Cola"], state='readonly', width=18)
        self.combo_estructura.set(self.estructura_seleccionada)
        self.combo_estructura.grid(row=0, column=1, padx=5, pady=5)
        
        #Escoger el tipo de documento
        ttk.Label(parent, text="Tipo de Documento:").grid(row=1, column=0, sticky='W', pady=5)
        self.combo_tipo_id = ttk.Combobox(parent, values=["CC", "TI", "Pasaporte"], state='readonly', width=15)
        self.combo_tipo_id.grid(row=1, column=1, padx=5, pady=5)

        #Insertar el documento
        ttk.Label(parent, text="Número ID:").grid(row=2, column=0, sticky='w', padx=(20,0))
        self.entrada_numero_id = ttk.Entry(parent, width=20)
        self.entrada_numero_id.grid(row=2, column=1, padx=5, pady=5)

        #Nombre
        ttk.Label(parent, text="Nombre:").grid(row=3, column=0, sticky='w', pady=5)
        self.entrada_nombre = ttk.Entry(parent, width=25)
        self.entrada_nombre.grid(row=3, column=1, padx=5, pady=5)
        
        #Edad
        ttk.Label(parent, text="Edad:").grid(row=4, column=0, sticky='w', padx=(20,0))
        self.entrada_edad = ttk.Entry(parent, width=20)
        self.entrada_edad.grid(row=4, column=1, padx=5, pady=5)

        #Estrato
        ttk.Label(parent, text="Estrato:").grid(row=5, column=0, sticky='w', pady=5)
        self.combo_estrato = ttk.Combobox(parent, values=["1", "2", "3", "4", "5", "6"], state='readonly', width=15)
        self.combo_estrato.grid(row=5, column=1, padx=0, pady=5)

            #Evento para actualizar el copago cuando cambie el estrato
        self.combo_estrato.bind('<<ComboboxSelected>>', self.actualizar_copago_preview)

        #Atencion
        ttk.Label(parent, text="Tipo de Atención:").grid(row=6, column=0, sticky='w', padx=(20,0))
        self.combo_atencion = ttk.Combobox(parent, values=["Medicina General", "Laboratorio"], state='readonly', width=20)
        self.combo_atencion.grid(row=6, column=1, padx=0, pady=5)
            #Evento para actualizar el copago cuando cambie el tipo de atención
        self.combo_atencion.bind('<<ComboboxSelected>>', self.actualizar_copago_preview)

        #Copago (row=7)
        ttk.Label(parent, text="Copago:").grid(row=7, column=0, sticky='W', pady=5)
        self.entrada_copago = ttk.Entry(parent, width=15)
        self.entrada_copago.insert(0, "$0")
        self.entrada_copago.config(state='readonly')
        self.entrada_copago.grid(row=7, column=1, padx=0, pady=5)


        #Fecha (row=8)
        ttk.Label(parent, text="Fecha Ingreso:").grid(row=8, column=0, sticky='w', padx=(20,0))
        
        self.entrada_fecha = DateEntry(parent, width= 18, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy', locale='es_ES')
        self.entrada_fecha.grid(row=8, column=1, padx=5, pady=5, sticky='W')

        


        #Botones (Registrar / Limpiar) (row=9)
        frame_botones_form = ttk.Frame(parent)
        frame_botones_form.grid(row=9, column=0, columnspan=4, pady=15)

        ttk.Button(frame_botones_form, text="Registrar Paciente", command=self.registrar_paciente).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones_form, text="Limpiar Registro", command=self.limpiar_formulario).pack(side=tk.LEFT, padx=5)



    def crear_tabla(self, parent):
        frame_scroll = ttk.Frame(parent)
        frame_scroll.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(frame_scroll)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = ttk.Scrollbar(frame_scroll, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview

        columnas = ("Tipo ID", "ID", "Nombre", "Edad", "Estrato", "Tipo atención", "Copago", "Fecha Ingreso")
        self.tabla = ttk.Treeview(frame_scroll, columns=columnas, height=12, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.heading("#0", text="Datos de Usuarios")
        
        for col in columnas:
            self.tabla.column(col, anchor=tk.CENTER, width=110)
            self.tabla.heading(col, text=col)
        
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)
        
        self.tabla.pack(fill=tk.BOTH, expand=True)

    def actualizar_copago_preview(self, event=None):

                    estrato = self.combo_estrato.get()
                    tipo_atencion = self.combo_atencion.get()
                    
                    if estrato and tipo_atencion:
                        # Crear un paciente temporal solo para calcular el copago
                        paciente_temp = Paciente(
                            tipo_id="",
                            numero_id="",
                            nombre="",
                            edad=0,
                            estrato= estrato,
                            tipo_atencion=tipo_atencion,
                            fecha_ingreso=""
                        )
                        
                        copago = paciente_temp.calcular_copago()
                        self.entrada_copago.config(state='normal')
                        self.entrada_copago.delete(0, tk.END)
                        self.entrada_copago.insert(0, f"${copago:,}")
                        self.entrada_copago.config(state='readonly')

    def registrar_paciente(self):
        try:
            if not all([self.combo_tipo_id.get(), self.entrada_numero_id.get(), self.entrada_nombre.get(), self.entrada_edad.get(),
                       self.combo_estrato.get(), self.combo_atencion.get()]):
                messagebox.showwarning("Advertencia", "Completa todos los campos")
                return
            
            estructura_seleccionada = self.combo_estructura.get()

            #Obtener la fecha del DataEntry
            try:
                fecha_seleccionada = self.entrada_fecha.get_date().strftime("%d-%m-%Y")
            except Exception as e:
                messagebox.showerror("Error", "Fecha de ingreso inválida. Por favor seleccione una fecha válida.")
                return
            
            paciente = Paciente(
                tipo_id=self.combo_tipo_id.get(),
                numero_id=self.entrada_numero_id.get(),
                nombre=self.entrada_nombre.get(),
                edad=int(self.entrada_edad.get()),
                estrato=self.combo_estrato.get(),
                tipo_atencion=self.combo_atencion.get(),
                fecha_ingreso= fecha_seleccionada
            )
            
            self.gestor.agregarPaciente(paciente, estructura_seleccionada)
            self.estructura_seleccionada = estructura_seleccionada
            self.label_estructura.config(text=estructura_seleccionada)
            
            messagebox.showinfo("Éxito", 
                              f"Paciente registrado en: {estructura_seleccionada}")
            self.limpiar_formulario()
            self.actualizar_tabla()
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número")

   
    def limpiar_formulario(self):
        """Limpia los campos del formulario"""
        self.combo_tipo_id.set('')
        self.entrada_numero_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_edad.delete(0, tk.END)
        self.combo_estrato.set('')
        self.combo_atencion.set('')
        self.entrada_copago.config(state='normal')
        self.entrada_copago.delete(0, tk.END)
        self.entrada_copago.insert(0, "$0")
        self.entrada_copago.config(state='readonly')
        self.entrada_fecha.set_date(datetime.now())

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        estructura_visualizar = self.combo_ver_estructura.get()
        pacientes = self.gestor.obtenerPacientes(estructura_visualizar)
        
        for paciente in pacientes:
            valores = (
                paciente['tipo_id'],
                paciente['id_numero'],
                paciente['nombre'],
                paciente['edad'],
                paciente['estrato'],
                paciente['tipo_atencion'],
                f"${paciente['copago']:,}",
                paciente['fecha_ingreso']
            )
            self.tabla.insert('', tk.END, values=valores)
    
    def cambiar_visualizacion(self, event=None):
        self.actualizar_tabla()
    
    def deshacer_operacion(self):
        operacion = self.gestor.deshacerUltimaOperacion()
        if operacion:
            messagebox.showinfo("Deshacer", f"Operación deshecha: {operacion}")
            self.actualizar_tabla()
        else:
            messagebox.showwarning("Advertencia", "No hay operaciones para deshacer")
    
    
    def salir_aplicacion(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir de la aplicación?"):
            self.parent.destroy()

#-----------------punto de incio-----------------------#
if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()