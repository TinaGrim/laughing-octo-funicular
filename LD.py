import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenuBar,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton
from PySide6.QtGui import QColor, QFont, QPixmap,QIcon
from PySide6.QtCore import Qt, QTimer,QSize,QThread
import sys
import time
import webbrowser
import threading
LD_Function = os.path.abspath("C:/Users/User/OneDrive - itc.edu.kh/Desktop/WorkSpace/programing/Python/LD-Player")
print("Adding to path:", LD_Function)

if LD_Function not in sys.path:
    sys.path.append(LD_Function)

print("Current sys.path:")
for p in sys.path:
    print(p)
import Main as Open # type: ignore

class BobPrimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Girm Prime App")
        self.setGeometry(100, 100, 1500, 800)

        pixmap = QPixmap("Logo/logo_icon_big.png").scaled(128, 128)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        self.setStyleSheet("""
            QMainWindow, QWidget{
            background-color: #292c3b;
            margin: 0px;
            padding: 0px;
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
        """)
        os.system("cls")
        self.starttime = time.time()
        self.time_label = QLabel()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)  
        self.update_time()
        self.init()
        
    
    def update_time(self) -> None:
        """Update the time label with current time using replace"""
        elapsed = int(time.time() - self.starttime)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_label.setText(f'<div style="font-size: 70px;">{hours:02}:{minutes:02}:{seconds:02}</div>')

    def init(self) -> None:
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        """"Tabs"""
        self.Tabs = QTabWidget()
        self.Tabs.addTab(QLabel("Hello"), "Devices")
        self.Tabs.addTab(self.Tab_auto_post(), "Auto Post")
        """End Tabs"""
        
        """Inside the main layout"""
        main_layout.addWidget(self.Left_view(), 3) 
        main_layout.addWidget(self.Tabs, 7)
             
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def Tab_auto_post(self) -> QWidget:

        auto_post_widget = QWidget()
        auto_post_layout = QHBoxLayout()
        
        # On left side
        """Schedule"""
        Group_Box_Schedule = QGroupBox()
        Group_schedule = QVBoxLayout()
        Group_schedule.addWidget(QCheckBox("Enable Schedule Post"))
        Group_schedule.addWidget(QCheckBox("Enable Post When Run"))
        Group_schedule.addWidget(QCheckBox("Shutdown PC"))
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
        LD_Table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        LD_Table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        LD_Table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        LD_Table.setCellWidget(0, 0, QCheckBox("1"))
        LD_Table.setCellWidget(1, 0, QCheckBox("2"))
        LD_Table.setItem(0, 1, QTableWidgetItem("LD 1"))
        LD_Table.setItem(1, 1, QTableWidgetItem("LD 2"))
        
        """End Table"""

        
        auto_post_layout_left_widget = QWidget()
        auto_post_layout_left = QVBoxLayout()
        
        auto_post_layout_left.addWidget(Group_Box_Schedule)
        auto_post_layout_left.addWidget(LD_Table)
        
        auto_post_layout_left_widget.setLayout(auto_post_layout_left)
        
        # On right side
        auto_post_layout_right_widget = QWidget()
        auto_post_layout_right = QVBoxLayout()
        
        """"Header"""

        page_setup_layout_Header = QHBoxLayout()
        Open_ld = QPushButton("➕")
        Open_ld.clicked.connect(lambda: self.start_thread(Open.LDPlayer().run, 2))
        page_setup_layout_Header.addWidget(Open_ld)
        page_setup_layout_Header.addWidget(QPushButton("🗑️"))
        page_setup_layout_Header.addWidget(QPushButton("✒️"))
  
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
        
        auto_post_layout.addWidget(auto_post_layout_left_widget,3)
        auto_post_layout.addWidget(auto_post_layout_right_widget,7)
        
        auto_post_widget.setLayout(auto_post_layout)
        
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
        table = QTableWidget(2, 4)
        table.setHorizontalHeaderLabels(["No.", "LD Name", "ID", "Activity"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setAutoFillBackground(False)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeMode.Stretch)
        table.setItem(0, 0, QTableWidgetItem("1"))
        table.setItem(1, 0, QTableWidgetItem("2"))
        table.setItem(0, 1, QTableWidgetItem("emulator"))
        table.setItem(1, 1, QTableWidgetItem("emulator"))
        table.setItem(0, 2, QTableWidgetItem("23"))
        table.setItem(1, 2, QTableWidgetItem("25"))
        table.setItem(0, 3, QTableWidgetItem("Activity 1"))
        table.setItem(1, 3, QTableWidgetItem("Activity2"))
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
        table_Box_Bottom.addWidget(QPushButton("💡"))
        table_layout.addWidget(QLabel("Active Devices"))
        table_layout.addWidget(table)
        table_layout.addLayout(table_Box_Bottom)
        table_Box_layout.setLayout(table_layout)
        """"End Bottom Box"""
        
        Left_Panel.addLayout(Head_left_panel)
        Left_Panel.addWidget(table_Box_layout)
        
        left_widget.setLayout(Left_Panel)
        return left_widget

    def start_thread(self, func, *args, **kwargs) -> None:
        self.My_thread = Threader(func,*args,**kwargs)
        self.My_thread.start()


class Threader(QThread):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.arg = args
        self.kwargs = kwargs
    def run(self):
        self.func(*self.arg, **self.kwargs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BobPrimeApp()  
    window.show()
    app.exec()
