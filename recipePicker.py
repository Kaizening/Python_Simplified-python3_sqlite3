import tkinter as tk
from PIL import ImageTk

bg_colour = "#3d6466"

def load_frame1():
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
    print("Hellow Mariya")

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
