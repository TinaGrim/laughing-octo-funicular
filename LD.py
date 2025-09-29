import os
import sys
import cv2
import time
import signal
import dotenv
import logging
import requests
import platform
import threading
import webbrowser
from LD_Player import *
from typing import Optional
from threading import Thread
from flask import Flask, jsonify , request, url_for
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout

signal.signal(signal.SIGINT, signal.SIG_DFL)
dotenv.load_dotenv(dotenv_path=".env")



server = Flask(__name__)
Thread(target=lambda: server.run(port=5000),daemon=True).start()





class NoLog(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/LDActivity" not in record.getMessage()
logging.getLogger('werkzeug').addFilter(NoLog())

@server.before_request
def before_request():
    if "/LDActivity" not in request.path:
        print(f"[ \033[92mSERVER\033[0m ] {request.method} {request.path}")

@server.route("/")
def index():
    links = []
    for rule in server.url_map.iter_rules():
        if "GET" in getattr(rule, "methods", set()) and len(rule.arguments) == 0:
            links.append(f'<li><a href="{url_for(rule.endpoint)}">{url_for(rule.endpoint)}</a></li>')
    links.pop(0)  
    return f"<ul>{''.join(links)}</ul>"


LDActivity_data = {}
@server.route("/schedule")
def scheduleFunc():
    return jsonify(scheduleClose=GUI.scheduleCheck())

@server.route("/LDActivity", methods=["GET", "POST"])
def LDActivity():

    if request.method == "POST":
        data = request.get_json()

        for key in data.keys():
            LDActivity_data[key] = data[key]
        
        return jsonify(LDActivity=data)
    elif request.method == "GET":
        
        return jsonify(LDActivity=LDActivity_data)
    else:
        return jsonify(LDActivity=[])


RemainingID = []
@server.route("/openOrder", methods=["GET", "POST"])
def openOrder():

    for btn in GUI.LD_Button_list_qp.buttons():
        btn.setChecked(False)
        
    if request.method == "POST":
        ID = request.get_json()
        RemainingID.clear()
        RemainingID.extend(ID)
        print("[ \033[92mOK\033[0m ] " + "RemainingID after POST: ", RemainingID)
        return jsonify(openOrder=RemainingID)
    elif request.method == "GET":
        return jsonify(openOrder=RemainingID)
    else:
        return jsonify(openOrder=[])

class BobPrimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        global GUI
        GUI = self
        self.Grim = option()
        self.setWindowTitle("Girm Prime App")
        self.setGeometry(100, 100, 1900, 800)
        with open("style.qss") as f:
            self.setStyleSheet(f.read())
            
        
        self.logo = "Logo/logo_icon_big.png"
        if os.path.exists(self.logo):
            icon = QIcon(self.logo)
            self.setWindowIcon(icon)
        else:
            print("Some logo not found")
            sys.exit(1)
        #setup widgets
        self.time_label = QLabel()
        self.timer = QTimer()
        self.activityTimer = QTimer()
        self.DevicesTimer = QTimer()
        self.LDNameTimer = QTimer()
        self.DeviceList = QTimer()
        self.scheduleClose = False
        self.checkBox = QCheckBox()
        self.Check_Box_LD_Name = []
        self.Check_Box_List_Devices = []
        self.LD_Button_list_qp = QButtonGroup(self)
        self.LD_Button_list_qp.setExclusive(False)
        self.devices_list_qp = QButtonGroup(self)
        self.devices_list_qp.setExclusive(False)
        self.specific_ld_ID = []
        self.specific_list_devices_ID = []
        self.activity_LD = {}
        self.timeline_table_list = []


        #widgets
        self.Open_ld = QPushButton("➕")
        self.Open_ld.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.deleteButton = QPushButton("🗑️")
        self.deleteButton.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.createButton = QPushButton("✒️")
        self.createButton.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.qrbutton = QPushButton("💡")
        self.closeAppium = QCheckBox("Auto Close Appium")
        self.closeAppium.setChecked(True)
        
        #timer
        self.starttime = time.time()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)
        
        #table activity
        self.activityTimer.timeout.connect(self.update_activity_table)
        self.activityTimer.start(1000)
        
        #table LDName
        self.LDNameTimer.timeout.connect(self.update_auto_post_table)
        self.LDNameTimer.start(60000)
        self.LD_Button_list_qp.idToggled.connect(self.Select_LDPlayer)
        
        #table devices
        self.DevicesTimer.timeout.connect(self.update_devices_table)
        self.DevicesTimer.start(30000)

        #table devices list
        self.DeviceList.timeout.connect(self.update_devices_list)
        self.DeviceList.start(30000)
        self.devices_list_qp.idToggled.connect(self.Select_list_devices)
        
        #trigger
        self.Open_ld.clicked.connect(lambda: self.openLD())
        self.qrbutton.clicked.connect(lambda: self.open_qr("Logo/qr.jpg", 500, 800))
        self.closeAppium.stateChanged.connect(lambda: self.scheduleCheck())


        #Init
        self.update_time()
        self.init()


    def scheduleCheck(self) -> bool:
        self.scheduleClose = self.closeAppium.isChecked()
        return self.scheduleClose

    def openLD(self) -> None:
        if not self.specific_ld_ID:
            return
        self.select_all_ld.setChecked(False)
        self.selected_LD.setText(f"{0} Selected")
        self.start_thread(LDPlayer().run, self.specific_ld_ID)
        
    def check_activity(self) -> list[str]:
        try:
            self.drivers = self.Grim.current_ld()
            return self.drivers if self.drivers is not None else []
        except Exception as e:
            print(f"Error checking activity: {e}")
            return []
        
    def update_time(self) -> None:
        """Update the time label with current time using replace"""
        elapsed = int(time.time() - self.starttime)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_label.setText(f'<div style="font-size: 50px;">{hours:02}:{minutes:02}:{seconds:02}</div>')
        
        
        
    #======================================================================================================
    def update_activity_table(self)->QTableWidget:
        driver_list = self.check_activity()

        activity = requests.get("http://127.0.0.1:5000/LDActivity", {})
        activityData = activity.json()['LDActivity']

        if not hasattr(self,'table') or self.table is None:
            self.table = QTableWidget(0, 4)
 
            #config
            self.table.setHorizontalHeaderLabels(["No.", "LD Name", "ID", "Activity"])
            self.table.verticalHeader().setVisible(False)
            self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

            self.table.setAutoFillBackground(False)
            self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.table.resizeColumnsToContents()

            self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  
            self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  
            self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) 
        self.update_exist_activity_table(driver_list, activityData)
        return self.table

    def update_exist_activity_table(self, driver_list: list[str], activityData: list[dict]):

        if not driver_list:
            self.table.setRowCount(0)
            return
        for i, driverName in enumerate(driver_list):
            status = "No Action..."
            
            if driverName in activityData:
                status = activityData[driverName].get('status', 'No Action...')
            
            self.table.setRowCount(len(driver_list))
            self.table.setItem(i,0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i,1, QTableWidgetItem(driverName))
            self.table.setItem(i,2, QTableWidgetItem(str(int((int(driverName[-2:])-50)/2-1))))
            self.table.setItem(i,3, QTableWidgetItem(status))


        
    #=============================================================================================
    def update_devices_list(self) -> QWidget:
        list_devices = self.Grim.check_ld_in_list()  # Sample [<LD Name>]
        if not hasattr(self, "devices_list") or self.devices_list is None:
            self.devices_list = QTableWidget(0, 2)
            self.devices_list.setHorizontalHeaderLabels(["ID", "LD Name"])
            self.devices_list.verticalHeader().setVisible(False)
            self.devices_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.devices_list.setAutoFillBackground(False)
            self.devices_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.devices_list.resizeColumnsToContents()
            self.devices_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.devices_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        if getattr(self, "select_all_devices", None):
            self.select_all_devices.setChecked(False)
            self.selected_Devices.setText(f"{0} Selected")
        self.update_exist_devices_list(list_devices)
        return self.devices_list

    def update_exist_devices_list(self, list_devices: list[str]) -> None:
        if not self.devices_list:
            return
        for i in range(0, len(list_devices)):
            self.devices_list.setRowCount(len(list_devices))
            self.list_devices_checkBox = QCheckBox(str(i+1))
            self.devices_list_qp.addButton(self.list_devices_checkBox, i+1)
            self.devices_list.setCellWidget(i, 0, self.list_devices_checkBox)
            self.devices_list.setItem(i, 1, QTableWidgetItem(list_devices[i]))
            self.Check_Box_List_Devices.append(self.list_devices_checkBox)
            
    #==================================================================================================
    def update_active_table(self) -> QTableWidget:
        driver_list = self.Grim.check_ld_in_list()# Sample [<LD Name>]
        if not hasattr(self, 'active_table') or self.active_table is None:
            self.active_table = QTableWidget(0, 2)
            self.active_table.setHorizontalHeaderLabels(["ID", "LD Name"])
            self.active_table.verticalHeader().setVisible(False)
            self.active_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.active_table.setAutoFillBackground(False)
            self.active_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.active_table.resizeColumnsToContents()
            self.active_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.active_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) 
            self.active_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        if getattr(self, "select_all_active", None):
            self.select_all_active_ld.setChecked(False)
            self.selected_ld_active.setText(f"{0} Selected")
        self.update_exist_active_table(driver_list)
        return self.active_table

    def update_exist_active_table(self, driver_list: list[str]) -> None:
        if not driver_list:
            self.active_table.setRowCount(0)
            return

        for i, driver_name in enumerate(driver_list):
            self.active_table.setRowCount(len(driver_list))

            self.checkBox = QCheckBox(str(i + 1))
            self.active_table.setCellWidget(i, 0, self.checkBox)
            self.active_table.setItem(i, 1, QTableWidgetItem(driver_name))
        
    #==================================================================================================
    def update_auto_post_table(self) -> QTableWidget:

        driver_list = self.Grim.check_ld_in_list()# Sample [<LD Name>]

        if not hasattr(self, 'LDName_table') or self.LDName_table is None:
            self.LDName_table = QTableWidget(0, 2)
            self.LDName_table.setHorizontalHeaderLabels(["ID", "LD Name"])
            self.LDName_table.verticalHeader().setVisible(False)
            self.LDName_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.LDName_table.setAutoFillBackground(False)
            self.LDName_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            
            self.LDName_table.resizeColumnsToContents()
            self.LDName_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.LDName_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        if getattr(self, "select_all_ld", None):
            self.select_all_ld.setChecked(False)
            self.selected_LD.setText(f"{0} Selected")
        self.update_exist_auto_post_table(driver_list)
        return self.LDName_table
    
    def update_exist_auto_post_table(self, driver_list: list[str]) -> None:
        if not driver_list:
            self.LDName_table.setRowCount(0)
            return
        
        for i, driver_name in enumerate(driver_list):
            self.LDName_table.setRowCount(len(driver_list))
            
            self.checkBox = QCheckBox(str(i + 1))
            self.LD_Button_list_qp.addButton(self.checkBox, i + 1)
            self.LDName_table.setCellWidget(i, 0, self.checkBox)
            self.LDName_table.setItem(i, 1, QTableWidgetItem(driver_name))
            self.Check_Box_LD_Name.append(self.checkBox)
            
    #==================================================================================================
    def update_auto_post_timeline_table(self):
        logo1 = QTableWidgetItem()
        logo1.setIcon(QIcon("Logo/icons8-video-64.png"))
        
        logo2 = QTableWidgetItem()
        logo2.setIcon(QIcon("Logo/icons8-photo-64.png"))
        logo3 = QTableWidgetItem()
        logo3.setIcon(QIcon("Logo/icons8-book-64.png"))
        
        logo4 = QTableWidgetItem()
        logo4.setIcon(QIcon("Logo/icons8-reel-50.png"))
        
        time = QTableWidgetItem("time")
        x = QTableWidgetItem("x")
        if not hasattr(self, 'time_line_table') or self.timeline_table is None:
            self.timeline_table = QTableWidget(0, 6)
            self.timeline_table.setHorizontalHeaderItem(0, logo1)
            self.timeline_table.setHorizontalHeaderItem(1, logo2)
            self.timeline_table.setHorizontalHeaderItem(2, logo3)
            self.timeline_table.setHorizontalHeaderItem(3, logo4)
            self.timeline_table.setHorizontalHeaderItem(4, time)
            self.timeline_table.setHorizontalHeaderItem(5, x)
            # Example: set width for each column
            self.timeline_table.setColumnWidth(0, 50)
            self.timeline_table.setColumnWidth(1, 50)
            self.timeline_table.setColumnWidth(2, 50)
            self.timeline_table.setColumnWidth(3, 50)  
            self.timeline_table.setColumnWidth(4, 100) 
            self.timeline_table.setColumnWidth(5, 120) 

            self.timeline_table.verticalHeader().setVisible(False)
            self.timeline_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.timeline_table.setAutoFillBackground(False)
            self.timeline_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.update_exits_auto_post_timeline_table()
        return self.timeline_table

    def update_exits_auto_post_timeline_table(self):
        if not self.timeline_table:
            return
        for i in range(0, len(self.timeline_table_list)):
            self.timeline_table.setRowCount(len(self.timeline_table_list))
            self.timeline_table.setItem(i, 0, QTableWidgetItem(self.timeline_table_list[i][0]))
            self.timeline_table.setItem(i, 1, QTableWidgetItem(self.timeline_table_list[i][1]))
            self.timeline_table.setItem(i, 2, QTableWidgetItem(self.timeline_table_list[i][2]))
            self.timeline_table.setItem(i, 3, QTableWidgetItem(self.timeline_table_list[i][3]))
            self.timeline_table.setItem(i, 4, QTableWidgetItem(self.timeline_table_list[i][4]))
            self.timeline_table.setItem(i, 5, QTableWidgetItem(self.timeline_table_list[i][5]))
        return self.timeline_table
    #===================================================================================================
    def update_devices_table(self) -> QTableWidget:
        
        list_devices = self.Grim.check_ld_in_list()  # Sample [<LD Name>]
        MacS = self.Grim.LD_devieces_detail("propertySettings.macAddress")  # Sample ["00:11:22:33:44:55"]
        Models = self.Grim.LD_devieces_detail("propertySettings.phoneModel")  # Sample ["Model1", "Model2"]
        Manufacturers = self.Grim.LD_devieces_detail("propertySettings.phoneManufacturer")  # Sample ["Manufacturer1", "Manufacturer2"]
        
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


    def init(self) -> None:
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        """"Tabs"""
        cornerContainer = QWidget()
        cornerLayout = QHBoxLayout()

        lineSearch = QLineEdit()
        lineSearch.setPlaceholderText("Search...")
        lineSearch.setFixedHeight(24)  
        lineSearch.setStyleSheet("margin: 0px; padding: 2px;")  

        cornerSwitchButton = QPushButton("Switch")
        cornerSwitchButton.setStyleSheet("margin: 0px; padding: 4px 20px; ")
        cornerFlagButton = QPushButton("Flag")
        cornerFlagButton.setStyleSheet("margin: 0px; padding: 4px 20px; ")
        cornerSaveButton = QPushButton("Save")
        cornerSaveButton.setStyleSheet("margin: 0px; padding: 4px 20px; ")

        cornerLayout.addWidget(cornerSwitchButton)
        cornerLayout.addWidget(cornerFlagButton)
        cornerLayout.addWidget(lineSearch)
        cornerLayout.addWidget(cornerSaveButton)
        cornerLayout.setContentsMargins(0, 0, 0, 0)
        cornerLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  

        
        cornerContainer.setLayout(cornerLayout)
        cornerContainer.setFixedHeight(30) 
        cornerContainer.setStyleSheet("margin: 0px;")

        self.Tabs = QTabWidget()
        self.Tabs.addTab(self.Tab_Devices(), "Devices")
        self.Tabs.addTab(self.Tab_Active(), "Active")
        self.Tabs.addTab(self.Tab_auto_post(), "Auto Post")
        self.Tabs.addTab(self.Tab_manage(), "Manage")
        self.Tabs.setCornerWidget(cornerContainer) 
        """End Tabs"""
        
        """Inside the main layout"""
        main_layout.addWidget(self.Left_view(), 3) 
        main_layout.addWidget(self.Tabs, 7)
             
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

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
    
    def Tab_Active(self) -> QWidget:
        active_widget = QWidget()
        active_layout = QHBoxLayout(active_widget)
        active_layout.setContentsMargins(0, 0, 0, 0)
        
        #
        #active
        #
        active_widget_main = QWidget()
        active_layout_main = QVBoxLayout(active_widget_main)
        active_layout_main.setContentsMargins(0, 0, 0, 0)
        
        active_widget_main_top = QWidget()
        active_layout_main_top = QGridLayout(active_widget_main_top)
        active_layout_main_top.setContentsMargins(10, 10, 0, 0)
        
        #
        #notify action
        #

        self.check_primary_location = QCheckBox("Check Primary Location")
        self.check_primary_location.setChecked(False)
        self.check_notification = QCheckBox("Check Notification")
        self.check_notification.setChecked(False)
        self.check_notification_value = QSpinBox()
        self.check_notification_value.setValue(0)
        #
        #scroll action
        #
        self.scroll_newsfeed = QCheckBox("Scroll News Feed")
        self.scroll_newsfeed.setChecked(False)
        self.scroll_newsfeed_start_value = QSpinBox()
        self.scroll_newsfeed_start_value.setValue(0)
        self.scroll_newsfeed_widget = QWidget()
        self.scroll_newsfeed_layout = QHBoxLayout(self.scroll_newsfeed_widget)
        self.scroll_newsfeed_end_value = QSpinBox()
        self.scroll_newsfeed_end_value.setValue(0)
        self.scroll_newsfeed_layout.addWidget(self.scroll_newsfeed_end_value)
        self.scroll_newsfeed_layout.addWidget(QLabel("Minutes"))
        self.scroll_newsfeed_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_video = QCheckBox("Scroll Video")
        self.scroll_video.setChecked(False)
        self.scroll_video_start_value = QSpinBox()
        self.scroll_video_start_value.setValue(0)
        self.scroll_video_widget = QWidget()
        self.scroll_video_layout = QHBoxLayout(self.scroll_video_widget)
        self.scroll_video_end_value = QSpinBox()
        self.scroll_video_end_value.setValue(0)
        self.scroll_video_layout.addWidget(self.scroll_video_end_value)
        self.scroll_video_layout.addWidget(QLabel("Minutes"))
        self.scroll_video_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_reels = QCheckBox("Scroll Reels")
        self.scroll_reels.setChecked(False)
        self.scroll_reels_start_value = QSpinBox()
        self.scroll_reels_start_value.setValue(0)
        self.scroll_reels_widget = QWidget()
        self.scroll_reels_layout = QHBoxLayout(self.scroll_reels_widget)
        self.scroll_reels_end_value = QSpinBox()
        self.scroll_reels_end_value.setValue(0)
        self.scroll_reels_layout.addWidget(self.scroll_reels_end_value)
        self.scroll_reels_layout.addWidget(QLabel("Minutes"))
        self.scroll_reels_layout.setContentsMargins(0, 0, 0, 0)
        
        #
        #confirm action
        #
        self.confirm_friend = QCheckBox("Confirm Friend")
        self.confirm_friend.setChecked(False)
        self.confirm_friend_value = QSpinBox()
        self.confirm_friend_value.setValue(0)
        self.add_friend = QCheckBox("Add Friend")
        self.add_friend.setChecked(False)
        self.add_friend_value = QSpinBox()
        self.add_friend_value.setValue(0)
        #
        # post action
        #
        self.reaction_post = QCheckBox("Reaction Post")
        self.reaction_post.setChecked(False)
        self.reaction_post_value = QSpinBox()
        self.reaction_post_value.setValue(0)
        #
        # check message action
        #
        self.check_message = QCheckBox("Check Message")
        self.check_message.setChecked(False)
        self.check_message_value = QSpinBox()
        self.check_message_value.setValue(0)
        self.reply_widget = QWidget()
        self.reply_layout = QHBoxLayout(self.reply_widget)
        self.reply = QCheckBox("Reply")
        self.reply.setChecked(False)
        self.reply_value = QLineEdit()
        self.reply_value.setText(r"{Hi|Hello|Hey|How are you}")
        self.reply_layout.addWidget(self.reply)
        self.reply_layout.addWidget(self.reply_value)
        self.reply_layout.setContentsMargins(0, 0, 0, 0)

        #
        # create post action
        #
        self.create_post = QCheckBox("Create Post")
        self.create_post.setChecked(False)
        self.create_post_value = QSpinBox()
        self.create_post_value.setValue(0)
        self.photo_img = QCheckBox("Photo")
        self.photo_img.setChecked(False)
        self.photo_widget = QWidget()
        self.photo_layout = QHBoxLayout(self.photo_widget)
        self.photo_img_value = QLineEdit()
        self.photo_img_value.setText(r"C:/path/to/photo.jpg")
        self.photo_img_browse = QPushButton("...")
        self.photo_img_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")

        self.photo_layout.addWidget(self.photo_img)
        self.photo_layout.addWidget(self.photo_img_value)
        self.photo_layout.addWidget(self.photo_img_browse)
        self.photo_layout.setContentsMargins(0, 0, 0, 0)
        
        #
        # story action
        #
        self.check_Story = QCheckBox("Check Story")
        self.check_Story.setChecked(False)
        self.check_Story_value = QSpinBox()
        self.check_Story_value.setValue(0)
        self.story_video_widget = QWidget()
        self.story_video_layout = QHBoxLayout(self.story_video_widget)
        self.story_video_value = QLineEdit()
        self.story_video_value.setText(r"C:/path/to/video.mp4")
        self.story_video_browse = QPushButton("...")
        self.story_video_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")

        self.story_video_layout.addWidget(self.story_video_value)
        self.story_video_layout.addWidget(self.story_video_browse)
        self.story_video_layout.setContentsMargins(0, 0, 0, 0)
        #
        # comment action
        #
        self.comment_post = QCheckBox("Comment Post")
        self.comment_post.setChecked(False)
        self.comment_post_value = QSpinBox()
        self.comment_post_value.setValue(0)
        self.comment_post_value_box = QLineEdit()
        self.comment_post_value_box.setText(r"comment1, comment2, comment3")
        
        #
        # share action
        #
        self.share_post_group = QCheckBox("Share Post to Group")
        self.share_post_group.setChecked(False)
        self.share_post_group_value = QSpinBox()
        self.share_post_group_value.setValue(0)
        self.profile_widget = QWidget()
        self.profile_layout = QHBoxLayout(self.profile_widget)
        self.profile = QCheckBox("Profile")
        self.profile_group_value = QLineEdit()
        self.profile_group_value.setPlaceholderText(r"profile link1, profile link2, profile link3")
        self.profile_layout.addWidget(self.profile)
        self.profile_layout.addWidget(self.profile_group_value)
        self.profile_layout.setContentsMargins(0, 0, 0, 0)
        #
        # loop action
        #
        self.Number_loop_time_label = QLabel("Number of Active Loops")
        self.Number_loop_time_value = QSpinBox()
        self.Number_loop_time_value.setValue(1)
        self.active_between_time = QCheckBox("Active Between Time")
        self.active_between_time.setChecked(False)
        self.active_between_time_start_value = QSpinBox()
        self.active_between_time_start_value.setValue(0)
        self.active_between_time_end_value = QSpinBox()
        self.active_between_time_end_value.setValue(0)
        #
        # install apk action
        #
        self.install_apk_widget = QWidget()
        self.install_apk_layout = QHBoxLayout(self.install_apk_widget)
        self.install_apk = QCheckBox("Install APK")
        self.install_apk.setChecked(False)
        self.install_apk_value = QLineEdit()
        self.install_apk_value.setText(r"C:/path/to/app.apk")
        self.install_apk_browse = QPushButton("...")
        self.install_apk_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        self.install_apk_layout.addWidget(self.install_apk)
        self.install_apk_layout.addWidget(self.install_apk_value)
        self.install_apk_layout.addWidget(self.install_apk_browse)
        self.install_apk_layout.setContentsMargins(0, 0, 0, 0)
        
        #
        # shutdown action
        #
        self.shutdown_when_finish = QCheckBox("Shutdown when finish")
        self.shutdown_when_finish.setChecked(False)


        active_layout_main_top.addWidget(self.check_notification, 0, 0)
        active_layout_main_top.addWidget(self.check_notification_value, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.check_primary_location, 0, 3)
        active_layout_main_top.addWidget(self.scroll_newsfeed, 1, 0)
        active_layout_main_top.addWidget(self.scroll_newsfeed_start_value, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.scroll_newsfeed_widget, 1, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.scroll_video, 2, 0)
        active_layout_main_top.addWidget(self.scroll_video_start_value, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.scroll_video_widget, 2, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.scroll_reels, 3, 0)
        active_layout_main_top.addWidget(self.scroll_reels_start_value, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 3, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.scroll_reels_widget, 3, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.confirm_friend, 4, 0)
        active_layout_main_top.addWidget(self.confirm_friend_value, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.add_friend, 4, 2)
        active_layout_main_top.addWidget(self.add_friend_value, 4, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.reaction_post, 5, 0)
        active_layout_main_top.addWidget(self.reaction_post_value, 5, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.check_message, 6, 0)
        active_layout_main_top.addWidget(self.check_message_value, 6, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.reply_widget, 6, 2, 1, 2)
        active_layout_main_top.addWidget(self.create_post, 7, 0)
        active_layout_main_top.addWidget(self.create_post_value, 7, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.photo_widget, 7, 2, 1, 2)
        active_layout_main_top.addWidget(self.check_Story, 8, 0)
        active_layout_main_top.addWidget(self.check_Story_value, 8, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.story_video_widget, 8, 2, 1, 2)
        active_layout_main_top.addWidget(self.comment_post, 9, 0)
        active_layout_main_top.addWidget(self.comment_post_value, 9, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.comment_post_value_box, 9, 2, 1, 2)
        active_layout_main_top.setColumnStretch(3, 1)
        active_layout_main_top.addWidget(self.share_post_group, 10, 0)
        active_layout_main_top.addWidget(self.share_post_group_value, 10, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.profile_widget, 10, 2, 1, 2)
        active_layout_main_top.addWidget(self.Number_loop_time_label, 11, 0)
        active_layout_main_top.addWidget(self.Number_loop_time_value, 11, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("Times"), 11, 2)
        active_layout_main_top.addWidget(self.active_between_time, 12, 0)
        active_layout_main_top.addWidget(self.active_between_time_start_value, 12, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 12, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.active_between_time_end_value, 12, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.shutdown_when_finish, 13, 0)
        active_layout_main_top.addWidget(self.install_apk_widget, 13, 1, 1, 3)
        active_layout_main_top.setRowStretch(14, 1)
        active_layout_main_top.setSpacing(18)


        #
        #facebook app name
        #       
        facebook_app_widget = QWidget()
        facebook_app_layout = QVBoxLayout(facebook_app_widget)
        
        facebook_app = QHBoxLayout()
        facebook_app_label = QLabel("Facebook App Number")
        facebook_app_value = QSpinBox()
        facebook_app_value.setValue(1)
        facebook_app_switch_account = QCheckBox("Switch Account")
        facebook_app.addWidget(facebook_app_label)
        facebook_app.addWidget(facebook_app_value)
        facebook_app.addStretch(1)
        facebook_app.addWidget(facebook_app_switch_account)
        facebook_app.addWidget(QLabel("ID-1"))
        
        facebook_app_layout.addLayout(facebook_app)

        active_layout_main.addWidget(active_widget_main_top, 9)
        active_layout_main.addWidget(facebook_app_widget, 1)
        
        #
        #table
        #
        active_table_widget = QWidget()
        active_table_layout = QVBoxLayout(active_table_widget)
        #
        #header
        #
        active_table_layout_top_widget = QWidget()
        active_table_layout_top = QHBoxLayout(active_table_layout_top_widget)
        self.enable_active = QCheckBox("Enable Active")
        self.enable_active.setChecked(True)
        self.select_all_active_ld = QCheckBox("Select All")
        active_table_layout_top.addWidget(self.enable_active)
        active_table_layout_top.addStretch(1)
        active_table_layout_top.addWidget(self.select_all_active_ld)

        #
        #bottom
        #
        active_table_bottom_widget = QWidget()
        active_table_bottom_layout = QHBoxLayout(active_table_bottom_widget)
        self.selected_ld_active = QLabel("Selected")
        self.active_selected_start = QSpinBox()
        self.active_selected_start.setValue(0)
        self.active_selected_stop = QSpinBox()
        self.active_selected_stop.setValue(len(self.Grim.check_ld_in_list()))
        self.active_selected_click = QPushButton("Here")
        
        active_table_bottom_layout.addWidget(self.selected_ld_active)
        active_table_bottom_layout.addStretch(1)
        active_table_bottom_layout.addWidget(self.active_selected_start)
        active_table_bottom_layout.addWidget(self.active_selected_stop)
        active_table_bottom_layout.addWidget(self.active_selected_click)

        active_table_layout.addWidget(active_table_layout_top_widget)
        active_table_layout.addWidget(self.update_active_table())
        active_table_layout.addWidget(active_table_bottom_widget)
        
        active_layout.addWidget(active_widget_main, 8)
        active_layout.addWidget(active_table_widget, 2)
        return active_widget

    def Tab_manage(self) -> QWidget:
        ld_manage_widget = QWidget()
        ld_manage_layout = QHBoxLayout(ld_manage_widget)
        ld_manage_layout.setContentsMargins(0, 0, 0, 0)
        ld_manage_layout.setSpacing(5)
        #
        #left
        #
        ld_manage_list = QWidget()
        manage_list_layout = QVBoxLayout(ld_manage_list)
        

        
        manage_list_layout.addWidget(self.update_devices_list(),9)
        manage_list_layout.addWidget(self.selected_list_devices(), 1)
        manage_list_layout.setContentsMargins(5, 20, 0, 0)
        #
        #right
        #
        ld_manage_manager = QWidget()
        ld_manage_manager_layout = QVBoxLayout(ld_manage_manager)
        ld_manage_manager_layout.setContentsMargins(0, 10, 0, 0)

        ld_manage_group_boxtop = QGroupBox("Enable LDPlayer Manager")
        ld_manage_group_boxtop.setCheckable(True)
        ld_manage_group_boxtop.setChecked(True)
        ld_manage_manager_layout_top = QVBoxLayout(ld_manage_group_boxtop)
        
        number_active = QHBoxLayout()
        number = QLabel("Number of Active Batch")
        number_value = QSpinBox()
        number_value.setStyleSheet("margin: 0px;")
        
        number_value.setValue(1)
        number_active.addWidget(number)
        number_active.addWidget(number_value)
        number_active.addStretch(1)

        new_ld = QHBoxLayout()
        new_ld_label = QCheckBox("Add New LDPlayers")
        new_ld_value = QSpinBox()
        new_ld_value.setValue(1)
        new_ld_value.setStyleSheet("margin: 0px;")

        copy_from = QCheckBox("Copy From")
        copy_from_value = QComboBox()
        copy_from_value.addItems(self.Grim.check_ld_in_list())
        copy_from_value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        
        new_ld.addWidget(new_ld_label)
        new_ld.addWidget(new_ld_value)
        new_ld.addWidget(copy_from)
        new_ld.addWidget(copy_from_value)
        
        backup = QHBoxLayout()
        backup_label = QCheckBox("Backup LDPlayer To")
        backup_value = QLineEdit()
        backup_value.setText(r"C:/path/to/backup.zip")
        backup_browse = QPushButton("...")
        backup_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        
        backup.addWidget(backup_label)
        backup.addWidget(backup_value)
        backup.addWidget(backup_browse)
        
        restore = QHBoxLayout()
        restore_label = QCheckBox("Restore LDPlayer From")
        restore_value = QLineEdit()
        restore_value.setText(r"C:/path/to/backup.zip")
        restore_browse = QPushButton("...")
        restore_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        
        restore.addWidget(restore_label)
        restore.addWidget(restore_value)
        restore.addWidget(restore_browse)
        
        remove = QHBoxLayout()
        remove_label = QCheckBox("Remove LDPlayer")
        remove.addWidget(remove_label)
        shutdown = QHBoxLayout()
        shutdown_label = QCheckBox("Shutdown PC When Finish")
        shutdown.addWidget(shutdown_label)
        
        ld_manage_manager_layout_top.addLayout(number_active)
        ld_manage_manager_layout_top.addLayout(new_ld)
        ld_manage_manager_layout_top.addLayout(backup)
        ld_manage_manager_layout_top.addLayout(restore)
        ld_manage_manager_layout_top.addLayout(remove)
        ld_manage_manager_layout_top.addLayout(shutdown)
        ld_manage_manager_layout_top.addStretch(1)

        ld_manage_manager_layout_top.setContentsMargins(10, 20, 0, 0)
        
        ld_manage_group_boxbottom = QGroupBox("Enable LDPlayer Manager")
        ld_manage_group_boxbottom.setCheckable(True)
        ld_manage_group_boxbottom.setChecked(True)
        ld_manage_manager_layout_bottom = QVBoxLayout(ld_manage_group_boxbottom)
        autoput = QHBoxLayout()
        autoput_label = QCheckBox("Auto Pull Account/Page Name")
        clear_existing = QCheckBox("Clear Existing Names")
        
        autoput.addWidget(autoput_label)
        autoput.addWidget(clear_existing)
        autoput.addStretch(1)
        
        FBlocal = QHBoxLayout()
        FBlocal_label = QCheckBox("FB Login")
        FBlocal_value = QLineEdit()
        FBlocal_value.setText(r"C:/path/to/FBlocal.txt")
        FBlocal_browse = QPushButton("...")
        FBlocal_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        account_page_name = QCheckBox("Account/Page Name")
        account_page_name_btn = QPushButton("@")
        account_page_name_btn.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        FBlocal.addWidget(FBlocal_label)
        FBlocal.addWidget(FBlocal_value)
        FBlocal.addWidget(FBlocal_browse)
        FBlocal.addWidget(account_page_name)
        FBlocal.addWidget(account_page_name_btn)
        
        createpage = QHBoxLayout()
        createpage_label = QCheckBox("Create Pages")
        createpage.addWidget(createpage_label)
        shutdownbottom = QHBoxLayout()
        shutdownbottom_label = QCheckBox("Shutdown PC When Finish")
        shutdownbottom.addWidget(shutdownbottom_label)

        ld_manage_manager_layout_bottom.addLayout(autoput)
        ld_manage_manager_layout_bottom.addLayout(FBlocal)
        ld_manage_manager_layout_bottom.addLayout(createpage)
        ld_manage_manager_layout_bottom.addLayout(shutdownbottom)
        ld_manage_manager_layout_bottom.addStretch(1)
        ld_manage_manager_layout_bottom.setContentsMargins(10, 20, 0, 0)

        ld_manage_group_boxtop.setStyleSheet("margin: 8px;")
        ld_manage_group_boxbottom.setStyleSheet("margin: 8px;")

        ld_manage_manager_layout.addWidget(ld_manage_group_boxtop)
        ld_manage_manager_layout.addWidget(ld_manage_group_boxbottom)
        ld_manage_layout.addWidget(ld_manage_list, 3)
        ld_manage_layout.addWidget(ld_manage_manager, 7)

        return ld_manage_widget
    

    def Tab_auto_post(self) -> QWidget:

        auto_post_widget = QWidget()
        auto_post_layout = QHBoxLayout()
        auto_post_layout.setContentsMargins(0, 0, 0, 0)  
        auto_post_layout.setSpacing(5)  
        #
        # On left side
        #
        """Schedule"""
        Group_Box_Schedule = QGroupBox()
        Group_schedule = QVBoxLayout()
        
        
        Group_schedule.addWidget(QCheckBox("Enable Schedule Post"))
        Group_schedule.addWidget(QCheckBox("Enable Post When Run"))
        Group_schedule.addWidget(QCheckBox("Shutdown PC"))
        Group_schedule.addWidget(self.closeAppium)
        Group_Box_Schedule.setLayout(Group_schedule)
        """End Schedule"""
        

        
        auto_post_layout_left_widget = QWidget()
        auto_post_layout_left = QVBoxLayout()
        
        auto_post_layout_left.addWidget(Group_Box_Schedule)
        auto_post_layout_left.addWidget(self.update_auto_post_table())
        auto_post_layout_left.addWidget(self.selected_LD_name())
        auto_post_layout_left.setContentsMargins(5, 20, 0, 0)
        auto_post_layout_left_widget.setLayout(auto_post_layout_left)
        auto_post_layout_left_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        #
        # On right side
        #
        auto_post_layout_right_widget = QWidget()
        auto_post_layout_right = QVBoxLayout()
        
        """"Header"""
        auto_post_layout_Header = QHBoxLayout()

        auto_post_layout_Header.addWidget(self.Open_ld)
        auto_post_layout_Header.addWidget(self.deleteButton)
        auto_post_layout_Header.addWidget(self.createButton)
  
        """End Header"""
        
        """Page Setup Group"""
        page_setup_layout_Group = QGroupBox("Page Setup")
        page_setup_layout_Group_Layout = QVBoxLayout(page_setup_layout_Group)
        
        page_setup_header = QHBoxLayout()
        self.enable_post = QCheckBox("Enable Post")
        self.enable_post.setChecked(False)
        page_setup_name = QLabel("Page Name")
        page_setup_name_value = QLineEdit("Grim")
        page_setup_app = QLabel("App")
        page_setup_app_value = QLineEdit("com.facebook.katana")
        page_setup_header.addWidget(self.enable_post)
        page_setup_header.addWidget(page_setup_name)
        page_setup_header.addWidget(page_setup_name_value)
        page_setup_header.addWidget(page_setup_app)
        page_setup_header.addWidget(page_setup_app_value)
        
        
        page_setup_main_widget = QWidget()
        page_setup_main_layout = QVBoxLayout(page_setup_main_widget)
        
        Tab_page_setup = QTabWidget()
        Tab_page_setup.addTab(QLabel("Reel"), "Reel")
        Tab_page_setup.addTab(QLabel("Text"), "Text")
        Tab_page_setup.addTab(QLabel("Story"), "Story")
        Tab_page_setup.addTab(QLabel("Video"), "Video")
        
        page_setup_bottom_widget = QWidget()
        page_setup_bottom_layout = QHBoxLayout(page_setup_bottom_widget)
        
        page_setup_schedule_widget = QWidget()
        page_setup_schedule_layout = QVBoxLayout(page_setup_schedule_widget)
        
        page_setup_post_on = QGroupBox("Comment on post")
        page_setup_post_on_layout = QHBoxLayout(page_setup_post_on)
        self.Reel = QCheckBox("Reel")
        self.Text = QCheckBox("Photo")
        self.Story = QCheckBox("video")
        page_setup_post_on_layout.addWidget(self.Reel)
        page_setup_post_on_layout.addWidget(self.Text)
        page_setup_post_on_layout.addWidget(self.Story)
        page_setup_post_on_layout.setContentsMargins(5, 0, 0, 0)
        page_setup_post_on.setStyleSheet("margin: 10px 0px; padding: 0px;")
        
        
        page_setup_schedule_day = QGroupBox("Everyday")
        page_setup_schedule_day.setCheckable(True)
        page_setup_schedule_day.setChecked(True)
        
        page_setup_schedule_day_layout = QVBoxLayout(page_setup_schedule_day)
        
        page_setup_schedule_day_widget1 = QWidget()
        page_setup_schedule_day_layout1 = QHBoxLayout(page_setup_schedule_day_widget1)
        self.Monday = QCheckBox("Mon")
        self.Tuesday = QCheckBox("Tue")
        self.Wednesday = QCheckBox("Wed")
        self.Thursday = QCheckBox("Thu")
        page_setup_schedule_day_widget2 = QWidget()
        page_setup_schedule_day_layout2 = QHBoxLayout(page_setup_schedule_day_widget2)
        
        self.Friday = QCheckBox("Fri")
        self.Saturday = QCheckBox("Sat")
        self.Sunday = QCheckBox("Sun")
        page_setup_schedule_day_layout1.addWidget(self.Monday)
        page_setup_schedule_day_layout1.addWidget(self.Tuesday)
        page_setup_schedule_day_layout1.addWidget(self.Wednesday)
        page_setup_schedule_day_layout1.addWidget(self.Thursday)
        page_setup_schedule_day_layout1.addStretch(1)
        
        page_setup_schedule_day_layout1.setContentsMargins(5, 0, 0, 0)
        page_setup_schedule_day_widget1.setStyleSheet("margin: 10px 0px 0px 0px; padding: 0px;")
        
        
        page_setup_schedule_day_layout2.addWidget(self.Friday)
        page_setup_schedule_day_layout2.addWidget(self.Saturday)
        page_setup_schedule_day_layout2.addWidget(self.Sunday)
        page_setup_schedule_day_layout2.addStretch(1)
        
        page_setup_schedule_day_layout2.setContentsMargins(5, 0, 0, 0)
        page_setup_schedule_day_widget2.setStyleSheet("margin: 0px 0px 0px 0px; padding: 0px;")
        
        page_setup_schedule_day.setStyleSheet("margin: 10px 0px; padding: 0px;")
        
        page_setup_schedule_day_layout.addWidget(page_setup_schedule_day_widget1)
        page_setup_schedule_day_layout.addWidget(page_setup_schedule_day_widget2)
        page_setup_schedule_day_layout.setContentsMargins(0, 0, 0, 0)
        
        page_setup_schedule_layout.addWidget(page_setup_post_on)
        page_setup_schedule_layout.addStretch(1)
        page_setup_schedule_layout.addWidget(page_setup_schedule_day)
        
        page_setup_schedule_layout.setContentsMargins(0, 0, 0, 0)
        page_setup_schedule_widget.setStyleSheet("margin: 5px; padding: 0px;")
        
        page_setup_timeline = QWidget()
        page_setup_timeline_layout = QVBoxLayout(page_setup_timeline)
        
        page_setup_timeline_group = QGroupBox()
        page_setup_timeline_group_layout = QVBoxLayout(page_setup_timeline_group)
        page_setup_timeline_group_layout.addWidget(self.update_auto_post_timeline_table())
        

        page_setup_timeline_bottom = QHBoxLayout()
        self.dashboard = QCheckBox("Dashboard")
        self.posttable = QPushButton("☰ Post Table")
        self.timeline = QPushButton("⏱︎ Timeline")
        page_setup_timeline_bottom.addWidget(self.dashboard)
        page_setup_timeline_bottom.addWidget(self.posttable)
        page_setup_timeline_bottom.addWidget(self.timeline)
        
        page_setup_timeline_layout.addWidget(page_setup_timeline_group)
        page_setup_timeline_layout.addLayout(page_setup_timeline_bottom)

        page_setup_bottom_layout.addWidget(page_setup_schedule_widget)
        page_setup_bottom_layout.addWidget(page_setup_timeline)
        page_setup_bottom_layout.setContentsMargins(0, 0, 0, 0)
        page_setup_bottom_widget.setStyleSheet("margin: 0px; padding: 0px;")
        
        page_setup_main_layout.addWidget(Tab_page_setup)
        page_setup_main_layout.addWidget(page_setup_bottom_widget)
        page_setup_main_layout.setContentsMargins(10, 0, 0, 0)
        page_setup_main_widget.setStyleSheet("margin: 5px; padding: 0")

        page_setup_layout_Group_Layout.addLayout(page_setup_header)
        page_setup_layout_Group_Layout.addWidget(page_setup_main_widget)
        page_setup_layout_Group_Layout.setContentsMargins(5, 10, 10, 0)
        page_setup_layout_Group.setStyleSheet("margin: 5px; padding: 0px;")

        """End Page Setup Group"""
        
        auto_post_layout_right.addLayout(auto_post_layout_Header)
        auto_post_layout_right.addWidget(page_setup_layout_Group)

        auto_post_layout_right_widget.setLayout(auto_post_layout_right)
        auto_post_layout_right_widget.setStyleSheet("margin: 5px")
        
        auto_post_layout.addWidget(auto_post_layout_left_widget,3)
        auto_post_layout.addWidget(auto_post_layout_right_widget,7)
        
        auto_post_widget.setLayout(auto_post_layout)
        auto_post_widget.setStyleSheet("margin: 0px;")

        return auto_post_widget
    
    
    def Select_LDPlayer(self, id: int, checked: bool):
        count = 0
        for checkbox in self.LD_Button_list_qp.buttons():
            if checkbox.isChecked():
                count += 1
        if (checked):
            self.select_all_ld.setChecked(all(btn.isChecked() for btn in self.LD_Button_list_qp.buttons()))
        else:
            self.select_all_ld.setChecked(False)
        self.ld_count = count
        self.selected_LD.setText(f"{self.ld_count} Selected")
        self.specific_ld_ID = [self.LD_Button_list_qp.id(b) for b in self.LD_Button_list_qp.buttons() if b.isChecked()]

    
        if checked:
            if self.LDName_table.item(id-1, 1):
                item = self.LDName_table.item(id-1, 1)
                if item is not None:
                    item.setBackground(QColor("#07417a"))
        else:
            if self.LDName_table.item(id-1, 1):
                item = self.LDName_table.item(id-1, 1)
                if item is not None:
                    item.setBackground(QColor("#292c3b"))
                    
    def Select_list_devices(self,id: int, checked: bool) -> None:
        count = 0
        for checkbox in self.devices_list_qp.buttons():
            if checkbox.isChecked():
                count += 1
        if (checked):
            self.select_all_devices.setChecked(all(btn.isChecked() for btn in self.devices_list_qp.buttons()))
        else:
            self.select_all_devices.setChecked(False)
        self.device_count = count
        self.selected_Devices.setText(f"{self.device_count} Selected")
        self.specific_list_devices_ID = [self.devices_list_qp.id(b) for b in self.devices_list_qp.buttons() if b.isChecked()]
        
        if checked:
            if self.devices_table.item(id-1, 1):
                item = self.devices_table.item(id-1, 1)
                if item is not None:
                    item.setBackground(QColor("#07417a"))
        else:
            if self.devices_table.item(id-1, 1):
                item = self.devices_table.item(id-1, 1)
                if item is not None:
                    item.setBackground(QColor("#292c3b"))
    
    def selected_list_devices(self)-> QWidget:
        select_list_devices_widget = QWidget()
        select_list_devices_layout = QVBoxLayout(select_list_devices_widget)

        select_list_devices_layout_top = QHBoxLayout()
        select_list_devices_layout_bottom = QHBoxLayout()
        
        #top
        self.selected_Devices = QLabel("0 Selected")
        self.select_all_devices = QCheckBox("Select All")
        self.select_all_devices.stateChanged.connect(lambda: self.select_all_devices_changed(self.select_all_devices.isChecked()))
        
        select_list_devices_layout_top.addWidget(self.selected_Devices)
        select_list_devices_layout_top.addStretch(1)
        select_list_devices_layout_top.addWidget(self.select_all_devices)
        try:
            MAX = len(self.Grim.check_ld_in_list())
        except: 
            print(f"cannot get a max value for spinBox Raise")
        #bottom
        
        
        self.spinBox_select_all_list_devices_start = QSpinBox(self)
        self.spinBox_select_all_list_devices_start.setRange(1, MAX)
        self.spinBox_select_all_list_devices_start.setValue(1)
        
        toLabel = QLabel("To")
        toLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinBox_select_all_list_devices_end = QSpinBox(self)
        self.spinBox_select_all_list_devices_end.setRange(1, MAX)
        self.spinBox_select_all_list_devices_end.setValue(MAX)
        self.spinBox_select_all_list_devices_end.valueChanged.connect(lambda v: self.selectRange("end",v))
        self.spinBox_select_all_list_devices_start.valueChanged.connect(lambda v: self.selectRange("start",v))

        confirm = QPushButton("☑︎")
        confirm.clicked.connect(lambda: self.confirmSelectRange_list_devices(self.spinBox_select_all_list_devices_start.value(), self.spinBox_select_all_list_devices_end.value()))
        confirm.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        select_list_devices_layout_bottom.addWidget(self.spinBox_select_all_list_devices_start)
        select_list_devices_layout_bottom.addWidget(toLabel)
        select_list_devices_layout_bottom.addWidget(self.spinBox_select_all_list_devices_end)
        select_list_devices_layout_bottom.addWidget(confirm, 0)
        


        select_list_devices_layout.addLayout(select_list_devices_layout_top)
        select_list_devices_layout.addLayout(select_list_devices_layout_bottom)
        
        select_list_devices_layout.setContentsMargins(5, 0, 0, 0)
        return select_list_devices_widget
    
    def confirmSelectRange_list_devices(self,start: int, end: int) -> None:
        self.select_all_devices_ld = all(btn.isChecked() for btn in self.devices_list_qp.buttons())
        count = 0 
        for i in range(start, end+1):
            btn = self.devices_list_qp.button(i)
            if btn:
                btn.setChecked(True)
        for checkbox in self.devices_list_qp.buttons():
            count += 1 if checkbox.isChecked() else 0
        self.list_devices_count = count
        self.select_all_devices.setChecked(self.select_all_devices_ld)
        self.selected_Devices.setText(f"{self.list_devices_count} Selected")
        self.specific_list_devices_ID = [self.devices_list_qp.id(b) for b in self.devices_list_qp.buttons() if b.isChecked()]

    def select_all_devices_changed(self, checked: bool) -> None:
        self.select_all_devices_ld: bool = all(btn.isChecked() for btn in self.devices_list_qp.buttons())
        if checked:
            self.confirmSelectRange_list_devices(1, len(self.Grim.check_ld_in_list()))
            self.select_all_devices.setChecked(True)
        else:
            self.select_all_devices.setChecked(False)
    
    def selected_LD_name(self) -> QWidget:
        select_ld_name_widget = QWidget()
        select_ld_name_widget_layout = QVBoxLayout()
        
        select_ld_name_layout_top = QHBoxLayout()
        select_ld_name_layout_bottom = QHBoxLayout()
        
        #top
        self.selected_LD = QLabel("0 Selected")
        self.select_all_ld = QCheckBox("Select All")
        self.select_all_ld.stateChanged.connect(lambda: self.select_all_ld_changed(self.select_all_ld.isChecked()))

        select_ld_name_layout_top.addWidget(self.selected_LD)
        select_ld_name_layout_top.addStretch(1)
        select_ld_name_layout_top.addWidget(self.select_all_ld)
        
        try:
            MAX = len(self.Grim.check_ld_in_list())
        except:
            print(f"cannot get a max value for spinBox Raise")
            
        #bottom
        self.spinBox_select_all_ld_ld_name_start = QSpinBox(self)
        self.spinBox_select_all_ld_ld_name_start.setRange(1, MAX)
        self.spinBox_select_all_ld_ld_name_start.setValue(1)
        

        toLabel = QLabel("To")
        toLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinBox_select_all_ld_ld_name_end = QSpinBox(self)
        self.spinBox_select_all_ld_ld_name_end.setRange(1, MAX)
        self.spinBox_select_all_ld_ld_name_end.setValue(MAX)
        self.spinBox_select_all_ld_ld_name_end.valueChanged.connect(lambda v: self.selectRange("end",v))
        self.spinBox_select_all_ld_ld_name_start.valueChanged.connect(lambda v: self.selectRange("start",v))
        
        confirm = QPushButton("☑︎")
        confirm.clicked.connect(lambda: self.confirmSelectedRange(self.spinBox_select_all_ld_ld_name_start.value(), self.spinBox_select_all_ld_ld_name_end.value()))
        confirm.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        select_ld_name_layout_bottom.addWidget(self.spinBox_select_all_ld_ld_name_start)
        select_ld_name_layout_bottom.addWidget(toLabel)
        select_ld_name_layout_bottom.addWidget(self.spinBox_select_all_ld_ld_name_end)
        select_ld_name_layout_bottom.addWidget(confirm, 0)
        
        select_ld_name_widget_layout.addLayout(select_ld_name_layout_top)
        select_ld_name_widget_layout.addLayout(select_ld_name_layout_bottom)
        select_ld_name_widget_layout.setContentsMargins(5, 0, 0, 0)  
        select_ld_name_widget.setLayout(select_ld_name_widget_layout)
        
        return select_ld_name_widget
    
    def confirmSelectedRange(self, start: int, end: int) -> None:
        
        self.select_all_ld_ld_name = all(btn.isChecked() for btn in self.LD_Button_list_qp.buttons())
        count = 0
        for i in range(start, end + 1):
            btn = self.LD_Button_list_qp.button(i)
            if btn:
                btn.setChecked(True)
        for checkbox in self.LD_Button_list_qp.buttons():
            count += 1 if checkbox.isChecked() else 0
        self.ld_count = count
        self.select_all_ld.setChecked(self.select_all_ld_ld_name)
        self.selected_LD.setText(f"{self.ld_count} Selected")
        self.specific_ld_ID = [self.LD_Button_list_qp.id(b) for b in self.LD_Button_list_qp.buttons() if b.isChecked()]

    def select_all_ld_changed(self, checked: bool) -> None:
        self.select_all_ld_ld_name: bool = all(btn.isChecked() for btn in self.LD_Button_list_qp.buttons())
        if checked:
            self.confirmSelectedRange(1, len(self.Grim.check_ld_in_list()))
            self.select_all_ld.setChecked(True)
        else:
            self.select_all_ld.setChecked(False)

        
    def selectRange(self, which: str, value: int) -> None:
        try:
            max_value = len(self.Grim.check_ld_in_list())
        except:
            print("Error occurred while getting max value")
        start = self.spinBox_select_all_ld_ld_name_start.value()
        end = self.spinBox_select_all_ld_ld_name_end.value()
        
        if self.spinBox_select_all_ld_ld_name_start.maximum() != max_value:
            self.spinBox_select_all_ld_ld_name_start.setMaximum(max_value)
        if self.spinBox_select_all_ld_ld_name_end.maximum() != max_value:
            self.spinBox_select_all_ld_ld_name_end.setMaximum(max_value)

        if which == "start":
            if value <= end:
                
                self.spinBox_select_all_ld_ld_name_start.setValue(value)
            else:
                self.spinBox_select_all_ld_ld_name_start.setValue(value - 1)
        elif which == "end":
            if value >= start:
                
                self.spinBox_select_all_ld_ld_name_end.setValue(value)
            else:
                self.spinBox_select_all_ld_ld_name_end.setValue(value + 1)
                
    def Left_view(self) -> QWidget:
        
        left_widget = QWidget()
        Left_Panel = QVBoxLayout()

        
        """"Header"""
        Head_left_panel = QHBoxLayout()
        Head_left_panel.addWidget(QLabel('<div style="font-size: 100px;">▶️</div>'))
        Head_left_panel.addWidget(QLabel('<div style="font-size: 100px;">⏹️</div>'))
        Head_left_panel.addWidget(self.time_label)  
        """End Header"""

        
        """"Table"""
        table_Box_layout = QGroupBox()
        table_layout = QVBoxLayout()
        table_Box_Bottom = QHBoxLayout()
        #Content in the func
        """End Table"""

        """"Bottom Box"""
        Menu = QPushButton("Menu")
        Menu.setIcon(QIcon("Logo/drop-down-menu.png"))
        Menu.setIconSize(QSize(25, 25))  
        table_Box_Bottom.addWidget(Menu)
        table_Box_Bottom.addStretch(1)
        
        
        Group = QPushButton("🗿Group")
        Group.clicked.connect(lambda: self.start_thread(webbrowser.open, "https://t.me/assemly"))
        table_Box_Bottom.addWidget(QPushButton("📩Email"))
        table_Box_Bottom.addWidget(QPushButton("⛓️‍💥API"))
        table_Box_Bottom.addWidget(Group)
        table_Box_Bottom.addWidget(QPushButton("📃Log"))
        table_Box_Bottom.addWidget(self.qrbutton)
        table_layout.addWidget(QLabel("Active Devices"))
        table_layout.addWidget(self.update_activity_table())
        table_layout.addLayout(table_Box_Bottom)
        table_Box_layout.setLayout(table_layout)
        """"End Bottom Box"""
        
        Left_Panel.addLayout(Head_left_panel)
        Left_Panel.addWidget(table_Box_layout)
        
        left_widget.setLayout(Left_Panel)
        left_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        return left_widget
    

    
    def open_qr(self, path: str ,width: int,height: int) -> None:
        """Open QR code in browser"""
        qr_path = path

        if(not os.path.exists(qr_path)):
            print("QR Image Not Found")
            
        qr = cv2.imread(qr_path)
        if(qr is None):
            return
        
        try:
            qr = cv2.resize(qr, (width, height))  
            
            cv2.imshow("QR Code", qr)
            cv2.waitKey(0)

        except Exception as e:
            print(f"Error opening QR code: {e}")

    def start_thread(self, func, *args, **kwargs) -> None:
        self.My_thread = Threader(func, *args, **kwargs)
        self.My_thread.start()
        


class Proxy(QProxyStyle):
    def subControlRect(self,control: QStyle.ComplexControl, opt: QStyleOptionSpinBox, subControl: QStyle.SubControl, widget: Optional[QSpinBox] = None,) -> QRect:
        rect = super().subControlRect(control, opt, subControl, widget)  # type: ignore
        if control == QStyle.ComplexControl.CC_SpinBox:
            total_w = widget.width() if widget is not None else rect.width()
            total_h = rect.height()
            if subControl == QStyle.SubControl.SC_SpinBoxUp:
                rect.setLeft(total_w - 30)
                rect.setRight(total_w)
                rect.setBottom(total_h - 13)

            elif subControl == QStyle.SubControl.SC_SpinBoxDown:
                rect.setTop(total_h - 13)
                rect.setLeft(total_w - 30)
                rect.setRight(total_w)

            elif subControl == QStyle.SubControl.SC_SpinBoxEditField:
                rect.setLeft(25)
                rect.setRight(total_w - 40)

        return rect

if __name__ == "__main__":
    
    if platform.system() != "Windows":
        sys.exit("Only Windows supported!")
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setStyle(Proxy())
    window = BobPrimeApp()  
    window.show()
    sys.exit(app.exec())