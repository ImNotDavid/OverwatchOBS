import utils
from classes import attributes, Team

class GameStat:
    def __init__(self,file) -> None:
        base_data = utils.import_data(file)
        base_player_data = utils.get_player_stats(base_data)
        teamNames = utils.get_team_names(base_data)
        self.teams = [Team(name,base_player_data=base_player_data) for name in teamNames]
        self.map,self.mode = utils.get_map_info(base_data)
        score_info = utils.get_map_score(base_data)
        winner = score_info['winner']
        if winner == 0:
            self.winner = "Draw"
        else:
            self.winner = teamNames[winner-1]
        self.score = {teamNames[0]:score_info['score'][0],teamNames[1]:score_info['score'][1]}
        self.duration = score_info['time']
        
        