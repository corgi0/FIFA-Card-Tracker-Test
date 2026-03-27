import csv

from selenium import webdriver

driver = webdriver.Chrome()


def parse_url_to_id(url):
    split = url.split('/')
    i = split.index('player') + 1 # id is the next item after player
    return split[i]

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

            URL = input("Enter sofifa url: ")

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
