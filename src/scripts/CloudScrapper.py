import pandas as pd
import difflib
import os
import requests
import concurrent.futures
import re

# Load datasets
df_stats = pd.read_csv('FIFA WC 2022 Players Stats.csv', encoding='latin1')
df_ids = pd.read_csv('fifa_wc_players_with_ids_improved.csv', encoding='latin1')


def norm(name): return str(name).lower().strip()


df_stats['norm_name'] = df_stats['Player Name '].apply(norm)
df_ids['norm_name'] = df_ids['player_name'].apply(norm)
id_map = dict(zip(df_ids['norm_name'], df_ids['player_id']))


def get_best_match(name, choices):
    if name in choices: return name
    matches = difflib.get_close_matches(name, choices, n=1, cutoff=0.65)
    return matches[0] if matches else None


output_dir = 'player_images'
os.makedirs(output_dir, exist_ok=True)
download_tasks = []

for _, row in df_stats.iterrows():
    player_name = str(row['Player Name ']).strip()
    safe_name = re.sub(r'[^a-zA-Z0-9_ -]', '', player_name).strip().replace(" ", "_")
    best_match = get_best_match(row['norm_name'], list(id_map.keys()))
    player_id = id_map.get(best_match) if best_match else None

    if pd.notna(player_id):
        pid_str = str(int(player_id)).zfill(6)
        img_url = f"https://cdn.sofifa.net/players/{pid_str[:3]}/{pid_str[3:6]}/22_240.png"
        file_path = os.path.join(output_dir, f"{safe_name}.png")
        download_tasks.append((img_url, file_path))


def download_image(task):
    url, path = task
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://sofifa.com/'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            return True
    except:
        pass
    return False


# Download concurrently for speed
print("Downloading 814 images... Please wait.")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(download_image, download_tasks))
print(f"Success! Downloaded {sum(results)} images to the 'player_images' folder.")