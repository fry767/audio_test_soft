# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'audio_test.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1086, 924)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.test_progb = QtWidgets.QProgressBar(self.centralwidget)
        self.test_progb.setGeometry(QtCore.QRect(850, 60, 118, 23))
        self.test_progb.setProperty("value", 24)
        self.test_progb.setObjectName("test_progb")
        self.start_test_pb = QtWidgets.QPushButton(self.centralwidget)
        self.start_test_pb.setGeometry(QtCore.QRect(910, 20, 80, 23))
        self.start_test_pb.setObjectName("start_test_pb")
        self.Connect_pb = QtWidgets.QPushButton(self.centralwidget)
        self.Connect_pb.setGeometry(QtCore.QRect(820, 20, 80, 23))
        self.Connect_pb.setObjectName("Connect_pb")
        self.load_lb = QtWidgets.QLabel(self.centralwidget)
        self.load_lb.setGeometry(QtCore.QRect(640, 100, 451, 21))
        self.load_lb.setObjectName("load_lb")
        self.glitch_cb = QtWidgets.QComboBox(self.centralwidget)
        self.glitch_cb.setGeometry(QtCore.QRect(630, 10, 131, 21))
        self.glitch_cb.setObjectName("glitch_cb")
        self.test_dur_le = QtWidgets.QLineEdit(self.centralwidget)
        self.test_dur_le.setGeometry(QtCore.QRect(1000, 20, 113, 29))
        self.test_dur_le.setObjectName("test_dur_le")
        self.b1_stats_lw = QtWidgets.QListWidget(self.centralwidget)
        self.b1_stats_lw.setGeometry(QtCore.QRect(110, 10, 256, 192))
        self.b1_stats_lw.setObjectName("b1_stats_lw")
        self.b2_stats_lw = QtWidgets.QListWidget(self.centralwidget)
        self.b2_stats_lw.setGeometry(QtCore.QRect(370, 10, 256, 192))
        self.b2_stats_lw.setObjectName("b2_stats_lw")
        self.show_bet_cb = QtWidgets.QCheckBox(self.centralwidget)
        self.show_bet_cb.setGeometry(QtCore.QRect(630, 40, 121, 22))
        self.show_bet_cb.setObjectName("show_bet_cb")
        self.show_from_le = QtWidgets.QLineEdit(self.centralwidget)
        self.show_from_le.setGeometry(QtCore.QRect(630, 60, 41, 29))
        self.show_from_le.setObjectName("show_from_le")
        self.show_to_le = QtWidgets.QLineEdit(self.centralwidget)
        self.show_to_le.setGeometry(QtCore.QRect(700, 60, 41, 29))
        self.show_to_le.setObjectName("show_to_le")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 92, 182))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.select_folder_pb = QtWidgets.QPushButton(self.layoutWidget)
        self.select_folder_pb.setObjectName("select_folder_pb")
        self.verticalLayout.addWidget(self.select_folder_pb)
        self.load_db_pb = QtWidgets.QPushButton(self.layoutWidget)
        self.load_db_pb.setObjectName("load_db_pb")
        self.verticalLayout.addWidget(self.load_db_pb)
        self.analyze_pb = QtWidgets.QPushButton(self.layoutWidget)
        self.analyze_pb.setObjectName("analyze_pb")
        self.verticalLayout.addWidget(self.analyze_pb)
        self.analyze_slider = QtWidgets.QSlider(self.layoutWidget)
        self.analyze_slider.setMaximum(20)
        self.analyze_slider.setOrientation(QtCore.Qt.Horizontal)
        self.analyze_slider.setObjectName("analyze_slider")
        self.verticalLayout.addWidget(self.analyze_slider)
        self.analysis_sens_te = QtWidgets.QLabel(self.layoutWidget)
        self.analysis_sens_te.setObjectName("analysis_sens_te")
        self.verticalLayout.addWidget(self.analysis_sens_te)
        self.test_pb = QtWidgets.QPushButton(self.layoutWidget)
        self.test_pb.setObjectName("test_pb")
        self.verticalLayout.addWidget(self.test_pb)
        self.plot_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.plot_scroll.setGeometry(QtCore.QRect(10, 210, 1061, 701))
        self.plot_scroll.setWidgetResizable(True)
        self.plot_scroll.setObjectName("plot_scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1059, 699))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.plot_scroll.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1086, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_test_pb.setText(_translate("MainWindow", "Start Test"))
        self.Connect_pb.setText(_translate("MainWindow", "Connect "))
        self.load_lb.setText(_translate("MainWindow", "TextLabel"))
        self.show_bet_cb.setText(_translate("MainWindow", "Show between"))
        self.select_folder_pb.setText(_translate("MainWindow", "Select folder"))
        self.load_db_pb.setText(_translate("MainWindow", "Load DB"))
        self.analyze_pb.setText(_translate("MainWindow", "Analyze"))
        self.analysis_sens_te.setText(_translate("MainWindow", "TextLabel"))
        self.test_pb.setText(_translate("MainWindow", "Test"))
