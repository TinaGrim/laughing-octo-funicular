from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option
class Active():
    def __init__(self, GUI) -> None:
        self.GUI = GUI
        self.opt = option()
        
        def _get(key, default=None):
            return self.GUI.config["Active"][key]
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

            "check_notification": _bool("check_notification"),
            "check_notification_time": _int("check_notification_time"),
            "check_primary_location": _bool("check_primary_location", False),

            "scroll_feed": _bool("scroll_feed"),
            "scroll_feed_start": _int("scroll_feed_start"),
            "scroll_feed_end": _int("scroll_feed_end"),

            "scroll_video": _bool("scroll_video"),
            "scroll_video_start": _int("scroll_video_start"),
            "scroll_video_end": _int("scroll_video_end"),

            "scroll_reel": _bool("scroll_reel"),
            "scroll_reel_start": _int("scroll_reel_start"),
            "scroll_reel_end": _int("scroll_reel_end"),

            "confirm_friend": _bool("confirm_friend"),
            "confirm_friend_time": _int("confirm_friend_time"),

            "add_friend": _bool("add_friend"),
            "add_friend_time": _int("add_friend_time"),

            "react_post": _bool("react_post"),
            "react_post_time": _int("react_post_time"),

            "check_message": _bool("check_message"),
            "check_message_time": _int("check_message_time"),

            "reply": _bool("reply"),
            "reply_text": _str("reply_text", "{Hi|Hello|Hey|How are you}"),

            "check_post": _bool("check_post"),
            "check_post_time": _int("check_post_time"),

            "photo": _bool("photo"),
            "photo_loc": _str("photo_loc", "C:/path/to/photo.jpg"),

            "check_story": _bool("check_story"),
            "check_story_time": _int("check_story_time"),

            "video_loc": _str("video_loc", "C:/path/to/video.mp4"),

            "comment_post": _bool("comment_post"),
            "comment_post_time": _int("comment_post_time"),
            "comment_text": _str("comment_text", ""),

            "share_to_gp": _bool("share_to_gp"),
            "share_to_gp_time": _int("share_to_gp_time"),

            "profile": _bool("profile"),
            "profile_link": _str("profile_link", ""),

            "active_loop": _int("active_loop"),
            "active_between": _bool("active_between"),
            "active_between_start": _int("active_between_start"),
            "active_between_end": _int("active_between_end"),

            "shutdown": _bool("shutdown"),

            "install_apk": _bool("install_apk"),
            "apk_loc": _str("apk_loc", "C:/path/to/app.apk"),

            "facebook_app_number": _int("facebook_app_number"),
            "switch_account": _int("switch_account"),
            "enable_active": _bool("enable_active")
        }
        
        #
        # notify action
        #
        self.check_primary_location = QCheckBox("Check Primary Location")
        self.check_primary_location.setChecked(self.config["check_primary_location"])
        self.check_notification = QCheckBox("Check Notification")
        self.check_notification.setChecked(self.config["check_notification"])
        self.check_notification_time = QSpinBox()
        self.check_notification_time.setValue(self.config["check_notification_time"])

        #
        # scroll action
        #
        self.scroll_feed = QCheckBox("Scroll News Feed")
        self.scroll_feed.setChecked(self.config["scroll_feed"])
        self.scroll_feed_start = QSpinBox()
        self.scroll_feed_start.setValue(self.config["scroll_feed_start"])
        self.scroll_feed_end = QSpinBox()
        self.scroll_feed_end.setValue(self.config["scroll_feed_end"])
        self.scroll_feed_widget = QWidget()
        self.scroll_feed_layout = QHBoxLayout(self.scroll_feed_widget)
        self.scroll_feed_layout.addWidget(self.scroll_feed_end)
        self.scroll_feed_layout.addWidget(QLabel("Minutes"))
        self.scroll_feed_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_video = QCheckBox("Scroll Video")
        self.scroll_video.setChecked(self.config["scroll_video"])
        self.scroll_video_start = QSpinBox()
        self.scroll_video_start.setValue(self.config["scroll_video_start"])
        self.scroll_video_end = QSpinBox()
        self.scroll_video_end.setValue(self.config["scroll_video_end"])
        self.scroll_video_widget = QWidget()
        self.scroll_video_layout = QHBoxLayout(self.scroll_video_widget)
        self.scroll_video_layout.addWidget(self.scroll_video_end)
        self.scroll_video_layout.addWidget(QLabel("Minutes"))
        self.scroll_video_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_reel = QCheckBox("Scroll Reels")
        self.scroll_reel.setChecked(self.config["scroll_reel"])
        self.scroll_reel_start = QSpinBox()
        self.scroll_reel_start.setValue(self.config["scroll_reel_start"])
        self.scroll_reel_end = QSpinBox()
        self.scroll_reel_end.setValue(self.config["scroll_reel_end"])
        self.scroll_reel_widget = QWidget()
        self.scroll_reel_layout = QHBoxLayout(self.scroll_reel_widget)
        self.scroll_reel_layout.addWidget(self.scroll_reel_end)
        self.scroll_reel_layout.addWidget(QLabel("Minutes"))
        self.scroll_reel_layout.setContentsMargins(0, 0, 0, 0)

        #
        # confirm action
        #
        self.confirm_friend = QCheckBox("Confirm Friend")
        self.confirm_friend.setChecked(self.config["confirm_friend"])
        self.confirm_friend_time = QSpinBox()
        self.confirm_friend_time.setValue(self.config["confirm_friend_time"])
        self.add_friend = QCheckBox("Add Friend")
        self.add_friend.setChecked(self.config["add_friend"])
        self.add_friend_time = QSpinBox()
        self.add_friend_time.setValue(self.config["add_friend_time"])

        #
        # post action
        #
        self.react_post = QCheckBox("React Post")
        self.react_post.setChecked(self.config["react_post"])
        self.react_post_time = QSpinBox()
        self.react_post_time.setValue(self.config["react_post_time"])

        #
        # check message action
        #
        self.check_message = QCheckBox("Check Message")
        self.check_message.setChecked(self.config["check_message"])
        self.check_message_time = QSpinBox()
        self.check_message_time.setValue(self.config["check_message_time"])
        self.reply = QCheckBox("Reply")
        self.reply.setChecked(self.config["reply"])
        self.reply_text = QLineEdit()
        self.reply_text.setPlaceholderText(r"{Hi|Hello|Hey|How are you}")
        self.reply_text.setText(self.config["reply_text"])

        #
        # create post action
        #
        self.check_post = QCheckBox("Create Post")
        self.check_post.setChecked(self.config["check_post"])
        self.check_post_time = QSpinBox()
        self.check_post_time.setValue(self.config["check_post_time"])
        self.photo = QCheckBox("Photo")
        self.photo.setChecked(self.config["photo"])
        self.photo_loc = QLineEdit()
        self.photo_loc.setPlaceholderText(r"C:/path/to/photo.jpg")
        self.photo_loc.setText(self.config["photo_loc"])
        
        self.photo_browse = QPushButton("...")
        self.photo_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")

        #
        # story action
        #
        self.check_story = QCheckBox("Check Story")
        self.check_story.setChecked(self.config["check_story"])
        self.check_story_time = QSpinBox()
        self.check_story_time.setValue(self.config["check_story_time"])
        self.video_loc = QLineEdit()
        self.video_loc.setPlaceholderText(r"C:/path/to/video.mp4")
        self.video_loc.setText(self.config["video_loc"])
        self.story_video_browse = QPushButton("...")
        self.story_video_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")

        #
        # comment action
        #
        self.comment_post = QCheckBox("Comment Post")
        self.comment_post.setChecked(self.config["comment_post"])
        self.comment_post_time = QSpinBox()
        self.comment_post_time.setValue(self.config["comment_post_time"])
        self.comment_text = QLineEdit()
        self.comment_text.setPlaceholderText(r"comment1, comment2, comment3")
        self.comment_text.setText(self.config["comment_text"])

        #
        # share action
        #
        self.share_to_gp = QCheckBox("Share Post to Group")
        self.share_to_gp.setChecked(self.config["share_to_gp"])
        self.share_to_gp_time = QSpinBox()
        self.share_to_gp_time.setValue(self.config["share_to_gp_time"])
        self.profile = QCheckBox("Profile")
        self.profile_link = QLineEdit()
        self.profile_link.setPlaceholderText(r"profile link1, profile link2, profile link3")
        self.profile_link.setText(self.config["profile_link"])

        #
        # loop action
        #
        self.active_loop = QSpinBox()
        self.active_loop.setValue(self.config["active_loop"])
        self.active_between = QCheckBox("Active Between Time")
        self.active_between.setChecked(self.config["active_between"])
        self.active_between_start = QSpinBox()
        self.active_between_start.setValue(self.config["active_between_start"])
        self.active_between_end = QSpinBox()
        self.active_between_end.setValue(self.config["active_between_end"])
        self.active_between_end_widget = QWidget()
        self.active_between_end_layout = QHBoxLayout(self.active_between_end_widget)
        self.active_between_end_layout.addWidget(self.active_between_end)
        self.active_between_end_layout.addWidget(QLabel("Minutes"))

        #
        # install apk action
        #
        self.install_apk = QCheckBox("Install APK")
        self.install_apk.setChecked(self.config["install_apk"])
        self.apk_loc = QLineEdit()
        self.apk_loc.setPlaceholderText(r"C:/path/to/app.apk")
        self.apk_loc.setText(self.config["apk_loc"])
        self.install_apk_browse = QPushButton("...")
        self.install_apk_browse.setStyleSheet("margin: 0px; padding: 2px 10px; ")

        #
        # shutdown action
        #
        self.shutdown = QCheckBox("Shutdown when finish")
        self.shutdown.setChecked(self.config["shutdown"])
        #
        # table action
        #
        self.enable_active = QCheckBox("Enable Active")
        self.enable_active.setChecked(self.config["enable_active"])
        
        
        # trigger
        # ---- Toggles  ----
        for name in [
            "check_notification",
            "check_primary_location",
            "scroll_feed",
            "scroll_video",
            "scroll_reel",
            "confirm_friend",
            "add_friend",
            "react_post",
            "check_message",
            "reply",
            "check_post",
            "photo",
            "check_story",
            "comment_post",
            "share_to_gp",
            "profile",
            "active_between",
            "shutdown",
            "install_apk",
            "enable_active"
            
        ]:
            widget = getattr(self, name)
            widget.toggled.connect(lambda state, n=name: self.GUI.change_config("Active", n, str(state)))

        # ---- spinbox ----
        for name in [
            "check_notification_time",
            "scroll_feed_start",
            "scroll_feed_end",
            "scroll_video_start",
            "scroll_video_end",
            "scroll_reel_start",
            "scroll_reel_end",
            "confirm_friend_time",
            "add_friend_time",
            "react_post_time",
            "check_message_time",
            "check_post_time",
            "comment_post_time",
            "share_to_gp_time",
            "active_loop",
            "active_between_start",
            "active_between_end",
            # "facebook_app_number",
            # "switch_account"
        ]:
            widget = getattr(self, name)
            widget.valueChanged.connect(lambda value, n=name: self.GUI.change_config("Active", n, str(value)))

        # ---- Text ----
        for name in [
            "reply_text",
            "photo_loc",
            "video_loc",
            "comment_text",
            "profile_link",
            "apk_loc"
        ]:
            widget = getattr(self, name)
            widget.textChanged.connect(lambda text, n=name: self.GUI.change_config("Active", n, text))

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
        


        active_layout_main_top.addWidget(self.check_notification, 0, 0)
        active_layout_main_top.addWidget(self.check_notification_time, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.check_primary_location, 0, 3)

        active_layout_main_top.addWidget(self.scroll_feed, 1, 0)
        active_layout_main_top.addWidget(self.scroll_feed_start, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.scroll_feed_widget, 1, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        active_layout_main_top.addWidget(self.scroll_video, 2, 0)
        active_layout_main_top.addWidget(self.scroll_video_start, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.scroll_video_widget, 2, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        active_layout_main_top.addWidget(self.scroll_reel, 3, 0)
        active_layout_main_top.addWidget(self.scroll_reel_start, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 3, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.scroll_reel_widget, 3, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        active_layout_main_top.addWidget(self.confirm_friend, 4, 0)
        active_layout_main_top.addWidget(self.confirm_friend_time, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.add_friend, 4, 2)
        active_layout_main_top.addWidget(self.add_friend_time, 4, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        active_layout_main_top.addWidget(self.react_post, 5, 0)
        active_layout_main_top.addWidget(self.react_post_time, 5, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        active_layout_main_top.addWidget(self.check_message, 6, 0)
        active_layout_main_top.addWidget(self.check_message_time, 6, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.reply, 6, 2)
        active_layout_main_top.addWidget(self.reply_text, 6, 3, 1, 2)
        
        active_layout_main_top.addWidget(self.check_post, 7, 0)
        active_layout_main_top.addWidget(self.check_post_time, 7, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.photo, 7, 2, 1, 2)
        active_layout_main_top.addWidget(self.photo_loc, 7, 3)
        active_layout_main_top.addWidget(self.photo_browse, 7, 4)
        active_layout_main_top.addWidget(self.check_story, 8, 0)
        active_layout_main_top.addWidget(self.check_story_time, 8, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.video_loc, 8, 2, 1, 2)
        active_layout_main_top.addWidget(self.story_video_browse, 8, 4)

        active_layout_main_top.addWidget(self.comment_post, 9, 0)
        active_layout_main_top.addWidget(self.comment_post_time, 9, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.comment_text, 9, 2, 1, 4)

        active_layout_main_top.addWidget(self.share_to_gp, 10, 0)
        active_layout_main_top.addWidget(self.share_to_gp_time, 10, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(self.profile, 10, 2, 1, 2)
        active_layout_main_top.addWidget(self.profile_link, 10, 3, 1, 2)
        
        active_layout_main_top.addWidget(QLabel("Number of Active Loops"), 11, 0)
        active_layout_main_top.addWidget(self.active_loop, 11, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("Times"), 11, 2)

        active_layout_main_top.addWidget(self.active_between, 12, 0)
        active_layout_main_top.addWidget(self.active_between_start, 12, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        active_layout_main_top.addWidget(QLabel("To"), 12, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        active_layout_main_top.addWidget(self.active_between_end_widget, 12, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        active_layout_main_top.addWidget(self.shutdown, 13, 0)
        active_layout_main_top.addWidget(self.install_apk, 13, 1)
        active_layout_main_top.addWidget(self.apk_loc, 13, 2, 1, 2)
        active_layout_main_top.addWidget(self.install_apk_browse, 13, 4)

        active_layout_main_top.setColumnStretch(3, 1)
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
        self.select_all_active_ld = QCheckBox("Select All")
        active_table_layout_top.addWidget(self.enable_active)
        active_table_layout_top.addStretch(1)
        active_table_layout_top.addWidget(self.select_all_active_ld)

        #
        #bottom
        #
        active_table_bottom_widget = QWidget()
        self.selected_ld_active = QLabel("Selected")
        self.active_selected_start = QSpinBox()
        self.active_selected_start.setValue(0)
        self.active_selected_stop = QSpinBox()
        self.active_selected_stop.setValue(len(self.opt.check_ld_in_list()))
        self.active_selected_click = QPushButton("Here")
        active_table_bottom_layout = QHBoxLayout(active_table_bottom_widget)
        
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
    
    def update_active_table(self) -> QTableWidget:
        driver_list = self.opt.check_ld_in_list()# Sample [<LD Name>]
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