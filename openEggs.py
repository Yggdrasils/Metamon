import random

contents = {"Potion":0, "N metamon":0, "YDiamond":0, "PDiamond":0, "Donuts":0, "USM":0, "MPB":0, "Grimsz Board":0, "R metamon":0, "Duke":0, "Spaceship":0, "Satelite":0, "Rocket":0}



number = 100000

for i in range(number):
    r = random.random()
    if 0 <= r <= 0.5791157:
        print("open 3 Potion")
        contents["Potion"] += 3
    elif 0.5791157 < r <= 0.582449:
        print("open 1 N metamon")
        contents["N metamon"] += 1
    elif 0.582449 < r <= 0.6157823:
        print("open 1 YDiamond")
        contents["YDiamond"] += 1
    elif 0.6157823 < r <= 0.6161156:
        print("open 1 PDiamond")
        contents["PDiamond"] += 1
    elif 0.6161156 < r <= 0.9494489:
        print("open 3 Donuts")
        contents["Donuts"] += 3
    elif 0.9494488 < r <= 0.9994489:
        print("open 10 USM")
        contents["USM"] += 10
    elif 0.9994489 < r <= 0.9994656:
        print("open 1 MPB")
        contents["MPB"] += 1
    elif 0.9994656 < r <= 0.9994666:
        print("open 1 Grimsz Board")
        contents["Grimsz Board"] += 1
    elif 0.9994666 < r <= 0.9996333:
        print("open 1 R metamon")
        contents["R metamon"] += 1
    elif 0.9996333 < r <= 0.99965:
        print("open 1 Duke")
        contents["Duke"] += 1
    elif 0.99964 < r <= 0.9998167:
        print("open 1 Satelite")
        contents["Satelite"] += 1
    elif 0.9998166 < r <= 0.9998334:
        print("open 1 Spaceship")
        contents["Spaceship"] += 1
    elif 0.9998333 < r <= 1:
        print("open 1 Rocket")
        contents["Rocket"] += 1

s = "Totally opened " + str(number) + " eggs: "
for key in contents:
    if contents[key] != 0:
        s = s + str(contents[key]) + " " + key + "; "
print(s)
