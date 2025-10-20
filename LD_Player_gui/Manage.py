from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option

class Manage():
    def __init__(self, GUI):
        self.GUI = GUI
        self.Devices = self.GUI.Devices
        self.opt = option()
        self.devices_list_qp = QButtonGroup()
        self.devices_list_qp.setExclusive(False)
        self.Check_Box_List_Devices = []
        def _get(key, default=None):
            return self.GUI.config["Manage"][key]
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
        # widget
        self.enable_ld_manager = QGroupBox("Enable LDPlayer Manager")
        self.enable_ld_manager.setCheckable(True)
        self.enable_ld_manager.setChecked(True)
        self.number_of_active = QSpinBox()
        self.number_of_active.setStyleSheet("margin: 0px;")
        
        self.number_of_active.setValue(1)
        self.add_new_ld = QCheckBox("Add New LDPlayers")
        self.add_new_ld_count = QSpinBox()
        self.add_new_ld_count.setValue(1)
        self.add_new_ld_count.setStyleSheet("margin: 0px;")

        self.copy_ld = QCheckBox("Copy From")
        self.backup = QCheckBox("Backup LDPlayer To")
        self.backup_loc = QLineEdit()
        self.backup_loc.setText(r"C:/path/to/self.backup.zip")
        self.backup_browse = QPushButton("...")
        self.backup_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        self.restore = QCheckBox("Restore LDPlayer From")
        self.restore_loc = QLineEdit()
        self.restore_loc.setText(r"C:/path/to/self.backup.zip")
        self.restore_browse = QPushButton("...")
        self.restore_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        self.remove_ld = QCheckBox("Remove LDPlayer")
        self.shutdown = QCheckBox("Shutdown PC When Finish")
        self.enable_facebook_manager = QGroupBox("Enable LDPlayer Manager")
        self.enable_facebook_manager.setCheckable(True)
        self.enable_facebook_manager.setChecked(True)
        self.enable_ld_manager.setStyleSheet("margin: 8px;")
        self.enable_facebook_manager.setStyleSheet("margin: 8px;")
        self.auto_pull_name = QCheckBox("Auto Pull Account/Page Name")
        self.clear_exist_name = QCheckBox("Clear Existing Names")
        self.fb_login = QCheckBox("FB Login")
        self.fb_login_loc = QLineEdit()
        self.fb_login_loc.setText(r"C:/path/to/FBlocal.txt")
        self.account_name = QCheckBox("Account/Page Name")
        self.account_name_btn = QPushButton("@")
        self.create_page = QCheckBox("Create Pages")
        self.shutdown_pc = QCheckBox("Shutdown PC When Finish")
        self.account_name_btn.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        self.copy_ld_from = QComboBox()
        self.copy_ld_from.addItems(self.opt.check_ld_in_list())
        self.copy_ld_from.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.config = {
            "enable_ld_manager": _bool("enable_ld_manager"),
            "backup_loc": _str("backup_loc"),
            "restore_loc": _str("restore_loc"),
            "enable_facebook_manager": _bool("enable_facebook_manager"),
            "fb_login_loc": _str("fb_login_loc")
        }
        # __ text __
        for wid in [
            "backup_loc", "restore_loc", "fb_login_loc",
        ]:
            widget = getattr(self, wid)
            widget.textChanged.connect(lambda text, w=wid: self.GUI.change_config("Manage", w, text))
        # __ toggle __
        for wid in [
            "enable_ld_manager",
            "enable_facebook_manager"
        ]:
            widget = getattr(self, wid)
            widget.toggled.connect(lambda checked, w=wid: self.GUI.change_config("Manage", w, str(checked)))

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

        ld_manage_manager_layout_top = QVBoxLayout(self.enable_ld_manager)

        number_active = QHBoxLayout()
        number = QLabel("Number of Active Batch")
        number_active.addWidget(number)
        number_active.addWidget(self.number_of_active)
        number_active.addStretch(1)

        add_new_ld = QHBoxLayout()
        
        
        add_new_ld.addWidget(self.add_new_ld)
        add_new_ld.addWidget(self.add_new_ld_count)
        add_new_ld.addWidget(self.copy_ld)
        add_new_ld.addWidget(self.copy_ld_from)        
        
        backup = QHBoxLayout()
        backup.addWidget(self.backup)
        backup.addWidget(self.backup_loc)
        backup.addWidget(self.backup_browse)
        
        restore = QHBoxLayout()
        
        restore.addWidget(self.restore)
        restore.addWidget(self.restore_loc)
        restore.addWidget(self.restore_browse)
        
        remove = QHBoxLayout()
        remove.addWidget(self.remove_ld)
        shutdown = QHBoxLayout()
        shutdown.addWidget(self.shutdown)
        
        ld_manage_manager_layout_top.addLayout(number_active)
        ld_manage_manager_layout_top.addLayout(add_new_ld)
        ld_manage_manager_layout_top.addLayout(backup)
        ld_manage_manager_layout_top.addLayout(restore)
        ld_manage_manager_layout_top.addLayout(remove)
        ld_manage_manager_layout_top.addLayout(shutdown)
        ld_manage_manager_layout_top.addStretch(1)

        ld_manage_manager_layout_top.setContentsMargins(10, 20, 0, 0)
        
        
        ld_manage_manager_layout_bottom = QVBoxLayout(self.enable_facebook_manager)
        autoput = QHBoxLayout()
        autoput.addWidget(self.auto_pull_name)
        autoput.addWidget(self.clear_exist_name)
        autoput.addStretch(1)
        
        FBlocal = QHBoxLayout()
        FBlocal_browse = QPushButton("...")
        FBlocal_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")
        FBlocal.addWidget(self.fb_login)
        FBlocal.addWidget(self.fb_login_loc)
        FBlocal.addWidget(FBlocal_browse)
        FBlocal.addWidget(self.account_name)
        FBlocal.addWidget(self.account_name_btn)
        
        createpage = QHBoxLayout()
        createpage.addWidget(self.create_page)
        shutdownbottom = QHBoxLayout()
        shutdownbottom.addWidget(self.shutdown_pc)

        ld_manage_manager_layout_bottom.addLayout(autoput)
        ld_manage_manager_layout_bottom.addLayout(FBlocal)
        ld_manage_manager_layout_bottom.addLayout(createpage)
        ld_manage_manager_layout_bottom.addLayout(shutdownbottom)
        ld_manage_manager_layout_bottom.addStretch(1)
        ld_manage_manager_layout_bottom.setContentsMargins(10, 20, 0, 0)


        ld_manage_manager_layout.addWidget(self.enable_ld_manager)
        ld_manage_manager_layout.addWidget(self.enable_facebook_manager)
        ld_manage_layout.addWidget(ld_manage_list, 3)
        ld_manage_layout.addWidget(ld_manage_manager, 7)

        return ld_manage_widget
    
    def update_devices_list(self) -> QWidget:
        list_devices = self.opt.check_ld_in_list()  # Sample [<LD Name>]
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
        # if getattr(self, "select_all_devices", None):
        #     self.select_all_devices.setChecked(False)
        #     self.selected_Devices.setText(f"{0} Selected")
        self.update_exist_devices_list(list_devices)
        return self.devices_list

    def update_exist_devices_list(self, list_devices: list[str]) -> None:
        if not self.devices_list:
            return
        for i in range(0, len(list_devices)):
            self.devices_list.setRowCount(len(list_devices))
            self.list_devices_checkBox = QCheckBox(str(i+1))
            self.list_devices_checkBox.setChecked(True if (i+1) in getattr(self, "specific_list_devices_ID", []) else False)
            self.devices_list_qp.addButton(self.list_devices_checkBox, i+1)
            self.devices_list.setCellWidget(i, 0, self.list_devices_checkBox)
            self.devices_list.setItem(i, 1, QTableWidgetItem(list_devices[i]))
            self.Check_Box_List_Devices.append(self.list_devices_checkBox)
            
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
            if self.Devices.devices_table.item(id-1, 1):
                item = self.Devices.devices_table.item(id-1, 1)
                if item is not None:
                    item.setBackground(QColor("#07417a"))
        else:
            if self.Devices.devices_table.item(id-1, 1):
                item = self.Devices.devices_table.item(id-1, 1)
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
            MAX = len(self.opt.check_ld_in_list())
        except: 
            print(f"cannot get a max value for spinBox Raise")
        #bottom
        
        
        self.spinBox_select_all_list_devices_start = QSpinBox()
        self.spinBox_select_all_list_devices_start.setRange(1, MAX)
        self.spinBox_select_all_list_devices_start.setValue(1)
        
        toLabel = QLabel("To")
        toLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinBox_select_all_list_devices_end = QSpinBox()
        self.spinBox_select_all_list_devices_end.setRange(1, MAX)
        self.spinBox_select_all_list_devices_end.setValue(MAX)
        self.spinBox_select_all_list_devices_end.valueChanged.connect(lambda v: self.GUI.selectRange("end",v))
        self.spinBox_select_all_list_devices_start.valueChanged.connect(lambda v: self.GUI.selectRange("start",v))

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
            self.confirmSelectRange_list_devices(1, len(self.opt.check_ld_in_list()))
            self.select_all_devices.setChecked(True)
        else:
            self.select_all_devices.setChecked(False)


            
