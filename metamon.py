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
        self.login_data = {"address": self.address,"msg": self.msg, "sign": self.sign}
        self.checkBag_data = self.address_data
        self.getWalletPropertyList_data = {"address": address, "page": "1", "pageSize": "100"}
        self.composeMonsterEgg_data = self.address_data
        self.startBattle_data = {"address": address, "battleLevel": "1", "monsterA": "", "monsterB": "883061"} #"442383" "214650"
        self.openMonsterEgg_data = self.address_data
        self.updateMonster_data = {"nftId": "394090", "address": self.address}
    
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
        self.headers["accesstoken"] = res["data"]

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
        page = 1
        while 1:
            self.getWalletPropertyList_data["page"] = str(page)
            res = json.loads(self.s.post(getWalletPropertyList_url, data=self.getWalletPropertyList_data, headers=self.headers).text)
            if res["data"]["metamonList"]:
                self.metamon_list += res["data"]["metamonList"]
                page += 1
            else:
                break 
    
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
        if res["code"] == "SUCCESS":
            print("Compose sucess")
        else:
            print("Compose fail")

    def openMonsterEgg(self, number=100000):
        self.checkBag()
        t = {"Potion":0, "YDiamond":0, "PDiamond":0, "N":0, "R":0, "SR":0, "SSR":0}
        if number > self.egg:
            number = self.egg
        for i in range(number):
            res = json.loads(self.s.post(openMonsterEgg_url, data=self.openMonsterEgg_data, headers=self.headers).text)
            if res["code"] == "SUCCESS":
                if res["data"]["category"] == "Metamon":
                    t[res["data"]["rarity"]] += 1
                    print("open", res["data"]["rarity"], res["data"]["category"], res["data"]["tokenId"])
                else:
                    if res["data"]["category"] == "Potion":
                        t["Potion"] += 2
                    else:
                        t[res["data"]["category"]] += 1
                    print("open", res["data"]["amount"], res["data"]["category"])
            else:
                print("Open egg failed")
            # time.sleep(2*random.random())
        print("Totally opened", str(number), "eggs:",str(t["Potion"]),"Potion;",str(t["YDiamond"]),"YDiamond;",str(t["PDiamond"]),"PDiamond;",str(t["N"]),"N;",str(t["R"]),"R;",str(t["SR"]),"SR;",str(t["SSR"]),"SSR;")

    def updateMonster(self, monster):
        self.checkBag()
        self.updateMonster_data["nftId"] = monster["id"]
        if self.materials[monster["rarity"]] >= 1:
            res = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
            if res["code"] == "SUCCESS":
                self.materials[monster["rarity"]] -= 1
                print(monster["id"], monster["rarity"], "Metamon update to level", str(monster["level"]+1)+"!")
            else:
                print("Update failed. Materials is not enough.")

    def startBattle(self, update=1, sleep_time=2):
        for monster in self.metamon_list:
            id = monster["id"]
            exp = monster["exp"]
            exp_max = monster["expMax"]
            tear = monster["tear"]
            rarity = monster["rarity"]
            level = monster["level"]
            self.startBattle_data["battleLevel"] = level//21+1
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
                    if res["data"]["challengeResult"] == True:
                        win += 1
                    if res["data"]["challengeResult"] == False:
                        lose += 1
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
                else:
                    exp = 0
            if battle != 0:
                print(id, rarity, "Metamon battled:", str(battle)+"; ", "Win:", str(win)+"; ", "Lose:", str(lose)+";", "Win rate:", str(round(win/battle*100, 2))+"%;")
                time.sleep(sleep_time)

if __name__ == "__main__":
    my_address = "" # Your wallet address
    my_sign = "" # Your sign
    my_msg = ""  # Your msg
    my_metamon = metamon(address=my_address, sign=my_sign, msg=my_msg)
    # my_metamon.set_local_time("06:00")    # You can set a loacl time which scrypt will run. The time format is "xx:xx", hour and minute
    # my_metamon.set_utc_time("22:00")    # You can also set a utc time which scrypt will run. The time format is "xx:xx", hour and minute
    my_metamon.login()
    my_metamon.getWalletPropertyList()
    my_metamon.checkBag()
    my_metamon.startBattle(update=1, sleep_time=2)    #Auto-battle, if the exp is full, it will automatically level up. If you don't want to level up, set update=-1
    my_metamon.composeMonsterEgg() # You can change the number, the default is max number which you can compose.
    my_metamon.openMonsterEgg(number=0) # You can change the number, the default is max number which you can compose. Uncomment will unlock the opening eggs function.
    my_metamon.check()
