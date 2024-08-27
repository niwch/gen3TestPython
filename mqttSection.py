import paho.mqtt.client as mqtt

from readJson import getMqttCfg

class mqttSection:
    def __init__(self, mqttFn, on_connectCB, on_messageCB):  
        
        # 链接mqtt网关
        mqttJson = getMqttCfg(mqttFn)
        if mqttJson is not None:
            self.client = mqtt.Client(client_id=mqttJson["clientid"], clean_session=True)
            # 设置回调函数
            self.client.on_connect = on_connectCB
            self.client.on_message = on_messageCB
            ret = self.client.connect(mqttJson["address"], mqttJson["port"], 60)
            print(ret)
        else:
            raise ValueError("mqtt config param error")

    def disconnect(self):
        print("close mqtt connect")
        self.client.disconnect()    

    # 链接状态
    def is_connected(self) :
        return self.client.is_connected()
       
    # 订阅
    def subscribe(self, topic) :
        print("subscribe {}".format(topic))
        self.client.subscribe(topic)
        
    # 发布消息
    def publish(self, topic, msg) : 
        print("publish topic[{}] message[{}]".format(topic, msg))
        self.client.publish(topic, msg)

    # 定义一个函数来启动 MQTT 客户端
    def start_mqtt_client(self):
        self.client.loop_forever()
    
    def stop_mqtt_client(self) :
        self.client.loop_stop(force=True)