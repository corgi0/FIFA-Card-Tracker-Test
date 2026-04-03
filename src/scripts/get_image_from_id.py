import csv, requests, os

def main():
    output_dir = '../../player_images'
    player_csv = '../wc_players_with_ids.csv'
    with open('../../player_images/player_0.png', 'rb') as i:
        default_image = i.read()
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://sofifa.com/'}
    with open (player_csv, 'r') as f:
        players = csv.DictReader(f)
        for player in players:
            pid = player['sofifa_id']
            id_str = str(pid)
            url = f"https://cdn.sofifa.net/players/{id_str[:3]}/{id_str[3:6]}/22_240.png"
            output_file = os.path.join(output_dir, f"{player['sofifa_id']}.png")
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.content
                    print(f"Downloaded image for {player['player_name']}")
                else:
                    data = default_image
                    print(f"Failed to download image for {player['player_name']}, status code: {response.status_code}. Using defualt image.")
            except Exception as e:
                data = default_image
                print(f"Error downloading image for {player['player_name']}: {e}. Using default.")

            with open (output_file, 'wb') as img:
                img.write(data)


if __name__ == "__main__":
    main()
