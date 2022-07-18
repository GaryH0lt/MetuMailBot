from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

import sys
from mail import HocamMail


class AppWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.mail_campaign_service = HocamMail()

        self.username_label = QLabel(self)
        self.username_textbox = QLineEdit(self)

        self.password_label = QLabel(self)
        self.password_textbox = QLineEdit(self)
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.ok_button = QPushButton(self)

        self.status_bar_label = QLabel(self)
        self.status_bar_timer = QTimer(self)

        self.interface_setup()
        self.set_signal_slot_connections()

    def interface_setup(self):
        # Main window
        self.setWindowTitle("HocamMail")
        self.setFixedSize(400, 350)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Username
        self.username_label.setText("Username:")
        self.username_label.setGeometry(75, 75, 250, 25)
        self.username_textbox.setGeometry(75, 100, 250, 25)

        # Password
        self.password_label.setText("Password:")
        self.password_label.setGeometry(75, 150, 250, 25)
        self.password_textbox.setGeometry(75, 175, 250, 25)

        # OK Button
        self.ok_button.setText("OK")
        self.ok_button.setGeometry(250, 250, 100, 25)

        # Status Bar
        self.statusBar().addWidget(self.status_bar_label)
        self.status_bar_label.setText("Welcome to HocamMail")
        self.status_bar_timer.setInterval(900)
        self.status_bar_timer.setSingleShot(True)

    def set_signal_slot_connections(self):
        self.ok_button.clicked.connect(self.login)
        self.status_bar_timer.timeout.connect(self.status_bar_timeout_event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.login()
        event.accept()

    def progress_function(self, n):
        progress_dict = dict()
        progress_dict[1] = " Login successful."
        progress_dict[2] = " Mail template successfully retrieved."
        progress_dict[3] = " Mail successfully sent."
        self.status_bar_label.setText(progress_dict[n])

    def login(self):
        # Get username and password from text boxes.
        username = self.username_textbox.text()
        password = self.password_textbox.text()

        # Clear the text boxes.
        self.username_textbox.setText("")
        self.password_textbox.setText("")

        # Return if username is not entered.
        if len(username) == 0:
            self.status_bar_label.setText("Please enter your username")
            self.status_bar_timer.start()
            return

        # Return if password is not entered.
        if len(password) == 0:
            self.status_bar_label.setText("Please enter your password")
            self.status_bar_timer.start()
            return

        # Attempt to log in, return if login fails.
        success = self.mail_campaign_service.login(username, password)
        if not success:
            self.status_bar_label.setText("Login was unsuccessful.")
            self.status_bar_timer.start()
            return
        # progress_callback.emit(1)

        # Attempt to get the mail template, return if unsuccessful.
        success = self.mail_campaign_service.get_mail_template()
        if not success:
            self.status_bar_label.setText("Unable to retrieve the mail template.")
            self.status_bar_timer.start()
            return
        # progress_callback.emit(2)

        # Attempt to send the mail, return if unsuccessful.
        success = self.mail_campaign_service.send_mail_template()
        if not success:
            self.status_bar_label.setText("Unable to send the mail.")
            self.status_bar_timer.start()
            return
        # progress_callback.emit(3)
        self.status_bar_timer.start()

    def status_bar_timeout_event(self):
        self.status_bar_label.setText("Welcome to HocamMail")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AppWindow()
    main_window.show()

    sys.exit(app.exec_())
