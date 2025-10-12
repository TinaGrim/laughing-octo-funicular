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
from server.server_routes import init
from LD_Player_gui.Active import Active
from LD_Player_gui.Devices import Devices
from LD_Player_gui.Manage import Manage
from LD_Player_gui.Auto_Post import Auto_Post
from PySide6.QtGui import QCloseEvent, QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from flask import Flask, jsonify , request, url_for, render_template, blueprints
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
signal.signal(signal.SIGINT, signal.SIG_DFL)
from configparser import ConfigParser

server = Flask(__name__, template_folder='server', static_folder='style')


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
    return render_template("index.html", links=links)

class BobPrimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        global GUI
        GUI = self
        self.Grim = option()
        self.setWindowTitle("Girm Prime App")
        self.setGeometry(100, 100, 1900, 800)
        self.logo = "Logo/logo_icon_big.png"
        self._load()
        self.headers = {
            "Content-Type": "application/json",
        }
        self.resume = True
        self.stop = False
        self.LDPlayers = []
        self.LDPlayer_indexs = []
        
        
        #setup widgets
        self.time_label = QLabel()
        self.timer = QTimer()
        self.activityTimer = QTimer()
        self.LDPlayer_time = QTimer()
        self.DevicesTimer = QTimer()
        self.LDNameTimer = QTimer()
        self.DeviceList = QTimer()
        self.scheduleClose = True
        self.checkBox = QCheckBox()
        self.specific_ld_ID = []
        self.specific_list_devices_ID = []
        self.activity_LD = {}
        self.play = QPushButton()
        self.pause = QPushButton()

        
        self.Devices = Devices(self)
        self.Manage = Manage(self)
        self.Active = Active(self)
        self.Auto_Post = Auto_Post(self)
        

        #widgets
        self.qrbutton = QPushButton("💡")
        self.qrbutton.clicked.connect(lambda: self.open_qr("Logo/qr.jpg", 500, 800))

        
        #timer
        self.starttime = time.time()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)
        
        self.LDPlayer_time.timeout.connect(self.New_LDPlayer_Detect)
        self.LDPlayer_time.start(3000)
        
        #table activity
        self.activityTimer.timeout.connect(self.update_activity_table)
        self.activityTimer.start(1000)
        
        #table LDName
        self.LDNameTimer.timeout.connect(self.Auto_Post.update_auto_post_table)
        self.LDNameTimer.start(60000)
        self.Auto_Post.LD_Button_list_qp.idToggled.connect(self.Auto_Post.Select_LDPlayer)
        
        #table devices
        self.DevicesTimer.timeout.connect(self.Devices.update_devices_table)
        self.DevicesTimer.start(30000)

        #table devices list
        self.DeviceList.timeout.connect(self.Manage.update_devices_list)
        self.DeviceList.start(30000)
        self.Manage.devices_list_qp.idToggled.connect(self.Manage.Select_list_devices)
        

        
        # trigger
        self.pause.clicked.connect(lambda: self.Stop_LDPlayer(True))
        self.play.clicked.connect(lambda: self.Stop_LDPlayer(False))
        
        # Auto Post

        
        #Init
        self.update_time()
        self.init()
    
    def _load(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        
        if os.path.exists(self.logo):
            icon = QIcon(self.logo)
            self.setWindowIcon(icon)
        else:
            print("Some logo not found")
            sys.exit(1)
        
        with open("style/style.qss") as f:
            self.setStyleSheet(f.read())
        self.remove_underline(self)
        
    def remove_underline(self, widget) -> None:
        for chile in widget.findChildren(QLineEdit):
            font = chile.font()
            font.setUnderline(False)
            chile.setFrame(False)
            chile.setFont(font)

    def Stop_LDPlayer(self, stop) -> None:
        if stop:
            for LDPlayer in self.LDPlayers:
                LDPlayer.stop()
        else:
            for LDPlayer in self.LDPlayers:
                LDPlayer.resume()
        self.resume = not stop
        print(self.resume)
        
    def LDPlayer_Start(self, IDs: list[int]) -> None:
        self.Auto_Post.select_all_ld.setChecked(False)
        self.Auto_Post.selected_LD.setText(f"{0} Selected")
        for btn in self.Auto_Post.LD_Button_list_qp.buttons():
            btn.setChecked(False)
        print("Starting LD Players: ", IDs)
        if not IDs:
            return
        for ID in IDs:
            if not any(ldplayer.ID == ID for ldplayer in self.LDPlayers):
                ldplayer = LDPlayer(self, ID)
                self.LDPlayers.append(ldplayer)
        print("LDPlayers: ", self.LDPlayers)
        

        threading.Thread(target=self.LDPlayer_Process,args=(IDs,)).start()


    def New_LDPlayer_Detect(self) -> None:
        try:
            ids = self.Grim.current_ld_ids()
            print(self.LDPlayer_indexs, ids)
            if self.LDPlayer_indexs == ids :
                return
            else:
                self.LDPlayer_indexs = ids
                for index, ID in enumerate(self.LDPlayer_indexs):
                    
                    self.Grim.Arrangment(ID, index)
                    time.sleep(1)
    
        except Exception as e:
            print(f"Error arranging LDPlayer windows: {e}")

    def LDPlayer_Process(self, IDs: list[int]) -> None:
        steps = [
            lambda ld: ld.open(),
            lambda ld: time.sleep(5),
            lambda ld: ld.check_command(),
            lambda ld: ld.remote()
        ]
        
        for step in steps:
            for ld in self.LDPlayers:
                if ld.ID in IDs:
                    step(ld)
                    if step == steps[0]:
                        time.sleep(5)
        
    def update_time(self) -> None:
        """Update the time label with current time using replace"""
        elapsed = int(time.time() - self.starttime)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_label.setText(f'<span >{hours:02}:{minutes:02}:{seconds:02}</span>')
        

        
    #======================================================================================================
    def update_activity_table(self)->QTableWidget:
        driver_list = self.Grim.current_ld_names()
        try:
            activity = requests.get("http://127.0.0.1:5000/LDActivity", headers=self.headers, timeout=5)
            if activity.status_code == 200:
                activity_jason = activity.json()
                activityData = activity_jason.get('LDActivity', {})
            else:
                print(f"Server returned status code: {activity.status_code}")
                activityData = {}
        except requests.exceptions.ConnectionError:
            activityData = {}
        except Exception as e:
            print(f"Error connecting to server: {e}")
            activityData = {}
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

    def update_exist_activity_table(self, driver_list: list[str], activityData: dict):

        if not driver_list:
            self.table.setRowCount(0)
            return
        for i, driverName in enumerate(driver_list):
            
            if driverName in activityData:
                status = activityData[driverName].get('status', 'No Action...')
            else:
                status = "No Action..."
            self.table.setRowCount(len(driver_list))
            self.table.setItem(i,0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i,1, QTableWidgetItem(driverName))
            self.table.setItem(i,2, QTableWidgetItem(str(int((int(driverName[-2:])-50)/2-1))))
            self.table.setItem(i,3, QTableWidgetItem(status))



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
        self.Tabs.addTab(self.Devices.Tab_Devices(), "Devices")
        self.Tabs.addTab(self.Active.Tab_Active(), "Active")
        self.Tabs.addTab(self.Auto_Post.Tab_auto_post(), "Auto Post")
        self.Tabs.addTab(self.Manage.Tab_manage(), "Manage")
        self.Tabs.setCornerWidget(cornerContainer) 
        """End Tabs"""
        
        """Inside the main layout"""
        main_layout.addWidget(self.Left_view(), 3) 
        main_layout.addWidget(self.Tabs, 7)
             
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

                
    def Left_view(self) -> QWidget:
        
        left_widget = QWidget()
        Left_Panel = QVBoxLayout()

        
        """"Header"""
        Head_left_panel = QHBoxLayout()
        self.play.setIcon(QIcon("Logo/play.png"))
        self.play.setIconSize(QSize(100, 100))
        self.play.setStyleSheet("background-color: none; border: none;")
        self.pause.setIcon(QIcon("Logo/pause.png"))
        self.pause.setIconSize(QSize(100, 100))
        self.pause.setStyleSheet("background-color: none; border: none;")
        font = QFont()
        font.setPointSize(40)
        self.time_label.setFont(font)
        Head_left_panel.addWidget(self.play)
        Head_left_panel.addWidget(self.pause)
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
            

    def closeEvent(self, event: QCloseEvent) -> None:
        self.save_settings()
        self.stop = True
        event.accept()
         
    def save_settings(self) -> None:
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        print("Settings saved")


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
                rect.setRight(total_w - 2)
                rect.setBottom(total_h - 14)

            elif subControl == QStyle.SubControl.SC_SpinBoxDown:
                rect.setTop(total_h - 14)
                rect.setLeft(total_w - 30)
                rect.setRight(total_w - 2)
                rect.setBottom(total_h - 2)

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
    
    init(server, window)
    Thread(target=lambda: server.run(port=5000),daemon=True).start()
    
    window.show()
    sys.exit(app.exec())