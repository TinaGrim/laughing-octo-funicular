from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option, LDPlayer
import cv2
import os
class Auto_Post():
    def __init__(self, GUI) -> None:
        self.GUI = GUI
        self.opt = option()
        def _get(key, default=None):
            return self.GUI.config["Auto_Post"][key]
        def _bool(key, default=False):
            v = _get(key, default)
            if isinstance(v, bool): return v
            return str(v).lower() in ("true", "1", "yes", "on")
        def _int(key, default=0):
            try: return int(_get(key, default))
            except Exception: return default
        def _str(key, default=""):
            v = _get(key, default)
            return str(v if v is not None else default)
        
        self.config = {
            "enable_schedule_post": _bool("enable_schedule_post"),
            "enable_post_when_run": _bool("enable_post_when_run"),
            "shutdown_pc": _bool("shutdown_pc"),
            "close_appium": _bool("close_appium"),
            "enable_post": _bool("enable_post"),
            "page_name": _str("page_name"),
            "app_name": _str("app_name"),
            "comment_on_post_reel": _bool("comment_on_post_reel"),
            "comment_on_post_photo": _bool("comment_on_post_photo"),
            "comment_on_post_video": _bool("comment_on_post_video"),
            "everyday": _bool("everyday"),
            "mon" : _bool("mon"),
            "tue" : _bool("tue"),
            "wed" : _bool("wed"),
            "thu" : _bool("thu"),
            "fri" : _bool("fri"),
            "sat" : _bool("sat"),
            "sun" : _bool("sun"),
        }
        # setup
        self.Check_Box_LD_Name = []
        self.timeline_table_list = []
        self.specific_ld_ID = []
        
        
        # widgets
        self.LD_Button_list_qp = QButtonGroup()
        self.LD_Button_list_qp.setExclusive(False)
        
        
        self.enable_schedule_post = QCheckBox("Enable Schedule Post")
        self.enable_schedule_post.setChecked(self.config["enable_schedule_post"])
        self.enable_post_when_run = QCheckBox("Enable Post When Run")
        self.enable_post_when_run.setChecked(self.config["enable_post_when_run"])
        self.shutdown_pc = QCheckBox("Shutdown PC")
        self.shutdown_pc.setChecked(self.config["shutdown_pc"])

        self.close_appium = QCheckBox("Auto Close Appium")
        self.close_appium.setChecked(self.config["close_appium"])
        
        
        self.Open_ld = QPushButton("➕")
        self.Open_ld.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.deleteButton = QPushButton("🗑️")
        self.deleteButton.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.createButton = QPushButton("✒️")
        self.createButton.setStyleSheet("margin: 0px 0px 10px 0px;")
        self.enable_post = QCheckBox("Enable Post")
        self.enable_post.setChecked(self.config["enable_post"])
        self.page_name = QLineEdit()
        self.page_name.setText(self.config["page_name"])
        self.app_name = QLineEdit()
        self.app_name.setText(self.config["app_name"])
        self.comment_on_post_reel = QCheckBox("Reel")
        self.comment_on_post_reel.setChecked(self.config["comment_on_post_reel"])
        self.comment_on_post_photo = QCheckBox("Photo")
        self.comment_on_post_photo.setChecked(self.config["comment_on_post_photo"])
        self.comment_on_post_video = QCheckBox("Video")
        self.comment_on_post_video.setChecked(self.config["comment_on_post_video"])
        self.mon = QCheckBox("Mon")
        self.mon.setChecked(self.config["mon"])
        self.tue = QCheckBox("Tue")
        self.tue.setChecked(self.config["tue"])
        self.wed = QCheckBox("Wed")
        self.wed.setChecked(self.config["wed"])
        self.thu = QCheckBox("Thu")
        self.thu.setChecked(self.config["thu"])
        self.fri = QCheckBox("Fri")
        self.fri.setChecked(self.config["fri"])
        self.sat = QCheckBox("Sat")
        self.sat.setChecked(self.config["sat"])
        self.sun = QCheckBox("Sun")
        self.sun.setChecked(self.config["sun"])
        
        self.dashboard = QCheckBox("Dashboard")
        self.posttable = QPushButton("☰ Post Table")
        self.timeline = QPushButton("⏱︎ Timeline")
        self.everyday = QGroupBox("Everyday")
        self.everyday.setCheckable(True)
        self.everyday.setChecked(self.config["everyday"])


        #trigger
        self.Open_ld.clicked.connect(lambda: self.GUI.LDPlayer_Start(self.specific_ld_ID))
        self.close_appium.stateChanged.connect(lambda: self.scheduleCheck())
        # __ bool __
        for key in [
            "enable_schedule_post",
            "enable_post_when_run",
            "shutdown_pc",
            "close_appium",
            "enable_post",
            "comment_on_post_reel",
            "comment_on_post_photo",
            "comment_on_post_video",
            "everyday",
            "mon",
            "tue",
            "wed",
            "thu",
            "fri",
            "sat",
            "sun",
        ]:
            widget = getattr(self, key)
            widget.toggled.connect(lambda checked, b=key: self.GUI.change_config("Auto_Post", b, str(checked)))
        # __ text __
        for text in [
            "page_name",
            "app_name",
        ]:
            widget = getattr(self, text)
            widget.textChanged.connect(lambda value, t=text: self.GUI.change_config("Auto_Post", t, value))
        
    def scheduleCheck(self) -> bool:
        self.scheduleClose = self.close_appium.isChecked()
        return self.scheduleClose
              
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


        Group_schedule.addWidget(self.enable_schedule_post)
        Group_schedule.addWidget(self.enable_post_when_run)
        Group_schedule.addWidget(self.shutdown_pc)
        Group_schedule.addWidget(self.close_appium)
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
        page_setup_name = QLabel("Page Name")
        page_setup_app = QLabel("App")
        page_setup_header.addWidget(self.enable_post)
        page_setup_header.addWidget(page_setup_name)
        page_setup_header.addWidget(self.page_name)
        page_setup_header.addWidget(page_setup_app)
        page_setup_header.addWidget(self.app_name)
        
        
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
        page_setup_post_on_layout.addWidget(self.comment_on_post_reel)
        page_setup_post_on_layout.addWidget(self.comment_on_post_photo)
        page_setup_post_on_layout.addWidget(self.comment_on_post_video)
        page_setup_post_on_layout.setContentsMargins(5, 0, 0, 0)
        page_setup_post_on.setStyleSheet("margin: 10px 0px; padding: 0px;")
        
        

        page_setup_schedule_day_layout = QVBoxLayout(self.everyday)

        page_setup_schedule_day_widget1 = QWidget()
        page_setup_schedule_day_layout1 = QHBoxLayout(page_setup_schedule_day_widget1)
        page_setup_schedule_day_widget2 = QWidget()
        page_setup_schedule_day_layout2 = QHBoxLayout(page_setup_schedule_day_widget2)
        page_setup_schedule_day_layout1.addWidget(self.mon)
        page_setup_schedule_day_layout1.addWidget(self.tue)
        page_setup_schedule_day_layout1.addWidget(self.wed)
        page_setup_schedule_day_layout1.addWidget(self.thu)
        page_setup_schedule_day_layout1.addStretch(1)
        
        page_setup_schedule_day_layout1.setContentsMargins(5, 0, 0, 0)
        page_setup_schedule_day_widget1.setStyleSheet("margin: 10px 0px 0px 0px; padding: 0px;")
        
        
        page_setup_schedule_day_layout2.addWidget(self.fri)
        page_setup_schedule_day_layout2.addWidget(self.sat)
        page_setup_schedule_day_layout2.addWidget(self.sun)
        page_setup_schedule_day_layout2.addStretch(1)
        
        page_setup_schedule_day_layout2.setContentsMargins(5, 0, 0, 0)
        page_setup_schedule_day_widget2.setStyleSheet("margin: 0px 0px 0px 0px; padding: 0px;")
        
        self.everyday.setStyleSheet("margin: 10px 0px; padding: 0px;")
        
        page_setup_schedule_day_layout.addWidget(page_setup_schedule_day_widget1)
        page_setup_schedule_day_layout.addWidget(page_setup_schedule_day_widget2)
        page_setup_schedule_day_layout.setContentsMargins(0, 0, 0, 0)
        
        page_setup_schedule_layout.addWidget(page_setup_post_on)
        page_setup_schedule_layout.addStretch(1)
        page_setup_schedule_layout.addWidget(self.everyday)
        
        page_setup_schedule_layout.setContentsMargins(0, 0, 0, 0)
        page_setup_schedule_widget.setStyleSheet("margin: 5px; padding: 0px;")
        
        page_setup_timeline = QWidget()
        page_setup_timeline_layout = QVBoxLayout(page_setup_timeline)
        
        page_setup_timeline_group = QGroupBox()
        page_setup_timeline_group_layout = QVBoxLayout(page_setup_timeline_group)
        page_setup_timeline_group_layout.addWidget(self.update_auto_post_timeline_table())
        

        page_setup_timeline_bottom = QHBoxLayout()
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
            item = self.LDName_table.item(id-1, 1)
            if item is not None:
                item.setBackground(QColor("#07417a"))
        else:
            item = self.LDName_table.item(id-1, 1)
            if item is not None:
                item.setBackground(QColor("#292c3b"))
    
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
            MAX = len(self.opt.check_ld_in_list())
        except:
            print(f"cannot get a max value for spinBox Raise")
            
        #bottom
        self.spinBox_select_all_ld_ld_name_start = QSpinBox()
        self.spinBox_select_all_ld_ld_name_start.setRange(1, MAX)
        self.spinBox_select_all_ld_ld_name_start.setValue(1)
        

        toLabel = QLabel("To")
        toLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinBox_select_all_ld_ld_name_end = QSpinBox()
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
            self.confirmSelectedRange(1, len(self.opt.check_ld_in_list()))
            self.select_all_ld.setChecked(True)
        else:
            self.select_all_ld.setChecked(False)

        
    def selectRange(self, which: str, value: int) -> None:
        try:
            max_value = len(self.opt.check_ld_in_list())
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
                
                
                
                
    def update_auto_post_table(self) -> QTableWidget:

        driver_list = self.opt.check_ld_in_list()# Sample [<LD Name>]

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
    

