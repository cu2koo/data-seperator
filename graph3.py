import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, locale="de_DE")
graphPath = "graph"


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "is been created.")


createPath(graphPath)


def parser(date):
    return pd.datetime.strptime(date, '%d.%m.%Y %H:%M')


df = pd.read_csv("result/kuehlschrank.csv", sep=";", decimal=",",
                 date_parser=parser, parse_dates=["Datum"])

print(df)

fig, ax = plt.subplots()
ax.plot(df["Datum"], df["Füllstand gesamt"])
ax.set_title("Füllstand des Kühlschranks", pad=15.0)
ax.set_xlabel("Zeitpunkt", loc="center", labelpad=10.0)
ax.set_ylabel("Füllstand", loc="center", labelpad=10.0)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%a, %d.%m."))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
ax.grid(True)
fig.set_figheight(9.6)
fig.set_figwidth(12.8)

fig, ax = plt.subplots(2, 2, figsize=(20, 30), sharey=True)
faecher = ("Füllstand 1. Fach", "Füllstand 2. Fach",
           "Füllstand 3. Fach", "Füllstand 4. Fach")

count = 0
for fach in faecher:
    x = int(count/2)
    y = count % 2
    ax[x, y].plot(df["Datum"], df[fach])
    ax[x, y].set_title(fach, pad=15.0)
    ax[x, y].set_xlabel("Zeitpunkt", loc="center", labelpad=10.0)
    ax[x, y].set_ylabel("Füllstand", loc="center", labelpad=10.0)
    ax[x, y].xaxis_date()
    ax[x, y].xaxis.set_major_formatter(mdates.DateFormatter("%d.%m."))
    ax[x, y].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax[x, y].grid(True)
    count += 1

fig, ax = plt.subplots()
ax.plot(df["Datum"], df["Füllstand gesamt"],
        label="Füllstand gesamt", linewidth=4.0)
for fach in faecher:
    ax.plot(df["Datum"], df[fach], label=fach)
ax.set_title("Füllstande des Kühlschranks", pad=15.0)
ax.set_xlabel("Zeitpunkt", loc="center", labelpad=10.0)
ax.set_ylabel("Füllstand", loc="center", labelpad=10.0)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%a, %d.%m."))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
ax.grid(True)
ax.legend()
fig.set_figheight(9.6)
fig.set_figwidth(12.8)


plt.show()
