# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'board.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_board_selector_window(object):
    def setupUi(self, board_selector_window):
        board_selector_window.setObjectName("board_selector_window")
        board_selector_window.setEnabled(True)
        board_selector_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(board_selector_window)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(44, 43, 526, 291))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.board_lw = QtWidgets.QListWidget(self.widget)
        self.board_lw.setObjectName("board_lw")
        self.verticalLayout.addWidget(self.board_lw)
        self.b1_id_pb = QtWidgets.QPushButton(self.widget)
        self.b1_id_pb.setObjectName("b1_id_pb")
        self.verticalLayout.addWidget(self.b1_id_pb)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.board_2_lb = QtWidgets.QLabel(self.widget)
        self.board_2_lb.setObjectName("board_2_lb")
        self.verticalLayout_2.addWidget(self.board_2_lb)
        self.board2_lw = QtWidgets.QListWidget(self.widget)
        self.board2_lw.setObjectName("board2_lw")
        self.verticalLayout_2.addWidget(self.board2_lw)
        self.b2_id_pb = QtWidgets.QPushButton(self.widget)
        self.b2_id_pb.setObjectName("b2_id_pb")
        self.verticalLayout_2.addWidget(self.b2_id_pb)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.selectBoard_pb = QtWidgets.QPushButton(self.widget)
        self.selectBoard_pb.setObjectName("selectBoard_pb")
        self.verticalLayout_3.addWidget(self.selectBoard_pb)
        board_selector_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(board_selector_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        board_selector_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(board_selector_window)
        self.statusbar.setObjectName("statusbar")
        board_selector_window.setStatusBar(self.statusbar)

        self.retranslateUi(board_selector_window)
        QtCore.QMetaObject.connectSlotsByName(board_selector_window)

    def retranslateUi(self, board_selector_window):
        _translate = QtCore.QCoreApplication.translate
        board_selector_window.setWindowTitle(_translate("board_selector_window", "MainWindow"))
        self.label.setText(_translate("board_selector_window", "Board 1"))
        self.b1_id_pb.setText(_translate("board_selector_window", "ID B1"))
        self.board_2_lb.setText(_translate("board_selector_window", "Board 2"))
        self.b2_id_pb.setText(_translate("board_selector_window", "ID B2"))
        self.selectBoard_pb.setText(_translate("board_selector_window", "Select board"))
