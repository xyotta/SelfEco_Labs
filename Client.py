import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GameClient:
    def __init__(self, api_url="https://127.0.0.1:2999/liveclientdata/allgamedata"):
        self.api_url = api_url
        self.is_connected = False

    def check_connection(self):
        try:
            requests.get(self.api_url, timeout=1, verify=False)
            self.is_connected = True
            return True
        except:
            self.is_connected = False
            return False

    def get_game_data(self):
        if not self.check_connection():
            return None
        try:
            response = requests.get(self.api_url, timeout=1, verify=False)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def parse_player_stats(self, data):
        """
        Шукає гравця у списку allPlayers, щоб дістати правильний CS.
        """
        if not data:
            return 0, 0, 0

        try:
            game_data = data.get('gameData') or {}
            game_time = game_data.get('gameTime', 0)

            active_player = data.get('activePlayer') or {}
            current_gold = active_player.get('currentGold', 0)
            summoner_name = active_player.get('summonerName')

            creep_score = 0
            all_players = data.get('allPlayers', [])

            found = False
            for player in all_players:
                if player.get('summonerName') == summoner_name:
                    scores = player.get('scores', {})
                    creep_score = scores.get('creepScore', 0)
                    found = True
                    break


            if not found:
                scores = active_player.get('scores') or {}
                creep_score = scores.get('creepScore', 0)


            print(f"DEBUG: Name={summoner_name} | Gold={current_gold} | CS={creep_score} | Time={game_time:.1f}")

            return current_gold, creep_score, game_time

        except Exception as e:
            print(f"PARSING ERROR: {e}")
            return 0, 0, 0