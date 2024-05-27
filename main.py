from bs4 import BeautifulSoup
import requests
import json


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    with open("data/index.html", "w") as file:
        file.write(response.text)

def get_json():
    import requests

    headers = {
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'accept': 'application/json, text/plain, */*',
        'Referer': 'https://1xlite-650927.top/ru/live/fifa/2627439-fc24-penalty',
        'x-requested-with': 'XMLHttpRequest',
        'x-hd': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWlkIjoiT2FhMDNJMXlYemdBTHNPaEFRb1R1bXRZTVU3Y0hMcGI0SUlHKzBGV0RPWlJUeDlENmJYakZpY2NHd2FCVDBmWG85dzFLOHpoeFU4TlVnclRnMHgxcVFWbU5YdGtCSmVLNkx6N0tySG12a0FNdTc4RGx3YWE2US9tL0hTaGNOTHFOSExyNWx5S3VSa0VmUzVTV0I3SW41TVc1NEdieW9Ka24xQUN4a0dGMk16U2EvdnA2cEQwWTR6VmE1aTEyaXdBbFBBMm5nWTFqRTdoTkV2N1BRUVJ2clp4ODFtZXFkc1BIZkdnTXdoVGYvQzhIdmhKVXMwc1c2RGd6dG1KQU4xR2ZqWGsrNmV5UkhXRGNvTDBDZmdVbVNzMTR5SjMxbTF1TE82Mk5jbW5mekExdGlXLytzSXRYSzNxZkRyR1RpTHNUdk11VXRGOGM4M2tscDBpZUJ5cDRzS3RNemc2T2Zjck5wcGpDOWhHQkp5WStnbmFCMmVNMGVPRyt6aWNtR0hrVGZ6MkNZTVZmWTEvQzc0emUvY3EvMFNMWHB1WiIsImV4cCI6MTcxNjY3NDQxNiwiaWF0IjoxNzE2NjYwMDE2fQ.HgYySw_h6JIGmjt2VVJo_eTPRYsR16HhHiojl7QOdtO4b38PYJZepcwO13JuHe0cLwaZ7xzyZ-OUSJSFwGAOtw',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'sports': '85',
        'champs': '2627439',
        'count': '20',
        'gr': '285',
        'mode': '4',
        'country': '1',
        'getEmpty': 'true',
        'virtualSports': 'true',
        'noFilterBlockEvent': 'true',
    }

    response = requests.get('https://1xlite-650927.top/service-api/LiveFeed/Get1x2_VZip', params=params, headers=headers)

    with open("data/json.json", "w") as file:
        file.write(json.dumps(response.json(), indent=4))



def get_data() -> list:
    games_data = []

    with open("data/index.html", "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, "lxml")

    ul_games = soup.find("ul", class_ = "ui-dashboard-champ__games")
    games_list = ul_games.find_all("li", class_="ui-dashboard-game dashboard-game")

    for game_li in games_list:
        game_data_dict = {}

        teams_names_divs = game_li.find("span", class_= "team-scores__teams team-scores-teams").find_all("span", class_="caption__label")
        game_data_dict["teams"] = [team.text.strip() for team in teams_names_divs]

        score_spans = game_li.find_all("span", class_= "game-scores__num")
        game_data_dict["scores"] = [score_span.text.strip() for score_span in score_spans]

        games_data.append(game_data_dict)


    with open("data/json.json", "r") as file:
        json_data = json.load(file)
        
    for i, game_dict in enumerate(json_data["Value"]):
        win1 = game_dict["AE"][0]["ME"][0]["C"]
        win2 = game_dict["AE"][0]["ME"][1]["C"]

        total_ME = game_dict["AE"][1]["ME"]
        total_coefs = {}

        j=0
        while j < len(total_ME):
            total_coefs[str(total_ME[j]["P"])] = [total_ME[j]["C"], total_ME[j+1]["C"]]
            j+=2

        games_data[i]["wins"] = [win1, win2]
        games_data[i]["totals"] = total_coefs

    return games_data

def print_data(games_data: list):
    for game_data in games_data:
        print("\n")
        print(f'{game_data["teams"][0]} ({game_data["scores"][0]}:{game_data["scores"][1]}) {game_data["teams"][1]}')
        print(f' П1    {game_data["wins"][0]}     П2 {game_data["wins"][1]}')

        for total_param, total_coefs in game_data["totals"].items():
            print(f'ТБ {total_param.replace(".", ",")}  @{total_coefs[0]}     ТМ {total_param.replace(".", ",")}  @{total_coefs[1]}')
            

def main():
    get_html("https://1xlite-650927.top/ru/live/fifa/2627439-fc24-penalty")
    get_json()
    games_data = get_data()

    print_data(games_data)

if __name__ == "__main__":
    main()