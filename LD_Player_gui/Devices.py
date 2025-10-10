from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option

class Devices():
    def __init__(self, GUI):
        self.GUI = GUI
        self.opt = option()
        self.config = {
            "LD_loc": self.GUI.config["Devices"]["LD_loc"],
            "Sys_loc": self.GUI.config["Devices"]["Sys_loc"],
            "Number_Of_Active_LD": self.get_int("Number_Of_Active_LD"),
            "Wait_After_LD_Boot": self.get_int("Wait_After_LD_Boot"),
            "Between_LD_Minutes": self.get_int("Between_LD_Minutes"),
            "Hardware_Acceleration": self.get_bool("Hardware_Acceleration"),
            "NVIDIA_GPU": self.get_bool("NVIDIA_GPU"),
            "Check_Ip": self.get_bool("Check_Ip"),
            "GPS_Timezone": self.get_bool("GPS_Timezone"),
            "Block_Ip": self.get_bool("Block_Ip"),
            "Auto_Advance_config": self.get_bool("Auto_Advance_config"),
            "CPU_Count": self.get_int("CPU_Count"),
            "RAM_Count": self.get_int("RAM_Count"),
            "Arangement": self.get_bool("Arangement"),
            "Arangement_Count": self.get_int("Arangement_Count"),
            "Auto_Fit": self.get_bool("Auto_Fit"),
            "Screen_Resolution": self.GUI.config["Devices"]["Screen_Resolution"],
            "Run_At_Startup": self.get_bool("Run_At_Startup"),
            "Run_At_Startup_Seconds": self.get_int("Run_At_Startup_Seconds"),
            "Auto_Stop": self.get_bool("Auto_Stop"),
            "Auto_Stop_Minutes": self.get_int("Auto_Stop_Minutes"),
            "Shutdown": self.get_bool("Shutdown"),
            "Clear_Cache": self.get_bool("Clear_Cache"),
            "Clear_Cache_Count": self.get_int("Clear_Cache_Count"),
            "Clear_FB": self.get_bool("Clear_FB"),
            "Clear_LD": self.get_bool("Clear_LD"),
            "Clear_LD_GB": self.get_int("Clear_LD_GB"),
            "Close_All_When_Stop": self.get_bool("Close_All_When_Stop")
            
        }
        
        # Widgets
        self.LD_loc = QLineEdit(self.config["LD_loc"])
        self.browse_LD = QPushButton("Browse")
        
        self.Sys_loc = QLineEdit(self.config["Sys_loc"])
        self.browse_Sys = QPushButton("Browse")
        
        self.Number_Of_Active_LD = QSpinBox()
        self.Number_Of_Active_LD.setValue(self.config["Number_Of_Active_LD"])
        self.Wait_After_LD_Boot = QSpinBox()
        self.Wait_After_LD_Boot.setValue(self.config["Wait_After_LD_Boot"])
        self.Between_LD_Start = QSpinBox()
        self.Between_LD_Start.setValue(self.config["Between_LD_Minutes"])
        
        self.Hardware_Accel = QCheckBox("Hardware Accel")
        self.Hardware_Accel.setChecked(self.config["Hardware_Acceleration"])
        self.NVIDIA_GPU = QCheckBox("NVIDIA GPU")
        self.NVIDIA_GPU.setChecked(self.config["NVIDIA_GPU"])
    
        self.Checkip = QCheckBox("Check IP")
        self.GPS = QCheckBox("GPS/TimeZone")
        self.BlockIP = QCheckBox("Block IP")
        self.Checkip.setChecked(self.config["Check_Ip"])
        self.GPS.setChecked(self.config["GPS_Timezone"])
        self.BlockIP.setChecked(self.config["Block_Ip"])
        
        self.Auto_Advance_config = QCheckBox("Auto LDplayer Advanced Configuration")
        self.Auto_Advance_config.setChecked(self.config["Auto_Advance_config"])
        
        self.CPU_Count = QComboBox()
        self.CPU_Count.addItems(["1 core","2 cores","3 cores","4 cores","5 cores","6 cores","7 cores","8 cores"])
        self.CPU_Count.setCurrentIndex(self.get_int("CPU_Count")-1)
        self.RAM_MB = QComboBox()
        self.RAM_MB.addItems(["512MB","1GB","2GB","3GB","4GB"])
        self.RAM_MB.setCurrentIndex(self.get_int("RAM_Count")-1)
        
        self.Arangement = QCheckBox("Arrange LDplayer")
        self.Arangement_Count = QSpinBox()
        self.Arangement_Count.setValue(self.get_int("Arangement_Count"))
        self.Arangement_Count.setStyleSheet("margin: 0px;")
        self.Auto_Fit = QCheckBox("Auto Fit")
        self.Auto_Fit.setChecked(self.config["Auto_Fit"])
        
        self.Screen_Resolution = QComboBox()
        self.Screen_Resolution.addItems(["1280x720","1920x1080","2560x1440","3840x2160"])
        self.Screen_Resolution.setCurrentIndex(next((i for i in range(self.Screen_Resolution.count()) if self.Screen_Resolution.itemText(i) == self.GUI.config["Devices"]["Screen_Resolution"]), 0))
        
        self.Run_At_Startup = QCheckBox("Run at Startup")
        self.Run_At_Startup.setChecked(self.config["Run_At_Startup"])
        self.Run_At_Startup_Seconds = QSpinBox()
        self.Run_At_Startup_Seconds.setValue(self.get_int("Run_At_Startup_Seconds"))
        self.Run_At_Startup_Seconds.setStyleSheet("margin: 0px;")
        
        self.Auto_Stop = QCheckBox("Auto Stop at")
        self.Auto_Stop.setChecked(self.config["Auto_Stop"])
        self.Auto_Stop_Minutes = QSpinBox()
        self.Auto_Stop_Minutes.setValue(self.get_int("Auto_Stop_Minutes"))
        self.Auto_Stop_Minutes.setStyleSheet("margin: 0px;")
        
        self.Shutdown = QCheckBox("Shutdown")
        self.Shutdown.setChecked(self.config["Shutdown"])
        
        self.Clear_Cache = QCheckBox("Clear cache every run counts")
        self.Clear_Cache.setChecked(self.config["Clear_Cache"])
        self.Clear_Cache_Count = QSpinBox()
        self.Clear_Cache_Count.setValue(self.get_int("Clear_Cache_Count"))
        self.Clear_Cache_Count.setStyleSheet("margin: 0px;")
        
        self.Clear_FB = QCheckBox("Clear FB user data if exceeds 900 MB")
        self.Clear_FB.setChecked(self.config["Clear_FB"])
        self.Clear_LD = QCheckBox("Clear LDPlayer if exceeds ")
        self.Clear_LD.setChecked(self.config["Clear_LD"])
        self.Clear_LD_GB = QSpinBox()
        self.Clear_LD_GB.setValue(self.get_int("Clear_LD_GB"))
        self.Clear_LD_GB.setStyleSheet("margin: 0px;")
        
        self.Close_All_When_Stop = QCheckBox("Close all LD when stop")
        self.Close_All_When_Stop.setChecked(self.config["Close_All_When_Stop"])
        
        # trigger
        self.browse_LD.clicked.connect(self.LD_dir)
        self.browse_Sys.clicked.connect(self.Sys_dir)
        
        
        
        
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
        
        
        devices_locate_widget_layout_top.addWidget(labeltop1)
        devices_locate_widget_layout_top.addWidget(self.LD_loc)
        devices_locate_widget_layout_top.addWidget(self.browse_LD)
        
        
        devices_locate_widget_layout_bottom = QHBoxLayout()

        labelbottom1 = QLabel("System Location")
        
        devices_locate_widget_layout_bottom.addWidget(labelbottom1)
        devices_locate_widget_layout_bottom.addWidget(self.Sys_loc)
        devices_locate_widget_layout_bottom.addWidget(self.browse_Sys)

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
        label2 = QLabel("Wait after LD Boot")
        label3 = QCheckBox("Between LD Start")

        Gpu_box = QGroupBox()
        Gpu_vbox = QVBoxLayout(Gpu_box)
        Gpu_vbox.addWidget(self.Hardware_Accel)
        Gpu_vbox.addWidget(self.NVIDIA_GPU)
        
        label6 = QPushButton("App")
        devices_information_widget_layout_top.addWidget(label1)
        devices_information_widget_layout_top.addWidget(self.Number_Of_Active_LD)
        devices_information_widget_layout_top.addStretch(1)
        devices_information_widget_layout_top.addWidget(label2)
        devices_information_widget_layout_top.addWidget(self.Wait_After_LD_Boot)
        devices_information_widget_layout_top.addStretch(1)
        devices_information_widget_layout_top.addWidget(label3)
        devices_information_widget_layout_top.addWidget(self.Between_LD_Start)
        devices_information_widget_layout_top.addStretch(1)
        devices_information_widget_layout_top.addWidget(Gpu_box)
        devices_information_widget_layout_top.addWidget(label6)
        devices_information_widget_layout_top.setAlignment(Qt.AlignmentFlag.AlignVertical_Mask)

        devices_information_widget_layout_bottom_widget = QWidget()
        devices_information_widget_layout_bottom = QHBoxLayout(devices_information_widget_layout_bottom_widget)
        
        devices_setting_box = QGroupBox("LDPlayer Setting")
        devices_setting_box_layout = QVBoxLayout(devices_setting_box)
        
        devices_setting_box_layout_IP = QHBoxLayout()

        devices_setting_box_layout_IP.addWidget(self.Checkip)
        devices_setting_box_layout_IP.addWidget(self.GPS)
        devices_setting_box_layout_IP.addWidget(self.BlockIP)
        
        devices_setting_box_layout_auto_config = QHBoxLayout()
        devices_setting_box_layout_auto_config.addWidget(self.Auto_Advance_config)

        devices_setting_box_layout_cpu = QHBoxLayout()
        label_cpu = QLabel("CPU")
        label_ram = QLabel("RAM")
        devices_setting_box_layout_cpu.addWidget(label_cpu, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_box_layout_cpu.addWidget(self.CPU_Count)
        devices_setting_box_layout_cpu.addWidget(label_ram, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_box_layout_cpu.addWidget(self.RAM_MB)

        devices_setting_box_layout_arrange = QHBoxLayout()

        devices_setting_box_layout_arrange.addWidget(self.Arangement)
        devices_setting_box_layout_arrange.addWidget(self.Arangement_Count)
        devices_setting_box_layout_arrange.addWidget(self.Auto_Fit)
        

        devices_setting_box_layout_screen = QHBoxLayout()

        screen_resolution = QLabel("Screen")
        
        devices_setting_box_layout_screen.addWidget(screen_resolution, alignment=Qt.AlignmentFlag.AlignRight)
        devices_setting_box_layout_screen.addWidget(self.Screen_Resolution, alignment=Qt.AlignmentFlag.AlignLeft)


        devices_setting_box_layout_startup = QHBoxLayout()
        label_startup_second = QLabel("Seconds")
        devices_setting_box_layout_startup.addWidget(self.Run_At_Startup)
        devices_setting_box_layout_startup.addWidget(self.Run_At_Startup_Seconds)
        devices_setting_box_layout_startup.addWidget(label_startup_second)
        
        devices_setting_box_layout_autostop = QHBoxLayout()
        label_autostop_second = QLabel("Minutes")
        devices_setting_box_layout_autostop.addWidget(self.Auto_Stop)
        devices_setting_box_layout_autostop.addWidget(self.Auto_Stop_Minutes)
        devices_setting_box_layout_autostop.addWidget(label_autostop_second)
        devices_setting_box_layout_autostop.addWidget(self.Shutdown)

        devices_setting_box_layout_clearcache = QHBoxLayout()
        devices_setting_box_layout_clearcache.addWidget(self.Clear_Cache)
        devices_setting_box_layout_clearcache.addWidget(self.Clear_Cache_Count)
        
        devices_setting_box_layout_iffbexceed = QHBoxLayout()
        devices_setting_box_layout_iffbexceed.addWidget(self.Clear_FB)
        devices_setting_box_layout_ifldexceed = QHBoxLayout()
        label_ifldexceed_MB = QLabel("GB")
        devices_setting_box_layout_ifldexceed.addWidget(self.Clear_LD)
        devices_setting_box_layout_ifldexceed.addWidget(self.Clear_LD_GB)
        devices_setting_box_layout_ifldexceed.addWidget(label_ifldexceed_MB)
        
        devices_setting_box_layout_closeld = QHBoxLayout()
        devices_setting_box_layout_closeld.addWidget(self.Close_All_When_Stop)

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
    
    def LD_dir(self) -> None:
        dir = QFileDialog.getExistingDirectory(self.GUI, "Select LDPlayer Directory", "")
        if dir:
            print("Selected directory:", dir)
            self.LD_loc.setText(dir)
    def Sys_dir(self) -> None:
        dir = QFileDialog.getExistingDirectory(self.GUI, "Select System Directory", "")
        if dir:
            print("Selected directory:", dir)
            self.Sys_loc.setText(dir)

    def get_bool(self, value) -> bool:
        return self.GUI.config["Devices"][value] in [True, 'True', 'true', 1, '1']
    def get_int(self, value) -> int:
        return int(self.GUI.config["Devices"][value])
    
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