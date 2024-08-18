import glob
import os
import threading
import time
import argparse
from controller import controller

mqtt_init_done = threading.Event()
mqtt_result_done = threading.Event()

def forever(directory, cmd) :
    if args.cmd is not None:
        run(os.path.join(directory, "mqtt.json"), os.path.join(directory, cmd + ".json"))
    else:
        json_files = glob.glob(os.path.join(directory, '*.json'))
        for file in json_files:
            if os.path.basename(file) != "mqtt.json":
                run(os.path.join(directory, "mqtt.json"), file)

def run(mqttFn, stubfn):
    try:
        ctrlInst = controller(mqttFn, stubfn, mqtt_init_done, mqtt_result_done)
    except ValueError as e:    
        print("param error, test failed")    

    # 等待初始化结束
    mqtt_init_done.wait()
    # 执行cmd
    ctrlInst.execute()

    ret = mqtt_result_done.wait(timeout=300)
    ctrlInst.teardown(ret)

def main(args):   
    forever(args.dir, args.cmd)    

if __name__ == "__main__":   
    parser = argparse.ArgumentParser(description="gen3 test scrpt") 
    parser.add_argument('--dir', nargs='?', help="config file dir", required=True)
    parser.add_argument('--cmd', nargs='?', help="command", required=False)
    args = parser.parse_args()

    main(args)    

