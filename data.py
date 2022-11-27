import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_index(list_montage, list_fräserei, amount_done, type):
    index = -1

    current_amount = 0

    for i, obj in enumerate(list_montage):
        if str(obj).__contains__(type):
            current_amount = current_amount + 1
        if current_amount > amount_done:
            index = i
            break

    if type == "10 P-200":
        while list_fräserei[index] == "10 GEH-100":
            index = index - 1

    return index


def verschiebung_durchführen(montage, vormontage, fräserei, dreherei, stanzerei, periode):

    highest_length = 0

    if len(montage) > highest_length:
        highest_length = len(montage)
    if len(vormontage) > highest_length:
        highest_length = len(vormontage)
    if len(fräserei) > highest_length:
        highest_length = len(fräserei)
    if len(dreherei) > highest_length:
        highest_length = len(dreherei)
    if len(stanzerei) > highest_length:
        highest_length = len(stanzerei)

    while len(montage) < highest_length:
        montage.insert(0, "0")
    while len(vormontage) < highest_length:
        vormontage.insert(0, "0")
    while len(fräserei) < highest_length:
        fräserei.insert(0, "0")
    while len(dreherei) < highest_length:
        dreherei.insert(0, "0")
    while len(stanzerei) < highest_length:
        stanzerei.insert(0, "0")

    while len(periode) < highest_length:
        periode.append(str(len(periode)+1))

    return montage, vormontage, fräserei, dreherei, stanzerei, periode


auftrag = pd.read_csv("Auftrag_1.csv", sep=";")
# auftrag = pd.read_csv("Auftrag_2.csv", sep=";")

p_100 = auftrag.query('Produkt == "P-100"')
p_101 = auftrag.query('Produkt == "P-101"')
p_200 = auftrag.query('Produkt == "P-200"')

highest = -1

verschiebung = False

########## montage

montage = []

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
        res2[x - 1] = 10

#######################################################################

res3 = []

for x in range(19):
    if p_200.get(str(x)) is not None:
        if int(p_200.get(str(x)) > 0) == 1:
            res3.append(int(p_200.get(str(x))))
        elif len(res3) > 0:
            res3.append(0)

for x in range(len(res3)):
    if res3[x] == 20:
        res3[x] = 10
        res3[x - 1] = 10

########## zusammenfügen

for x in range(len(res2)):
    if res2[len(res2) - x - 1] != 0:
        if montage[len(montage) - x - 1] == 0:
            montage[len(montage) - x - 1] = "10 P-101"
        else:
            added = False
            for y in range(len(montage)):
                if montage[len(montage) - y - 1] == 0 and (len(montage) - y - 1) < x:
                    montage[len(montage) - y - 1] = "10 P-101"
                    added = True
            if added is False:
                montage.insert(0, "10 P-101")

for x in range(len(res3)):
    if res3[len(res3) - x - 1] != 0:
        if montage[len(montage) - x - 1] == 0:
            montage[len(montage) - x - 1] = "10 P-200"
        else:
            added = False
            for y in range(len(montage)):
                if montage[len(montage) - y - 1] == 0 and (len(montage) - y - 1) < x:
                    montage[len(montage) - y - 1] = "10 P-200"
                    added = True
            if added is False:
                montage.insert(0, "10 P-200")

while montage[-1] == 0:
    montage.pop()
    highest = highest - 1

while len(montage) < highest:
    montage.insert(0, 0)

########## vormontage

vormontage = montage.copy()

vormontage.append(0)

vormontage.pop(0)

geh_amount_100 = 0
geh_amount_200 = 0

for i, obj in enumerate(vormontage.copy()):
    if obj == "10 P-100":
        geh_amount_100 = geh_amount_100 + 10
        vormontage[i] = "10 ROT-100"
    if obj == "10 P-101":
        geh_amount_100 = geh_amount_100 + 10
        vormontage[i] = "10 ROT-101"
    if obj == "10 P-200":
        geh_amount_200 = geh_amount_200 + 10
        vormontage[i] = "10 ROT-200"

wel_amount_100 = geh_amount_100
wel_amount_200 = geh_amount_200

########## fräserei

fräserei = [0] * highest

geh_amount_100_done = 0

while geh_amount_100 >= 50:

    index = get_index(montage, fräserei, geh_amount_100_done, "10 P-10")

    for x in range(5):
        fräserei.insert(index, "10 GEH-100")
        fräserei.pop(0)
        index = index - 1

    geh_amount_100 = geh_amount_100 - 50

    geh_amount_100_done = geh_amount_100_done + 5

if geh_amount_100 < 50:

    index = get_index(montage, fräserei, geh_amount_100_done, "10 P-10")

    for x in range(int(geh_amount_100 / 10)):
        fräserei.insert(index, "10 GEH-100")
        fräserei.pop(index - 1)
        index = index - 1

geh_amount_200_done = 0

while geh_amount_200 >= 50:

    index = get_index(montage, fräserei, geh_amount_200_done, "10 P-200")

    for x in range(5):
        fräserei.insert(index, "10 GEH-200")
        fräserei.pop(0)
        index = index - 1

    geh_amount_200 = geh_amount_200 - 50

    geh_amount_200_done = geh_amount_200_done + 5

