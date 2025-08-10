import os

from flask import Flask, jsonify
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenuBar,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionComplex,QStyleOptionSpinBox,QAbstractSpinBox
from PySide6.QtGui import QColor, QFont, QPixmap,QIcon
from PySide6.QtCore import Qt, QTimer,QSize,QThread, QRect
import sys
import time
import webbrowser
from threading import Thread
import dotenv
from typing import Optional
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
    # Be robust if LDcount hasn't been set yet
    count = getattr(GUI, "LDcount", 0)
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
        self.LDNameTimer = QTimer()
        self.scheduleClose = False
        self.checkBox = QCheckBox()
        self.checkBoxlist = []
        self.ld_list_name_gp = QButtonGroup(self)
        self.ld_list_name_gp.setExclusive(False)  
        
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
        self.LDNameTimer.start(60000)
        self.ld_list_name_gp.idToggled.connect(self.Select_LDPlayer)
        
        #trigger
        self.Open_ld.clicked.connect(lambda: self.startLD(1))
        self.qrbutton.clicked.connect(lambda: self.open_qr("Logo/qr.jpg", 500, 800))
        self.closeAppium.stateChanged.connect(lambda: self.scheduleCheck())
        self.checkBox.stateChanged.connect(self.Select_LDPlayer)

        #Init
        self.update_time()
        self.init()

    def Select_LDPlayer(self, id: int, checked: bool):
        print(f"Selected LDPlayer {id}: {checked}")


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
        driver_list = Option().check_ld_in_list()
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
            self.ld_list_name_gp.addButton(self.checkBox, i + 1)
            self.LDName_table.setCellWidget(i, 0, self.checkBox)
            self.LDName_table.setItem(i, 1, QTableWidgetItem(driver_name))
            self.checkBoxlist.append(self.checkBox)


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
        self.Tabs.setCornerWidget(cornerContainer) 
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
        self.selected = QLabel(f"{1} Selected")
        self.select_all = QCheckBox("Select All")
        
        select_ld_name_layout_top.addWidget(self.selected)
        select_ld_name_layout_top.addStretch(1)
        select_ld_name_layout_top.addWidget(self.select_all)
        
        try:
            MAX = len(Option().check_ld_in_list())
        except:
            print(f"cannot get a max value for spinBox Raise")
            
        #bottom
        self.spinBox_selectAll_start = QSpinBox(self)
        

        self.spinBox_selectAll_start.setRange(0, MAX)
        self.spinBox_selectAll_start.setValue(0)
        

        toLabel = QLabel("To")
        toLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinBox_selectAll_end = QSpinBox(self)

        self.spinBox_selectAll_end.setRange(0, MAX)
        self.spinBox_selectAll_end.setValue(MAX)
        self.spinBox_selectAll_end.valueChanged.connect(lambda v: self.selectRange("end",v))
        self.spinBox_selectAll_start.valueChanged.connect(lambda v: self.selectRange("start",v))
        confirm = QPushButton("☑︎")
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

    def selectRange(self, which: str, value: int) -> None:
        try:
            max_value = len(Option().check_ld_in_list())
        except:
            print("Error occurred while getting max value")
        start = self.spinBox_selectAll_start.value()
        end = self.spinBox_selectAll_end.value()
        
        if self.spinBox_selectAll_start.maximum() != max_value:
            self.spinBox_selectAll_start.setMaximum(max_value)
        if self.spinBox_selectAll_end.maximum() != max_value:
            self.spinBox_selectAll_end.setMaximum(max_value)

        if which == "start":
            if value < end:
                
                self.spinBox_selectAll_start.setValue(value)
            else:
                self.spinBox_selectAll_start.setValue(value - 1)
        elif which == "end":
            if value > start:
                
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
        rect = super().subControlRect(control, opt, subControl, widget)  # type: ignore[arg-type]
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
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    LD = LDPlayer()
    app = QApplication(sys.argv)
    app.setStyle(Proxy())
    window = BobPrimeApp()  
    window.show()
    app.exec()