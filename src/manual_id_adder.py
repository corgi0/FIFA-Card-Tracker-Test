import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse

driver = webdriver.Chrome()


def parse_url_to_id(url):
    split = url.split('/')
    i = split.index('player') + 1 # id is the next item after player
    return split[i]

def get_final_url(query):
    url = "https://www.google.com/search?btnI=1&q=" + urllib.parse.quote(query)
    driver.get(url + query.replace(' ', '+'))

    # Wait until we land on the sofifa page
    WebDriverWait(driver, 10).until(
        lambda d: "sofifa" in d.current_url and 'player' in d.current_url
    )
    return driver.current_url

def main():
    with open('unmatched.txt', 'r') as unmatched, \
        open('wc_players_with_ids.csv', 'a') as out:
        writer = csv.DictWriter(out, fieldnames=['sofifa_id','sticker_id','player_name','team','position','birth_year'])
        # No writeheader since were appending
        for player in unmatched:
            player_data = player.split(',')
            player_sticker = player_data[0]
            player_name = player_data[1]
            player_team = player_data[2]
            player_position = player_data[3]
            player_birth_year = player_data[4]

            query = f'{player_name} sofifa id'
            URL = get_final_url(query)

            try:
                ID = parse_url_to_id(URL)

                print(f"Got ID for {player_name}: {ID}")

                writer.writerow({
                    'sofifa_id': ID,
                    'sticker_id': player_sticker,
                    'player_name': player_name,
                    'team': player_team,
                    'position': player_position,
                    'birth_year': player_birth_year
                })
            except Exception as e:
                print(f"Failed for {player_name}, error: {e}")
                print(f"URL used: {URL}")


if __name__ == "__main__":
    main()
