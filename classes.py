import json

attributes =    ["Eliminations",
                "Final Blows",
                "Deaths",
                "All Damage Dealt",
                "Barrier Damage Dealt",
                "Hero Damage Dealt",
                "Healing",
                "Healing Recieved",
                "Self Healing",
                "Damage Taken",
                "Damage Blocked",
                "Defensive Assists",
                "Offensive Assists",
                "Ultimates Earned",
                "Ultimates Used",
                "Multikill Best",
                "Multikills",
                "Solo Kills",
                "Objective Kills",
                "Environmental Kills",
                "Environmental Deaths",
                "Critical Hits",
                "Critical Hit Accuracy",
                "Scoped Accuracy",
                "Scoped Critical Hit Accuracy",
                "Scoped Critical Hit Kills",
                "Shots Fired",
                "Shots Hit",
                "Shots Missed",
                "Scoped Shots Fired",
                "Scoped Shots Hit",
                "Weapon Accuracy",
                "Hero Time Played"]

positive = ["Eliminations",
            "Final Blows",
            "All Damage Dealt",
            "Barrier Damage Dealt",
            "Hero Damage Dealt",
            "Healing",
            "Self Healing",
            "Damage Blocked",
            "Defensive Assists",
            "Offensive Assists",
            "Ultimates Earned",
            "Ultimates Used",
            "Multikill Best",
            "Multikills",
            "Solo Kills",
            "Objective Kills",
            "Environmental Kills",
            "Critical Hits",
            "Critical Hit Accuracy",
            "Scoped Accuracy",
            "Scoped Critical Hit Accuracy",
            "Scoped Critical Hit Kills",
            "Shots Fired",
            "Shots Hit",
            "Scoped Shots Fired",
            "Scoped Shots Hit",
            "Weapon Accuracy",
            "Hero Time Played"]

intStats = ["Eliminations",
            "Final Blows",
            "Deaths",
            "Defensive Assists",
            "Offensive Assists",
            "Ultimates Earned",
            "Ultimates Used",
            "Multikill Best",
            "Multikills",
            "Solo Kills",
            "Objective Kills",
            "Environmental Kills",
            "Environmental Deaths",
            "Critical Hits",
            "Scoped Critical Hit Kills",
            "Shots Fired",
            "Shots Hit",
            "Shots Missed",
            "Scoped Shots Fired",
            "Scoped Shots Hit"]

floatStats = ["All Damage Dealt",
            "Barrier Damage Dealt",
            "Hero Damage Dealt",
            "Healing",
            "Healing Recieved",
            "Self Healing",
            "Damage Taken",
            "Damage Blocked",
            "Hero Time Played"]

accStats = ["Critical Hit Accuracy",
            "Scoped Accuracy",
            "Scoped Critical Hit Accuracy",
            "Weapon Accuracy"]

tankStats = ["Hero Damage Dealt",
            "Damage Blocked",
            "Eliminations"]

dpsStats = ["Hero Damage Dealt",
            "Final Blows",
            "Ultimates Used"]

supStats = ["Hero Damage Dealt",
            "Healing",
            "Ultimates Used"]

heroStats = {"Ashe":{"role":"dps","stat":"Critical Hit Accuracy"},
             "Bastion":{"role":"dps","stat":"Weapon Accuracy"},
             "Cassidy":{"role":"dps","stat":"Critical Hit Accuracy"},
             "Echo":{"role":"dps","stat":"Ultimates Used"},
             "Genji":{"role":"dps","stat":"Solo Kills"},
             "Hanzo":{"role":"dps","stat":"Critical Hits"},
             "Junkrat":{"role":"dps","stat":"Solo Kills"},
             "Mei":{"role":"dps","stat":"Self Healing"},
             "Pharah":{"role":"dps","stat":"Ultimates Used"},
             "Reaper":{"role":"dps","stat":"Weapon Accuracy"},
             "Sojourn":{"role":"dps","stat":"Critical Hit Accuracy"},
             "Soldier: 76":{"role":"dps","stat":"Weapon Accuracy"},
             "Sombra":{"role":"dps","stat":"Ultimates Used"},
             "Symmetra":{"role":"dps","stat":"Weapon Accuracy"},
             "Torbjorn":{"role":"dps","stat":"Ultimates Used"},
             "Tracer":{"role":"dps","stat":"Weapon Accuracy"},
             "Widowmaker":{"role":"dps","stat":"Scoped Critical Hit Accuracy"},
             "D.Va":{"role":"tank","stat":"Ultimates Used"},
             "Doomfist":{"role":"tank","stat":"Ultimates Used"},
             "Junker Queen":{"role":"tank","stat":"Healing"},
             "Orisa":{"role":"tank","stat":"Damage Taken"},
             "Ramattra":{"role":"tank","stat":"Ultimates Used"},
             "Reinhardt":{"role":"tank","stat":"Ultimates Used"},
             "Roadhog":{"role":"tank","stat":"Healing"},
             "Sigma":{"role":"tank","stat":"Ultimates Used"},
             "Winston":{"role":"tank","stat":"Weapon Accuracy"},
             "Wrecking Ball":{"role":"tank","stat":"Weapon Accuracy"},
             "Zarya":{"role":"tank","stat":"Defensive Assists"},
             "Ana":{"role":"support","stat":"Offensive Assists"},
             "Baptiste":{"role":"support","stat":"Critical Hit Accuracy"},
             "Brigitte":{"role":"support","stat":"Damage Blocked"},
             "Kiriko":{"role":"support","stat":"Critical Hit Accuracy"},
             "Lifeweaver":{"role":"support","stat":"Offensive Assists"},
             "Lucio":{"role":"support","stat":"Environmental Kills"},
             "Mercy":{"role":"support","stat":"Ultimates Used"},
             "Moira":{"role":"support","stat":"Ultimates Used"},
             "Zenyatta":{"role":"support","stat":"Weapon Accuracy"}}
