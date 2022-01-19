from cgi import test
from concurrent.futures import process
from statistics import mean
from audio_test_bench.AudioAnalyzer.audio_analyzer import AudioAnalyzer
from spark_cli import SparkCLI
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
from datetime import datetime

# Add AudioAnalyzer/src to PYTHONPATH
lib_path = os.path.abspath(os.path.join('audio_test_bench','AudioAnalyzer'))
sys.path.append(lib_path)
import audio_analyzer as analyzer
test_margin = 1 #1s


# create filename
path = "test_result"
os.makedirs(path, exist_ok=True)
now = datetime.now()
now_dir = now.strftime("%d-%m-%Y_%H_%M_%S")
path = os.path.join(path, now_dir)
os.makedirs(path, exist_ok=True)
b1_db_name = path + "/audioB1TX"
b2_db_name = path + "/audioB2TX"
recording_name = path + "/audio.wav"
capture_name = path + "/wav_result.png"
# Create database
writer_instance = DataWriterSQLite(b1_db_name)
writer_instanceB2 = DataWriterSQLite(b2_db_name)

#duo
cliB1 = SparkCLI('207D38A35056','../spark-dev/app/demo/common/protocol/src/proto/')
cliB2 = SparkCLI('207538A35056','../spark-dev/app/demo/common/protocol/src/proto/')
#evk
#cliB1 = SparkCLI('205A33A5484E','../spark-dev/app/demo/common/protocol/src/proto/')
#cliB2 = SparkCLI('2082338E484E','../spark-dev/app/demo/common/protocol/src/proto/')

cliB1.connect()
cliB2.connect()

print("Connected to both audio board, launching audio ...")
audioB1 = cliB1.launch_audio()
audioB2 = cliB2.launch_audio()
audioB1.set_cfg_file("board1_unidir")
audioB2.set_cfg_file("board2_unidir")
audioB1.start()
audioB2.start()
time.sleep(1)
print("Audio launch on both board, initializing DB ...")
audioB1.wps.reset_stats()
audioB2.wps.reset_stats()
statsB1, wps = audioB1.get_stats()
statsB2, wpsB2 = audioB2.get_stats()
# Create table
table_name = "audioB1"
table_nameB2 = "audioB2"
statsB1, wps = audioB1.get_stats()
statsB2, wpsB2 = audioB2.get_stats()
statsB1.update(wps)
statsB2.update(wpsB2)
writer_instance.create_table(table_name, statsB1)
writer_instanceB2.create_table(table_nameB2, statsB2)

input('DB initialized, starting recording, press enter to start ...')
fs = 44100  # Sample rate
seconds = 900  # Duration of recording
x = sd.query_devices()
sd.default.device = 'HD-Audio Generic: ALC1220 Analog (hw:1,0)'
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)

audioB1.wps.reset_stats()
audioB2.wps.reset_stats()
audioB1.get_stats()
audioB1.get_stats()
audioB2.get_stats()
audioB2.get_stats()
process_start = 0
process_dur = 0
for i in range(seconds * 5):
    if (0.2 - process_dur > 0):
        time.sleep(0.2 - process_dur)
    process_start = datetime.timestamp(datetime.now())
    statsB1, wps = audioB1.get_stats()
    statsB1.update(wps)
    statsB2, wpsB2 = audioB2.get_stats()
    statsB2.update(wpsB2)
    writer_instance.insert(table_name, statsB1)
    writer_instanceB2.insert(table_nameB2, statsB2)
    print(((i) / (seconds * 5)) * 100, '%')
    process_dur = datetime.timestamp(datetime.now()) - process_start


sd.wait()  # Wait until recording is finished
write(recording_name, fs, myrecording)  # Save as WAV file
print("Recording finished, starting analyzer ...")

analyzer_rec = AudioAnalyzer()
record = analyzer_rec.read_audio_file(recording_name)
analyzer_rec.analyze_audio(record)
print("Analyzer finished")

reader_instance = DataReaderSQLite(b1_db_name)
reader_instanceB2 = DataReaderSQLite(b2_db_name)
elapse_time = reader_instance.read(table_name, 'elapsed_time_ms')
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

input_data = read(recording_name)

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
