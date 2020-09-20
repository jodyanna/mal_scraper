import os
import csv
from matplotlib import pyplot as plt


class Entry:
    def __init__(self):
        self.position = 0
        self.titles = []
        self.scores = []


def main():
    # Set up
    csv_names = os.listdir("./csv")
    csv_names.sort()

    entry1 = Entry()
    entry2 = Entry()

    # Get input from user
    entry1.position = get_input()
    entry2.position = get_input()

    # Get data from csv files
    csv_data = []
    for file in csv_names:
        data = csv_file_reader(file)
        csv_data.append(data)

    # Get dates
    dates = get_dates(csv_names)

    # Parse data
    parse_csv(csv_data, entry1)
    parse_csv(csv_data, entry2)

    # Plot graph
    plot_graph(entry1, entry2, dates)


def get_input():
    return int(input("Enter position of entry: "))


def csv_file_reader(file_name):
    path = "./csv/"
    csv_data = []
    with open(path + file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    return csv_data


def get_dates(file_names):
    dates = []
    for file in file_names:
        date = file[11:21]
        dates.append(date)

    return dates


def parse_csv(data, cls):
    for file in data:
        title_check = True
        entry = file[cls.position]

        if len(cls.titles) > 0:
            if entry["Title"] != cls.titles[0]:
                title_check = False
                for index, search in enumerate(file):
                    if search["Title"] == cls.titles[0]:
                        entry = file[index]
                        title_check = True

        if title_check:
            cls.titles.append(entry["Title"])
            cls.scores.append(float(entry["Score"]))

        if not title_check:
            cls.titles.append(None)
            cls.scores.append(None)


def plot_graph(entry1, entry2, dates):
    plt.figure(figsize=(12, 7))

    plt.plot(dates, entry2.scores, label=entry2.titles[0])
    plt.plot(dates, entry1.scores, label=entry1.titles[0])

    plt.suptitle("MAL Rankings")
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.legend()

    plt.xticks(rotation="90")

    plt.show()


main()
