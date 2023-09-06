import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import re
import sqlite3
import  vista
#clase general
class Modelo:  
    def __init__(self):
        self.conexion = sqlite3.connect("Base_de_datos_Pets.db")
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        sql = """CREATE TABLE IF NOT EXISTS perritos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                raza varchar(20) NOT NULL,
                edad varchar(20),
                nombre varchar(20))
        """
        cursor.execute(sql)
        self.conexion.commit()
        """
        try:
            conexion()
            crear_tabla()
        except:
            print("La base de datos ya existe.")
        """  

    def abrir_modificacion(self, treeview, ventana):
        formulario = tk.Toplevel(ventana)
        formulario.title("Registrar Animalito")
        seleccionado = treeview.focus()
        if seleccionado:
            id_seleccionado = treeview.item(seleccionado)["text"]

            con = conexion()
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM perritos WHERE id = ?", (id_seleccionado,))
            resultado = cursor.fetchone()

            formulario = tk.Toplevel(ventana)
            formulario.title("Modificar Animalito")

            raza_label = tk.Label(formulario, text="Raza:")
            raza_label.pack()
            raza_entry = tk.Entry(formulario)
            raza_entry.pack()
            raza_entry.insert(tk.END, resultado[1])

            edad_label = tk.Label(formulario, text="Edad:")
            edad_label.pack()
            edad_entry = tk.Entry(formulario)
            edad_entry.pack()
            edad_entry.insert(tk.END, resultado[2])

            nombre_label = tk.Label(formulario, text="Nombre:")
            nombre_label.pack()
            nombre_entry = tk.Entry(formulario)
            nombre_entry.pack()
            nombre_entry.insert(tk.END, resultado[3])

        def modificar_animalito():
            raza = self.raza_entry.get()
            edad = self.edad_entry.get()
            nombre = self.nombre_entry.get()

            if raza == "" or edad == "" or nombre == "":
                messagebox.showerror(
                    "Cuidado",
                    "No se ha modificado al animalito porque aún hay campos vacíos",
                )
            else:
                cursor.execute("UPDATE perritos SET raza=?, edad=?, nombre=? WHERE id=?", (raza, edad, nombre, id_seleccionado))
                self.conexion.commit()
                messagebox.showinfo("Modificación exitosa", "Animalito modificado con éxito")
                formulario.destroy()
                self.actualizar_treeview(treeview)

            modificar_boton = tk.Button(formulario, text="Modificar", command=modificar_animalito)
            modificar_boton.pack()
            #else:
            #    messagebox.showinfo("Modificar", "Selecciona un perro para modificar")
    
    def actualizar_treeview(self, arbolview):
            arbolview.delete(*arbolview.get_children())

            sql = "SELECT * FROM perritos ORDER BY id ASC"
            con = self.conexion()
            cursor = con.cursor()
            datos = cursor.execute(sql)
            resultado = datos.fetchall()
            for x in resultado:
                arbolview.insert("", "end", text=x[0], values=(x[1], x[2], x[3]))

    def abrir_formulario(self, ventana, treeview):
        formulario = tk.Toplevel(ventana)
        formulario.title("Registrar Animalito")

        raza_label = tk.Label(formulario, text="Raza:")
        raza_label.pack()
        raza_entry = tk.Entry(formulario)
        raza_entry.pack()

        edad_label = tk.Label(formulario, text="Edad:")
        edad_label.pack()
        edad_entry = tk.Entry(formulario)
        edad_entry.pack()

        nombre_label = tk.Label(formulario, text="Nombre:")
        nombre_label.pack()
        nombre_entry = tk.Entry(formulario)
        nombre_entry.pack()

    def agregar_animalito():
        raza = raza_entry.get()
        edad = edad_entry.get()
        nombre = nombre_entry.get()

        if raza == "" or edad == "" or nombre == "":
            messagebox.showerror(
                "Cuidado",
                "No se ha registrado al animalito porque aún hay campos vacíos",
            )
        else:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO perritos(raza, edad, nombre) VALUES (?, ?, ?)", (raza, edad, nombre))
            conexion.commit()
            messagebox.showinfo("Registro exitoso", "Animalito registrado con éxito")
            formulario.destroy()
            self.actualizar_treeview(treeview)
        registrar_boton = tk.Button(formulario, text="Registrar", command=agregar_animalito)
        registrar_boton.pack()


    def buscar_coincidencias(self, busqueda):
        coincidencias = []
        if busqueda:
            con = self.conexion()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM perritos WHERE raza LIKE ? OR edad LIKE ? OR nombre LIKE ?", ('%' + busqueda + '%', '%' + busqueda + '%', '%' + busqueda + '%'))
            resultado = cursor.fetchall()
            for x in resultado:
                coincidencias.append({"ID": x[0], "Raza": x[1], "Edad": x[2], "Nombre": x[3]})

        return coincidencias           
                
