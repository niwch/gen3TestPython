# gen3TestPython
测试工具

## 安装
```
pip install paho-mqtt

(optioal)
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients

```

## 测试命令
``` txt
// 订阅
mosquitto_sub -h broker.emqx.io -p 1883 -t SIF_SSPF_WakeupRequest -t SendSignalResult -t GetRawSignalResult -t VSP_Step -t VSP_RemoteControlEvent -t VSP_ReportControlResult -t VSP_UploadCarStatus

// 发布
1. 模拟vsp 向车端发送控车报文 VSP_RemoteControlEvent ，为了获取控车指令的request ID
mosquitto_pub -h broker.emqx.io -p 1883 -t VSP_RemoteControlEvent -m "{"time":1721181600,"messagetype":"1101","cmd":{"requestId":"1234","remoteKe":"doorlockcontrol","operation":"1"}}" 

2. 模拟车端回复 VSP_ReportControlResult 控车结果报文

3. 模拟车端回复 VSP_UploadCarStatus 车辆状态报文

```