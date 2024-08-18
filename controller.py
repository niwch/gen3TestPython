import json
import threading
from mqttSection import mqttSection
from readJson import readJson
from enum import Enum

class assertionType(Enum):
    ControlResult = 1
    CarStatus = 2

class controller:
    def __init__(self, mqttFn, stubfn, mqtt_init_done, mqtt_result_done):
        # 创建json 实例
        self.jsonInst = readJson(stubfn)
        self.result = False
        self.status = False
        # 创建mqtt实例     
        try:   
            self.mqttInst = mqttSection(mqttFn, self.on_connect, self.on_message)  
            self.mqttThred = threading.Thread(target = self.mqttInst.start_mqtt_client)
            self.mqttThred.daemon = True  # 设置为守护线程
            self.mqttThred.start() 
            self.mqtt_init_done = mqtt_init_done
            self.mqtt_result_done = mqtt_result_done    
        except ValueError as e:    
            print(f"Error: {e}")
            raise  
        
        # 字典用于保存请求-应答的关系
        self.dict = {}
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        if str(rc) == "0":                        
            self.setup()
        self.mqtt_init_done.set()

    # 当接收到消息时的回调函数
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        
        vspStub = self.jsonInst.getTopic_sub("VSPStub")
        # vsp Stub发出的实际命令
        if len(vspStub) > 0 and msg.topic == vspStub[0]:
            # 将payload转json
            data = json.loads(msg.payload.decode('utf-8'))
            cmd = data["cmd"]["remoteKey"]
            if self.dict.get(cmd) != None:
                self.dict.pop(cmd)
                self.dict[data["cmd"]["requestId"]] = 0
                print("recv topic[{}] cmd[{}] requestId[{}]".format(vspStub[0], cmd, data["cmd"]["requestId"]))
        elif len(vspStub) > 1 and msg.topic == vspStub[1]:
            # 将payload转json
            data = json.loads(msg.payload.decode('utf-8'))
            reqId = data["requestid"]
            if self.dict.get(reqId) != None:
                self.result = self.assertion(assertionType.ControlResult, data)
                print("recv topic[{}] requestId[{}] result[{}]".format(vspStub[1], reqId, self.result))
        elif len(vspStub) > 2 and msg.topic == vspStub[2]:
            # 将payload转json
            data = json.loads(msg.payload.decode('utf-8'))
            reqId = data["requestid"]
            if self.dict.get(reqId) != None:
                self.status = self.assertion(assertionType.CarStatus, data)
                self.dict.pop(reqId)
                print("recv topic[{}] requestId[{}] status[{}]".format(vspStub[2], reqId, self.status))
                self.mqtt_result_done.set()
    
    def setup(self) :
        # vsp 订阅的topic
        vspSubTopic = self.jsonInst.getTopic_sub("VSPStub")
        print("is_connected {}".format(self.mqttInst.is_connected()))
        # 订阅主题
        for item in vspSubTopic:
            self.mqttInst.subscribe(item)

        # 发布 stub信息
        nmTopic = self.jsonInst.getTopic_pub("NMStub")
        for item in nmTopic:
            # print(item["topic"], item["message"])
            self.mqttInst.publish(item["topic"], json.dumps(item["message"]))

        S2STopic = self.jsonInst.getTopic_pub("S2SStub")
        for item in S2STopic:
            self.mqttInst.publish(item["topic"], json.dumps(item["message"]))
    
    def execute(self) :
        node = self.jsonInst.getTopic_pub("VSPStub")
        self.mqttInst.publish(node["topic"], json.dumps(node["message"]))
        cmd = node["message"]["cmd"]
        arg = node["message"]["arg"]
        print("execute cmd[{}] arg[{}]".format(cmd, arg))

        # 请求放入字典
        self.dict[cmd] = arg

    def assertion(self, type, jsonData):
        if assertionType.ControlResult == type:
            if "result" in jsonData and jsonData["result"] == 0:
                return True
        elif assertionType.CarStatus == type:
            if "status" in jsonData:
                print(jsonData["status"])
                print( self.jsonInst.expect_result("VSP_UploadCarStatus"))
                if jsonData["status"] == self.jsonInst.expect_result("VSP_UploadCarStatus"):
                    return True

        return False
        
    def teardown(self, ret):
        data = self.jsonInst.getTopic_pub("VSPStub")
        cmd = data["message"]["cmd"]
        arg = data["message"]["arg"]

        if ret == False:
            print("test cmd[{}] arg[{}] Timeout".format(cmd, arg))
        else: 
            suc = "test cmd[{}] arg[{}] Success".format(cmd, arg)
            fail = "test cmd[{}] arg[{}] Failed".format(cmd, arg)  
            vspStub = self.jsonInst.getTopic_sub("VSPStub")
            if len(vspStub) == 2: 
                if self.result == True:
                    print(suc)
                else:
                    print(fail)
            elif len(vspStub) == 3:
                if self.result == True and self.status == True:
                    print(suc)
                else:
                    print(fail)