if geh_amount_200 < 50:

    index = get_index(montage, fräserei, geh_amount_200_done, "10 P-200")

    for x in range(int(geh_amount_200 / 10)):
        fräserei.insert(index + 1, "10 GEH-200")
        fräserei.pop(0)
        index = index - 1

########## dreherei

dreherei = [0] * highest

while wel_amount_100 > 0:
    index = -1

    for i, x in enumerate(vormontage):
        if str(x).__contains__("10 ROT-10"):
            index = i
            break

    for x in range(6):
        dreherei.insert(index, "10 WEL-100")
        dreherei.pop(0)
        index = index - 1

    wel_amount_100 = wel_amount_100 - 60

while wel_amount_200 > 0:
    index = -1

    for i, x in enumerate(vormontage):
        if str(x).__contains__("10 ROT-200"):
            index = i
            break

    if dreherei[index] != "0":
        for i, x in enumerate(dreherei):
            if str(x).__contains__("10 WEL-100"):
                break
            index = i + 1

    for x in range(6):
        dreherei.insert(index, "10 WEL-200")
        index = index - 1
        if index < 0:
            verschiebung = True
            index = 0
        else:
            dreherei.pop(0)

    wel_amount_200 = wel_amount_200 - 60

########## stanzerei

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
    if obj == "10 ROT-200":
        stanzerei.insert((i), "10 RAD-200")
        stanzerei.pop(-1)

stanzerei.append(0)
stanzerei.pop(0)

########## create dataframe

abt = ["Montage", "Vormontage", "Fräserei", "Dreherei", "Stanzerei"]

per = list(range(1, highest + 1, 1))

if verschiebung is True:
    montage, vormontage, fräserei, dreherei, stanzerei, per = verschiebung_durchführen(montage, vormontage, fräserei, dreherei, stanzerei, per)

data = [montage, vormontage, fräserei, dreherei, stanzerei]

df = pd.DataFrame(data, abt, per)

print(df.to_string())

########## create gantt chart

fig, gnt = plt.subplots()

gnt.set_xlim(0, int(per[-1]))
gnt.set_ylim(0, 5)

gnt.set_xlabel('Periode')
gnt.set_ylabel('Abteilung')

gnt.set_xticks(list(range(0, int(per[-1]), 1)))
gnt.set_yticks(list(range(0, 5, 1)))
gnt.set_xticklabels('')
gnt.set_yticklabels('')
gnt.set_xticks(list(np.arange(0.5, int(per[-1]), 1)), minor=True)
gnt.set_xticklabels(list(np.arange(1, int(per[-1])+1, 1)), minor=True)
gnt.set_yticks(list(np.arange(0.5, 5, 1)), minor=True)
gnt.set_yticklabels(reversed(abt), minor=True)

gnt.grid(True)

for i, obj in enumerate(montage):
    if obj == "10 P-100":
        gnt.broken_barh([(i, 1)], (4, 1), facecolors=('xkcd:red'))
    if obj == "10 P-101":
        gnt.broken_barh([(i, 1)], (4, 1), facecolors=('xkcd:blue'))
    if obj == "10 P-200":
        gnt.broken_barh([(i, 1)], (4, 1), facecolors=('xkcd:brown'))

for i, obj in enumerate(vormontage):
    if obj == "10 ROT-100":
        gnt.broken_barh([(i, 1)], (3, 1), facecolors=('xkcd:orange'))
    if obj == "10 ROT-101":
        gnt.broken_barh([(i, 1)], (3, 1), facecolors=('xkcd:cyan'))
    if obj == "10 ROT-200":
        gnt.broken_barh([(i, 1)], (3, 1), facecolors=('xkcd:tan'))

for i, obj in enumerate(fräserei):
    if obj == "10 GEH-100":
        gnt.broken_barh([(i, 1)], (2, 1), facecolors=('xkcd:green'))
    if obj == "10 GEH-200":
        gnt.broken_barh([(i, 1)], (2, 1), facecolors=('xkcd:lime green'))

for i, obj in enumerate(dreherei):
    if obj == "10 WEL-100":
        gnt.broken_barh([(i, 1)], (1, 1), facecolors=('xkcd:yellow'))
    if obj == "10 WEL-200":
        gnt.broken_barh([(i, 1)], (1, 1), facecolors=('xkcd:goldenrod'))

for i, obj in enumerate(stanzerei):
    if obj == "10 RAD-100":
        gnt.broken_barh([(i, 1)], (0, 1), facecolors=('xkcd:pink'))
    if obj == "5 RAD-101":
        gnt.broken_barh([(i, 1)], (0, 1), facecolors=('xkcd:magenta'))
    if obj == "10 RAD-200":
        gnt.broken_barh([(i, 1)], (0, 1), facecolors=('xkcd:violet'))

if verschiebung:
    tage = int(per[-1]) - highest
    gnt.text(0, 5.3, 'Vorsicht: Der Auftrag hat sich um ' + str(tage) + ' Tage nach hinten verschoben!', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

plt.show()
