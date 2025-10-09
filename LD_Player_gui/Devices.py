from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option

class Devices():
    def __init__(self, GUI):
        self.GUI = GUI
        self.opt = option()
    
    def Tab_Devices(self) -> QWidget:
        devices_widget = QWidget()
        devices_widget_layout = QVBoxLayout(devices_widget)
        #Top
        devices_browser_widget = QWidget()
        devices_browser_widget_layout = QHBoxLayout(devices_browser_widget)
        
        devices_locate_widget = QWidget()
        devices_locate_widget_layout = QVBoxLayout(devices_locate_widget)
        
        devices_locate_widget_layout_top = QHBoxLayout()

        labeltop1 = QLabel("LDplayer Location")
        self.ldplayer_directory_box_top = QLineEdit(r"C:/Program Files/ldplayer")
        labeltop3 = QPushButton("Browse")
        
        
        devices_locate_widget_layout_top.addWidget(labeltop1)
        devices_locate_widget_layout_top.addWidget(self.ldplayer_directory_box_top)
        devices_locate_widget_layout_top.addWidget(labeltop3)
        
        
        devices_locate_widget_layout_bottom = QHBoxLayout()

        labelbottom1 = QLabel("System Location")
        self.system_directory_box_bottom = QLineEdit(r"C:/Program Files/ldplayer")
        labelbottom3 = QPushButton("Browse")
        
        devices_locate_widget_layout_bottom.addWidget(labelbottom1)
        devices_locate_widget_layout_bottom.addWidget(self.system_directory_box_bottom)
        devices_locate_widget_layout_bottom.addWidget(labelbottom3)
        
        devices_locate_widget_layout.addLayout(devices_locate_widget_layout_top)
        devices_locate_widget_layout.addLayout(devices_locate_widget_layout_bottom)

        devices_upload = QPushButton("Upload")

        devices_upload.setStyleSheet("margin: 0px; padding: 40px 60px; ")
        devices_browser_widget_layout.addWidget(devices_locate_widget, 8)
        devices_browser_widget_layout.addWidget(devices_upload, 2)
        devices_browser_widget_layout.setContentsMargins(0, 0, 0, 0)

        #Bottom
        devices_information_widget = QWidget()
        devices_information_widget_layout = QVBoxLayout(devices_information_widget)
        
        devices_information_widget_layout_top_widget = QWidget()
        devices_information_widget_layout_top = QHBoxLayout(devices_information_widget_layout_top_widget)
        QLabel("LDplayer")
        label1 = QLabel("Number of active LD")
        label1_value = QSpinBox()
        label1_value.setValue(1)
        label2 = QLabel("Wait after LD Boot")
        label2_value = QSpinBox()
        label2_value.setValue(30)
        label3 = QCheckBox("Between LD Start")
        label3_value = QSpinBox()
        label3_value.setValue(30)
        
        self.Gpu_box = QGroupBox()
        self.Gpu_vbox = QVBoxLayout(self.Gpu_box)
        label4 = QCheckBox("Hardware Accel")
        label5 = QCheckBox("NVIDIA GPU")
        self.Gpu_vbox.addWidget(label4)
        self.Gpu_vbox.addWidget(label5)
        label6 = QPushButton("App")
        devices_information_widget_layout_top.addWidget(label1)
        devices_information_widget_layout_top.addWidget(label1_value)
        devices_information_widget_layout_top.addStretch(1)
        devices_information_widget_layout_top.addWidget(label2)
        devices_information_widget_layout_top.addWidget(label2_value)
        devices_information_widget_layout_top.addStretch(1)
        devices_information_widget_layout_top.addWidget(label3)
        devices_information_widget_layout_top.addWidget(label3_value)
        devices_information_widget_layout_top.addStretch(1)
        devices_information_widget_layout_top.addWidget(self.Gpu_box)
        devices_information_widget_layout_top.addWidget(label6)
        devices_information_widget_layout_top.setAlignment(Qt.AlignmentFlag.AlignVertical_Mask)

        devices_information_widget_layout_bottom_widget = QWidget()
        devices_information_widget_layout_bottom = QHBoxLayout(devices_information_widget_layout_bottom_widget)
        
        devices_setting_box = QGroupBox("LDPlayer Setting")
        devices_setting_box_layout = QVBoxLayout(devices_setting_box)
        
        devices_setting_box_layout_IP = QHBoxLayout()
        self.Checkbox = QCheckBox("Check IP")
        self.GPS = QCheckBox("GPS/TimeZone")
        self.BlockIP = QCheckBox("Block IP")
        devices_setting_box_layout_IP.addWidget(self.Checkbox)
        devices_setting_box_layout_IP.addWidget(self.GPS)
        devices_setting_box_layout_IP.addWidget(self.BlockIP)
        
        devices_setting_box_layout_auto_config = QHBoxLayout()
        label_auto_config = QCheckBox("Auto LDplayer Advanced Configuration")
        devices_setting_box_layout_auto_config.addWidget(label_auto_config)
        
        devices_setting_box_layout_cpu = QHBoxLayout()
        label_cpu = QLabel("CPU")
        label_cpu_list = QComboBox()
        label_cpu_list.addItems(["1 core","2 cores","3 cores","4 cores","5 cores","6 cores","7 cores","8 cores"])
        label_cpu_list.setCurrentIndex(1)
        label_ram = QLabel("RAM")
        label_ram_list = QComboBox()
        label_ram_list.addItems(["512MB","1GB","2GB","3GB","4GB"])
        
        devices_setting_box_layout_cpu.addWidget(label_cpu, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_box_layout_cpu.addWidget(label_cpu_list)
        devices_setting_box_layout_cpu.addWidget(label_ram, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_box_layout_cpu.addWidget(label_ram_list)

        devices_setting_box_layout_arrange = QHBoxLayout()
        label_arrange = QCheckBox("Arrange LDplayer")
        label_arrange_value = QSpinBox()
        label_arrange_value.setValue(5)
        label_arrange_value.setStyleSheet("margin: 0px;")
        Auto_fit = QCheckBox("Auto Fit")
        devices_setting_box_layout_arrange.addWidget(label_arrange)
        devices_setting_box_layout_arrange.addWidget(label_arrange_value)
        devices_setting_box_layout_arrange.addWidget(Auto_fit)
        

        devices_setting_box_layout_screen = QHBoxLayout()

        screen_resolution = QLabel("Screen")
        screen_resolution_list = QComboBox()
        screen_resolution_list.addItems(["1280x720","1920x1080","2560x1440","3840x2160"])
        screen_resolution_list.setCurrentIndex(1)
        devices_setting_box_layout_screen.addWidget(screen_resolution, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_box_layout_screen.addWidget(screen_resolution_list, alignment=Qt.AlignmentFlag.AlignCenter)


        devices_setting_box_layout_startup = QHBoxLayout()
        label_startup = QCheckBox("Run at Startup")
        label_startup_value = QSpinBox()
        label_startup_value.setValue(30)
        label_startup_value.setStyleSheet("margin: 0px;")
        label_startup_second = QLabel("Seconds")
        devices_setting_box_layout_startup.addWidget(label_startup)
        devices_setting_box_layout_startup.addWidget(label_startup_value)
        devices_setting_box_layout_startup.addWidget(label_startup_second)
        
        devices_setting_box_layout_autostop = QHBoxLayout()
        label_autostop = QCheckBox("Auto Stop at")
        label_autostop_value = QSpinBox()
        label_autostop_value.setValue(30)
        label_autostop_value.setStyleSheet("margin: 0px;")  
        label_autostop_second = QLabel("Minutes")
        label_autostop_shutdown = QCheckBox("Shutdown")
        
        devices_setting_box_layout_autostop.addWidget(label_autostop)
        devices_setting_box_layout_autostop.addWidget(label_autostop_value)
        devices_setting_box_layout_autostop.addWidget(label_autostop_second)
        devices_setting_box_layout_autostop.addWidget(label_autostop_shutdown)

        devices_setting_box_layout_clearcache = QHBoxLayout()
        label_clearcache = QCheckBox("Clear cache every run counts")
        label_clearcache_value = QSpinBox()
        label_clearcache_value.setValue(200)
        label_clearcache_value.setStyleSheet("margin: 0px;")
        devices_setting_box_layout_clearcache.addWidget(label_clearcache)
        devices_setting_box_layout_clearcache.addWidget(label_clearcache_value)
        
        devices_setting_box_layout_iffbexceed = QHBoxLayout()
        label_iffbexceed = QCheckBox("Clear FB user data if exceeds 900 MB")
        devices_setting_box_layout_iffbexceed.addWidget(label_iffbexceed)
        devices_setting_box_layout_ifldexceed = QHBoxLayout()
        label_ifldexceed = QCheckBox("Clear LDPlayer if exceeds ")
        label_ifldexceed_value = QSpinBox()
        label_ifldexceed_value.setValue(2)
        label_ifldexceed_value.setStyleSheet("margin: 0px;")
        label_ifldexceed_MB = QLabel("GB")
        devices_setting_box_layout_ifldexceed.addWidget(label_ifldexceed)
        devices_setting_box_layout_ifldexceed.addWidget(label_ifldexceed_value)
        devices_setting_box_layout_ifldexceed.addWidget(label_ifldexceed_MB)
        
        devices_setting_box_layout_closeld = QHBoxLayout()
        label_closeld = QCheckBox("Close all LD when stop")
        devices_setting_box_layout_closeld.addWidget(label_closeld)

        devices_setting_box_layout.addLayout(devices_setting_box_layout_IP)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_auto_config)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_cpu)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_arrange)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_screen)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_startup)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_autostop)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_clearcache)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_iffbexceed)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_ifldexceed)
        devices_setting_box_layout.addStretch(1)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_closeld)
        devices_setting_box_layout.addStretch(1)

        devices_setting_box.setStyleSheet("margin: 5px; padding: 0;")
        devices_setting_box_layout.setContentsMargins(10, 20, 0, 0)


        
        devices_information_widget_layout_bottom.addWidget(self.update_devices_table(), 6)
        devices_information_widget_layout_bottom.addWidget(devices_setting_box, 4)
        
        devices_information_widget_layout.addWidget(devices_information_widget_layout_top_widget, 1)
        devices_information_widget_layout.addWidget(devices_information_widget_layout_bottom_widget, 9)
        devices_information_widget_layout.setContentsMargins(0, 0, 0, 0)
        LDLabel = QLabel("LDplayer Setup")
        LDLabel.setStyleSheet("font-size: 40px; color: gray;margin: 10px 0px 10px 10px;")
        devices_widget_layout.addWidget(devices_browser_widget, 1)
        devices_widget_layout.addWidget(LDLabel, 1)
        devices_widget_layout.addWidget(devices_information_widget, 9)
        devices_widget_layout.setContentsMargins(30, 5, 5, 5)
        return devices_widget
    
    def update_devices_table(self) -> QTableWidget:
        
        list_devices = self.opt.check_ld_in_list()  # Sample [<LD Name>]
        MacS = self.opt.LD_devieces_detail("propertySettings.macAddress")  # Sample ["00:11:22:33:44:55"]
        Models = self.opt.LD_devieces_detail("propertySettings.phoneModel")  # Sample ["Model1", "Model2"]
        Manufacturers = self.opt.LD_devieces_detail("propertySettings.phoneManufacturer")  # Sample ["Manufacturer1", "Manufacturer2"]

        if not hasattr(self, "devices_table") or self.devices_table is None:
            self.devices_table = QTableWidget(0, 5)
            self.devices_table.setHorizontalHeaderLabels(["ID", "LD Name", "MAC", "Model", "M.facturer"])
            self.devices_table.verticalHeader().setVisible(False)
            self.devices_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.devices_table.setAutoFillBackground(False)
            self.devices_table.resizeColumnsToContents()
            self.devices_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.devices_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) 
            self.devices_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) 
            self.devices_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) 
            self.devices_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch) 
            self.update_exist_devices_table(list_devices, MacS, Models, Manufacturers)
        return self.devices_table

    def update_exist_devices_table(self, list_devices: list[str], MacS: list[str], Models: list[str], Manufacturers: list[str]) -> None:
        if not self.devices_table:
            return

        for i in range(0, len(list_devices)):
            self.devices_table.setRowCount(len(list_devices))
            self.devices_table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.devices_table.setItem(i, 1, QTableWidgetItem(list_devices[i]))
            self.devices_table.setItem(i, 2, QTableWidgetItem(MacS[i] if i < len(MacS) else ""))
            self.devices_table.setItem(i, 3, QTableWidgetItem(Models[i] if i < len(Models) else ""))
            self.devices_table.setItem(i, 4, QTableWidgetItem(Manufacturers[i] if i < len(Manufacturers) else ""))