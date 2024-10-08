# gen3TestPython
测试工具
linux环境，需要支持python3

## 安装
```
pip install paho-mqtt

(optioal)
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients

```

## 启动
配置文件中每一个json代表一个测试用例
```
python3 ./main.py --dir=$PATH --cmd=$cmd
// PATH: 配置文件路径
// cmd: 配置文件路径中的某一个json文件前缀，可选，不填写cmd默认全部测试

eg: python3 ./main.py --dir=$HOME/gen3TestPython/config                         // 测试配置路径下的所有用例
eg: python3 ./main.py --dir=$HOME/gen3TestPython/config --cmd=doorlockcontrol   // 测试配置路径下的doorlockcontrol用例
```

## 自测命令
``` txt
// 订阅
mosquitto_sub -h broker.emqx.io -p 1883 -t SIF_SSPF_WakeupRequest -t SendSignalResult -t GetRawSignalResult -t VSP_Step -t VSP_RemoteControlEvent -t VSP_ReportControlResult -t VSP_UploadCarStatus

// 发布
1. 模拟vsp 向车端发送控车报文 VSP_RemoteControlEvent ，为了获取控车指令的request ID
mosquitto_pub -h broker.emqx.io -p 1883 -t VSP_RemoteControlEvent -m '{"time":1721181600,"messagetype":"1101","cmd":{"requestId":"1234","remoteKey":"doorlockcontrol","operation":"1"}}' 

2. 模拟车端回复 VSP_ReportControlResult 控车结果报文
mosquitto_pub -h broker.emqx.io -p 1883 -t VSP_ReportControlResult -m '{"cmdtime":1721181600,"requestid":"1234","result":0,"failmessage":"","errorcode":0,"msgid":0,"msgidtoack":0}'

3. 模拟车端回复 VSP_UploadCarStatus 车辆状态报文
mosquitto_pub -h broker.emqx.io -p 1883 -t VSP_UploadCarStatus -m '{"time":1721181600,"requestid":"1234","business":"0","status":{"doorlockstatus":"0"}}'
```