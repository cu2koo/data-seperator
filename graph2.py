import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import locale
import numpy as np

locale.setlocale(locale.LC_TIME, locale="de_DE")
graphPath = "graph"


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "is been created.")


createPath(graphPath)


def parser(date):
    return pd.datetime.strptime(date, '%Y-%m-%d')


df1 = pd.read_csv("result/living-room-results.csv", sep=",")
df2 = pd.read_csv("result/dining-room-results.csv", sep=",")

explode = (0.025, 0.1)
colors = ((156/255, 235/255, 155/255), (235/255, 175 /
          255, 143/255), (177/255, 148/255, 240/255))
labels = ("Nutzung mit Anwesenheit",
          "Nutzung ohne Anwesenheit")
angle = 180

fig, ax = plt.subplots()
arr = df1.values[0][3:5]
ax.pie(arr, explode, labels=labels, startangle=angle,
       colors=colors, autopct='%1.1f%%', shadow=True, textprops={'size': 'smaller'}, radius=1.0)
ax.set_title("Lichtnutzung mit und ohne Anwesenheit (Wohnzimmer)")
fig, ax = plt.subplots()
arr = df2.values[0][3:5]
ax.pie(arr, explode, labels=labels, startangle=angle,
       colors=colors, autopct='%1.1f%%', shadow=True, textprops={'size': 'smaller'}, radius=1.0)
ax.set_title("Lichtnutzung mit und ohne Anwesenheit (Esszimmer)")


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha='center')


fig, ax = plt.subplots()
width = 0.35
arr = df1.values[0][3:]
labels = ("Nutzung mit Anwesenheit",
          "Nutzung ohne Anwesenheit",
          "Keine Nutzung mit Anwesenheit")
ax.bar(labels, arr, width, label=labels, color=colors)
ax.set_ylabel('Anzahl der erfassten Perioden (5 Minuten)', labelpad=10.0)
ax.set_title(
    'Absolute Ergebnisse der Lichtnutzung (Wohnzimmer mit gemessenen 1344 Perioden)', pad=15.0)
ax.text(0, arr[0]//2, arr[0], ha='center')
ax.text(1, arr[1]//2, arr[1], ha='center')
ax.text(2, arr[2]//2, arr[2], ha='center')

fig, ax = plt.subplots()
width = 0.35
arr = df2.values[0][3:]
labels = ("Nutzung mit Anwesenheit",
          "Nutzung ohne Anwesenheit",
          "Keine Nutzung mit Anwesenheit")
ax.bar(labels, arr, width, label=labels, color=colors)
ax.set_ylabel('Anzahl der erfassten Perioden (5 Minuten)', labelpad=10.0)
ax.set_title(
    'Absolute Ergebnisse der Lichtnutzung (Esszimmer mit gemessenen 1260 Perioden) ', pad=15.0)
ax.text(0, arr[0]//2, arr[0], ha='center')
ax.text(1, arr[1]//2, arr[1], ha='center')
ax.text(2, arr[2]//2, arr[2], ha='center')

df1 = pd.read_csv("result/living-room-results-per-day.csv",
                  sep=",", date_parser=parser, parse_dates=["Datum"])
df2 = pd.read_csv("result/dining-room-results-per-day.csv",
                  sep=",", date_parser=parser, parse_dates=["Datum"])

labels = []
data = [[], [], []]
for val in df1.values:
    date = dt.datetime(val[0].year, val[0].month,
                       val[0].day).strftime("%a, %d.%m.")
    labels.append(date)
    data[0].append(val[4])
    data[1].append(val[5])
    data[2].append(val[6])
x = np.arange(len(labels))
width = 0.2
fig, ax = plt.subplots()
rects1 = ax.bar(x - width, data[0],
                width, label='Nutzung mit Anwesenheit', color=colors[0])
rects2 = ax.bar(x, data[1],
                width, label='Nutzung ohne Anwesenheit', color=colors[1])
rects3 = ax.bar(x + width, data[2], width,
                label='Keine Nutzung mit Anwesenheit', color=colors[2])

ax.set_ylabel('Anzahl der erfassten Perioden (5 Minuten)', labelpad=10.0)
ax.set_title('Absolute Ergebnisse der Lichtnutzung (Wohnzimmer) nach Tagen')
ax.set_xticks(x, labels)
ax.legend()
ax.bar_label(rects1, padding=2)
ax.bar_label(rects2, padding=2)
ax.bar_label(rects3, padding=2)
fig.tight_layout()


labels = []
data = [[], [], []]
for val in df2.values:
    date = dt.datetime(val[0].year, val[0].month,
                       val[0].day).strftime("%a, %d.%m.")
    labels.append(date)
    data[0].append(val[4])
    data[1].append(val[5])
    data[2].append(val[6])
x = np.arange(len(labels))
width = 0.2
fig, ax = plt.subplots()
rects1 = ax.bar(x - width, data[0],
                width, label='Nutzung mit Anwesenheit', color=colors[0])
rects2 = ax.bar(x, data[1],
                width, label='Nutzung ohne Anwesenheit', color=colors[1])
rects3 = ax.bar(x + width, data[2], width,
                label='Keine Nutzung mit Anwesenheit', color=colors[2])

ax.set_ylabel('Anzahl der erfassten Perioden (5 Minuten)', labelpad=10.0)
ax.set_title('Absolute Ergebnisse der Lichtnutzung (Esszimmer) nach Tagen')
ax.set_xticks(x, labels)
ax.legend()
ax.bar_label(rects1, padding=2)
ax.bar_label(rects2, padding=2)
ax.bar_label(rects3, padding=2)
fig.tight_layout()


plt.show()
