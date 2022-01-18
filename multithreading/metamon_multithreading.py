import requests
import json
import time
import math
import random
from threading import Thread
from telnetlib import Telnet

ip_url = "http://api.tianqiip.com/getip"

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
        self.s.keep_alive = False

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
        self.startBattle_data = {"address": address, "battleLevel": "1", "monsterA": "", "monsterB": "454193"} #"883061"
        self.openMonsterEgg_data = self.address_data
        self.updateMonster_data = {"nftId": "394090", "address": self.address}

    def set_proxies(self, secret, num=5, times=5, open=1):
        self.secret = secret
        self.times = times
        self.proxies = []
        if open == 1:
            for i in range(num):
                self.proxies.append(self.get_proxy())
        else:
            for i in range(num):
                self.proxies.append({"http":"http://127.0.0.1:10809", "https":"http://127.0.0.1:10809"})
        self.proxies.append({})

    def get_proxy(self):
        payload = {"secret":self.secret, "type":"json", "num":1, "time":self.times, "port":2}
        res = json.loads(requests.get(ip_url, params=payload).text)
        if res["code"] == 1000:
            data = res["data"][0]
            proxy = {"http":"http://{ip}:{port}".format(ip=data["ip"],port=data["port"]), "https":"http://{ip}:{port}".format(ip=data["ip"],port=data["port"])}
        else:
            print("get ip failed")
            proxy = {}
        # print(proxy)
        
        return proxy

    def login(self):
        res = json.loads(self.s.post(login_url, data=self.login_data, proxies=self.proxies[-1]).text)
        if res["code"] == "SUCCESS":
            self.headers["accesstoken"] = res["data"]
            print("Login success")
        else:
            print("Login fail")

    def checkBag(self):
        res = json.loads(self.s.post(checkBag_url, data=self.checkBag_data, headers=self.headers, proxies=self.proxies[-1]).text)
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
            if res["data"]["metamonList"]:
                self.metamon_list = res["data"]["metamonList"]
            else:
                print("getWalletPropertyList fail")
    
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
        res = json.loads(self.s.post(composeMonsterEgg_url, data=self.composeMonsterEgg_data, headers=self.headers, proxies=self.proxies[-1]).text)
        print(res["message"])

    def openMonsterEgg(self, number=100000):
        self.checkBag()
        t = {}
        s = "Totally opened " + str(number) + " eggs: "        
        if number > self.egg:
            number = self.egg
        for i in range(number):
            res = json.loads(self.s.post(openMonsterEgg_url, data=self.openMonsterEgg_data, headers=self.headers, proxies=self.proxies[-1]).text)
            if res["code"] == "SUCCESS":
                if t.get(res["data"]["category"]) == None:
                    t[res["data"]["category"]] = res["data"]["amount"]
                else:
                    t[res["data"]["category"]] += res["data"]["amount"]
                print("open", res["data"]["amount"], res["data"]["category"])
            else:
                print("Open egg failed")
        for key in t:
            s = s + str(t[key]) + " " + key + "; "
        print(s)
        
    def updateMonster(self, monster, thread):
        self.checkBag()
        updateMonster_data = self.updateMonster_data.copy()
        updateMonster_data["nftId"] = monster["id"]
        if self.materials[monster["rarity"]] >= 1:
            res = json.loads(self.s.post(updateMonster_url, data=updateMonster_data, headers=self.headers, proxies=self.proxies[thread]).text)
            if res["code"] == "SUCCESS":
                self.materials[monster["rarity"]] -= 1
                print("Thread", str(thread)+":", monster["id"], monster["rarity"], "Metamon update to level", str(monster["level"]+1)+"!")
            else:
                print("Update failed. Materials is not enough.")
                return 0

        return 1
        

    def startBattle(self, metamon_list, thread):
        startBattle_data = self.startBattle_data.copy()
        self.checkBag()
        t = 0
        for monster in metamon_list:
            id = monster["id"]
            exp = monster["exp"]
            exp_max = monster["expMax"]
            tear = monster["tear"]
            rarity = monster["rarity"]
            startBattle_data["monsterA"] = id
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
                try:
                    res = self.s.post(startBattle_url, data = startBattle_data, headers=self.headers, proxies=self.proxies[thread])
                    res = json.loads(res.text)
                    if res["code"] == "SUCCESS":
                        battle += 1
                        win += res["data"]["challengeResult"]
                        lose += bool(1-res["data"]["challengeResult"])
                        exp += res["data"]["challengeExp"]
                        self.fragment += res["data"]["bpFragmentNum"]
                        self.raca -= self.fee
                        tear -= 1
                    else:
                        pass
                    if exp >= exp_max:
                        self.updateMonster(monster, thread)
                        exp = 0
                except:
                    self.proxies[thread] = self.get_proxy()
            if battle != 0:
                print("Thread", str(thread)+":", id, rarity, "Metamon battled:", str(battle)+"; ", "Win:", str(win)+"; ", "Lose:", str(lose)+";", "Win rate:", str(round(win/battle*100, 2))+"%;")
                t += 1
                if t%12 == 0:
                    self.proxies[thread] = self.get_proxy()

    def multithreading_battle(self, count):
        per = math.ceil(len(self.metamon_list) / count)
        new_metamon_list = [self.metamon_list[i*per:(i+1)*per] for i in range(count)]
        t_batttle = []
        for i in range(count):
            t_batttle.append(Thread(target=self.startBattle, args=(new_metamon_list[i], i)))
        for i in t_batttle:
            i.start()
        for i in t_batttle:
            i.join()


if __name__ == "__main__":
    addr = ""
    sign = ""
    msg = ""
    secret = ""
    threads = 5
    
    my_metamon = metamon(address=addr, sign=sign, msg=msg)
    my_metamon.set_proxies(secret=secret,num=threads,times=5,open=1)
    # print(my_metamon.proxies)
    my_metamon.login()
    my_metamon.getWalletPropertyList()
    my_metamon.checkBag()
    my_metamon.multithreading_battle(threads)    #Auto-battle, if the exp is full, it will automatically level up. If you don't want to level up, set update=-1
    my_metamon.composeMonsterEgg() # You can change the number, the default is max number which you can compose.
    my_metamon.openMonsterEgg(number=0) # You can change the number, the default is max number which you can compose. Uncomment will unlock the opening eggs function.
    my_metamon.check()
