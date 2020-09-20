"""This module scrapes the top 200 ranked entries from MyAnimeList.net's 'Top Anime' pages."""

import os
import requests
import csv
import time
from bs4 import BeautifulSoup
from datetime import datetime
from random import shuffle

# Global Constants
NUM_TITLES_PER_PAGE = 50
LINK_0_50 = "https://myanimelist.net/topanime.php"
LINK_50_100 = "https://myanimelist.net/topanime.php?limit=50"
LINK_100_150 = "https://myanimelist.net/topanime.php?limit=100"
LINK_150_200 = "https://myanimelist.net/topanime.php?limit=150"


def main():
    # Get data from website
    table_0_50 = get_table(LINK_0_50)
    table_50_100 = get_table(LINK_50_100)
    table_100_150 = get_table(LINK_100_150)
    table_150_200 = get_table(LINK_150_200)

    # Parse data from table into lists
    top_50 = parse_table(table_0_50)
    top_50_100 = parse_table(table_50_100)
    top_100_150 = parse_table(table_100_150)
    top_150_200 = parse_table(table_150_200)

    # Write csv file
    top_200 = top_50 + top_50_100 + top_100_150 + top_150_200
    write_csv(top_200)


def get_table(url):
    source = requests.get(url, timeout=10).text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find("table", class_="top-ranking-table")

    # Delay next request by 15-25 seconds
    delay = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    shuffle(delay)
    time.sleep(delay.pop())

    return table


def parse_table(table):
    # Create empty lists
    ranks = [0] * NUM_TITLES_PER_PAGE
    titles = [0] * NUM_TITLES_PER_PAGE
    scores = [0] * NUM_TITLES_PER_PAGE
    num_eps = [0] * NUM_TITLES_PER_PAGE
    air_dates = [0] * NUM_TITLES_PER_PAGE
    num_members = [0] * NUM_TITLES_PER_PAGE

    for i, tr in enumerate(table.find_all("tr", class_="ranking-list")):
        rank = tr.find("td", class_="rank ac").span.text
        ranks[i] = rank

        title = tr.div.a.text
        titles[i] = title

        score = tr.find("td", class_="score ac fs14").span.text
        scores[i] = score

        title_info = tr.find("div", class_="information di-ib mt4").text.split("\n")
        num_eps[i] = title_info[1].lstrip()
        air_dates[i] = title_info[2].lstrip()
        num_members[i] = title_info[3].lstrip()

    return list(zip(ranks, titles, scores, num_eps, air_dates, num_members))


def write_csv(top_200):
    # Create directory if one does not exist
    path = "./csv"
    if not os.path.isdir(path):
        os.mkdir(path)

    # Create name for file containing today's date
    file_path = path + "/top200anime" + str(datetime.today().strftime("%Y-%m-%d")) + ".csv"

    with open(file_path, "w") as outfile:
        headers = ["#", "Title", "Score", "Episodes", "Date", "Popularity"]

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(headers)

        for entry in top_200:
            csv_writer.writerow(entry)


main()
