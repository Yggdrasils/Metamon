import requests
import json
import time
import random
from datetime import datetime

api_url = "https://metamon-api.radiocaca.com/usm-api/"
login_url = api_url + "login"
checkBag_url = api_url + "checkBag"
getWalletPropertyList_url = api_url + "getWalletPropertyList"
composeMonsterEgg_url = api_url + "composeMonsterEgg"
startBattle_url = api_url + "startBattle"
openMonsterEgg_url = api_url + "openMonsterEgg"
updateMonster_url = api_url + "updateMonster"
expUpMonster_url = api_url + "expUpMonster"
addAttr_url = api_url + "addAttr"
sendLoginCode_url = api_url + "owner-setting/email/sendLoginCode"
verifyLoginCode_url = api_url + "owner-setting/email/verifyLoginCode"

buy_url = "https://metamon-api.radiocaca.com/usm-api/official-sale/buy"

class metamon(object):

    def __init__(self, address, sign, msg):
        self.address = address
        self.sign = sign
        self.msg = msg
        self.headers = {}

        self.s = requests.Session()

        self.raca = 0
        self.potion = 0
        self.ydiamond = 0
        self.pdiamond = 0
        self.fragment = 0
        self.egg = 0
        self.fee = 10
        self.metamon_list = []

        self.address_data = {"address": self.address}
        self.login_data = {"address": self.address,"msg": self.msg, "sign": self.sign, "network":1, "clientType": "MetaMask"}
        self.checkBag_data = self.address_data
        self.getWalletPropertyList_data = {"address": self.address, "orderType": "-1", "levelUp":0}
        self.composeMonsterEgg_data = self.address_data
        self.startBattle_data = {"address": self.address, "battleLevel": "1", "monsterA": "", "monsterB": "883061"} #"442383" "214650"
        self.openMonsterEgg_data = self.address_data
        self.updateMonster_data = {"nftId": "394090", "address": self.address}
        self.expUpMonster_data = {"address": self.address, "nftId":"0"}
        self.addAttr_data = {"nftId":"0", "attrType":"1"}
        self.buy_data = {"address": self.address, "orderId": 111}

    def set_local_time(self, local_time = "06:00"):
        self.local_hour, self.local_minute = [int(i) for i in local_time.split(":")]
        while 1:
            time_now = time.localtime(time.time())
            hour_now = time_now.tm_hour
            minute_now = time_now.tm_min
            if self.local_hour == hour_now and self.local_minute == minute_now:
                break
            else:
                time.sleep(50)

    def set_utc_time(self, utc_time = "22:00"):
        self.utc_hour, self.utc_minute = [int(i) for i in utc_time.split(":")]
        while 1:
            time_now = datetime.utcfromtimestamp(time.time())
            hour_now = time_now.hour
            minute_now = time_now.minute
            if self.utc_hour == hour_now and self.utc_minute == minute_now:
                break
            else:
                time.sleep(50)
    
    def login(self):
        res = json.loads(self.s.post(login_url, data=self.login_data).text)
        if res["code"] == "SUCCESS":
            self.headers["accesstoken"] = res["data"]["accessToken"]
            print("Login success")
        else:
            print("Login fail")

    def sendLoginCode(self):
        res = json.loads(self.s.post(sendLoginCode_url, data=self.address_data, headers=self.headers).text)
        if res["code"] == "SUCCESS":
            print("Send code success")
        else:
            print("Send code fail")

    def verifyLoginCode(self):
        code = input("Input verify code: ")
        verifyLoginCode_data = {**self.address_data, **{"code":code}}
        res = json.loads(self.s.post(verifyLoginCode_url, data=verifyLoginCode_data, headers=self.headers).text)
        if res["code"] == "SUCCESS":
            print("Verify success")
        else:
            print("Verify fail")
        
    def checkBag(self):
        res = json.loads(self.s.post(checkBag_url, data=self.checkBag_data, headers=self.headers).text)
        for item in res["data"]["item"]:
            if item["bpType"] == 1:
                self.fragment = int(item["bpNum"])
            if item["bpType"] == 2:
                self.potion = int(item["bpNum"])
            if item["bpType"] == 3:
                self.ydiamond = int(item["bpNum"])
            if item["bpType"] == 4:
                self.pdiamond = int(item["bpNum"])
            if item["bpType"] == 5:
                self.raca = int(item["bpNum"])
            if item["bpType"] == 6:
                self.egg = int(item["bpNum"])
        self.materials = {"N":self.potion, "R":self.ydiamond, "SR":self.pdiamond, "SSR":self.pdiamond}

    def getWalletPropertyList(self):
        self.metamon_list = []
        res = json.loads(self.s.post(getWalletPropertyList_url, data=self.getWalletPropertyList_data, headers=self.headers).text)
        if res["code"] == "SUCCESS":
            self.metamon_list += res["data"]["metamonList"]
        else:
            print("Acquire metamon fail")
    
    def check(self):
        self.checkBag()
        print("=================")
        print("RACA:", self.raca)
        print("Potion:", self.potion)
        print("YDiamond:", self.ydiamond)
        print("PDiamond:", self.pdiamond)
        print("Fragment:", self.fragment)
        print("Egg:", self.egg)
        print("Metamon:", len(self.metamon_list))
        print("=================")

    def composeMonsterEgg(self):
        self.checkBag()
        res = json.loads(self.s.post(composeMonsterEgg_url, data=self.composeMonsterEgg_data, headers=self.headers).text)
        print(res["message"])

    def openMonsterEgg(self, number=0, sleep_time=0):
        self.checkBag()
        if number > self.egg:
            number = self.egg
        t = {}
        s = "Totally opened " + str(number) + " eggs: "
        for i in range(number):
            res = json.loads(self.s.post(openMonsterEgg_url, data=self.openMonsterEgg_data, headers=self.headers).text)
            if res["code"] == "SUCCESS":
                if t.get(res["data"]["category"]) == None:
                    t[res["data"]["category"]] = res["data"]["amount"] + (res["data"]["amount"]==0)
                else:
                    t[res["data"]["category"]] += res["data"]["amount"] + (res["data"]["amount"]==0)
                print("open", res["data"]["amount"] + (res["data"]["amount"]==0), res["data"]["category"])
            else:
                print("Open egg failed")
            time.sleep(sleep_time)
        for key in t:
            s = s + str(t[key]) + " " + key + "; "
        print(s)

    def updateMonster(self, monster):
        self.checkBag()
        self.updateMonster_data["nftId"] = monster["id"]
        if self.materials[monster["rarity"]] >= 1:
            res = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
            if res["code"] == "SUCCESS":
                self.materials[monster["rarity"]] -= 1
                print(monster["id"], monster["rarity"], "Metamon update to level", str(monster["level"]+1)+"!")
            else:
                print(res["code"])

    def updateAll(self):
        for i in range(2):
            self.getWalletPropertyList()
            for monster in self.metamon_list:
                if monster["exp"] >= monster["expMax"]:
                    self.updateMonster(monster)
                else:
                    pass

    def expUpMonster(self, lvrange=[1,60], pnumber=2):
        for monster in self.metamon_list:
            if lvrange[0] <= monster["level"] <= lvrange[1]:
                self.expUpMonster_data["nftId"] = monster["id"]
                for i in range(pnumber):
                    res = json.loads(self.s.post(expUpMonster_url, data=self.expUpMonster_data, headers=self.headers).text)
                    if res["code"] == "SUCCESS":
                        print(monster["tokenId"], monster["rarity"], "metamon exp +", res["data"])
                    else:
                        print(res["message"])
            else:
                pass
        self.updateAll()

    def addAttr(self, lvrange=[1,60], scarange=[305,400], attrtype="luck"):
        attribute = {"luck":"1", "courage":"2", "wisdom":"3", "size":"4", "stealth":"5"}
        for monster in self.metamon_list:
            if lvrange[0] <= monster["level"] <= lvrange[1] and scarange[0]<= monster["sca"]<=scarange[1]:
                self.addAttr_data["nftId"] = monster["id"]
                self.addAttr_data["attrType"] = attribute[attrtype]
                res = json.loads(self.s.post(addAttr_url, params={"address":self.address}, data=self.addAttr_data, headers=self.headers).text)
                if res["code"] == "SUCCESS":
                    print(monster["tokenId"], monster["rarity"], "metamon", res["data"]["title"], res["data"]["upperMsg"], attrtype, "+", res["data"]["upperNum"])

    def startBattle(self, update=1, sleep_time=2):
        self.getWalletPropertyList()
        for monster in self.metamon_list:
            if monster["level"] <= 59:
                id = monster["id"]
                exp = monster["exp"]
                exp_max = monster["expMax"]
                tear = monster["tear"]
                rarity = monster["rarity"]
                self.startBattle_data["monsterA"] = id
                battle = 0
                win = 0
                lose = 0
                update_result = 1
                if update_result == 0:
                    break
                if self.raca < self.fee:
                        # print("RACA is not enough")
                        break
                while tear:
                    if self.raca < self.fee:
                        print("RACA is not enough")
                        break
                    res = json.loads(self.s.post(startBattle_url, data = self.startBattle_data, headers=self.headers).text)
                    if res["code"] == "SUCCESS":
                        battle += 1
                        win += res["data"]["challengeResult"]
                        lose += bool(1-res["data"]["challengeResult"])
                        exp += res["data"]["challengeExp"]
                        self.fragment += res["data"]["bpFragmentNum"]
                        self.raca -= self.fee
                        tear -= 1
                    else:
                        print(res)
                    if update == 1:
                        if exp >= exp_max:
                            self.updateMonster(monster)
                            exp = 0
                            if monster["level"] == 59:
                                break
                    else:
                        exp = 0
                if battle != 0:
                    print(id, rarity, "Metamon battled:", str(battle)+"; ", "Win:", str(win)+"; ", "Lose:", str(lose)+";", "Win rate:", str(round(win/battle*100, 2))+"%;")
                    time.sleep(sleep_time)

    def buy(self, number=20):
        for i in range(number):
            res = json.loads(self.s.post(buy_url, data = self.buy_data, headers=self.headers).text)
            print(res["code"])

