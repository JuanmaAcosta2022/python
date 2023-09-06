import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import re
import sqlite3


#clase central
class Vista:
    def __init__(self, modelo):
        self.ventana = tk.Tk()
        self.ventana.title("Pet's")
        self.ventana.geometry("800x600")
        self.registrar_boton = tk.Button(self.ventana, text="Registrar")
        self.registrar_boton.pack() 
        self.modelo = modelo  # Guarda el modelo (Database) en el atributo
        
     # Crear el árbol   
    def actualizar_treeview(self, arbolview):
        arbolview.delete(*arbolview.get_children())

        sql = "SELECT * FROM perritos ORDER BY id ASC"
        con = self.conexion()
        cursor = con.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        for x in resultado:
            arbolview.insert("", "end", text=x[0], values=(x[1], x[2], x[3]))
                
    def mostrar_reporte(self):
        messagebox.showinfo("Reporte enviado", "Tu reporte ha sido enviado")

    def cambiar_color_fondo(self):
        colores = ["red", "green", "blue", "yellow", "pink", "purple", "orange"]
        color_fondo = random.choice(colores)
        self.ventana.configure(bg=color_fondo)
       
        tree = ttk.Treeview(self.ventana)
        tree['columns'] = ('raza', 'edad', 'nombre')
        tree.heading('#0', text='ID')
        tree.heading('raza', text='Raza')
        tree.heading('edad', text='Edad')
        tree.heading('nombre', text='Nombre')

        # BOTON DE REPORTE
        reporte_boton = tk.Button(self.ventana, text="Reporte", command=self.mostrar_reporte)
        reporte_boton.pack()
        tree.pack()
              
                # BOTON DE  BORRAR 
        borrar_perro_boton = tk.Button(self.ventana, text="Borrar Perro", command=self.borrar_registro)
        borrar_perro_boton.pack()
               
                # BOTON DE REGISTRAR
        registrar_boton = tk.Button(self.ventana, text="Registrar Animalito", command=self.abrir_formulario)
        registrar_boton.pack()
                     
                #BOTON MODIFICAR
        modificar_boton = tk.Button(self.ventana, text="Modificación de Registro",  command=self.abrir_modificacion)
        modificar_boton.pack()

        entrada_busqueda = tk.Entry(self.ventana)
        entrada_busqueda.pack()
              
                # Entry / búsqueda
        self.entrada_busqueda = tk.Entry(self.ventana)
        self.entrada_busqueda.pack()
                
                # Botón de búsqueda
        buscar_boton = tk.Button(self.ventana, text="Buscar", command=self.buscar_coincidencias)
        buscar_boton.pack()

                # Botón de cambiar color de fondo          
        cambiar_color_boton = tk.Button(self.ventana, text="Cambiar Color de Fondo", command=self.cambiar_color_fondo)
        cambiar_color_boton.pack()

        # Inicializar el árbol
        self.tree.pack()

    def mostrar_reporte(self):
        messagebox.showinfo("Reporte enviado", "Tu reporte ha sido enviado")

    def borrar_registro(self):
        # Obtener el ID seleccionado en el árbol
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un registro para borrar.")
            return

        id_seleccionado = self.tree.item(selected_item[0], 'text')
        
        # Llamar a la función de borrar_registro en el modelo
        self.modelo.borrar_registro(id_seleccionado)

        # Actualizar el árbol
        self.actualizar_treeview()

    def abrir_formulario(self):
        self.modelo.abrir_formulario(self.ventana, self.tree)

    def abrir_modificacion(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un registro para modificar.")
            return

        id_seleccionado = self.tree.item(selected_item[0], 'text')
        item_values = self.tree.item(selected_item[0], 'values')

        raza = item_values[0]
        edad = item_values[1]
        nombre = item_values[2]

        formulario_modificacion = tk.Toplevel(self.ventana)
        formulario_modificacion.title("Modificar Animalito")

        raza_label = tk.Label(formulario_modificacion, text="Nueva Raza:")
        raza_label.pack()
        raza_entry = tk.Entry(formulario_modificacion)
        raza_entry.insert(0, raza)
        raza_entry.pack()

        edad_label = tk.Label(formulario_modificacion, text="Nueva Edad:")
        edad_label.pack()
        edad_entry = tk.Entry(formulario_modificacion)
        edad_entry.insert(0, edad)
        edad_entry.pack()

        nombre_label = tk.Label(formulario_modificacion, text="Nuevo Nombre:")
        nombre_label.pack()
        nombre_entry = tk.Entry(formulario_modificacion)
        nombre_entry.insert(0, nombre)
        nombre_entry.pack()

        def guardar_cambios():
            nueva_raza = raza_entry.get()
            nueva_edad = edad_entry.get()
            nuevo_nombre = nombre_entry.get()

            if nueva_raza == "" or nueva_edad == "" or nuevo_nombre == "":
                messagebox.showerror(
                    "Cuidado",
                    "No se han guardado los cambios porque aún hay campos vacíos",
                )
            else:
                self.modelo.modificar_animalito(id_seleccionado, nueva_raza, nueva_edad, nuevo_nombre)
                messagebox.showinfo("Cambios guardados", "Cambios guardados con éxito")
                formulario_modificacion.destroy()
                self.actualizar_treeview()

        guardar_boton = tk.Button(formulario_modificacion, text="Guardar Cambios", command=guardar_cambios)
        guardar_boton.pack() 

    def buscar_coincidencias(self):
        busqueda = self.entrada_busqueda.get()

        if busqueda == "":
            messagebox.showerror("Cuidado", "Por favor, indique raza, edad o nombre de un animalito para buscar coincidencias")
            return

        coincidencias = self.modelo.buscar_coincidencias(busqueda)
        self.mostrar_coincidencias(coincidencias)
        
    def mostrar_coincidencias(self, coincidencias):
        self.tree.delete(*self.tree.get_children())
        for item in coincidencias:
            self.tree.insert("", "end", text=item["ID"], values=(item["Raza"], item["Edad"], item["Nombre"]))


    def cambiar_color_fondo(self):
        colores = ["red", "green", "blue", "yellow", "pink", "purple", "orange"]
        color_fondo = random.choice(colores)
        self.ventana.configure(bg=color_fondo)

