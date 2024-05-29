# -- coding: utf-8 --
# Librerias necesarias para la creacion de la interfaz grafica
from tkinter import Canvas, Tk, Frame, Label, Button, Radiobutton, StringVar, LEFT, RIGHT
from PIL import ImageTk, Image
from pathlib import Path
import B.Publicador as Publicador

# Get the current working directory
current_dir = Path(__file__).parent

actual_pose = None
previus_pose = None


def show_contenido(root):
    global cells 
    global lb_img_actual, lb_img_previus

    # Create a frame to hold the radio buttons and teach button
    frm_commands= Frame(root)
    frm_commands.pack(side=LEFT, fill = 'both', expand=True)

    # Create a variable to keep track of which radio button is selected
    radio_var = StringVar()
    radio_var.set(None)  # Set the default value to an empty string

    radio_buttons_text = ["[0, 0, 0, 0, 0]", "[25, 25, 20, -20, 0]", "[-35, 35, -30, 30, 0]", "[85, -20, 55, 25 , 0]", "[80, -35, 55, -45, 0]"]

    # Create five radio buttons
    for i in range(5):
        rb = Radiobutton(frm_commands, text=f"Pose {i+1} = {radio_buttons_text[i]}", variable=radio_var, value=f"{i+1}")
        rb.pack(fill="both", expand=True)

    teach_button = Button(frm_commands, text="Mover", bg="#94b43b", font=("Arial", 20), command=lambda: callback_teach_button(radio_var))
    teach_button.pack()

    # Create a frame to hold the table of articulation positions
    frm_positions = Frame(frm_commands)
    frm_positions.pack(side='bottom', anchor='center', padx=10, pady=10)

    # Define the data for the table
    data = [
        ["Articulación", "Valor"],
        ["q1", "value"],
        ["q2", "value"],
        ["q3", "value"],
        ["q4", "value"],
        ["q5", "value"]
    ]

    cells = [[] for _ in range(len(data))]

    # Create the table
    for i in range(len(data)):
        for j in range(len(data[i])):
            cell = Label(frm_positions, text=data[i][j], borderwidth=1, relief="solid", width=14, height=2, font=("Arial", 12))
            cell.grid(row=i, column=j)
            cells[i].append(cell)

    cells[0][0].config(font=("Arial", 12, "bold"))  # Set the font style to bold
    cells[0][1].config(font=("Arial", 12, "bold"))  # Set the font style to bold

    # Create a frame to hold the images
    frm_images = Frame(root)
    frm_images.pack(side=RIGHT, padx=10, pady=10, fill = 'both', expand=True)
    
    lb_txt_previus = Label(frm_images, text="Última posición enviada", font=("Arial", 16))
    lb_txt_previus.grid(row = 0, column = 0, padx= 10)

    lb_txt_actual = Label(frm_images, text="Posición actual", font=("Arial", 16))
    lb_txt_actual.grid(row = 0, column = 1, padx= 10)

    lb_img_previus = Label(frm_images)
    lb_img_previus.grid(row=1, column=0, padx=10, pady=10)

    lb_img_actual = Label(frm_images)
    lb_img_actual.grid(row=1, column=1, padx=10, pady=10)


def show_encabezado(root):
    frm_encabezado = Frame(root, bg="#cccccc")
    frm_encabezado.pack(fill='x')

    img_logo = Image.open(current_dir / "Image" / "Unal.svg")
    img_logo = img_logo.resize((100, 100), Image.LANCZOS)  # resize to 100x100 pixels
    img_logo = ImageTk.PhotoImage(img_logo)  # convert the image object to a tkinter-compatible photo image

    lb_img_logo = Label(frm_encabezado, image=img_logo)
    lb_img_logo.image = img_logo  # keep a reference to the image to prevent it from being garbage collected
    lb_img_logo.pack(side=LEFT)
    
    frm_names = Frame(frm_encabezado, bg="#94b43b")
    frm_names.pack(side=LEFT, fill='both', expand=True)

    # Create three labels under each other
    lb_lab4 = Label(frm_names, text="Laboratorio 4, Cinemática Directa", bg="#94b43b", font=("Arial", 16))
    lb_lab4.pack(fill='x')

    lb_name1= Label(frm_names, text="Hector Alejandro Montes Lobaton", bg="#94b43b", font=("Arial", 14))
    lb_name1.pack(fill='x')

    lb_name1= Label(frm_names, text="Bryan Steven Pinilla Castro", bg="#94b43b", font=("Arial", 14))
    lb_name1.pack(fill='x')


    
    Button(frm_encabezado, text="EXIT", command=root.destroy).pack(side=LEFT)


def callback_teach_button(radio_var):
    global actual_pose, previus_pose
    previus_pose = actual_pose
    actual_pose = int(radio_var.get())
    callback_images(previus_pose, actual_pose)
    Publicador.joint_publisher(actual_pose - 1) 
    Publicador.listener()
    
    
# Function that displays an image based on the selected radio button
def callback_images(previus_pose: int, actual_pose: int):

    # Map the selected option to an image file
    dic_img_path = {
        1: current_dir / "Image" / "1.png",
        2: current_dir / "Image" / "2.png",
        3: current_dir / "Image" / "3.png",
        4: current_dir / "Image" / "4.png",
        5: current_dir / "Image" / "5.png",
    }

    default = current_dir / "Image" / "0.jpg"

    actual_img_path = dic_img_path.get(actual_pose, default)
    previus_img_path = dic_img_path.get(previus_pose, default)

    # Load the image
    actual_img = Image.open(actual_img_path)
    actual_img = actual_img.resize((300, 300), Image.LANCZOS)  # Resize the image to 300x300 pixels

    previus_img = Image.open(previus_img_path)
    previus_img = previus_img.resize((300, 300), Image.LANCZOS)  # Resize the image to 300x300 pixels

    # Convert the image to a PhotoImage object
    photo_actual = ImageTk.PhotoImage(actual_img)
    photo_previus = ImageTk.PhotoImage(previus_img)

    # Set the image of the label
    lb_img_actual.config(image=photo_actual)
    lb_img_actual.image = photo_actual  # Keep a reference to the image to prevent it from being garbage collected

    lb_img_previus.config(image=photo_previus)
    lb_img_previus.image = photo_previus  # Keep a reference to the image to prevent it from being garbage collected

def data_to_HMI(data):
    global cells
    cells[1][1].config(text=f"{data[0]:.2f}°")
    cells[2][1].config(text=f"{data[1]:.2f}°")
    cells[3][1].config(text=f"{data[2]:.2f}°")
    cells[4][1].config(text=f"{data[3]:.2f}°")
    cells[5][1].config(text=f"{data[4]:.2f}°")

def main():

    root = Tk() # Create an instance of tkinter window
    root.geometry("1000x600") # Define the geometry of the window
    root.title("Interfaz") # Set the title of the window

    show_encabezado(root)
    show_contenido(root)

    root.mainloop()

if __name__ == '__main__':
    main()
