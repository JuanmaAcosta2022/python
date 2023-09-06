import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import re
import sqlite3
from modelo import Modelo
from vista import Vista

class MyApp:
    def __init__(self):
        self.ventana = tk.Tk()

        self.modelo = Modelo()
        self.vista = Vista(self.modelo)

        self.controlador = Controlador(self.ventana, self.modelo)
        self.vista.registrar_boton.config(command=self)
        #self.vista.buscar_boton.config(command=self)
        #self.vista.cambiar_color_boton.config(command=self.controlador.cambiar_color_fondo)

    def run(self):
        self.ventana.mainloop()

#cuidado cone sta funcion que engloba otra accion. 
class Controlador:
    def __init__ (self, ventana, modelo):
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
                raza = self.vista.raza_entry.get()
                edad = self.vista.edad_entry.get()
                nombre = self.vista.nombre_entry.get()

                if raza == "" or edad == "" or nombre == "":
                    messagebox.showerror("Cuidado","No se ha registrado al animalito porque aún hay campos vacíos")
                    return
                else:
                    conexion = sqlite3.connect('nombre_base_de_datos.db')
                    cursor = conexion.cursor()
                    cursor.execute("INSERT INTO perritos(raza, edad, nombre) VALUES (?, ?, ?)", (raza, edad, nombre))
                    self.conexion.commit()
                    messagebox.showinfo("Registro exitoso", "Animalito registrado con éxito")
                    self.formulario.destroy()
                    self.actualizar_treeview(treeview)
        #registrar boton  esta al mismo nivel que funcion agregar_animalito() pertenece a esta
            registrar_boton = tk.Button(formulario, text="Registrar", command=agregar_animalito)
            registrar_boton.pack()



    def buscar_coincidencias(self, entrada_busqueda, treeview):
        busqueda = self.vista.entrada_busqueda.get()
        coincidencias = []
        if busqueda == "":
            messagebox.showerror("Cuidado","Por favor, indique raza, edad o nombre de un animalito para buscar coincidencias",)
            return
         
            # Lógica para buscar coincidencias en el modelo y actualizar la vista
            coincidencias = self.modelo.buscar_coincidencias(busqueda)
            self.vista.mostrar_coincidencias(coincidencias)      
        else:
            con = self.modelo.conexion()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM perritos WHERE raza LIKE ? OR edad LIKE ? OR nombre LIKE ?", ('%' + busqueda + '%', '%' + busqueda + '%', '%' + busqueda + '%'))
            resultado = cursor.fetchall()
            for x in resultado:
                coincidencias.append(f"ID: {x[0]}, Raza: {x[1]}, Edad: {x[2]}, Nombre: {x[3]}")

            if coincidencias:
                messagebox.showinfo(
                        "Coincidencias",
                        f"Aquí están las coincidencias para '{busqueda}':\n\n" + "\n".join(coincidencias),
                    )
            else:
                messagebox.showinfo("Sin coincidencias", f"No se encontraron coincidencias para '{busqueda}'")

    def borrar_registro(self, treeview):
        seleccionado = treeview.focus()
        if seleccionado:
            id_seleccionado = treeview.item(seleccionado)["text"]

            respuesta = messagebox.askyesno(
                "Confirmación", f"¿Estás seguro de borrar el registro con ID {id_seleccionado}?"
            )

            if respuesta:
                con = self.conexion()
                cursor = con.cursor()
                cursor.execute("DELETE FROM perritos WHERE id = ?", (id_seleccionado,))
                con.commit()
                messagebox.showinfo("Registro borrado", f"Se borró el registro con ID {id_seleccionado}")
                self.actualizar_treeview(treeview)
        else:
            messagebox.showinfo("Borrar", "Selecciona un perro para borrar")
        
        RutaDescargaImagen = os.path.expanduser("~") + "/downloads/" #RUTA DE DESCARGA DEL USUARIO

        #actualizar_treeview(tree)
        try:
            logo_path = RutaDescargaImagen + "1a.png"
            logo_img = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(self.ventana, image=logo_img)
            logo_label.pack()
        except:
            pass

if __name__ == "__main__":
    app = MyApp()
    app.run()