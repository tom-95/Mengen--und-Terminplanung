import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

auftrag = pd.read_csv("Auftrag.csv", sep=";")

p_100 = auftrag.query('Produkt == "P-100"')
p_101 = auftrag.query('Produkt == "P-101"')

montage = []

highest = -1

for x in range(19):
    if p_100.get(str(x)) is not None:
        if int(p_100.get(str(x)) > 0) == 1:
            highest = x
            montage.append(int(p_100.get(str(x))))
        elif len(montage) > 0:
            highest = x
            montage.append(0)

for x in range(len(montage)):
    if montage[x] == 20:
        montage[x] = 10
        montage[x - 1] = 10

for x in range(len(montage)):
    if montage[x] == 10:
        montage[x] = "10 P-100"

#######################################################################

res2 = []

for x in range(19):
    if p_101.get(str(x)) is not None:
        if int(p_101.get(str(x)) > 0) == 1:
            res2.append(int(p_101.get(str(x))))
        elif len(res2) > 0:
            res2.append(0)

for x in range(len(res2)):
    if res2[x] == 20:
        res2[x] = 10
        res2[x-1] = 10

# zusammenfügen

for x in range(len(res2)):
    if res2[len(res2)-x-1] != 0:
        if montage[x] == 0:
            montage[x] = "10 P-101"
        else:
            added = False
            for y in range(len(montage)):
                if montage[len(montage) - y - 1] == 0 and (len(montage) - y - 1) < x:
                    montage[len(montage) - y - 1] = "10 P-101"
                    added = True
            if added is False:
                montage.insert(0, "10 P-101")

while montage[-1] == 0:
    montage.pop()
    highest = highest - 1

# print(res)
# print(highest)

while len(montage) < highest:
    montage.insert(0, 0)

#print(int(res.get("13")))

vormontage = montage.copy()

vormontage.append(0)

vormontage.pop(0)

geh_amount = 0

for i, obj in enumerate(vormontage.copy()):
    if obj == "10 P-100":
        geh_amount = geh_amount + 10
        vormontage[i] = "10 ROT-100"
    if obj == "10 P-101":
        geh_amount = geh_amount + 10
        vormontage[i] = "10 ROT-101"

wel_amount = geh_amount

fräserei = [0] * highest

while geh_amount >= 50:
    index = int(highest - (geh_amount/10) + 1)

    for x in range(5):
        fräserei.insert(index, "10 GEH-100")
        fräserei.pop(0)
        index = index - 1

    geh_amount = geh_amount - 50

if geh_amount < 50:
    index = int(highest - (geh_amount/10))

    for x in range(int(geh_amount/10)):
        fräserei.insert(index, "10 GEH-100")
        fräserei.pop(0)
        index = index - 1

dreherei = [0] * highest

while wel_amount > 0:
    index = int(highest - 1 - (wel_amount/10))

    for x in range(6):
        dreherei.insert(index, "10 WEL-100")
        dreherei.pop(0)
        index = index - 1

    wel_amount = wel_amount - 60

stanzerei = [0] * highest

for i, obj in enumerate(vormontage):
    if obj == "10 ROT-100":
        stanzerei.insert((i), "10 RAD-100")
        stanzerei.pop(-1)
    if obj == "10 ROT-101":
        stanzerei.insert((i), "5 RAD-101")
        stanzerei.insert((i), "5 RAD-101")
        stanzerei.pop(0)
        stanzerei.pop(-1)

stanzerei.append(0)
stanzerei.pop(0)

data = [montage, vormontage, fräserei, dreherei, stanzerei]

abt = ["Montage", "Vormontage", "Fräserei", "Dreherei", "Stanzerei"]

per = list(range(1, highest+1, 1))

df = pd.DataFrame(data, abt, per)

print(df.to_string())

##############################create gantt chart

fig, gnt = plt.subplots()

gnt.set_xlim(0, highest)
gnt.set_ylim(0, 5)

gnt.set_xlabel('Periode')
gnt.set_ylabel('Abteilung')

gnt.set_xticks(list(range(0, 17, 1)))
gnt.set_yticks(list(range(0, 5, 1)))
gnt.set_xticklabels('')
gnt.set_yticklabels('')
gnt.set_xticks(list(np.arange(0.5, 17, 1)), minor=True)
gnt.set_xticklabels(list(np.arange(1, 18, 1)), minor=True)
gnt.set_yticks(list(np.arange(0.5, 5, 1)), minor=True)
gnt.set_yticklabels(reversed(abt), minor=True)

gnt.grid(True)

for i, obj in enumerate(montage):
    if obj == "10 P-100":
        gnt.broken_barh([(i, 1)], (4, 1), facecolors=('tab:red'))
    if obj == "10 P-101":
        gnt.broken_barh([(i, 1)], (4, 1), facecolors=('tab:blue'))

for i, obj in enumerate(vormontage):
    if obj == "10 ROT-100":
        gnt.broken_barh([(i, 1)], (3, 1), facecolors=('tab:orange'))
    if obj == "10 ROT-101":
        gnt.broken_barh([(i, 1)], (3, 1), facecolors=('tab:cyan'))

for i, obj in enumerate(fräserei):
    if obj == "10 GEH-100":
        gnt.broken_barh([(i, 1)], (2, 1), facecolors=('tab:green'))

for i, obj in enumerate(dreherei):
    if obj == "10 WEL-100":
        gnt.broken_barh([(i, 1)], (1, 1), facecolors=('tab:olive'))

for i, obj in enumerate(stanzerei):
    if obj == "10 RAD-100":
        gnt.broken_barh([(i, 1)], (0, 1), facecolors=('tab:pink'))
    if obj == "5 RAD-101":
        gnt.broken_barh([(i, 1)], (0, 1), facecolors=('tab:purple'))

plt.show()