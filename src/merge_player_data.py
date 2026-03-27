import search as search_players
import csv

def format_name(name):
    first = name.split(" ")[0]
    last = name.split(" ")[-1]
    first_letter = first[0]
    return f"{first_letter}. {last}"

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

        # NOTE THE ORDER: id, sticker num, player name, team, position, birth year
        for wc_player in wc_players_csv:
            wc_p_name = format_name(wc_player["player"])
            for player in all_players_rows:
                found = False
                p_name = player["short_name"]
                if search_players.matches_text(p_name, wc_p_name):
                    output.writerow({
                        "sofifa_id": player["\ufeffsofifa_id"],
                        "sticker_id": "PLACEHOLDER",
                        "player_name": p_name,
                        "team": wc_player["team"],
                        "position": wc_player["position"],
                        "birth_year": wc_player["birth_year"]
                    })
                    found = True
                    matched += 1
                    break  # Move on to next World Cup player after first match.

            if not found:
                unmatched += 1
                unmatched_names.append(f"PLACEHOLDER,{wc_player['player']},{wc_player['team']},{wc_player['position']},{wc_player['birth_year']}")

        print(f"Matched {matched} players, {unmatched} unmatched.")
        for p in unmatched_names:
            print(p)
        for p in unmatched_names:
            with open('unmatched.txt', 'a') as f:
                f.write(f"{p}\n")



if __name__ == "__main__":
    main()