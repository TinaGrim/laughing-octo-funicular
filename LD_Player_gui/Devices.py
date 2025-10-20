from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option

class Devices():
    def __init__(self, GUI):
        self.GUI = GUI
        self.opt = option()
        
        def _get(key, default=None):
            return self.GUI.config["Devices"][key]
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
            "ld_loc": _str("ld_loc"),
            "sys_loc": _str("sys_loc"),
            "number_of_active_ld": _int("number_of_active_ld"),
            "wait_after_ld_boot": _int("wait_after_ld_boot"),
            "between_ld_minutes": _int("between_ld_minutes"),
            "hardware_acceleration": _bool("hardware_acceleration"),
            "nvidia_gpu": _bool("nvidia_gpu"),
            "check_ip": _bool("check_ip"),
            "gps_timezone": _bool("gps_timezone"),
            "block_ip": _bool("block_ip"),
            "auto_advance_config": _bool("auto_advance_config"),
            "cpu_count": _int("cpu_count"),
            "ram_count": _int("ram_count"),
            "arangement": _bool("arangement"),
            "arangement_count": _int("arangement_count"),
            "auto_fit": _bool("auto_fit"),
            "screen_resolution": _str("screen_resolution"),
            "run_at_startup": _bool("run_at_startup"),
            "run_at_startup_seconds": _int("run_at_startup_seconds"),
            "auto_stop": _bool("auto_stop"),
            "auto_stop_minutes": _int("auto_stop_minutes"),
            "shutdown": _bool("shutdown"),
            "clear_cache": _bool("clear_cache"),
            "clear_cache_count": _int("clear_cache_count"),
            "clear_fb": _bool("clear_fb"),
            "clear_ld": _bool("clear_ld"),
            "clear_ld_gb": _int("clear_ld_gb"),
            "close_all_when_stop": _bool("close_all_when_stop"),
        }

        
        # Widgets
        self.ld_loc = QLineEdit(self.config["ld_loc"])
        self.browse_ld = QPushButton("Browse")

        self.sys_loc = QLineEdit(self.config["sys_loc"])
        self.browse_sys = QPushButton("Browse")

        self.number_of_active_ld = QSpinBox()
        self.number_of_active_ld.setValue(self.config["number_of_active_ld"])

        self.wait_after_ld_boot = QSpinBox()
        self.wait_after_ld_boot.setValue(self.config["wait_after_ld_boot"])

        self.between_ld_minutes = QSpinBox()
        self.between_ld_minutes.setValue(self.config["between_ld_minutes"])

        self.hardware_acceleration = QCheckBox("Hardware Accel")
        self.hardware_acceleration.setChecked(self.config["hardware_acceleration"])

        self.nvidia_gpu = QCheckBox("NVIDIA GPU")
        self.nvidia_gpu.setChecked(self.config["nvidia_gpu"])

        self.check_ip = QCheckBox("Check IP")
        self.gps_timezone = QCheckBox("GPS/TimeZone")
        self.block_ip = QCheckBox("Block IP")
        self.check_ip.setChecked(self.config["check_ip"])
        self.gps_timezone.setChecked(self.config["gps_timezone"])
        self.block_ip.setChecked(self.config["block_ip"])

        self.auto_advance_config = QCheckBox("Auto LDplayer Advanced Configuration")
        self.auto_advance_config.setChecked(self.config["auto_advance_config"])

        self.cpu_count = QComboBox()
        self.cpu_count.addItems(["1 core","2 cores","3 cores","4 cores","5 cores","6 cores","7 cores","8 cores"])
        self.cpu_count.setCurrentIndex(self.config["cpu_count"] - 1)

        self.ram_count = QComboBox()
        ram_list = ["512MB","1GB","2GB","3GB","4GB"]
        self.ram_count.addItems(ram_list)
        self.ram_count.setCurrentIndex(ram_list.index(f"{self.config['ram_count']}GB") if f"{self.config['ram_count']}GB" in ram_list else 0)

        self.arangement = QCheckBox("Arrange LDplayer")
        self.arangement_count = QSpinBox()
        self.arangement_count.setValue(self.config["arangement_count"])
        self.arangement_count.setStyleSheet("margin: 0px;")

        self.auto_fit = QCheckBox("Auto Fit")
        self.auto_fit.setChecked(self.config["auto_fit"])

        self.screen_resolution = QComboBox()
        self.screen_resolution.addItems(["1280x720","1920x1080","2560x1440","3840x2160"])
        self.screen_resolution.setCurrentIndex(
            next(
                (i for i in range(self.screen_resolution.count())
                if self.screen_resolution.itemText(i) == self.config["screen_resolution"]),0
            )
        )

        self.run_at_startup = QCheckBox("Run at Startup")
        self.run_at_startup.setChecked(self.config["run_at_startup"])
        self.run_at_startup_seconds = QSpinBox()
        self.run_at_startup_seconds.setValue(self.config["run_at_startup_seconds"])
        self.run_at_startup_seconds.setStyleSheet("margin: 0px;")

        self.auto_stop = QCheckBox("Auto Stop at")
        self.auto_stop.setChecked(self.config["auto_stop"])
        self.auto_stop_minutes = QSpinBox()
        self.auto_stop_minutes.setValue(self.config["auto_stop_minutes"])
        self.auto_stop_minutes.setStyleSheet("margin: 0px;")

        self.shutdown = QCheckBox("Shutdown")
        self.shutdown.setChecked(self.config["shutdown"])

        self.clear_cache = QCheckBox("Clear cache every run counts")
        self.clear_cache.setChecked(self.config["clear_cache"])
        self.clear_cache_count = QSpinBox()
        self.clear_cache_count.setValue(self.config["clear_cache_count"])
        self.clear_cache_count.setStyleSheet("margin: 0px;")

        self.clear_fb = QCheckBox("Clear FB user data if exceeds 900 MB")
        self.clear_fb.setChecked(self.config["clear_fb"])

        self.clear_ld = QCheckBox("Clear LDPlayer if exceeds ")
        self.clear_ld.setChecked(self.config["clear_ld"])
        self.clear_ld_gb = QSpinBox()
        self.clear_ld_gb.setValue(self.config["clear_ld_gb"])
        self.clear_ld_gb.setStyleSheet("margin: 0px;")

        self.close_all_when_stop = QCheckBox("Close all LD when stop")
        self.close_all_when_stop.setChecked(self.config["close_all_when_stop"])

        
        # trigger
        self.browse_ld.clicked.connect(self.LD_dir)
        self.browse_sys.clicked.connect(self.Sys_dir)

        numeric_fields = {
            "number_of_active_ld": self.number_of_active_ld,
            "wait_after_ld_boot": self.wait_after_ld_boot,
            "between_ld_minutes": self.between_ld_minutes,
            "arangement_count": self.arangement_count,
            "run_at_startup_seconds": self.run_at_startup_seconds,
            "auto_stop_minutes": self.auto_stop_minutes,
            "clear_cache_count": self.clear_cache_count,
            "clear_ld_gb": self.clear_ld_gb,
        }

        for name, widget in numeric_fields.items():
            widget.valueChanged.connect(lambda value, n=name: self.GUI.change_config("Devices", n, str(value)))


        toggle_fields = [
            "hardware_acceleration",
            "nvidia_gpu",
            "check_ip",
            "gps_timezone",
            "block_ip",
            "auto_advance_config",
            "arangement",
            "auto_fit",
            "run_at_startup",
            "auto_stop",
            "shutdown",
            "clear_cache",
            "clear_fb",
            "clear_ld",
            "close_all_when_stop",
        ]

        for name in toggle_fields:
            widget = getattr(self, name)
            widget.toggled.connect(lambda checked, n=name: self.GUI.change_config("Devices", n, str(checked)))

        combo_fields = {
            "cpu_count": lambda index: str(index + 1),
            "ram_count": lambda index: str(index + 1),
            "screen_resolution": lambda index: self.screen_resolution.itemText(index),
        }

        for name, transform in combo_fields.items():
            widget = getattr(self, name)
            widget.currentIndexChanged.connect(lambda index, n=name, t=transform: self.GUI.change_config("Devices", n, t(index)))


        
        

            
    def Tab_Devices(self) -> QWidget:
        devices_widget = QWidget()
        devices_widget_layout = QVBoxLayout(devices_widget)

        devices_browser_widget = QWidget()
        devices_browser_widget_layout = QHBoxLayout(devices_browser_widget)

        devices_locate_widget = QWidget()
        devices_locate_widget_layout = QVBoxLayout(devices_locate_widget)

        # LDPlayer location row
        devices_locate_widget_layout_top = QHBoxLayout()
        label_ld = QLabel("LDPlayer Location")
        devices_locate_widget_layout_top.addWidget(label_ld)
        devices_locate_widget_layout_top.addWidget(self.ld_loc)
        devices_locate_widget_layout_top.addWidget(self.browse_ld)

        # System location row
        devices_locate_widget_layout_bottom = QHBoxLayout()
        label_sys = QLabel("System Location")
        devices_locate_widget_layout_bottom.addWidget(label_sys)
        devices_locate_widget_layout_bottom.addWidget(self.sys_loc)
        devices_locate_widget_layout_bottom.addWidget(self.browse_sys)

        devices_locate_widget_layout.addLayout(devices_locate_widget_layout_top)
        devices_locate_widget_layout.addLayout(devices_locate_widget_layout_bottom)

        # Upload button
        devices_upload = QPushButton("Upload")
        devices_upload.setStyleSheet("margin: 0px; padding: 40px 60px; ")

        devices_browser_widget_layout.addWidget(devices_locate_widget, 8)
        devices_browser_widget_layout.addWidget(devices_upload, 2)
        devices_browser_widget_layout.setContentsMargins(0, 0, 0, 0)

        devices_information_widget = QWidget()
        devices_information_widget_layout = QVBoxLayout(devices_information_widget)

        # Top information layout
        devices_information_top_widget = QWidget()
        devices_information_top_layout = QHBoxLayout(devices_information_top_widget)

        label_active_ld = QLabel("Number of active LD")
        label_wait_boot = QLabel("Wait after LD Boot")
        label_between_ld = QCheckBox("Between LD Start")

        gpu_box = QGroupBox()
        gpu_layout = QVBoxLayout(gpu_box)
        gpu_layout.addWidget(self.hardware_acceleration)
        gpu_layout.addWidget(self.nvidia_gpu)

        app_button = QPushButton("App")

        devices_information_top_layout.addWidget(label_active_ld)
        devices_information_top_layout.addWidget(self.number_of_active_ld)
        devices_information_top_layout.addStretch(1)
        devices_information_top_layout.addWidget(label_wait_boot)
        devices_information_top_layout.addWidget(self.wait_after_ld_boot)
        devices_information_top_layout.addStretch(1)
        devices_information_top_layout.addWidget(label_between_ld)
        devices_information_top_layout.addWidget(self.between_ld_minutes)
        devices_information_top_layout.addStretch(1)
        devices_information_top_layout.addWidget(gpu_box)
        devices_information_top_layout.addWidget(app_button)
        devices_information_top_layout.setAlignment(Qt.AlignmentFlag.AlignVertical_Mask)

        # Bottom settings layout
        devices_information_bottom_widget = QWidget()
        devices_information_bottom_layout = QHBoxLayout(devices_information_bottom_widget)

        devices_setting_box = QGroupBox("LDPlayer Setting")
        devices_setting_box_layout = QVBoxLayout(devices_setting_box)

        # IP, GPS, Block IP
        devices_setting_ip_layout = QHBoxLayout()
        devices_setting_ip_layout.addWidget(self.check_ip)
        devices_setting_ip_layout.addWidget(self.gps_timezone)
        devices_setting_ip_layout.addWidget(self.block_ip)

        # Auto configuration
        devices_setting_auto_layout = QHBoxLayout()
        devices_setting_auto_layout.addWidget(self.auto_advance_config)

        # CPU / RAM settings
        devices_setting_cpu_layout = QHBoxLayout()
        label_cpu = QLabel("CPU")
        label_ram = QLabel("RAM")
        devices_setting_cpu_layout.addWidget(label_cpu, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_cpu_layout.addWidget(self.cpu_count)
        devices_setting_cpu_layout.addWidget(label_ram, alignment=Qt.AlignmentFlag.AlignCenter)
        devices_setting_cpu_layout.addWidget(self.ram_count)

        # Arrangement
        devices_setting_arrange_layout = QHBoxLayout()
        devices_setting_arrange_layout.addWidget(self.arangement)
        devices_setting_arrange_layout.addWidget(self.arangement_count)
        devices_setting_arrange_layout.addWidget(self.auto_fit)

        # Screen resolution
        devices_setting_screen_layout = QHBoxLayout()
        label_screen = QLabel("Screen")
        devices_setting_screen_layout.addWidget(label_screen, alignment=Qt.AlignmentFlag.AlignRight)
        devices_setting_screen_layout.addWidget(self.screen_resolution, alignment=Qt.AlignmentFlag.AlignLeft)

        # Run at startup
        devices_setting_startup_layout = QHBoxLayout()
        label_startup_seconds = QLabel("Seconds")
        devices_setting_startup_layout.addWidget(self.run_at_startup)
        devices_setting_startup_layout.addWidget(self.run_at_startup_seconds)
        devices_setting_startup_layout.addWidget(label_startup_seconds)

        # Auto stop
        devices_setting_autostop_layout = QHBoxLayout()
        label_autostop_minutes = QLabel("Minutes")
        devices_setting_autostop_layout.addWidget(self.auto_stop)
        devices_setting_autostop_layout.addWidget(self.auto_stop_minutes)
        devices_setting_autostop_layout.addWidget(label_autostop_minutes)
        devices_setting_autostop_layout.addWidget(self.shutdown)

        # Clear cache
        devices_setting_clearcache_layout = QHBoxLayout()
        devices_setting_clearcache_layout.addWidget(self.clear_cache)
        devices_setting_clearcache_layout.addWidget(self.clear_cache_count)

        # Clear FB / LD
        devices_setting_clearfb_layout = QHBoxLayout()
        devices_setting_clearfb_layout.addWidget(self.clear_fb)

        devices_setting_clearld_layout = QHBoxLayout()
        label_ld_gb = QLabel("GB")
        devices_setting_clearld_layout.addWidget(self.clear_ld)
        devices_setting_clearld_layout.addWidget(self.clear_ld_gb)
        devices_setting_clearld_layout.addWidget(label_ld_gb)

        # Close all LD when stop
        devices_setting_closeall_layout = QHBoxLayout()
        devices_setting_closeall_layout.addWidget(self.close_all_when_stop)

        for layout in [
            devices_setting_ip_layout,
            devices_setting_auto_layout,
            devices_setting_cpu_layout,
            devices_setting_arrange_layout,
            devices_setting_screen_layout,
            devices_setting_startup_layout,
            devices_setting_autostop_layout,
            devices_setting_clearcache_layout,
            devices_setting_clearfb_layout,
            devices_setting_clearld_layout,
            devices_setting_closeall_layout,
        ]:
            devices_setting_box_layout.addLayout(layout)
        devices_setting_box_layout.addStretch(1)

        devices_setting_box.setStyleSheet("margin: 5px; padding: 0;")
        devices_setting_box_layout.setContentsMargins(10, 20, 0, 0)

        devices_information_bottom_layout.addWidget(self.update_devices_table(), 6)
        devices_information_bottom_layout.addWidget(devices_setting_box, 4)

        devices_information_widget_layout.addWidget(devices_information_top_widget, 1)
        devices_information_widget_layout.addWidget(devices_information_bottom_widget, 9)
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
            self.ld_loc.setText(dir)
            self.GUI.change_config("Devices", "LD_loc", dir)
            
    def Sys_dir(self) -> None:
        dir = QFileDialog.getExistingDirectory(self.GUI, "Select System Directory", "")
        if dir:
            print("Selected directory:", dir)
            self.sys_loc.setText(dir)
            self.GUI.change_config("Devices", "Sys_loc", dir)

    
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