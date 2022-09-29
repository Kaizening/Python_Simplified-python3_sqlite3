import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random

bg_colour = "#3d6466"

def fetch_db():
    # Establecer conexion base de datos
    connection = sqlite3.connect("data/recipes.db")
    # Crear objeto cursor
    cursor = connection.cursor()
    # Ahora podemos llamar comandos SQL en este objeto cursor
    # Cada receta esta guardada en un tabla distinta, el nombre de la receta es el titulo de la tabla
    # Cada fila de la tabla es un ingrediente de la receta, mientras que
    # las columnas son de 0 a 3, [0]id , [1]name, [2]quantity, [3]unit
    # El comando SQL para seleccionar todos los nombre de las tablas de una base de datos es:    
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    # Hacer un fetch para poder asignarlo a una variable, y luego imprimir esa variable
    all_tables = cursor.fetchall()
    
    # Crear la variable idx para que se le asigne un valor random de 0 a la cantidad total de tablas
    # La funcion len empieza a contar desde 1 es por ello que se le resta 1
    idx = random.randint(0, len(all_tables)-1)
    
    # Se da como indice el numero random generado para idx
    print(all_tables[idx])
    
    # Fetch ingredients
    # Debemos recordar que los ingredientes estan en lo que seria el campo de la columna [1], que corrsponda a la tabla0 [idx]
    table_name = all_tables[idx][1]
    # Una vez seleccionado el nombre de la tabla, podemos hacer un fetch de todos sus ingredientes
    cursor.execute("SELECT * FROM " + table_name + ";")
    # Guardamos todos los ingredientes seleccionados en table_records
    # Guardar los registros/filas de la tabla
    table_records = cursor.fetchall()    
    # Debemos terminar la conexion que hemos establecido
    connection.close()
    
    return table_name, table_records

def pre_process(table_name, table_records):
    # Quitar los numero al final del titulo, selecciona todo hasta 6 caracteres antes
    title = table_name[:-6]
    # Agregar espacios entre cada palabra, agregando un espacio antes de una mayuscula
    # Si el caracter es minuscula lo deja como esta, sino concatena un espacio
    # Usar el metodo join para concatenar todos los valores de una lista en un string
    title = "".join([char if char.islower() else " " + char for char in title])
    
    # Crear una lista vacia llamada ingredients
    ingredients = []
    
    # Ingredients
    # Repasar los ingredientes/filas de una tabla, en este caso una variable guarda
    # todos los registros de la tabla
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)
        # "2 cups of sugar"
    
    return title, ingredients
    

def load_frame1():
    # Este metodo apila un frame sobre otro. El mas relevante va arriba
    frame1.tkraise()   
    # Forma de prevenir que un widget child modifique el parent con el method propagate
    frame1.pack_propagate(False)    
    # frame1 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    # Una vez que tenemos cargada la imagen, podemos convertirla en un widget
    # tkinter no tiene un widget especifico para imagenes por lo que se usa el tipo Label
    # fundamental indicar que es image=logo_img
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    # Estamos obligados a acceder al atributo image, de nuestro logo_widget 
    # y volver a setearlo como logo_img
    logo_widget.image = logo_img
    logo_widget.pack()


    # Label widget
    tk.Label(
        frame1,
        text="Ready for your recipe?",
        bg=bg_colour,
        fg="white",
        font=("TkMenuFont", 14)
        ).pack()

    # Button widget
    tk.Button(
        frame1,
        text="SHUFFLE0",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command= lambda:load_frame2()# Es una funcion que se ejecuta cada vez que se presiona el boton
        ).pack(pady=20)

def load_frame2():
    # Para poder moverse entre frames, debemos iniciar cada frame con un .tkraise
    # Este metodo apila un frame sobre otro. El mas relevante va arriba
    frame2.tkraise()    
    # Recibimos de la funcion fetch_db() table_name y table_records
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)
    
    # frame1 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    # Una vez que tenemos cargada la imagen, podemos convertirla en un widget
    # tkinter no tiene un widget especifico para imagenes por lo que se usa el tipo Label
    # fundamental indicar que es image=logo_img
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_colour)
    # Estamos obligados a acceder al atributo image, de nuestro logo_widget 
    # y volver a setearlo como logo_img
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    
    # Label widget
    tk.Label(
        frame2,
        text=title,
        bg=bg_colour,
        fg="white",
        font=("TkHeadingFont", 20)
        ).pack(pady=25)
    
    for i in ingredients:
        # Para cada ingrediente se creara su propio label
        # Label widget
        tk.Label(
            frame2,
            text=i,
            bg=bg_colour,
            fg="white",
            font=("TkMenuFont", 12)
            ).pack()
        
    # Button widget
    tk.Button(
        frame2,
        text="BACK",
        font=("TkHeadingFont", 18),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command= lambda:load_frame1()# Es una funcion que se ejecuta cada vez que se presiona el boton. Este caso es frame1 para volver atras
        ).pack(pady=20)

# Initiallize app
root = tk.Tk()
root.title("Recipe Picker")

# Create a frame widget
frame1 = tk.Frame(root, width=500, height=500, bg=bg_colour)
# El frame2 no lleva ancho y altura, porque de desea que se ajuste al contenido
# ya que una receta puede ser mas larga que la otra
frame2 = tk.Frame(root, bg=bg_colour)

# Hace un loop en la tupla de frame1 a frame2
# luego llama al metodo grid por la variable de iteracion
for frame in (frame1, frame2):
    frame.grid(row=0, column=0)

# Llamar al la funcion load_frame1 ya que sino no se vera ningun elemento
load_frame1()


# Run app
root.mainloop()
