import urllib

import search as search_players
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

def format_name(name):
    first = name.split(" ")[0]
    last = name.split(" ")[-1]
    first_letter = first[0]
    return f"{first_letter}. {last}"

def get_id_from_url(url):
    split = url.split('/')
    i = split.index('player') + 1 # id is the next item after player
    return split[i]

def get_sofifa_url(query):
    url = "https://www.google.com/search?btnI=1&q=" + urllib.parse.quote(query)
    driver.get(url + query.replace(' ', '+'))

    # Wait until we land on the sofifa page
    WebDriverWait(driver, 10).until(
        lambda d: "sofifa" in d.current_url and 'player' in d.current_url
    )
    return driver.current_url

def search_sofifa_for_id(name):
    query = f'{name} sofifa id'
    URL = get_sofifa_url(query)
    return get_id_from_url(URL)

def main():
    with open("../Fifa 2022 Full Player Database.csv", 'r', newline='') as all_players, \
         open("../Fifa 2022 World Cup Player Database.csv", 'r', newline='') as wc_players, \
         open("wc_players_with_ids.csv", 'w', newline='') as output_file:
        all_players_rows = list(csv.DictReader(all_players))
        wc_players_csv = csv.DictReader(wc_players)

        fieldnames = ["sofifa_id", "sticker_id", "player_name", "team", "position", "birth_year"]
        output = csv.DictWriter(output_file, fieldnames)
        output.writeheader()

        matched = 0
        unmatched = 0
        unmatched_names = []
        new_row = {}

        # NOTE THE ORDER: id, sticker num, player name, team, position, birth year
        for wc_player in wc_players_csv:
            wc_p_name = format_name(wc_player["player"])
            new_row['sofifa_id'] = 0
            new_row['sticker_id'] = "PLACEHOLDER"
            new_row['player_name'] = wc_player["player"]
            new_row['team'] = wc_player["team"]
            new_row['position'] = wc_player["position"]
            new_row['birth_year'] = wc_player["birth_year"]
            for player in all_players_rows:
                found = False
                p_name = player["short_name"]
                if search_players.matches_text(p_name, wc_p_name):
                    new_row['sofifa_id'] = player["\ufeffsofifa_id"]
                    output.writerow(new_row)
                    found = True
                    matched += 1
                    break  # Move on to next World Cup player after first match.

            if not found:
                name = wc_player["player"]
                print(f"{name} not found. Adding from sofifa search...")
                try:
                    ID = search_sofifa_for_id(name)
                except Exception as e:
                    unmatched_names.append(name)
                    print(f"Search failed for {name}, error: {e}")
                    unmatched += 1
                    continue
                new_row['sofifa_id'] = ID
                output.writerow(new_row)

        print(f"Matched {matched} players, {unmatched} unmatched.")
        for p in unmatched_names:
            print(p)
        for p in unmatched_names:
            with open('unmatched.txt', 'a') as f:
                f.write(f"{p}\n")



if __name__ == "__main__":
    main()