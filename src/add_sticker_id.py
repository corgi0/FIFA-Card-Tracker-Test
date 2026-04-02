import csv, search as sp

def main():
    with open('wc_players_with_ids.csv', 'r') as player_file, \
        open('wc_stickers_with_ids_and_stickers.csv', 'w') as player_write_file, \
        open('panini_player_stickers.csv', 'r') as sticker_file:
        players = csv.DictReader(player_file)
        stickers = list(csv.DictReader(sticker_file))
        player_writer = csv.DictWriter(player_write_file, players.fieldnames)
        player_writer.writeheader()

        for player in players:
            p_name = player["player_name"]
            found = False
            for sticker in stickers:
                s_name = sticker["player_name"]
                if sp.matches_text(p_name, s_name):
                    player["sticker_id"] = sticker["sticker"]
                    player_writer.writerow(player)
                    found = True
                    break
            if not found:
                player["sticker_id"] = ""
                player_writer.writerow(player)
        #
        # print(players.fieldnames)

if __name__ == '__main__':
    main()