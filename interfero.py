import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#########################################################################################################################
###############################################Fonctions permettant de définir la zone de crop sur la FFT ###############
#########################################################################################################################

class SquareDrawer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.center_point = None
        self.current_rect = None
        self.finished = False
        self.square_coords = None
        self.fig, self.ax = plt.subplots()
        self.image = Image.open(self.image_path)

    def draw_square(self):
        # Afficher l'image avec matplotlib
        self.ax.imshow(self.image)

        # Connecter les événements de souris
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

        plt.show()

        # Boucle pour attendre que l'interaction soit terminée
        while not self.finished:
            plt.pause(0.1)

        return self.get_cropped_image()

    def on_press(self, event):
        if event.inaxes is not None:
            self.center_point = (int(event.xdata), int(event.ydata))
            # Supprimer le rectangle courant s'il existe
            if self.current_rect is not None:
                self.current_rect.remove()
                self.current_rect = None
            print(self.center_point)
            self.current_rect = patches.Rectangle((self.center_point[0], self.center_point[1]), 0, 0, linewidth=1, edgecolor='r', facecolor='none')
            self.ax.add_patch(self.current_rect)
            

    def on_motion(self, event):
        if self.center_point is not None and event.inaxes is not None:
            x_center, y_center = self.center_point
            x_corner, y_corner = int(event.xdata), int(event.ydata)
            half_side_length = int(((x_corner - x_center) ** 2 + (y_corner - y_center) ** 2) ** 0.5)
            x0 = x_center - half_side_length
            y0 = y_center - half_side_length
            width = 2 * half_side_length
            height = 2 * half_side_length
            self.current_rect.set_width(width)
            self.current_rect.set_height(height)
            self.current_rect.set_xy((x0, y0))
            plt.draw()

    def on_release(self, event):
        if self.center_point is not None and event.inaxes is not None:
            x_center, y_center = self.center_point
            x_corner, y_corner = int(event.xdata), int(event.ydata)
            half_side_length = int(((x_corner - x_center) ** 2 + (y_corner - y_center) ** 0.5))
            x0 = x_center - half_side_length
            y0 = y_center - half_side_length
            width = 2 * half_side_length
            height = 2 * half_side_length
            x1, y1 = x0 + width, y0 + height
            self.square_coords = {
                "top_left": (x0, y0),
                "bottom_right": (x1, y1)
            }
            print(f"Carré sélectionné: Coin haut-gauche ({x0}, {y0}), Coin bas-droit ({x1}, {y1}), Dimensions {width}x{height}")
            self.finished = True
            plt.close(self.fig)  # Ferme la fenêtre de l'image

    def get_cropped_image(self):
        if self.square_coords:
            x0, y0 = self.square_coords["top_left"]
            x1, y1 = self.square_coords["bottom_right"]
            # Découper la région sélectionnée de l'image
            cropped_image = self.image.crop((x0, y0, x1, y1))
            # Convertir l'image PIL en tableau numpy
            cropped_image_np = np.array(cropped_image)
            return cropped_image_np
        else:
            return None
#########################################################################################################################
############################################### MAIN ####################################################################
#########################################################################################################################


image_directory = "D:\\Seqence_diffusion\\test 1"
extension = "bmp"

images_path = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.split(".")[-1]== extension ]

for i, im_path in enumerate(images_path):
    image = Image.open(im_path)
    im_array = np.asarray(image)
    square_drawer = SquareDrawer(im_path)
    cropped_image_np = square_drawer.draw_square()
    print(f"Image découpée sous forme de tableau numpy :\n{cropped_image_np}")
    print("to")
    


