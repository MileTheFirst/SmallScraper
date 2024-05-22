from bs4 import BeautifulSoup
import requests

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

teams_in_games = []

def get_html(url):
    response = requests.get(url, headers=headers)

    with open("data/index.html", "w") as file:
        file.write(response.text)


def get_data():
    with open("data/index.html", "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, "lxml")

    ul_games = soup.find("ul", class_ = "ui-dashboard-champ__games")

    games_list = ul_games.find_all("li", class_="ui-dashboard-game dashboard-game")

    for game_li in games_list:
        teams_divs = game_li.find("span", class_= "team-scores__teams team-scores-teams").find_all("span", class_="caption__label")

        teams_in_games.append([team.text.strip() for team in teams_divs])
        
    print(teams_in_games)


def main():
    get_html("https://1xlite-650927.top/ru/live/fifa/2627439-fc24-penalty")
    get_data()

if __name__ == "__main__":
    main()