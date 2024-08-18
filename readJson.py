import json

class readJson: 
    def __init__(self, stubfn):     
        with open(stubfn, 'r') as file:
            self.stubInfo = json.load(file)        

    # 获取对应stub的 sub信息,返回数组或None
    def getTopic_sub(self, model) :
        if "sub" in self.stubInfo[model]:
            return self.stubInfo[model]["sub"]
        else: 
            return None
        
    # 获取对应stub的 pub信息,返回数组或None    
    def getTopic_pub(self, model) :
        if "pub" in self.stubInfo[model]:
            return self.stubInfo[model]["pub"]
        else:
            return None
    # 期待结果
    def expect_result(self, model) : 
        return self.stubInfo[model]["status"]
    
def getMqttCfg(path) :
    with open(path, 'r') as file:
        data = json.load(file)   
        return data["mqtt"]
    return None      
    
