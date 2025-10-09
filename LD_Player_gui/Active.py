from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QListWidget,QGroupBox,QMenu,QTabWidget,QLineEdit,QTableWidget,QTableWidgetItem,QBoxLayout,QCheckBox,QHeaderView,QPushButton, QButtonGroup,QSpinBox,QSizePolicy,QStyle,QProxyStyle,QStyleOptionSpinBox, QFileDialog, QComboBox, QGridLayout
from PySide6.QtGui import QColor, QFont,QIcon
from PySide6.QtCore import Qt, QTimer,QSize, QRect
from LD_Player import option
class Active():
    def __init__(self, Grim) -> None:
        self.Grim = Grim
        self.opt = option()
        
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
        self.active_selected_stop.setValue(len(self.opt.check_ld_in_list()))
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