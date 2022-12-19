import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    return pd.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')


df = pd.read_csv("result/bath.csv", sep=",", decimal=".",
                 date_parser=parser, parse_dates=["Date"])

# Humidity
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Humidity"])
ax.set_title("Luftfeuchtigkeit im Bad", pad=15.0)
ax.set_xlabel("Zeitpunkt", loc="center", labelpad=10.0)
ax.set_ylabel("Luftfeuchtigkeit in %", loc="center", labelpad=10.0)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%a, %d.%m."))
ax.grid(True)
fig.set_figheight(9.6)
fig.set_figwidth(12.8)

# https://www.ratgeber-luftfeuchtigkeit.de/luftfeuchtigkeit-im-badezimmer/
ax.axhline(70, c="r", ls="dotted")

# Temperature and Dew Point
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Temperature"], label="Temperatur in °C")
ax.plot(df["Date"], df["Dew Point"], label="Taupunkt in °C")
ax.set_title("Temperatur und Taupunkt im Bad", pad=15.0)
ax.set_xlabel("Zeitpunkt", loc="center", labelpad=10.0)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%a, %d.%m."))
ax.legend()
ax.grid(True)
fig.set_figheight(9.6)
fig.set_figwidth(12.8)

fig, ax = plt.subplots(2, 2, figsize=(20, 30), sharey=True)
dfSubs = [
    df[(df["Date"] > '2022-12-8 16:0:0') &
       (df["Date"] < '2022-12-8 18:0:0')],
    df[(df["Date"] > '2022-12-9 7:0:0') &
       (df["Date"] < '2022-12-9 9:0:0')],
    df[(df["Date"] > '2022-12-12 9:0:0') &
       (df["Date"] < '2022-12-12 11:0:0')],
    df[(df["Date"] > '2022-12-13 17:0:0') &
       (df["Date"] < '2022-12-13 19:0:0')]
]

count = 0
for dfSub in dfSubs:
    x = int(count/2)
    y = count % 2
    ax[x, y].plot(dfSub["Date"], dfSub["Temperature"],
                  label="Temperatur in °C")
    ax[x, y].plot(dfSub["Date"], dfSub["Dew Point"], label="Taupunkt in °C")

    date = pd.to_datetime(dfSub["Date"].values[0]).strftime("%d.%m.")
    ax[x, y].set_title(
        "Temperatur und Taupunkt im Bad (Extreme am " + date + ")", pad=15.0)
    ax[x, y].set_xlabel("Zeitpunkt", loc="center", labelpad=7.5)
    ax[x, y].xaxis_date()
    ax[x, y].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax[x, y].legend()
    ax[x, y].grid(True)
    count += 1

df = pd.read_csv("result/bath-extra.csv", sep=",", decimal=".",
                 date_parser=parser, parse_dates=["Date"])

# Humidity
dfSubs = [
    df[(df["Date"] > '2022-12-16 10:0:0') &
       (df["Date"] < '2022-12-16 11:0:0')],
    df[(df["Date"] > '2022-12-18 8:35:0') &
       (df["Date"] < '2022-12-18 9:35:0')]
]

fig, ax = plt.subplots(2, 1, figsize=(20, 30), sharey=True)
count = 0
for dfSub in dfSubs:
    x = count % 2
    ax[x].plot(dfSub["Date"], dfSub["Humidity"])
    date = pd.to_datetime(dfSub["Date"].values[0]).strftime("%d.%m.")
    ax[x].set_title(
        "Luftfeuchtigkeit im Bad (beim Duschen am " + date + ")", pad=15.0)
    ax[x].set_xlabel("Zeitpunkt", loc="center", labelpad=7.5)
    ax[x].set_ylabel("Luftfeuchtigkeit in %", loc="center", labelpad=7.5)
    ax[x].xaxis_date()
    ax[x].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax[x].legend()
    ax[x].grid(True)
    ax[x].axhline(70, c="r", ls="dotted")
    count += 1

fig, ax = plt.subplots(2, 1, figsize=(20, 30), sharey=True)
count = 0
for dfSub in dfSubs:
    x = count % 2
    ax[x].plot(dfSub["Date"], dfSub["Temperature"],
               label="Temperatur in °C")
    ax[x].plot(dfSub["Date"], dfSub["Dew Point"], label="Taupunkt in °C")

    date = pd.to_datetime(dfSub["Date"].values[0]).strftime("%d.%m.")
    ax[x].set_title(
        "Temperatur und Taupunkt im Bad (beim Duschen am " + date + ")", pad=15.0)
    ax[x].set_xlabel("Zeitpunkt", loc="center", labelpad=7.5)
    ax[x].xaxis_date()
    ax[x].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax[x].legend()
    ax[x].grid(True)
    count += 1

plt.show()
