import os
import sys
import cv2
import time
import logging
import requests
import dotenv
import signal
import platform
import threading
import webbrowser
from LD_Player import *
from typing import Optional
from threading import Thread
from flask import Flask, jsonify , request
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox

signal.signal(signal.SIGINT, signal.SIG_DFL)
dotenv.load_dotenv(dotenv_path=".git/.env")



server = Flask(__name__)
Thread(target=lambda: server.run(port=5000),daemon=True).start()





class NoLog(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/LDActivity" not in record.getMessage()
logging.getLogger('werkzeug').addFilter(NoLog())

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
        print("RemainingID after POST: ", RemainingID)
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
        self.Grim = Option()
        self.setWindowTitle("Girm Prime App")
        self.setGeometry(100, 100, 1500, 800)
        self.setStyleSheet("""
            QMainWindow, QWidget{
            background-color: #292c3b;
            color: white;
            }
            QCheckBox {
                color: white;
            }
            QCheckBox::indicator {
            width: 18px;
            height: 18px;
            }
            QCheckBox::indicator:checked {
            image: url(Logo/check1.png);
            }

            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #13599d;
                margin: 0px;
                padding: 5px;

            }
            QPushButton::pressed {
                background-color: #176ec3;
                margin: 0px;
                padding: 5px;
            }
            QTabBar::tab {
                margin: 0px;
                padding: 5px 30px;
                background-color: #292c3b
            }
            QTabBar::tab:selected {
                background-color: #176ec3;
                border-radius: 5px;
            }
            QTabWidget::pane {
                top: 0px;
                margin: 0px;
                padding: 0px;
                border: 2px solid #808080;
                border-radius: 5px;
            }
            QTabWidget > QWidget {
                margin: 0px;
                padding: 0px;
            }
            QGroupBox {
                border: 2px solid gray;
                border-radius: 5px;
                margin: 0px;
            }
            QGroupBox::title {
                subcontrol-origin: padding;
                subcontrol-position: top left; 
                background-color:#292c3b;
                padding: 0px 0px;
                margin: -13px 0px 20px 10px;
                border-radius: 10px;
                font-size: 12px;
            }
            QHeaderView {
                background-color: transparent;

                border-radius: 5px;
            }
        """)
        
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
        self.LD_Button_list_qp = QButtonGroup(self)
        self.LD_Button_list_qp.setExclusive(False)
        self.specificId = []
        self.activity_LD = {}


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
        self.LDNameTimer.timeout.connect(self.update_LDName_table)
        self.LDNameTimer.start(60000)
        self.LD_Button_list_qp.idToggled.connect(self.Select_LDPlayer)
        
        #table devices
        self.DevicesTimer.timeout.connect(self.update_devices_table)
        self.DevicesTimer.start(4000)
        
        #table devices list
        self.DeviceList.timeout.connect(self.update_devices_list)
        self.DeviceList.start(4000)
        
        #trigger
        self.Open_ld.clicked.connect(lambda: self.openLD())
        self.qrbutton.clicked.connect(lambda: self.open_qr("Logo/qr.jpg", 500, 800))
        self.closeAppium.stateChanged.connect(lambda: self.scheduleCheck())


        #Init
        self.update_time()
        self.init()

    def Select_LDPlayer(self, id: int, checked: bool):
        count = 0
        for checkbox in self.LD_Button_list_qp.buttons():
            if checkbox.isChecked():
                count += 1
        if (checked):
            self.select_all.setChecked(all(btn.isChecked() for btn in self.LD_Button_list_qp.buttons()))
        else:
            self.select_all.setChecked(False)
        self.count = count
        self.selected.setText(f"{self.count} Selected")
        self.specificId = [self.LD_Button_list_qp.id(b) for b in self.LD_Button_list_qp.buttons() if b.isChecked()]

    
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
                        
    def scheduleCheck(self) -> bool:
        self.scheduleClose = self.closeAppium.isChecked()
        return self.scheduleClose

    def openLD(self):
        if not self.specificId:
            return
        self.select_all.setChecked(False)
        self.selected.setText(f"{0} Selected")
        self.start_thread(LDPlayer().run, self.specificId)
        
    def check_activity(self):
        try:
            self.drivers = self.Grim.opened_drivers()
            return self.drivers if self.drivers is not None else []
        except Exception as e:
            print(f"Error checking activity: {e}")
            return []

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

        if not self.table and not driver_list:
            self.table.setRowCount(0)
            return
        for i, driverName in enumerate(driver_list):
            status = "No Action..."
            
            if driverName in activityData:
                status = activityData[driverName]['status']
            
            self.table.setRowCount(len(driver_list))
            self.table.setItem(i,0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i,1, QTableWidgetItem(driverName))
            self.table.setItem(i,2, QTableWidgetItem(str(int((int(driverName[-2:])-50)/2-1))))
            self.table.setItem(i,3, QTableWidgetItem(status))


    def update_time(self) -> None:
        """Update the time label with current time using replace"""
        elapsed = int(time.time() - self.starttime)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_label.setText(f'<div style="font-size: 50px;">{hours:02}:{minutes:02}:{seconds:02}</div>')
        
    def update_LDName_table(self) -> QTableWidget:
        driver_list = self.Grim.check_ld_in_list()
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
        if getattr(self, "select_all", None):
            self.select_all.setChecked(False)
            self.selected.setText(f"{0} Selected")
        self.update_exist_LDName_table(driver_list)
        return self.LDName_table
    
    def update_exist_LDName_table(self, driver_list: list[str]) -> None:
        if not self.LDName_table:
            return
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
        self.Tabs.addTab(QLabel("Hello"), "Active")
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
        labeltop1 = QLabel("Locate Device:")
        labeltop2 = QLabel("Locate Device:")
        labeltop3 = QLabel("Locate Device:")
        
        devices_locate_widget_layout_top.addWidget(labeltop1)
        devices_locate_widget_layout_top.addWidget(labeltop2)
        devices_locate_widget_layout_top.addWidget(labeltop3)
        
        devices_locate_widget_layout_bottom = QHBoxLayout()
        labelbottom1 = QLabel("Locate Device:")
        labelbottom2 = QLabel("Locate Device:")
        labelbottom3 = QLabel("Locate Device:")
        
        devices_locate_widget_layout_bottom.addWidget(labelbottom1)
        devices_locate_widget_layout_bottom.addWidget(labelbottom2)
        devices_locate_widget_layout_bottom.addWidget(labelbottom3)
        
        devices_locate_widget_layout.addLayout(devices_locate_widget_layout_top)
        devices_locate_widget_layout.addLayout(devices_locate_widget_layout_bottom)

        devices_upload = QPushButton("Upload")


        devices_browser_widget_layout.addWidget(devices_locate_widget, 8)
        devices_browser_widget_layout.addWidget(devices_upload, 2)

        #Bottom
        devices_information_widget = QWidget()
        devices_information_widget_layout = QVBoxLayout(devices_information_widget)
        
        devices_information_widget_layout_top_widget = QWidget()
        devices_information_widget_layout_top = QHBoxLayout(devices_information_widget_layout_top_widget)
        
        label1 = QLabel("Device Name:")
        label2 = QLabel("Device Name:")
        label3 = QLabel("Device Name:")
        label4 = QLabel("Device Name:")

        devices_information_widget_layout_top.addWidget(label1)
        devices_information_widget_layout_top.addWidget(label2)
        devices_information_widget_layout_top.addWidget(label3)
        devices_information_widget_layout_top.addWidget(label4)

        devices_information_widget_layout_bottom_widget = QWidget()
        devices_information_widget_layout_bottom = QHBoxLayout(devices_information_widget_layout_bottom_widget)
        
        devices_setting_box = QGroupBox("LDPlayer Setting")
        devices_setting_box_layout = QVBoxLayout(devices_setting_box)
        devices_setting_box_layout_IP = QHBoxLayout()
        labelip = QLabel("IP Address:")
        devices_setting_box_layout_IP.addWidget(labelip)
        devices_setting_box_layout_auto_config = QHBoxLayout()
        label_auto_config = QLabel("Auto Config:")
        devices_setting_box_layout_auto_config.addWidget(label_auto_config)
        devices_setting_box_layout_arrange = QHBoxLayout()
        label_arrange = QLabel("Arrange:")
        devices_setting_box_layout_arrange.addWidget(label_arrange)
        devices_setting_box_layout_screen = QHBoxLayout()
        label_screen = QLabel("Screen:")
        devices_setting_box_layout_screen.addWidget(label_screen)
        devices_setting_box_layout_startup = QHBoxLayout()
        label_startup = QLabel("Startup:")
        devices_setting_box_layout_startup.addWidget(label_startup)
        devices_setting_box_layout_autostop = QHBoxLayout()
        label_autostop = QLabel("Auto Stop:")
        devices_setting_box_layout_autostop.addWidget(label_autostop)
        devices_setting_box_layout_clearcache = QHBoxLayout()
        label_clearcache = QLabel("Clear Cache:")
        devices_setting_box_layout_clearcache.addWidget(label_clearcache)
        devices_setting_box_layout_iffbexceed = QHBoxLayout()
        label_iffbexceed = QLabel("If FB Exceed:")
        devices_setting_box_layout_iffbexceed.addWidget(label_iffbexceed)
        devices_setting_box_layout_ifldexceed = QHBoxLayout()
        label_ifldexceed = QLabel("If LD Exceed:")
        devices_setting_box_layout_ifldexceed.addWidget(label_ifldexceed)
        devices_setting_box_layout_closeld = QHBoxLayout()
        label_closeld = QLabel("Close LD:")
        devices_setting_box_layout_closeld.addWidget(label_closeld)

        devices_setting_box_layout.addLayout(devices_setting_box_layout_IP)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_auto_config)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_arrange)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_screen)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_startup)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_autostop)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_clearcache)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_iffbexceed)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_ifldexceed)
        devices_setting_box_layout.addLayout(devices_setting_box_layout_closeld)

        devices_information_widget_layout_bottom.addWidget(self.update_devices_table(), 4)
        devices_information_widget_layout_bottom.addWidget(devices_setting_box, 6)
        
        devices_information_widget_layout.addWidget(devices_information_widget_layout_top_widget, 1)
        devices_information_widget_layout.addWidget(devices_information_widget_layout_bottom_widget, 9)

        devices_widget_layout.addWidget(devices_browser_widget, 1)
        devices_widget_layout.addWidget(devices_information_widget, 9)
        return devices_widget
    
    def update_devices_table(self) -> QTableWidget:
        if not hasattr(self, "devices_table") or self.devices_table is None:
            self.devices_table = QTableWidget(0, 5)
            self.devices_table.setHorizontalHeaderLabels(["ID", "LD Name", "Status", "Model", "M.facturer"])
            self.devices_table.verticalHeader().setVisible(False)
            self.devices_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.devices_table.setAutoFillBackground(False)
            self.devices_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.devices_table.resizeColumnsToContents()
            self.devices_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.devices_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) 
            self.devices_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) 
            self.devices_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) 
            self.devices_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch) 
    
            self.update_exist_devices_table()
        return self.devices_table
    
    def update_exist_devices_table(self) -> None:
        if not self.devices_table:
            return
        for i in range(0,15):
            self.devices_table.setRowCount(15)
            self.devices_table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.devices_table.setItem(i, 1, QTableWidgetItem(f"LD Name"))
            self.devices_table.setItem(i, 2, QTableWidgetItem("Mac Address"))
            self.devices_table.setItem(i, 3, QTableWidgetItem("Model"))
            self.devices_table.setItem(i, 4, QTableWidgetItem("M.facturer"))
    def Tab_manage(self) -> QWidget:
        ld_manage_widget = QWidget()
        ld_manage_layout = QHBoxLayout(ld_manage_widget)
        
        #left
        ld_manage_list = QWidget()
        manage_list_layout = QVBoxLayout(ld_manage_list)
        
        manage_list_bottom_widget = QWidget()
        manage_list_bottom = QVBoxLayout(manage_list_bottom_widget)
        
        manage_list_bottom_top = QHBoxLayout()
        label1 = QLabel("LD Name:")
        label11 = QLabel("select")
        
        manage_list_bottom_top.addWidget(label1)
        manage_list_bottom_top.addWidget(label11)
        
        manage_list_bottom_bottom = QHBoxLayout()
        label2 = QLabel("LD ID:")
        label22 = QLabel("select")
        manage_list_bottom_bottom.addWidget(label2)
        manage_list_bottom_bottom.addWidget(label22)

        manage_list_bottom.addLayout(manage_list_bottom_top)
        manage_list_bottom.addLayout(manage_list_bottom_bottom)
        
        manage_list_layout.addWidget(self.update_devices_list(),9)
        manage_list_layout.addWidget(manage_list_bottom_widget, 1)

        #right
        ld_manage_manager = QWidget()
        ld_manage_manager_layout = QVBoxLayout(ld_manage_manager)
        ld_manage_manager_layout.setContentsMargins(0, 0, 0, 0)

        ld_manage_group_boxtop = QGroupBox("Enable LDPlayer Manager")
        ld_manage_manager_layout_top = QVBoxLayout(ld_manage_group_boxtop)
        
        number_active = QHBoxLayout()
        number = QLabel("Number of Active LD:")
        number_active.addWidget(number)
        cloneld = QHBoxLayout()
        clone = QLabel("Clone LD:")
        cloneld.addWidget(clone)
        backup = QHBoxLayout()
        backup_label = QLabel("Backup LD:")
        backup.addWidget(backup_label)
        restore = QHBoxLayout()
        restore_label = QLabel("Restore LD:")
        restore.addWidget(restore_label)
        remove = QHBoxLayout()
        remove_label = QLabel("Remove LD:")
        remove.addWidget(remove_label)
        shutdown = QHBoxLayout()
        shutdown_label = QLabel("Shutdown LD:")
        shutdown.addWidget(shutdown_label)
        
        ld_manage_manager_layout_top.addLayout(number_active)
        ld_manage_manager_layout_top.addLayout(cloneld)
        ld_manage_manager_layout_top.addLayout(backup)
        ld_manage_manager_layout_top.addLayout(restore)
        ld_manage_manager_layout_top.addLayout(remove)
        ld_manage_manager_layout_top.addLayout(shutdown)

        ld_manage_group_boxbottom = QGroupBox("Enable LDPlayer Manager")
        ld_manage_manager_layout_bottom = QVBoxLayout(ld_manage_group_boxbottom)
        autoput = QHBoxLayout()
        autoput_label = QLabel("Auto Put LD:")
        autoput.addWidget(autoput_label)
        FBlocal = QHBoxLayout()
        FBlocal_label = QLabel("FB Local LD:")
        FBlocal.addWidget(FBlocal_label)
        createpage = QHBoxLayout()
        createpage_label = QLabel("Create Page LD:")
        createpage.addWidget(createpage_label)
        shutdownbottom = QHBoxLayout()
        shutdownbottom_label = QLabel("Shutdown Bottom LD:")
        shutdownbottom.addWidget(shutdownbottom_label)

        ld_manage_manager_layout_bottom.addLayout(autoput)
        ld_manage_manager_layout_bottom.addLayout(FBlocal)
        ld_manage_manager_layout_bottom.addLayout(createpage)
        ld_manage_manager_layout_bottom.addLayout(shutdownbottom)

        ld_manage_manager_layout.addWidget(ld_manage_group_boxtop)
        ld_manage_manager_layout.addWidget(ld_manage_group_boxbottom)
        
        ld_manage_layout.addWidget(ld_manage_list, 3)
        ld_manage_layout.addWidget(ld_manage_manager, 7)

        return ld_manage_widget
    
    def update_devices_list(self) -> QWidget:
        
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
            
        self.update_exist_devices_list()
        return self.devices_list
    
    def update_exist_devices_list(self) -> None:
        if not self.devices_list:
            return
        for i in range(0, 15):
            self.devices_list.setRowCount(15)
            btn = QCheckBox(str(i+1))
            self.devices_list.setCellWidget(i, 0, btn)
            self.devices_list.setItem(i, 1, QTableWidgetItem(f"LD Name {i+1}"))

    def Tab_auto_post(self) -> QWidget:

        auto_post_widget = QWidget()
        auto_post_layout = QHBoxLayout()
        auto_post_layout.setContentsMargins(0, 0, 0, 0)  
        auto_post_layout.setSpacing(5)  
        
        # On left side
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
        auto_post_layout_left.addWidget(self.update_LDName_table())
        auto_post_layout_left.addWidget(self.selected_LD_name())
        auto_post_layout_left.setContentsMargins(5, 20, 0, 0)
        auto_post_layout_left_widget.setLayout(auto_post_layout_left)
        auto_post_layout_left_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        # On right side
        auto_post_layout_right_widget = QWidget()
        auto_post_layout_right = QVBoxLayout()
        
        """"Header"""
        page_setup_layout_Header = QHBoxLayout()

        page_setup_layout_Header.addWidget(self.Open_ld)
        page_setup_layout_Header.addWidget(self.deleteButton)
        page_setup_layout_Header.addWidget(self.createButton)
  
        """End Header"""
        
        """Page Setup Group"""
        
        page_setup_layout_Group = QGroupBox("Page Setup")
        page_setup_layout_Group_Layout = QVBoxLayout()
        
        page_setup_layout_Group_Layout.addWidget(QLabel("Page Name:"))
    
        page_setup_layout_Group.setLayout(page_setup_layout_Group_Layout)
        """End Page Setup Group"""
        
        auto_post_layout_right.addLayout(page_setup_layout_Header)
        auto_post_layout_right.addWidget(page_setup_layout_Group)

        auto_post_layout_right_widget.setLayout(auto_post_layout_right)
        auto_post_layout_right_widget.setStyleSheet("margin: 5px")
        
        auto_post_layout.addWidget(auto_post_layout_left_widget,3)
        auto_post_layout.addWidget(auto_post_layout_right_widget,7)
        
        auto_post_widget.setLayout(auto_post_layout)
        auto_post_widget.setStyleSheet("margin: 0px;")

        return auto_post_widget
    
    def selected_LD_name(self) -> QWidget:
        select_ld_name_widget = QWidget()
        select_ld_name_widget_layout = QVBoxLayout()
        
        select_ld_name_layout_top = QHBoxLayout()
        select_ld_name_layout_bottom = QHBoxLayout()
        
        #top
        self.selected = QLabel("0 Selected")
        self.select_all = QCheckBox("Select All")
        self.select_all.stateChanged.connect(lambda: self.select_all_changed(self.select_all.isChecked()))

        select_ld_name_layout_top.addWidget(self.selected)
        select_ld_name_layout_top.addStretch(1)
        select_ld_name_layout_top.addWidget(self.select_all)
        
        try:
            MAX = len(self.Grim.check_ld_in_list())
        except:
            print(f"cannot get a max value for spinBox Raise")
            
        #bottom
        self.spinBox_selectAll_start = QSpinBox(self)
        

        self.spinBox_selectAll_start.setRange(1, MAX)
        self.spinBox_selectAll_start.setValue(1)
        

        toLabel = QLabel("To")
        toLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinBox_selectAll_end = QSpinBox(self)

        self.spinBox_selectAll_end.setRange(1, MAX)
        self.spinBox_selectAll_end.setValue(MAX)
        self.spinBox_selectAll_end.valueChanged.connect(lambda v: self.selectRange("end",v))
        self.spinBox_selectAll_start.valueChanged.connect(lambda v: self.selectRange("start",v))
        
        confirm = QPushButton("☑︎")
        confirm.clicked.connect(lambda: self.confirmSelectedRange(self.spinBox_selectAll_start.value(), self.spinBox_selectAll_end.value()))
        confirm.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        select_ld_name_layout_bottom.addWidget(self.spinBox_selectAll_start)
        select_ld_name_layout_bottom.addWidget(toLabel)
        select_ld_name_layout_bottom.addWidget(self.spinBox_selectAll_end)
        select_ld_name_layout_bottom.addWidget(confirm, 0)
        
        select_ld_name_widget_layout.addLayout(select_ld_name_layout_top)
        select_ld_name_widget_layout.addLayout(select_ld_name_layout_bottom)
        select_ld_name_widget_layout.setContentsMargins(5, 0, 0, 0)  
        select_ld_name_widget.setLayout(select_ld_name_widget_layout)
        
        return select_ld_name_widget
    def confirmSelectedRange(self, start: int, end: int) -> None:
        self.selectAll = all(btn.isChecked() for btn in self.LD_Button_list_qp.buttons())
        count = 0
        for i in range(start, end + 1):
            btn = self.LD_Button_list_qp.button(i)
            if btn:
                btn.setChecked(True)
        for checkbox in self.LD_Button_list_qp.buttons():
            count += 1 if checkbox.isChecked() else 0
        self.count = count
        self.select_all.setChecked(self.selectAll)
        self.selected.setText(f"{self.count} Selected")
        self.specificId = [self.LD_Button_list_qp.id(b) for b in self.LD_Button_list_qp.buttons() if b.isChecked()]

    def select_all_changed(self, checked: bool) -> None:
        self.selectAll: bool = all(btn.isChecked() for btn in self.LD_Button_list_qp.buttons())
        if checked:
            self.confirmSelectedRange(1, len(self.Grim.check_ld_in_list()))
            self.select_all.setChecked(True)
        else:
            self.select_all.setChecked(False)

        
    def selectRange(self, which: str, value: int) -> None:
        try:
            max_value = len(self.Grim.check_ld_in_list())
        except:
            print("Error occurred while getting max value")
        start = self.spinBox_selectAll_start.value()
        end = self.spinBox_selectAll_end.value()
        
        if self.spinBox_selectAll_start.maximum() != max_value:
            self.spinBox_selectAll_start.setMaximum(max_value)
        if self.spinBox_selectAll_end.maximum() != max_value:
            self.spinBox_selectAll_end.setMaximum(max_value)

        if which == "start":
            if value <= end:
                
                self.spinBox_selectAll_start.setValue(value)
            else:
                self.spinBox_selectAll_start.setValue(value - 1)
        elif which == "end":
            if value >= start:
                
                self.spinBox_selectAll_end.setValue(value)
            else:
                self.spinBox_selectAll_end.setValue(value + 1)
                
    
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
    def subControlRect(
        self,
        control: QStyle.ComplexControl,
        opt: QStyleOptionSpinBox,
        subControl: QStyle.SubControl,
        widget: Optional[QSpinBox] = None,
    ) -> QRect:
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
                rect.setLeft(32)
                rect.setRight(total_w - 20)

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