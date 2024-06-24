from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QHBoxLayout, QMessageBox, QGroupBox, QTextEdit, QListWidget, QLineEdit, QInputDialog, QFileDialog

app = QApplication([])

main_win = QWidget()
main_win.show()
main_win.resize(1000, 800)
main_win.setWindowTitle("Easy Editor")

layout_main = QHBoxLayout()

layout_left = QVBoxLayout()
button_folder = QPushButton("Folder")
layout_left.addWidget(button_folder)
list_image = QListWidget()
layout_left.addWidget(list_image)

layout_right = QVBoxLayout()
label_image = QLabel("image")
layout_right.addWidget(label_image)
layout_bottomright = QHBoxLayout()
layout_right.addLayout(layout_bottomright)
left_button = QPushButton("Left")
layout_bottomright.addWidget(left_button)
right_button = QPushButton("Right")
layout_bottomright.addWidget(right_button)
mirror_button = QPushButton("Mirror")
layout_bottomright.addWidget(mirror_button)
sharp_button = QPushButton("Sharpness")
layout_bottomright.addWidget(sharp_button)
bw_button = QPushButton("B&W")
layout_bottomright.addWidget(bw_button)
crop_button = QPushButton("Crop")
layout_bottomright.addWidget(crop_button)
blur_button = QPushButton("Blur")
layout_bottomright.addWidget(blur_button)


layout_main.addLayout(layout_left)
layout_main.addLayout(layout_right, stretch = 4)

main_win.setLayout(layout_main)

from PIL import Image, ImageFilter, ImageEnhance
from PyQt5.QtGui import QPixmap

class ImageEditor():
    def __init__(self, filename):
        self.filename = filename
        self.open()
        self.showQlabel(self.filename)
    def open(self):
        self.img = Image.open(self.filename)
    def showQlabel(self, image_name):
        img_pix = QPixmap(image_name)
        w = label_image.width()
        h = label_image.height()
        img_pix = img_pix.scaled(w, h, Qt.KeepAspectRatio)
        label_image.setPixmap(img_pix)
    def get_name(self, action):
        name = self.filename.split(".")[0]
        ext = self.filename.split(".")[1]
        result = name + "_" + action + "." + ext
        return result
    def do_gray(self):
        self.img_edit = self.img.convert("L")
        save_name = self.get_name("gray")
        self.img_edit.save(save_name)
        self.showQlabel(save_name)

    def do_blur(self):
        self.img_blur = self.img.filter(ImageFilter.BLUR)
        save_name = self.get_name("blur")
        self.img_blur.save(save_name)
        self.showQlabel(save_name)

    def do_contrast(self):
        contrast_obj = ImageEnhance.Contrast(self.img)
        self.img_con = contrast_obj.enhance(1.5)
        save_name = self.get_name("contrast")
        self.img_con.save(save_name)
        self.showQlabel(save_name)

    def do_left(self):
        self.img_left = self.img.transpose(Image.ROTATE_90)
        save_name = self.get_name("left")
        self.img_left.save(save_name)
        self.showQlabel(save_name)

    def do_right(self):
        self.img_right = self.img.transpose(Image.ROTATE_270)
        save_name = self.get_name("right")
        self.img_right.save(save_name)
        self.showQlabel(save_name)

    def do_crop(self):
        box = (160, 120, 620, 650)
        self.img_edit = self.img.crop(box)
        save_name = self.get_name("crop")
        self.img_edit.save(save_name)
        self.showQlabel(save_name)

    def do_mirror(self):
        self.img_mirror = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        save_name = self.get_name("mirror")
        self.img_mirror.save(save_name)
        self.showQlabel(save_name)
    
import os

def select_folder():
    global file_path
    file_path = QFileDialog.getExistingDirectory()
    print("Folder:", file_path)
    update_list_widget()

def update_list_widget():
    global file_path
    file_list = os.listdir(file_path)
    images = []
    for file in file_list:
        if ".jpg" in file:
            images.append(file)
                
    list_image.clear()    
    list_image.addItems(images)

def select_image():
    global editor_obj
    select_file = list_image.selectedItems()[0].text()
    
    editor_obj = ImageEditor(select_file)

def do_bw():
    editor_obj.do_gray()
    update_list_widget()
bw_button.clicked.connect(do_bw)

def do_b():
    editor_obj.do_blur()
    update_list_widget()
blur_button.clicked.connect(do_b)

def do_l():
    editor_obj.do_left()
    update_list_widget()
left_button.clicked.connect(do_l)

def do_r():
    editor_obj.do_right()
    update_list_widget()
right_button.clicked.connect(do_r)

def do_c():
    editor_obj.do_contrast()
    update_list_widget()
sharp_button.clicked.connect(do_c)

def do_m():
    editor_obj.do_mirror()
    update_list_widget()
mirror_button.clicked.connect(do_m)

def do_cr():
    editor_obj.do_crop()
    update_list_widget()
crop_button.clicked.connect(do_cr)


list_image.itemClicked.connect(select_image)
button_folder.clicked.connect(select_folder)

# editor_obj.do_gray()
# editor_obj.do_blur()
# editor_obj.do_contrast()
# editor_obj.do_crop()
# editor_obj.do_mirror()
# editor_obj.do_left()
# editor_obj.do_right()


app.exec_()