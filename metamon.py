import requests
import json

api_url = "https://metamon-api.radiocaca.com/usm-api/"
login_url = api_url + "login"
checkBag_url = api_url + "checkBag"
getWalletPropertyList_url = api_url + "getWalletPropertyList"
composeMonsterEgg_url = api_url + "composeMonsterEgg"
startBattle_url = api_url + "startBattle"
openMonsterEgg_url = api_url + "openMonsterEgg"
updateMonster_url = api_url + "updateMonster"


class metamon(object):

    def __init__(self, address, sign):
        self.address = address
        self.sign = sign
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
        self.login_data = {"address": self.address,"msg": "LogIn", "sign": self.sign}
        self.checkBag_data = self.address_data
        self.getWalletPropertyList_data = {"address": address, "page": "1", "pageSize": "1000"}
        self.composeMonsterEgg_data = self.address_data
        self.startBattle_data = {"address": address, "battleLevel": "1", "monsterA": "", "monsterB": "214650"} # You can change monsterB to your metamon
        self.openMonsterEgg_data = self.address_data
        self.updateMonster_data = {"nftId": "", "address": self.address}
    
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
        self.getWalletPropertyList_r = json.loads(self.s.post(getWalletPropertyList_url, data=self.getWalletPropertyList_data, headers=self.headers).text)
        self.metamon_list = self.getWalletPropertyList_r["data"]["metamonList"]
    
    def check(self):
        self.checkBag()
        print("=================")
        print("RACA:", self.raca)
        print("Potion:", self.potion)
        print("YDiamond:", self.ydiamond)
        print("PDiamond:", self.pdiamond)
        print("Fragment:", self.fragment)
        print("Egg:", self.egg)
        print("Mintable Egg:", self.fragment//1000)
        print("Metamon:", len(self.metamon_list))
        print("=================")
        print("")

    def composeMonsterEgg(self, number=0):
        self.checkBag()
        compose_number = self.mintable_egg
        if number > compose_number:
            number = compose_number
        if number == 0:
            number = compose_number
        for i in range(number):
            self.s.post(composeMonsterEgg_url, data=self.composeMonsterEgg_data, headers=self.headers)
        print("Composed", str(number), "eggs")
        print("")

    def openMonsterEgg(self, number=0):
        self.checkBag()
        if number > self.egg:
            number = self.egg
        if number == 0:
            number = self.egg
        for i in range(number):
            self.openMonsterEgg_r = json.loads(self.s.post(openMonsterEgg_url, data=self.openMonsterEgg_data, headers=self.headers).text)
            print("open", self.openMonsterEgg_r["data"]["amount"], self.openMonsterEgg_r["data"]["category"])
        print("Totally opened", str(number), "eggs")
        print("")

    def updateMonster(self, monster):
        self.checkBag()
        id = monster["id"]
        level = monster["level"]
        rarity = monster["rarity"]
        self.updateMonster_data["nftId"] = id
        if rarity == 'N':
            if self.potion > 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.potion -= 1
                    print(id, "N Metamon update to level", str(level+1)+"!")
            else:
                if self.egg > 0:
                    self.openMonsterEgg(2)
                    self.updateMonster(monster)
                else:
                    if self.mintable_egg > 0:
                        self.composeMonsterEgg()
                        self.openMonsterEgg(2)
                        self.updateMonster(monster)
                    else:
                        print("Update failed")
                        return 0
        if rarity == 'R':
            if self.ydiamond > 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.ydiamond -= 1
                    print(id, "R Metamon update to level", str(level+1)+"!")
            else:
                print("Update failed")
                return 0
        if rarity == 'SR':
            if self.pdiamond > 1:
                self.updateMonster_r = json.loads(self.s.post(updateMonster_url, data=self.updateMonster_data, headers=self.headers).text)
                if self.updateMonster_r["result"] == 1:
                    self.pdiamond -= 1
                    print(id, "SR Metamon update to level", str(level+1)+"!")
            else:
                print("Update failed")
                return 0
        return 1

    def startBattle(self):
        for monster in self.metamon_list:
            id = monster["id"]
            token_id = monster["tokenId"]
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
            if self.raca < 50:
                    print("RACA is not enough")
                    break
            while 1:
                if self.raca < 50:
                    print("RACA is not enough")
                    break
                if tear == 0:
                    print(id, "Metamon energy is not enough")
                    break
                if exp < exp_max:
                    self.startBattle_r = json.loads(self.s.post(startBattle_url, data = self.startBattle_data, headers=self.headers).text)
                    battle += 1
                    if self.startBattle_r["data"]["challengeResult"] == True:
                        win += 1
                    if self.startBattle_r["data"]["challengeResult"] == False:
                        lose += 1
                    exp += self.startBattle_r["data"]["challengeExp"]
                    tear -= 1
                    self.raca -= 50
                    self.fragment += self.startBattle_r["data"]["bpFragmentNum"]
                if exp >= exp_max:
                    update_result = self.updateMonster(monster)
                    exp = 0
                if update_result == 0:
                    break
            print(id, rarity, "Metamon battled:", str(battle)+"; ", "Win:", str(win)+"; ", "Lose:", str(lose)+";")
        print("")


if __name__ == "__main__":
    my_address = "" # Your wallet address
    my_sign = "" # Your sign
    my_metamon = metamon(address=my_address, sign=my_sign)
    my_metamon.login()
    my_metamon.getWalletPropertyList()
    my_metamon.check()
    my_metamon.startBattle()    #Auto-battle, if the exp is full, it will automatically level up and if potions are not enough, it will break.
    my_metamon.composeMonsterEgg() # You can change the number, the default is max number which you can compose.
    # my_metamon.openMonsterEgg(number=5) # You can change the number, number=0 is max number which you can compose.
    my_metamon.check()
