import requests
import time
import os

def get_tv_seasons_titles(tmdb_id, api_key, language):
    url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={api_key}&language={language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        seasons = data.get('seasons', [])
        season_details = []
        for season in seasons:
            season_number = season['season_number']
            season_name = season['name']
            season_year = season['air_date'][:4] if season['air_date'] else "未知年份"
            season_info = f"第 {season_number} 季 ({season_year})"
            episodes = get_season_episodes(tmdb_id, season_number, api_key, language)
            season_details.append((season_info, episodes))
        return season_details
    else:
        print(f"Error: Unable to fetch data for TMDb ID {tmdb_id}")
        return []

def get_season_episodes(tmdb_id, season_number, api_key, language):
    url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season_number}?api_key={api_key}&language={language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        episodes = data.get('episodes', [])
        episode_titles = [f"{season_number}-{episode['episode_number']} {episode['name']}" for episode in episodes]
        return episode_titles
    else:
        print(f"Error: Unable to fetch episodes for season {season_number}")
        return []

def save_to_file(tmdb_id, season_details):
    output_dir = os.path.join(os.getcwd(), "tmdbid_title")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"tmdb_{tmdb_id}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        for season_info, episodes in season_details:
            file.write(season_info + "\n")
            for episode in episodes:
                file.write(episode + "\n")
            file.write("\n")  # Add a blank line between seasons
    return file_path

def check_api_key(api_key):
    url = f"https://api.themoviedb.org/3/configuration?api_key={api_key}"
    response = requests.get(url)
    return response.status_code == 200

def main():
    api_key_file = "api_key.txt"
    if not os.path.exists(api_key_file):
        with open(api_key_file, "w", encoding="utf-8") as file:
            file.write("api_key:\nlanguage:zh-CN\n")

    with open(api_key_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        api_key = lines[0].strip().split(":")[1].strip()
        language = lines[1].strip().split(":")[1].strip()

    if not api_key:
        api_key = input("请输入你的TMDb API密钥: ")
        while not check_api_key(api_key):
            print("API密钥无效，请重新输入。")
            api_key = input("请输入有效的TMDb API密钥: ")
        with open(api_key_file, "w", encoding="utf-8") as file:
            file.write(f"api_key:{api_key}\nlanguage:{language}\n")
    else:
        if not check_api_key(api_key):
            print("存储的API密钥无效。")
            api_key = input("请输入有效的TMDb API密钥: ")
            while not check_api_key(api_key):
                print("API密钥无效，请重新输入。")
                api_key = input("请输入有效的TMDb API密钥: ")
            with open(api_key_file, "w", encoding="utf-8") as file:
                file.write(f"api_key:{api_key}\nlanguage:{language}\n")

    user_language = input(f"请输入语言（默认 {language}）: ").strip()
    if user_language and user_language != language:
        language = user_language
        with open(api_key_file, "w", encoding="utf-8") as file:
            file.write(f"api_key:{api_key}\nlanguage:{language}\n")

    tmdb_ids = input("请输入TMDb ID（多个ID用逗号或空格隔开）: ").replace(',', ' ').split()
    for tmdb_id in tmdb_ids:
        tmdb_id = tmdb_id.strip()
        season_details = get_tv_seasons_titles(tmdb_id, api_key, language)
        if season_details:
            file_path = save_to_file(tmdb_id, season_details)
            print(f"TMDb ID {tmdb_id} 的数据已保存到 {file_path}")
        else:
            print(f"未能获取到TMDb ID {tmdb_id} 的数据。")
        time.sleep(2)  # 等待2秒以避免API调用过于频繁

    print(f"所有数据已保存到 {os.path.join(os.getcwd(), 'tmdbid_title')} 文件夹中。")

if __name__ == "__main__":
    main()
