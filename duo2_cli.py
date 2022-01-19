from spark_cli import SparkCLI
import time

cli = SparkCLI('207538A35056','../spark-dev/app/demo/common/protocol/src/proto/')
cli.connect()
audio = cli.launch_audio()
audio.set_cfg_file("board2_unidir")
audio.start()

for i in range(20):
    time.sleep(1)
    print(audio.get_stats())
 
 
