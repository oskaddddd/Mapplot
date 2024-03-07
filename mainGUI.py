from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QImage

import sys
import qdarktheme
from ReadSettings import *
from DataDysplay import *

import time

import PIL.Image
settings = Settings()

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('UI/UI.ui', self)
        
        self.map_scene = QGraphicsScene()
        self.map_viewer.setScene(self.map_scene)
        self.output = None
        
    

        ##########
        #SETTINGS#
        ##########

        #LOAD SETTINGS
        ##Mode
        self.mode_dropdown.setCurrentText(['Monocolor', 'RGB'][settings['mode']])
        ##Computation
        self.computation_dropdown.setCurrentText(['GPU', 'CPU'][['opencl', 'cpu'].index(settings['computation'])])
        ##Interpolation
        self.interpolation_dropdown.setCurrentText(['Delauny triangulation', 'IDW'][['delauny', 'idw'].index(settings['interpolation'])])
        ##Max min check
        self.manual_max_min_check.setChecked(settings['manual_max_min'])
        ##Max
        self.max_input.setValue(settings['max'])
        ##Min
        self.min_input.setValue(settings['min'])
        ##Create legend
        self.create_legend_check.setChecked(settings['create_legend'])
        #Horizontal alignment
        self.horizontal_alignment_dropdown.setCurrentText(['Right', 'Left'][['right', 'left'].index(settings['horizontal_alignment'])])
        #Vertical position
        self.vertical_position_slider.setValue(int(settings["vertical_position"]*100))
        #Scale   
        self.scale_slider.setValue(int(settings["scale"]*100))
        #Text scale
        self.text_scale_slider.setValue(int(settings["text_scale"]*100))
        ##Offset
        self.offset_input.setValue(settings['offset'])
        ##sections
        self.sections_input.setValue(settings['sections'])
        ##Units
        self.units_input.setText(settings['units'])
        ##Round To
        self.round_to_input.setValue(settings['round_to'])

        #Save Settings
        self.save_settings_button.clicked.connect(lambda: WriteSettings(settings))


        #CONNECT GENERAL SETTINGS
        ##Mode
        self.mode_dropdown.currentIndexChanged.connect(lambda data: self.change_setting(data, 'mode'))
        ##Computation
        self.computation_dropdown.currentIndexChanged.connect(lambda data: self.change_setting(['opencl', 'cpu'][data], 'computation'))        
        ##Interpolation
        self.interpolation_dropdown.currentIndexChanged.connect(lambda data: self.change_setting(['delauny', 'idw'][data], 'interpolation'))  
        ##Manual Max Min
        self.manual_max_min_check.stateChanged.connect(lambda data: self.change_setting(data==2, 'manual_max_min'))       
        ##Max
        self.max_input.valueChanged.connect(lambda data: self.change_setting(data, 'max'))
        ##Min
        self.min_input.valueChanged.connect(lambda data: self.change_setting(data, 'min'))


        #CONNECT LEGEND SETTINGS
        ##Create legend
        self.create_legend_check.stateChanged.connect(lambda data: self.change_setting(data==2, 'create_legend'))      
        ##Horizontal alignment
        self.horizontal_alignment_dropdown.currentIndexChanged.connect(lambda data: self.change_setting(['right', 'left'][data], 'horizontal_alignment'))
        ##Vertical position
        self.vertical_position_slider.valueChanged.connect(lambda data: self.change_setting(data/100, 'vertical_position'))
        ##Scale
        self.scale_slider.valueChanged.connect(lambda data: self.change_setting(data/100, 'scale'))
        ##Text scale
        self.text_scale_slider.valueChanged.connect(lambda data: self.change_setting(data/100, 'text_scale'))
        ##Offset
        self.offset_input.valueChanged.connect(lambda data: self.change_setting(data, 'offset'))
        ##Sections
        self.sections_input.valueChanged.connect(lambda data: self.change_setting(data, 'sections'))
        ##Units
        self.units_input.textChanged.connect(lambda data: self.change_setting(data, 'units'))
        ##Round to
        self.round_to_input.valueChanged.connect(lambda data: self.change_setting(data, 'round_to'))

        
        #Load data button
        self.load_data_button.clicked.connect(self.prepare_data)
        #Create Button
        self.create_button.clicked.connect(self.create_image)
        #Save image
        self.save_image_button.clicked.connect(self.save_image)
        self.show()
        
        self.error_message_timer = QTimer()
        self.error_message_timer.timeout.connect(lambda: self.error_message.setText(''))
        
    

    def save_image(self):
        if self.output == None:
            self.error_message.setText('Please create the image before saving it')
            self.error_message_timer.start(3000)
            return
        file = self.select_file("Images (*.png)", "Save image", 'save', '.png')
        self.output.save(file)
        

        
    
    
    def change_setting(self, data, setting):
        print(data)
        settings[setting] = data
        
    def create_image(self):

        t = time.time()
        mapObj = create_map()
        e = mapObj.ReadData()
        if e != None:
            self.error_message.setText(e)
            return
        self.output = mapObj.Interpolate()
        print('speed:', time.time()-t)
        
        
        qImage = QImage(self.output.tobytes(), self.output.size[0], self.output.size[1],QImage.Format.Format_RGBA8888)
        print(1)

        pixmap = QPixmap.fromImage(qImage)
        print(3)
        self.map_scene.clear()
        self.map_scene.addPixmap(pixmap)
        #self.map_viewer.shear()
        print(2)
        
        #self.map_viewer(QGraphicsView())
        #output.show()
    
    def prepare_data(self):
        file = self.select_file("All (*);;Json files (*.json)", "Select data file", 'open')
        if file == None: return
        data  = []
        with open(file, 'r') as f:
            data = json.load(f)
        prepare_data(data)
    
    def select_file(self, fileType, message, action, forceFileType = None):
        print(fileType)
        if action == 'open':
            fileName, _ = QFileDialog.getOpenFileName(self, message, "", fileType, options=QFileDialog.Option(1))
            print(fileName)
            if fileName:
                return fileName
        elif action == 'save':
            fileName, _ = QFileDialog.getSaveFileName(None, message, "", fileType)
            
            if fileName:
                if forceFileType != None and not fileName.endswith(forceFileType):
                    fileName+=forceFileType
                print(fileName)
                return fileName            
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    qdarktheme.setup_theme()
    
    window = Ui()
    app.exec()
    
