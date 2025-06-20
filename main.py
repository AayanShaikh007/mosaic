from random import sample
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QSpinBox, QFileDialog, QCheckBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import sys

from pathlib import Path
from PIL import Image

import mosaic

class mosaicinterface(QWidget):
    def __init__(self):
        self.uploadfail = False
    
    # PyQt depends on a system of classes and objects, particularly objects to 
    # represent parts of the GUI.
 
        super().__init__()

        self.setWindowTitle("Mosaic Generator")
        self.setGeometry(300, 100, 1000, 600)

        transition = 500

        # source box title
        self.tgttitle = QLabel("Source Files", self)
        # setting position of the title
        self.tgttitle.setGeometry(110+ transition,30,100,30)
        
        self.sourcebox = QComboBox(self)
        self.sourcebox.setGeometry(100 + transition,60,100,30)
        self.sourcebox.addItems(["Select", "Real-world", "Static Color"])

        down = 40

        #rows title
        self.rowstitle = QLabel("Rows", self)
        self.rowstitle.setGeometry(250 + transition, 30+ down, 80, 30)
        #rows box
        self.box1 = QSpinBox(self)
        self.box1.setGeometry(310 + transition, 30 + down, 80, 30)
        self.box1.setRange(0, 1080)
        self.box1.setValue(100)
        
        #cols title
        self.colstitle = QLabel("Columns", self)
        self.colstitle.setGeometry(250 + transition, 80 + down, 80, 30)

        #cols box
        self.box2 = QSpinBox(self)
        self.box2.setGeometry(310 + transition, 80 + down, 80, 30)
        self.box2.setRange(0, 1920)
        self.box2.setValue(200)
        
        #target title
        self.tgttitle = QLabel("Target Image", self)
        self.tgttitle.setGeometry(110 + transition, 90,100,30)

        self.check1 = QCheckBox("Use sample", self)
        self.check1.setGeometry(100 + transition, 150 ,100,30)

        # tgt preloaded samples box
        self.samplesbox = QComboBox(self)
        self.samplesbox.setGeometry(100 + transition ,120 ,100,30)
        self.samplesbox.addItems(["Select", "Sample 1", "Sample 2", "Sample 3", "Sample 4"])
        
        # upload image button
        self.uploadbtn = QPushButton("Upload image", self)
        # The upload image, generate, and view image buttons call a function when activated.
        self.uploadbtn.clicked.connect(self.uploadimage)
        self.uploadbtn.setGeometry(100 + transition, 200,100,30)

        # upload image checkbox
        self.check2 = QCheckBox("Upload Image", self)
        self.check2.setGeometry(100 + transition, 230 ,100,30)

        # generate button
        self.activatebtn = QPushButton("Generate", self)
        self.activatebtn.clicked.connect(self.activated)
        self.activatebtn.setGeometry(250 + transition, 200 ,150,30)
        
        # view image button
        self.viewbtn = QPushButton("View Product Image", self)
        self.viewbtn.clicked.connect(self.view)
        self.viewbtn.setGeometry(125, 250 ,150,30)


        #IMAGE LABEL
        self.label = QLabel(self, alignment= Qt.AlignmentFlag.AlignTop)
        self.pixmap = QPixmap("placeholder.png")
        # Scaling the image to fit the label box.
        self.scaledpixmap = self.pixmap.scaled(400,225)
        self.label.setPixmap(self.scaledpixmap)

        
    
    def uploadimage(self):
        # Makes the popup to upload the image. 
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Full-HD image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        # Makes sure that the file exists and then ensures that its Full HD
        if file_path:            
            from PIL import Image
            img = Image.open(file_path)
            if img.width != 1920 or img.height != 1080:
                print(f"img is not 1920x1080, not saved.")
        # If the image is good, it is previewed in the image box (pyqt label). 
            else:
                img.save("uploaded.jpg")
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(400,225, Qt.AspectRatioMode.IgnoreAspectRatio)
                self.label.setPixmap(pixmap)
    
    def activated(self):
        # this function is activated when the user presses generate. 
        print("generate clicked")

        placeholder = QPixmap("placeholder.png")
        scaledpixmap = placeholder.scaled(400,225, Qt.AspectRatioMode.IgnoreAspectRatio)
        self.label.setPixmap(scaledpixmap)
        # Fetching values of the checkboxes, the indices of the box containing image samples,
        # and the box containing source images. 

        sample_check = self.check1.isChecked()
        upload_check = self.check2.isChecked()

        index = self.samplesbox.currentIndex()
        srcindex = self.sourcebox.currentIndex()

        # making the target path, handling the sample image checkbox code. 
        if sample_check == True and index != 0 and upload_check == False:
            target_path = f"target{index}.jpg"
            print(target_path)
        
        # handling the uploaded image code
        elif upload_check == True and sample_check == False:
            if os.path.exists("uploaded.jpg"):
                target_path = "uploaded.jpg"
                print("uploaded")
    
        else:
            print("returning")
            return
        
        # specifying the image set the user wants to use. 
        if srcindex == 1:
            source_path = mosaic.real_path
        
        elif srcindex == 2:
            source_path = mosaic.static_path
        else:
            return

        rows = self.box1.value()
        cols = self.box2.value()

        if rows == 0 or cols == 0 or rows > 1080 or cols > 1920:
            print("invalid params")
            return

        print(target_path, rows, cols, source_path)

        mosaic.generate(target_path, rows, cols, source_path)

        mosaic_product = QPixmap("finalproduct.jpg")
        scaledmosaic = mosaic_product.scaled(400, 225, Qt.AspectRatioMode.IgnoreAspectRatio)
        self.label.setPixmap(scaledmosaic)
# Show the image when it has been generated in a popup. 
    def view(self):
        product = Path("finalproduct.jpg")
        if product.exists():
            product_pil = Image.open(product)
            product_pil.show()

# Standard code used in pyqt to start running the app, handle exit, etc. 
app = QApplication(sys.argv)
window = mosaicinterface()
window.show()
sys.exit(app.exec())