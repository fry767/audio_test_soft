from cgi import test
from statistics import mean
from audio_test_bench.AudioAnalyzer.audio_analyzer import AudioAnalyzer
from data_recorder import DataWriterSQLite
from data_recorder import DataReaderSQLite
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)
from datetime import datetime
import os
import time
import sys
import tkinter
from tkinter import filedialog
import numpy as np
import json

def search_for_file_path ():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

# Add AudioAnalyzer/src to PYTHONPATH
lib_path = os.path.abspath(os.path.join('audio_test_bench','AudioAnalyzer'))
sys.path.append(lib_path)
import audio_analyzer as analyzer
test_margin = 2 #1s


# Ask user to select dir
file_path_variable = search_for_file_path()

analyzer_rec = AudioAnalyzer()
record = analyzer_rec.read_audio_file(file_path_variable + '/audio.wav')
analyzer_rec.analyze_audio(record)
plt.plot(record['sinad left'])
db_name = file_path_variable + "/audioB1TX"  # Create database in RAM
db_nameB2 = file_path_variable + "/audioB2TX"  # Create database in RAM
reader_instance = DataReaderSQLite(db_name)
reader_instanceB2 = DataReaderSQLite(db_nameB2)
elapse_time = reader_instance.read('audioB1', 'elapsed_time_ms')
time_idx = 0
db_glitch_start = []
db_glitch_end = []
glitch_started = False
for i in range(len(record['glitch left']['start'])):
    glitch_start_time = record['glitch left']['start'][i] - test_margin
    glitch_end = record['glitch left']['end'][i] + test_margin
    for i in range(len(elapse_time) - 1):
        if elapse_time[i]/1000 >= glitch_start_time and not glitch_started:
            db_glitch_start.append(i)
            glitch_started = True
        elif elapse_time[i]/1000 >= glitch_end and glitch_started:
            db_glitch_end.append(i)
            glitch_started = False
            break

input_data = read(file_path_variable + '/audio.wav')

audio = input_data[1]
exit = False
res = reader_instance.description()
res1 = reader_instanceB2.description()
value  = 0
value1 = 0
value2 = 0
while exit == False:
    for x in range(len(res['audioB1'])):
        print(x, res['audioB1'][x])
    user_input = input('Enter stats idx for B1, or exit to quit')
    if (user_input == "exit"):
        exit = True
    else:
        value = int(user_input)

    for x in range(len(res1['audioB2'])):
        print(x, res1['audioB2'][x])
    user_input = input('Enter stats idx for B2, or exit to quit')
    if (user_input == "exit"):
        exit = True
    else:
        value1 = int(user_input)
    user_input = input('Enter stats idx for B2, or exit to quit')
    if (user_input == "exit"):
        exit = True
    else:
        value2 = int(user_input)
    stats_to_plot_b1 = reader_instance.read('audioB1', res['audioB1'][value])
    stats_to_plot_b2 = reader_instanceB2.read('audioB2', res1['audioB2'][value1])
    stats_to_plot_b3 = reader_instanceB2.read('audioB2', res1['audioB2'][value2])
    for i in range(len(db_glitch_start)):
        fig, ax = plt.subplots()
        fig.clear(True)

        plt.subplot(4, 1, 1)
        plt.gca().set_title(res['audioB1'][value])
        plt.plot(elapse_time[db_glitch_start[i] : db_glitch_end[i]], stats_to_plot_b1[db_glitch_start[i] : db_glitch_end[i]])

        plt.subplot(4, 1, 2)
        plt.gca().set_title(res1['audioB2'][value1])
        plt.plot(elapse_time[db_glitch_start[i] : db_glitch_end[i]], stats_to_plot_b2[db_glitch_start[i] : db_glitch_end[i]])

        plt.subplot(4, 1, 3)
        plt.gca().set_title(res1['audioB2'][value2])
        plt.plot(elapse_time[db_glitch_start[i] : db_glitch_end[i]], stats_to_plot_b3[db_glitch_start[i] : db_glitch_end[i]])

        plt.subplot(4, 1, 4)
        plt.gca().set_title('audio glitch')
        start = int((record['glitch left']['start'][i]) * 44100)
        end   = int((record['glitch left']['end'][i]) * 44100)
        x = []
        for j in range(end - start):
            x.append(int(start/44100) + j * 1/44100)
        plt.plot(x, audio[start : end])
        plt.show()
        input('press return to continue')
