# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'audio_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from sqlite3 import connect
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from cgi import test
from statistics import mean
from audio_test_bench.AudioAnalyzer.audio_analyzer import AudioAnalyzer
from spark_cli import SparkCLI
from data_recorder import DataWriterSQLite
from data_recorder import DataReaderSQLite
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import interactive
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from datetime import datetime
import os
import time
import sys
from datetime import datetime
from spark_cli.spark_cli_app import SparkCliApp
from audio_test_ui import Ui_MainWindow
import numpy as np
import mplcursors
import json
from board_ui import Ui_board_selector_window
import board

# Add AudioAnalyzer/src to PYTHONPATH
lib_path = os.path.abspath(os.path.join('../audio_test_bench', 'AudioAnalyzer'))
sys.path.append(lib_path)
import audio_analyzer as analyzer

table_name   = "audioB1"
table_nameB2 = "audioB2"
table_abs_time = "absTime"
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes_array = []
        #self.axes  = fig.add_subplot(311)
        #self.axes1 = fig.add_subplot(312)
        #self.axes2 = fig.add_subplot(313)
        fig.set_tight_layout(True)
        self.size = fig.get_size_inches()
        self.dpi = dpi
        self.figure = fig
        super(MplCanvas, self).__init__(self.figure)

    def reload_figure(self, subplot_num) :
        self.axes_array = []
        self.figure.clear(True)
        for i in range(subplot_num):
            self.axes_array.append(self.figure.add_subplot(subplot_num,1, i + 1))
        self.figure.set_tight_layout(True)
        self.size = self.figure.get_size_inches()

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    working_dir = 0
    working_test_path = 0
    analyzer_rec = AudioAnalyzer()
    record = {}
    board1_available_stats = {}
    board2_available_stats = {}
    db_glitch_start = []
    db_glitch_end = []
    elapse_time_ms = 0
    g1_title = "first"
    g2_title = "second"
    g3_title = "third"
    audioB1 = 0
    audioB2 = 0
    writer_instance = 0
    writer_instanceB2 = 0
    recording_name = 0
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.x1 = []
        self.x2 = []
        self.x3 = []
        self.y1 = dict()
        self.y1['data'] = []
        self.y1['name'] = []
        self.y2 = dict()
        self.y2['data'] = []
        self.y2['name'] = []
        self.y3 = []
        self.sinad = []
        self.sinadyZoom = []
        self.sinadx = []
        self.sinadxZoom = []
        self.no_audio = False
        #Board window
        self.new_window = QtWidgets.QMainWindow()
        self.board_ui = Ui_board_selector_window()
        self.board_ui.setupUi(self.new_window)
        self.board_ui_available_board = []
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)
        layoutToolbar = QtWidgets.QVBoxLayout()
        layoutToolbar.addWidget(toolbar)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.plot_wid.setLayout(layoutToolbar)
        #self.scrollAreaWidgetContents.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.scrollAreaWidgetContents.resize(1400,400)
        self.scrollAreaWidgetContents.setLayout(layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.show()
        self._update_plot()

        self.select_folder_pb.clicked.connect(self.select_folder)
        self.analyze_pb.clicked.connect(self.analyze_audio)
        self.load_db_pb.clicked.connect(self.load_board_db_field)
        self.test_pb.clicked.connect(self.plot_data)
        self.Connect_pb.clicked.connect(self.connect_to_board)
        self.start_test_pb.clicked.connect(self.start_test)
        self.test_dur_le.setText('15')
        self.test_progb.setValue(0)
        self.analyze_slider.valueChanged.connect(self.slider_update)
        self.analyze_slider.setValue(5)
        self.clear_all_b1_pb.clicked.connect(self.clear_all_b1)
        self.clear_all_b2_pb.clicked.connect(self.clear_all_b2)

        self.board_selector_pb.clicked.connect(self._open_board_window)
        self.board_ui.b1_id_pb.clicked.connect(self._board_window_id_board1)
        self.board_ui.b2_id_pb.clicked.connect(self._board_window_id_board2)
    def select_folder (self):
        dialog = QFileDialog(self)
        self.working_dir = dialog.getExistingDirectory(self, 'Choose test output folder', os.getcwd())
        self.log_te.append("Folder properly loaded !")
        #Check DB data number
        elapse_timeB1 = self._load_b1_db().read(table_name, 'elapsed_time_ms')
        elapse_timeB2 = self._load_b2_db().read(table_nameB2, 'elapsed_time_ms')
        if len(elapse_timeB1) != len(elapse_timeB2):
            self.log_te.append("Invalid stats input, length dont match")
        # TODO only one elapse time, could get one for both board
        self.elapse_time_ms = elapse_timeB1
    def analyze_audio(self):
        if os.path.exists(self.working_dir + '/audio.wav'):
            self.record = self.analyzer_rec.read_audio_file(self.working_dir + '/audio.wav')
            self.analyzer_rec.analyze_audio(self.record, self.analyze_slider.value())
            self.log_te.append("Analysis finished, starting glitch extraction")
            elapse_time = self.elapse_time_ms
            test_margin = 1 # 1second
            glitch_started = False
            glitch_details = []
            for i in range(len(self.record['glitch left']['start'])):
                glitch_start_time = self.record['glitch left']['start'][i] - test_margin
                glitch_end = self.record['glitch left']['end'][i] + test_margin
                for i in range(len(elapse_time) - 1):
                    if elapse_time[i]/1000 >= glitch_start_time and not glitch_started:
                        self.db_glitch_start.append(i)
                        glitch_started = True
                    elif elapse_time[i]/1000 >= glitch_end and glitch_started:
                        self.db_glitch_end.append(i)
                        glitch_started = False
                        glitch_details.append(str(glitch_end - glitch_start_time))
                        break
            self.glitch_cb.clear()
            self.glitch_cb.addItems(glitch_details)
            self.glitch_cb.setCurrentIndex(0)
            self.g1_title = "Audio SINAD"
            self._clear_axis()
            input_data = read(self.working_dir + '/audio.wav')
            audio = input_data[1]
            test_duration_length = len(audio)/44100
            step = int((test_duration_length / len(self.record['sinad left'])) * 1000)
            self.sinadx = []
            for i in range(len(self.record['sinad left'])):
                self.sinadx.append(i * step)
            self.sinad = self.record['sinad left']
            self.sinadxZoom = self.sinadx
            self.sinadyZoom = self.sinad
            self._update_plot()
        else:
            self.no_audio = True
            self.log_te.append("Cant find audio.wav files")
    def load_board_db_field(self):
        # Clear list widget of previously loaded DB
        while self.b1_stats_lw.count() > 0 :
            self.b1_stats_lw.takeItem(0)

        while self.b2_stats_lw.count() > 0 :
            self.b2_stats_lw.takeItem(0)

        self.board1_available_stats = self._load_b1_db().description()
        self.board2_available_stats = self._load_b2_db().description()
        for i in range(len(self.board1_available_stats[table_name])):
           item = QtWidgets.QListWidgetItem()
           item.setText(self.board1_available_stats[table_name][i])
           item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
           item.setCheckState(QtCore.Qt.Unchecked)
           self.b1_stats_lw.addItem(item)
        for i in range(len(self.board2_available_stats[table_nameB2])):
           item = QtWidgets.QListWidgetItem()
           item.setText(self.board2_available_stats[table_nameB2][i])
           item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
           item.setCheckState(QtCore.Qt.Unchecked)
           self.b2_stats_lw.addItem(item)

    def plot_data(self):
        glitch_windows_start = 0
        glitch_windows_stop  = 0
        if os.path.exists(self.working_dir + '/audio.wav'):
            self.no_audio = False
        else:
            self.no_audio = True

        if not self.no_audio:
            input_data = read(self.working_dir + '/audio.wav')
            audio = input_data[1]
        custom_window_started = False
        bypass_glitch_window  = False
        if self.show_bet_cb.isChecked() :
            #bypass glitch windows
            if self.show_from_le.text() != "" and self.show_to_le.text() != "":
                bypass_glitch_window = True
                for i in range(len(self.elapse_time_ms) - 1):
                    if self.elapse_time_ms[i]/1000 >= int(self.show_from_le.text()) and not custom_window_started:
                        glitch_windows_start = i
                        custom_window_started = True
                    elif self.elapse_time_ms[i]/1000 >= int(self.show_to_le.text()) and custom_window_started:
                        glitch_windows_stop = i
                        custom_window_started = False
                        break
        #no audio available, simply plot stat for the entire map if show_bet is not use
        elif self.no_audio:
            glitch_windows_start = 0
            #dummy read one row of the stats to check how much available to plot
            stats_to_plot_b1 = self._load_b1_db().read(table_name, self.board1_available_stats[table_name][0])
            glitch_windows_stop  = len(stats_to_plot_b1)
        else:
            glitch_windows_start = self.db_glitch_start[self.glitch_cb.currentIndex()]
            glitch_windows_stop  = self.db_glitch_end[self.glitch_cb.currentIndex()]
        self.g1_title = 'TX board'
        self.g2_title = 'RX board'
        self.g3_title = "Audio glitch"
        self._clear_axis()
        for i in range(self.b1_stats_lw.count()):
            item = self.b1_stats_lw.item(i)
            if item.checkState():
                stats_to_plot_b1 = self._load_b1_db().read(table_name, self.board1_available_stats[table_name][i])
                self.y1['data'].append(stats_to_plot_b1[glitch_windows_start : glitch_windows_stop])
                self.y1['name'].append(self.board1_available_stats[table_name][i])
        self.x1 = self.elapse_time_ms[glitch_windows_start : glitch_windows_stop]

        for i in range(self.b2_stats_lw.count()):
            item = self.b2_stats_lw.item(i)
            if item.checkState():
                stats_to_plot_b2 = self._load_b2_db().read(table_nameB2, self.board2_available_stats[table_nameB2][i])
                self.y2['data'].append(stats_to_plot_b2[glitch_windows_start : glitch_windows_stop])
                self.y2['name'].append(self.board2_available_stats[table_nameB2][i])
        self.x2 = self.x1

        # Compute audio X axis
        if not self.no_audio:
            x_axis_audio = []
            if len(self.record['glitch left']['start']) > 0:
                start = int((self.record['glitch left']['start'][self.glitch_cb.currentIndex()]) * 44100)
                end   = int((self.record['glitch left']['end'][self.glitch_cb.currentIndex()]) * 44100)
                for j in range(end - start):
                    x_axis_audio.append((int(start/44100) + j * 1/44100) * 1000)

            self.x3 = x_axis_audio
            self.y3 = audio[start : end]

            if bypass_glitch_window:
                self.sinadxZoom = []
                self.sinadyZoom = []
                windows_fetch = False
                start = int(int(self.show_from_le.text()) * 1000)
                end = int(int(self.show_to_le.text()) * 1000)
                window_start = 0
                window_stop = 0
                for i in range(len(self.sinadx)):
                    if (self.sinadx[i] >= start and windows_fetch == False):
                        window_start = i
                        windows_fetch = True
                    elif (self.sinadx[i] >= end and windows_fetch):
                        windows_fetch = False
                        window_stop = i
                        break
                self.sinadxZoom = self.sinadx[window_start : window_stop]
                self.sinadyZoom = self.sinad[window_start : window_stop]

        self._update_plot()

    def connect_to_board(self):
        if self.duo_rb.isChecked() :
            #duo
            cliB1 = SparkCLI('207D38A35056','../spark-dev/app/demo/common/protocol/src/proto/')
            cliB2 = SparkCLI('207538A35056','../spark-dev/app/demo/common/protocol/src/proto/')
        else :
            cliB1 = SparkCLI('205A33A5484E','../spark-dev/app/demo/common/protocol/src/proto/')
            cliB2 = SparkCLI('2082338E484E','../spark-dev/app/demo/common/protocol/src/proto/')
        try :
            cliB1.connect()
        except TimeoutError as e:
            self.log_te.append("Cant connect to board 1, check if serial is not connected elsewhere")
            return
        try :
            cliB2.connect()
        except TimeoutError as e:
            self.log_te.append("Cant connect to board 1, check if serial is not connected elsewhere")
            return
        self.audioB1 = cliB1.launch_audio()
        self.audioB2 = cliB2.launch_audio()
        if self.duo_rb.isChecked() :
            self.audioB1.set_cfg_file("board1_unidir")
            self.audioB2.set_cfg_file("board2_unidir")
        else :
            self.audioB1.set_cfg_file("board1_256k")
            self.audioB2.set_cfg_file("board2_256k")
        self.audioB1.start()
        self.audioB2.start()
        self.log_te.append("Connected to boards")
        time.sleep(1)
        self.audioB1.wps.reset_stats()
        self.audioB2.wps.reset_stats()
        statsB1, wps = self.audioB1.get_stats()
        statsB2, wpsB2 = self.audioB2.get_stats()
        self._build_up_db(statsB1, wps, statsB2, wpsB2)
        self.log_te.append("DB build")

    def start_test(self):
        seconds = int(float(self.test_dur_le.text()) * 60)  # Duration of recording
        if (not self.no_audio_cb.isChecked()):
            fs = 44100  # Sample rate
            x = sd.query_devices()
            sd.default.device = 'HD-Audio Generic: ALC1220 Analog (hw:1,0)'
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        #Populate absolute time table in DB
        absolute_time = dict()
        absolute_time['time_0'] = datetime.timestamp(datetime.now())
        self.audioB1.wps.reset_stats()
        self.audioB2.wps.reset_stats()
        self.audioB1.get_stats()
        self.audioB1.get_stats()
        self.audioB2.get_stats()
        self.audioB2.get_stats()
        process_start = 0
        process_dur = 0
        for i in range(seconds * 5):
            if (0.2 - process_dur > 0):
                time.sleep(0.2 - process_dur)
            process_start = datetime.timestamp(datetime.now())
            statsB1, wps = self.audioB1.get_stats()
            statsB2, wpsB2 = self.audioB2.get_stats()
            self._update_db(statsB1, wps, statsB2, wpsB2)
            self.test_progb.setValue(int(((i) / (seconds * 5)) * 100))
            process_dur = datetime.timestamp(datetime.now()) - process_start

        if (not self.no_audio_cb.isChecked()):
            sd.wait()  # Wait until recording is finished
            write(self.recording_name, fs, myrecording)  # Save as WAV file
        self.writer_instance.insert(table_abs_time, absolute_time)
        self.writer_instanceB2.insert(table_abs_time, absolute_time)
        self._log_register_dump()
        time.sleep(1)
        self._log_board_cfg()
        time.sleep(1)
        self.log_te.append("Test finished !!!!!")
        self.test_progb.setValue(100)

    def slider_update(self):
        self.analysis_sens_te.setText(str(self.analyze_slider.value()))

    def clear_all_b1(self):
        for i in range(self.b1_stats_lw.count()):
            self.b1_stats_lw.item(i).setCheckState(QtCore.Qt.Unchecked)

    def clear_all_b2(self):
        for i in range(self.b2_stats_lw.count()):
            self.b2_stats_lw.item(i).setCheckState(QtCore.Qt.Unchecked)

    def _build_up_db(self, statsB1, wpsB1, statsB2, wpsB2):
        # create filename
        path         = "test_result"
        os.makedirs(path, exist_ok=True)
        now = datetime.now()
        now_dir = now.strftime("%d-%m-%Y_%H_%M_%S")
        custom_label = self.test_lb.text() + now_dir
        path = os.path.join(path, custom_label)
        os.makedirs(path, exist_ok=True)
        b1_db_name     = path + "/" + table_name
        b2_db_name     = path + "/" + table_nameB2
        self.recording_name = path + "/audio.wav"
        self.working_test_path = path
        # Create database
        self.writer_instance   = DataWriterSQLite(b1_db_name)
        self.writer_instanceB2 = DataWriterSQLite(b2_db_name)
        # Create table
        statsB1.update(wpsB1)
        statsB2.update(wpsB2)

        absolute_time = dict()
        absolute_time['time_0'] = []
        self.writer_instance.create_table(table_name, statsB1)
        self.writer_instance.create_table(table_abs_time, absolute_time)
        self.writer_instanceB2.create_table(table_nameB2, statsB2)
        self.writer_instanceB2.create_table(table_abs_time, absolute_time)

    def _update_db(self, statsB1, wpsB1, statsB2, wpsB2):
        statsB1.update(wpsB1)
        statsB2.update(wpsB2)
        self.writer_instance.insert(table_name, statsB1)
        self.writer_instanceB2.insert(table_nameB2, statsB2)
    def _load_b1_db(self) :
        if (os.path.exists(self.working_dir + "/audioB1TX")):
            db_name = self.working_dir + "/audioB1TX"  # Create database in RAM
            reader_instance = DataReaderSQLite(db_name)
        else:
            db_name = self.working_dir + "/" + table_name  # Create database in RAM
            reader_instance = DataReaderSQLite(db_name)
        return reader_instance

    def _load_b2_db(self):
        if (os.path.exists(self.working_dir + "/audioB2TX")):
            db_name = self.working_dir + "/audioB2TX"  # Create database in RAM
            reader_instance = DataReaderSQLite(db_name)
        else:
            db_name = self.working_dir + "/" + table_nameB2  # Create database in RAM
            reader_instance = DataReaderSQLite(db_name)
        return reader_instance

    def _update_plot(self):
        # Append 2 additionnal graph when audio is present, one for sinad, one for audio glitch
        graph_number = len(self.y1['data']) + len(self.y2['data'])
        if (not self.no_audio):
            graph_number += 2
        self.sc.reload_figure(graph_number)
        self.scrollAreaWidgetContents.resize(1400,200 * (len(self.sc.axes_array)))
        array_current_index = 0
        #audio available, plot sinad
        if (not self.no_audio):
            self.sc.axes_array[array_current_index].plot(self.sinadxZoom, self.sinadyZoom, label='sinad')
            self.sc.axes_array[array_current_index].legend()
            self.sc.axes_array[array_current_index].set_title('Audio SINAD')
            array_current_index += 1
            self.sinadxZoom = self.sinadx
            self.sinadyZoom = self.sinad
        for i in range(len(self.y1['data'])):
            self.sc.axes_array[array_current_index].plot(self.x1, self.y1['data'][i], label=self.y1['name'][i])
            self.sc.axes_array[array_current_index].legend()
            self.sc.axes_array[array_current_index].set_title(self.g1_title)
            mplcursors.cursor(self.sc.axes_array[array_current_index])
            array_current_index += 1

        for i in range(len(self.y2['data'])):
            self.sc.axes_array[array_current_index].plot(self.x1, self.y2['data'][i], label=self.y2['name'][i])
            self.sc.axes_array[array_current_index].legend()
            self.sc.axes_array[array_current_index].set_title(self.g2_title)
            mplcursors.cursor(self.sc.axes_array[array_current_index])
            array_current_index += 1

        if len(self.y3) > 0:
            self.sc.axes_array[array_current_index].plot(self.x3, self.y3, 'r')
            self.sc.axes_array[array_current_index].set_title(self.g3_title)
            mplcursors.cursor(self.sc.axes_array[array_current_index])

        # Trigger the canvas to update and redraw.
        self.sc.draw()

    def _clear_axis(self):
        self.x1 = []
        self.x2 = []
        self.x3 = []
        self.y1['data'] = []
        self.y2['data'] = []
        self.y1['name'] = []
        self.y2['name'] = []
        self.y3 = []

    def _log_register_dump(self):
        file = open(str(self.working_test_path) + '/reg_dumpB1.txt', 'w')
        file.write(self.audioB1.wps.dump_register())
        file.close()
        file = open(str(self.working_test_path) + '/reg_dumpB2.txt', 'w')
        file.write(self.audioB2.wps.dump_register())
        file.close()
    def _log_board_cfg(self):
        file = open(str(self.working_test_path) + '/cfg_B1.txt', 'w')
        file.write(json.dumps(self.audioB1.wps.get_config(), indent=4))
        file.close()
        file = open(str(self.working_test_path) + '/cfg_B2.txt', 'w')
        file.write(json.dumps(self.audioB2.wps.get_config(), indent=4))
        file.close()


    #### BOARD WINDOWS ####
    def _open_board_window(self):
        while self.board_ui.board_lw.count() > 0 :
            self.board_ui.board_lw.takeItem(0)
        while self.board_ui.board2_lw.count() > 0 :
            self.board_ui.board2_lw.takeItem(0)
        available_board = board.get_available_serial()
        for i in range(len(available_board)):
           item = QtWidgets.QListWidgetItem()
           item.setText(available_board[i])
           item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
           item.setCheckState(QtCore.Qt.Unchecked)
           self.board_ui.board_lw.addItem(item)
        for i in range(len(available_board)):
           item = QtWidgets.QListWidgetItem()
           item.setText(available_board[i])
           item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
           item.setCheckState(QtCore.Qt.Unchecked)
           self.board_ui.board2_lw.addItem(item)
        self.board_ui_available_board = available_board
        self.new_window.show()

    def _board_window_id_board1(self):

        lw = self.board_ui.board_lw
        for i in range(lw.count()):
            item = lw.item(i)
            if item.checkState():
                id_cli = SparkCLI(self.board_ui_available_board[i], '../spark-dev/app/demo/common/protocol/src/proto/')
                try :
                    id_cli.connect()
                except TimeoutError as e:
                    self.log_te.append("Cant connect to board, check if serial is not connected elsewhere")
                    return
                id_cli.init_id()
                break

    def _board_window_id_board2(self):

        lw = self.board_ui.board2_lw
        for i in range(lw.count()):
            item = lw.item(i)
            if item.checkState():
                id_cli = SparkCLI(self.board_ui_available_board[i], '../spark-dev/app/demo/common/protocol/src/proto/')
                try :
                    id_cli.connect()
                except TimeoutError as e:
                    self.log_te.append("Cant connect to board, check if serial is not connected elsewhere")
                    return
                id_cli.init_id()
                break
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
