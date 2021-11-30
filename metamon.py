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
        self.mintable_egg = 0
        self.metamon_list = []

        self.address_data = {"address": self.address}
        self.login_data = {"address": self.address,"msg": self.msg, "sign": self.sign}
        self.checkBag_data = self.address_data
        self.getWalletPropertyList_data = {"address": address, "page": "1", "pageSize": "100"}
        self.composeMonsterEgg_data = self.address_data
        self.startBattle_data = {"address": address, "battleLevel": "1", "monsterA": "", "monsterB": "454193"} #"442383" "214650"
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
        self.login_r = json.loads(self.s.post(login_url, data=self.login_data).text)
        self.headers["accesstoken"] = self.login_r["data"]

    def checkBag(self):
        self.checkBag_r = json.loads(self.s.post(checkBag_url, data=self.checkBag_data, headers=self.headers).text)
        for item in self.checkBag_r["data"]["item"]:
            if item["bpType"] == 1:
                self.fragment = item["bpNum"]
            if item["bpType"] == 2:
                self.potion = item["bpNum"]
            if item["bpType"] == 3:
                self.ydiamond = item["bpNum"]
            if item["bpType"] == 4:
                self.pdiamond = item["bpNum"]
            if item["bpType"] == 5:
                self.raca = item["bpNum"]
            if item["bpType"] == 6:
                self.egg = item["bpNum"]
        self.mintable_egg = self.fragment // 1000

    def getWalletPropertyList(self):
        self.metamon_list = []
        page = 1
        while 1:
            self.getWalletPropertyList_data["page"] = str(page)
            self.getWalletPropertyList_r = json.loads(self.s.post(getWalletPropertyList_url, data=self.getWalletPropertyList_data, headers=self.headers).text)
            if self.getWalletPropertyList_r["data"]["metamonList"]:
                self.metamon_list += self.getWalletPropertyList_r["data"]["metamonList"]
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
        print("Mintable Egg:", self.mintable_egg)
        print("Metamon:", len(self.metamon_list))
        print("=================")

    def composeMonsterEgg(self, number=100000):
        self.checkBag()
        compose_number = self.mintable_egg
        if number > compose_number:
            number = compose_number
        for i in range(number):
            self.s.post(composeMonsterEgg_url, data=self.composeMonsterEgg_data, headers=self.headers)
        print("Composed", str(number), "eggs")
        print("")

    def openMonsterEgg(self, number=100000):
        self.checkBag()
        t_potion = 0
        t_ydiamond = 0
        t_pdiamond = 0
        t_n = 0
        t_r = 0
        t_sr = 0
        t_ssr = 0
        if number > self.egg:
            number = self.egg
        for i in range(number):
            self.openMonsterEgg_r = json.loads(self.s.post(openMonsterEgg_url, data=self.openMonsterEgg_data, headers=self.headers).text)
            if self.openMonsterEgg_r["code"] == "SUCCESS":
                if self.openMonsterEgg_r["data"]["category"] == "Metamon":
                    if self.openMonsterEgg_r["data"]["rarity"] == "N":
                        t_n += 1
                    if self.openMonsterEgg_r["data"]["rarity"] == "R":
                        t_r += 1
                    if self.openMonsterEgg_r["data"]["rarity"] == "SR":
                        t_sr += 1
                    if self.openMonsterEgg_r["data"]["rarity"] == "SSR":
                        t_ssr += 1
                    print("open", self.openMonsterEgg_r["data"]["rarity"], self.openMonsterEgg_r["data"]["category"], self.openMonsterEgg_r["data"]["tokenId"])
                else:
                    if self.openMonsterEgg_r["data"]["category"] == "Potion":
                        t_potion += 2
                    if self.openMonsterEgg_r["data"]["category"] == "YDiamond":
                        t_ydiamond += 1
                    if self.openMonsterEgg_r["data"]["category"] == "PDiamond":
                        t_pdiamond += 1
                    print("open", self.openMonsterEgg_r["data"]["amount"], self.openMonsterEgg_r["data"]["category"])
            else:
                print("Open egg failed")
            time.sleep(2*random.random())

        print("Totally opened", str(number), "eggs:",str(t_potion),"Potions;",str(t_ydiamond),"YDiamonds;",str(t_pdiamond),"PDiamonds;",str(t_n),"N;",str(t_r),"R;",str(t_sr),"SR;",str(t_ssr),"SSR;")

    def updateMonster(self, monster):
        self.checkBag()
        id = monster["id"]
        level = monster["level"]
        rarity = monster["rarity"]
        self.updateMonster_data["nftId"] = id
        if rarity == 'N':
            if self.potion >= 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.potion -= 1
                    print(id, "N Metamon update to level", str(level+1)+"!")
            else:
                print("Update failed. Potion is not enough.")
                return 0
        if rarity == 'R':
            if self.ydiamond >= 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.ydiamond -= 1
                    print(id, "R Metamon update to level", str(level+1)+"!")
            else:
                print("Update failed. YDiamond is not enough.")
                return 0
        if rarity == 'SR':
            if self.pdiamond >= 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.pdiamond -= 1
                    print(id, "SR Metamon update to level", str(level+1)+"!")
            else:
                print("Update failed. PDiamond is not enough.")
                return 0
        if rarity == 'SSR':
            if self.pdiamond >= 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.pdiamond -= 1
                    print(id, "SR Metamon update to level", str(level+1)+"!")
            else:
                print("Update failed. PDiamond is not enough.")
                return 0
        return 1
        

    def startBattle(self, update=1):
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
            if self.raca < 50:
                    # print("RACA is not enough")
                    break
            while tear:
                if self.raca < 50:
                    print("RACA is not enough")
                    break
                if exp < exp_max:
                    self.startBattle_r = json.loads(self.s.post(startBattle_url, data = self.startBattle_data, headers=self.headers).text)
                    battle += 1
                    if self.startBattle_r["data"]["challengeResult"] == True:
                        win += 1
                    if self.startBattle_r["data"]["challengeResult"] == False:
                        lose += 1
                    exp += self.startBattle_r["data"]["challengeExp"]
                    self.fragment += self.startBattle_r["data"]["bpFragmentNum"]
                    self.raca -= 50
                    tear -= 1
                else:
                    if update == 1:
                        update_result = self.updateMonster(monster)
                        exp = 0
                        if update_result == 0:
                            break
                    else:
                        pass
            if battle != 0:
                print(id, rarity, "Metamon battled:", str(battle)+"; ", "Win:", str(win)+"; ", "Lose:", str(lose)+";", "Win rate:", str(round(win/battle*100, 2))+"%;")
                time.sleep(2)


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
    my_metamon.startBattle(update=1)    #Auto-battle, if the exp is full, it will automatically level up. If you don't want to level up, set update=-1
    my_metamon.composeMonsterEgg() # You can change the number, the default is max number which you can compose.
    # my_metamon.openMonsterEgg(number=10) # You can change the number, the default is max number which you can compose. Uncomment will unlock the opening eggs function.
    my_metamon.check()
