import os
from flask import Flask, jsonify
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenuBar,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton
from PySide6.QtGui import QColor, QFont, QPixmap,QIcon
from PySide6.QtCore import Qt, QTimer,QSize,QThread
import sys
import time
import webbrowser
from threading import Thread
import dotenv

import signal
import cv2

signal.signal(signal.SIGINT, signal.SIG_DFL)
dotenv.load_dotenv(dotenv_path=".git/.env")
from LD_Player import *
import threading


server = Flask(__name__)
Thread(target=lambda: server.run(port=5000),daemon=True).start()


@server.route("/schedule")
def scheduleFunc():
    return jsonify(scheduleClose=GUI.scheduleCheck())

@server.route("/LDcount")
def LDcount():
    count = GUI.LDcount
    List = [i for i in range(1, count+1)]
    return jsonify(LDcount=List)

class BobPrimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        global GUI
        GUI = self
        
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
        self.LDNameTimer = QTimer()
        self.scheduleClose = False
        
        #widgets
        self.Open_ld = QPushButton("➕")
        self.Open_ld.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.deleteButton = QPushButton("🗑️")
        self.deleteButton.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.createButton = QPushButton("✒️")
        self.createButton.setStyleSheet("margin: 0px 0px 10px 0px;")
        
        self.qrbutton = QPushButton("💡")
        
        self.closeAppium = QCheckBox("Auto Close Appium")
        
        #timer
        self.starttime = time.time()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)
        
        #table activity
        self.activityTimer.timeout.connect(self.update_activity_table)
        self.activityTimer.start(3000)
        
        #table LDName
        self.LDNameTimer.timeout.connect(self.update_LDName_table)
        self.LDNameTimer.start(3000)
        
        #trigger
        self.Open_ld.clicked.connect(lambda: self.startLD(4))
        self.qrbutton.clicked.connect(lambda: self.open_qr("Logo/qr.jpg", 500, 800))
        self.closeAppium.stateChanged.connect(lambda: self.scheduleCheck())
        #Init
        
        self.update_time()
        self.init()

    
    def scheduleCheck(self) -> bool:
        self.scheduleClose = self.closeAppium.isChecked()
        return self.scheduleClose
    
    def startLD(self, number: int)-> int:
        """Start LD Player"""
        self.start_thread(LDPlayer().run, number)
        self.LDcount = number
        return self.LDcount

    def check_activity(self):
        try:
            self.drivers = Option().opened_drivers()
            return self.drivers if self.drivers is not None else []
        except Exception as e:
            print(f"Error checking activity: {e}")
            return []


        

    def update_activity_table(self)->QTableWidget:
        driver_list = self.check_activity()
        
        
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
        self.update_exist_activity_table(driver_list)
        return self.table

    def update_exist_activity_table(self, driver_list: list[str]):

        if not self.table:
            return
        if not driver_list:
            self.table.setRowCount(0)
            return
        for i, driver_name in enumerate(driver_list):
            self.table.setRowCount(len(driver_list))
            self.table.setItem(i,0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i,1, QTableWidgetItem(driver_name))
            self.table.setItem(i,2, QTableWidgetItem(str(i+1)))
            self.table.setItem(i,3, QTableWidgetItem("Activity"))
        
    
    def update_time(self) -> None:
        """Update the time label with current time using replace"""
        elapsed = int(time.time() - self.starttime)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_label.setText(f'<div style="font-size: 50px;">{hours:02}:{minutes:02}:{seconds:02}</div>')
        
    def update_LDName_table(self) -> QTableWidget:
        driver_list = self.check_activity()
        if not hasattr(self, 'LDName_table') or self.LDName_table is None:
            self.LDName_table = QTableWidget(0, 2)
            self.LDName_table.setHorizontalHeaderLabels(["No.", "LD Name"])
            self.LDName_table.verticalHeader().setVisible(False)
            self.LDName_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.LDName_table.setAutoFillBackground(False)
            self.LDName_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.LDName_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.LDName_table.resizeColumnsToContents()
            self.LDName_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  
            self.LDName_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
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
            self.LDName_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.LDName_table.setItem(i, 1, QTableWidgetItem(driver_name))

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
        self.Tabs.addTab(QLabel("Hello"), "Devices")
        self.Tabs.addTab(QLabel("Hello"), "Active")
        self.Tabs.addTab(self.Tab_auto_post(), "Auto Post")
        self.Tabs.addTab(QLabel("Hello"), "Manage")
        self.Tabs.setCornerWidget(cornerContainer, Qt.TopRightCorner) # type: ignore
        """End Tabs"""
        
        """Inside the main layout"""
        main_layout.addWidget(self.Left_view(), 3) 
        main_layout.addWidget(self.Tabs, 7)
             
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        
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
        
        """"Table"""
        LD_Table = QTableWidget(2,2)
        LD_Table.setHorizontalHeaderLabels(["No.", "LD Name"])
        LD_Table.verticalHeader().setVisible(False)
        LD_Table.setAutoFillBackground(True)
        LD_Table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        LD_Table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        LD_Table.resizeColumnsToContents()

        LD_Table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) 
        LD_Table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) 
        LD_Table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        LD_Table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        LD_Table.verticalHeader().setDefaultSectionSize(35)
        LD_Table.verticalHeader().setMinimumSectionSize(30)
        LD_Table.setCellWidget(0, 0, QCheckBox("1"))
        LD_Table.setCellWidget(1, 0, QCheckBox("2"))
        LD_Table.setItem(0, 1, QTableWidgetItem("LD 1"))
        LD_Table.setItem(1, 1, QTableWidgetItem("LD 2"))
        """End Table"""

        
        auto_post_layout_left_widget = QWidget()
        auto_post_layout_left = QVBoxLayout()
        
        auto_post_layout_left.addWidget(Group_Box_Schedule)
        auto_post_layout_left.addWidget(self.update_LDName_table())
        
        auto_post_layout_left_widget.setLayout(auto_post_layout_left)
        
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
        
if __name__ == "__main__":
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    LD = LDPlayer()
    app = QApplication(sys.argv)
    window = BobPrimeApp()  
    window.show()
    app.exec()