if __name__ == "__main__":
    addr1 = "" 
    addr2 = ""
    addr = [addr1, addr2]

    sign1 = ""
    sign2 = ""
    sign = [sign1, sign2]

    msg1 = ""
    msg2 = ""
    msg = [msg1, msg2]
    
    # ?????????????????????????????????addr2, sign2, msg2??????
    # if you only have one account, you should delete addr2, sign2, msg2

    number = [100, 200]
    # ????????????
    # the number of eggs which you want to open
    
    authentication = 0
    # ???????????????????????????????????????????????????1???????????????0
    # two factor authentication, if you have opened 2FA, then set the value to 1, otherwise set it to 0

    for i in range(len(addr)):
        my_metamon = metamon(address=addr[i], sign=sign[i], msg=msg[i])
        # ?????????????????????????????????address_sign_msg.png
        # login params, refer to address_sign_msg.png

        # my_metamon.set_local_time("06:00")    
        # my_metamon.set_utc_time("22:00")
        # ??????????????????????????????????????????????????????UTC????????????????????????"xx:xx"???"??????:??????"
        # You can also set a utc time which scrypt will run. The time format is "xx:xx", hour and minute

        my_metamon.login()
        
        if authentication:
            my_metamon.sendLoginCode()
            my_metamon.verifyLoginCode()
            
        my_metamon.getWalletPropertyList()
        my_metamon.checkBag()
        
        my_metamon.buy(number=100)
        # ??????????????????number???????????????
        # buy purple potion, the number is how much you want to buy

        # my_metamon.expUpMonster(lvrange=[1,40], pnumber=2)
        # ?????????????????????????????????????????????????????????lvrange?????????????????????????????????????????????????????????????????????2???
        # Using potions to add exp, you can select the level range of metamon and number of potion, up to 2 potions.

        # my_metamon.addAttr(lvrange=[40,60], scarange=[305,400], attrtype="luck")
        # ?????????????????????????????????????????????????????????lvrange???????????????scarange????????????luck courage wisdom size stealth
        # Using potion to add attrbute, you can select the level range and sca range of metamon and attrbuties: luck courage wisdom size stealth

        my_metamon.startBattle(update=1, sleep_time=random.random())    
        # ?????????????????????????????????????????????????????????update=-1?????????????????????
        # Auto-battle, if the exp is full, it will automatically level up. If you don't want to level up, set update=-1
        
        my_metamon.composeMonsterEgg()
        # ???????????????
        # compose metamon eggs

        my_metamon.openMonsterEgg(number=number[i], sleep_time=0)
        # ????????????????????????????????????????????????????????????????????????????????????100000????????????????????????0??????????????????0
        # You can change the number and interval time, the default number is zero and default interval time is zero. If you want to open all eggs, you can set ni=umber=10000. Uncomment will unlock the opening eggs function.

        my_metamon.check()