tank_heroes = ["D.Va", "Doomfist", "Junker Queen", "Orisa", "Ramattra", "Reinhardt", "Roadhog", "Sigma", "Winston","Wrecking Ball","Zarya"]
dps_heroes = ["Ashe","Bastion","Cassidy","Echo","Genji","Hanzo","Junkrat","Mei","Pharah","Reaper","Sojourn","Soldier: 76","Sombra","Symmetra","Torbjorn","Tracer","Widowmaker"]
sup_heroes = ["Ana","Baptiste","Brigitte","Kiriko","Lifeweaver","Lucio","Mercy","Moira","Zenyatta"]
alias={"Team 1":"Team 1",
       "Team 2":"Team 2",
       "Chem":"RCSU Chemistry",
       "Bio":"RCSU Biology"}

class Stat:
    def __init__(self,name,value) -> None:
        self.name=''
        if name in attributes:
            self.name = name
        else:
            raise(f"AttributeExecption: {name} is not a valid stat type")
        if self.name in positive : 
            #Higher stat is better
            self.compare = True
        else:
            #Lower stat is better
            self.compare = False
        try:
            self.value = float(value)
        except:
            self.value = 0.00
        self.type = self.set_type()
    
    def format_value(self):
        #return the string formatted stat value
        if self.name in intStats:
            return str(round(self.value))
        elif self.name in floatStats:
            return str(round(self.value,2))
        elif self.name in accStats:
            return f"{round(self.value*100)}%"
        else:
            return "[REDACTED]"
        
    def set_type(self):
        #return the type of stat int, float, acc
        if self.name in intStats:
            return "int"
        elif self.name in floatStats:
            return "float"
        elif self.name in accStats:
            return "acc"
        else:
            return "noType"

class HeroStat:
    def __init__(self,data) -> None:
        #takes a list of data and outputs specific hero stats
        meta = data[0][:4]
        self.team = meta[1]
        self.player = meta[2]
        self.name = meta[3]
        self.stats = []
        self.role = heroStats[self.name]['role']
        stats = data[0][4:]
        for idx,s in enumerate(stats):
            #go through each stat
            self.stats.append(Stat(attributes[idx],s))
        self.currated = self.get_currated_stats()
    def get_currated_stats(self):
        #return hero specific stats
        hero_name = self.name
        hero_attributes = heroStats[hero_name]
        role = hero_attributes['role']
        heroStat = hero_attributes['stat']
        if role == "dps":
            roleStats = dpsStats
        elif role == "tank":
            roleStats = tankStats
        else:
            roleStats = supStats
        res = []
        for s in roleStats:
            res.append(self.get_stat(s))
        res.append(self.get_stat(heroStat))
        res.append(self.get_stat("Deaths"))
        return res

    def get_stat(self, stat_name):
        return [stat for stat in self.stats if stat.name==stat_name][0]
        

class Player:
    def __init__(self, name, data) -> None:
        #takes all data and outputs a list of hero stats along with total stats
        player_data = [d for d in data if d[2] == name]
        self.name=name
        self.heroes = list(set([d[3] for d in player_data]))
        self.hero_stats = {}
        for hero in self.heroes:
            hero_data = [d for d in player_data if d[3] == hero]
            self.hero_stats[hero] = HeroStat(hero_data)
        

class Team: 
    def __init__(self, name, base_player_data) -> None:
        team_player_data=[data for data in base_player_data if data[1] == name]
        self.name = name
        #self.alias = alias[name]
        self.players = list(set([data[2] for data in base_player_data if data[1] == name]))
        self.player_stats = [Player(name,team_player_data) for name in self.players]

class Roster:
    def __init__(self,society,name,abbreviation,players):
        self.society = society
        self.name = name
        self.abbreviation = abbreviation
        self.players = players
    def export(self,file):
        with open(file,"w") as f:
            roster = {"society":self.society,
                      "name":self.name,
                      "abbreviation":self.abbreviation,
                      "players":self.players}
            f.write(json.dumps(roster))

            


