from game import GameStat
import shutil
import tkinter as tk
from tkinter import ttk
import os
import json
from classes import sup_heroes,dps_heroes,tank_heroes
import datetime

class StatGUI:
    def __init__(self,dir) -> None:
        self.Team1 = ""
        self.Team2 = ""
        self.scoreboard = {"bo":5,"map":0,"score1":0,"score2":0,"tagline":"","swap":0}
        menu_items = [{'text':"Home",'command':self.dummy},
                      {'text':"Bracket",'command':self.dummy},
                      {'text':"Roster",'command':self.roster_page_init},
                      {'text':"Maps",'command':self.dummy},
                      {'text':"In-game","command":self.generate_scoreboard},
                      {'text':"Stats",'command':self.stats_page},
                      {'text':"Replay",'command':self.dummy}]
        self.dir = dir
        self.games = self.update_stats()
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.columnconfigure(0,weight=1,uniform="fred")
        self.root.columnconfigure(1,weight=5,uniform="fred")
        self.root.rowconfigure(0,weight=1)


        self.font = 'Arial'
        menu = self.make_menu(self.root,menu_items,activebackground="grey")
        menu.grid(column=0,row=0,sticky="nwes")

        self.content = tk.Frame(self.root,bg='white')
        self.content.grid(column=1,row=0,sticky="nwes")


        self.root.grid()
        self.root.mainloop()
       

    def make_menu(self,parent,items,**options):
        menu = tk.Frame(parent)
        menu.columnconfigure(0,weight=1)
        for idx,item in enumerate(items):
            menu.rowconfigure(idx,weight=1)
            button = tk.Button(menu,text=item['text'],font=(self.font,16),command=item['command'],**options)
            button.grid(column=0,row=idx,sticky="news")
        return menu
    
    def dummy(self):
        self.content.destroy()
        pass 

    def stats_page(self):

        #Initial page grid setup
        self.update_stats()
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.grid(column=1,row=0,sticky="nwes")
        self.content.rowconfigure(index=0,weight=1,uniform="fred")
        self.content.rowconfigure(index=1,weight=1,uniform="fred")
        self.content.rowconfigure(index=2,weight=1,uniform="fred")
        self.content.rowconfigure(index=3,weight=6,uniform="fred")
        self.content.columnconfigure(index=0,weight=1,uniform="fred")
        self.content.columnconfigure(index=1,weight=1,uniform="fred")
        self.content.columnconfigure(index=2,weight=1,uniform="fred")
        self.content.columnconfigure(index=3,weight=1,uniform="fred")
        self.content.columnconfigure(index=4,weight=1,uniform="fred")

        #Page title
        title = tk.Label(self.content,text="Stats Panel",font=(self.font,18))
        title.grid(column=0,row=0,columnspan=5,sticky="news")
        map_label = tk.Label(self.content,text="Select Map",font=(self.font,14))
        map_label.grid(column=0,row=2,sticky="s")

        #Maps frame
        self.update_maps(self.content)

        


    def update_maps(self,parent):
        menu = tk.Frame(parent)
        menu.columnconfigure(0,weight=1)
        map_names = [game.map for game in self.games]
        for idx,item in enumerate(map_names):
            menu.rowconfigure(idx,weight=1)
            button = tk.Button(menu,text=item,font=(self.font,16),command=lambda item=item: self.update_player1(item,parent))
            button.grid(column=0,row=idx,sticky="news")
        menu.grid(column=0,row=3,sticky="news")
    
    def update_player1(self,map_name,parent):
        print(f"updating players1 for map {map_name}")
        menu = tk.Frame(parent)
        menu.columnconfigure(0,weight=1)
        player_names = [game.teams[0].players for game in self.games if game.map == map_name][0]
        for idx,item in enumerate(player_names):
            menu.rowconfigure(idx,weight=1)
            button = tk.Button(menu,text=item,font=(self.font,16),command=lambda item=item,map_name=map_name: self.update_heroes1(item,map_name,parent))
            button.grid(column=0,row=idx,sticky="news")
        menu.grid(row=3,column=1,sticky="news")
        
        print(f"updating players2 for map {map_name}")
        menu1 = tk.Frame(parent)
        menu1.columnconfigure(0,weight=1)
        player1_names = [game.teams[1].players for game in self.games if game.map == map_name][0]
        for idx,item in enumerate(player1_names):
            menu1.rowconfigure(idx,weight=1)
            button1 = tk.Button(menu1,text=item,font=(self.font,16),command=lambda item=item,map_name=map_name: self.update_heroes2(item,map_name,parent))
            button1.grid(column=0,row=idx,sticky="news")
        menu1.grid(row=3,column=2,sticky="news")
    
    def update_heroes1(self,player,map_name,parent):
        print(f"updating heroes for player1 {player} on map {map_name}")
        menu = tk.Frame(parent)
        menu.columnconfigure(0,weight=1)
        player_stats = [game.teams[0].player_stats for game in self.games if game.map == map_name][0]
        player_heroes = [play.heroes for play in player_stats if play.name == player][0]
        for idx,item in enumerate(player_heroes):
            menu.rowconfigure(idx,weight=1)
            button = tk.Button(menu,text=item,font=(self.font,16),command=lambda item=item,map_name=map_name,player=player: self.stats1(player,item,map_name,parent))
            button.grid(column=0,row=idx,sticky="news")
        menu.grid(row=3,column=3,sticky="news")
    
    def update_heroes2(self,player,map_name,parent):
        print(f"updating heroes for player1 {player} on map {map_name}")
        menu = tk.Frame(parent)
        menu.columnconfigure(0,weight=1)
        player_stats = [game.teams[1].player_stats for game in self.games if game.map == map_name][0]
        player_heroes = [play.heroes for play in player_stats if play.name == player][0]
        for idx,item in enumerate(player_heroes):
            menu.rowconfigure(idx,weight=1)
            button = tk.Button(menu,text=item,font=(self.font,16),command=lambda item=item,map_name=map_name,player=player: self.stats2(hero=item,player=player,map_name=map_name,parent=parent))
            button.grid(column=0,row=idx,sticky="news")
        menu.grid(row=3,column=4,sticky="news")

    def stats1(self,player,hero,map_name,parent):
        popout = tk.Toplevel()
        popout.title(f"stats for {player} playing {hero} on map {map_name}")
        popout.geometry("800x350")
        popout.columnconfigure(index=0,weight=1,uniform="fred")
        popout.columnconfigure(index=1,weight=1,uniform="fred")
        popout.columnconfigure(index=2,weight=1,uniform="fred")
        stats = [game.teams[0].player_stats for game in self.games if game.map == map_name][0]
        player_stats = [game.hero_stats for game in stats if game.name==player][0]
        hero_stats = player_stats[hero].stats
        stat_select = tk.StringVar(popout,"0")
        stats_col=[hero_stats[:11],hero_stats[11:22],hero_stats[22:]]
        for col,stat_list in enumerate(stats_col):
            for row,stat in enumerate(stat_list):
                popout.rowconfigure(row,weight=0,uniform="fred")
                button = tk.Radiobutton(popout,text=f'{stat.name}: {stat.format_value()}',font=(self.font,12),variable=stat_select, value=stat.name, command=lambda map_name=map_name,item=player_stats[hero], special=stat_select.get(): self.export_stats1(item,special,map_name))
                button.grid(row=row,column=col,stick="nw")
    
    def stats2(self,player,hero,map_name,parent):
        popout = tk.Toplevel()
        popout.title(f"stats for {player} playing {hero} on map {map_name}")
        popout.geometry("800x350")
        popout.columnconfigure(index=0,weight=1,uniform="fred")
        popout.columnconfigure(index=1,weight=1,uniform="fred")
        popout.columnconfigure(index=2,weight=1,uniform="fred")
        stats = [game.teams[1].player_stats for game in self.games if game.map == map_name][0]
        player_stats = [game.hero_stats for game in stats if game.name==player][0]
        hero_stats = player_stats[hero].stats
        stat_select = tk.StringVar(popout,"0")
        stats_col=[hero_stats[:11],hero_stats[11:22],hero_stats[22:]]
        for col,stat_list in enumerate(stats_col):
            for row,stat in enumerate(stat_list):
                popout.rowconfigure(row,weight=0,uniform="fred")
                button = tk.Radiobutton(popout,text=f'{stat.name}: {stat.format_value()}',font=(self.font,12),variable=stat_select, value=stat.name, command=lambda map_name=map_name,item=player_stats[hero], special=stat_select.get(): self.export_stats1(item,special,map_name))
                button.grid(row=row,column=col,stick="nw")

    def export_stats1(self,hero_stat,special,map_name):
        player_name = hero_stat.player
        team_name = hero_stat.team
        hero_name = hero_stat.name
        role = hero_stat.role
        currated = hero_stat.get_currated_stats()
        shutil.copy(rf"assets/maps/{map_name}.mp4",r"broadcast/stats/map.mp4")
        shutil.copy(rf"assets/heroes/{hero_name}.png",r"broadcast/stats/hero1.png")
        with open(r"broadcast/stats/player1_name.txt","w") as f:
            f.write(player_name)
        with open(r"broadcast/stats/player1_role.txt","w") as f:
            f.write(role)
        shutil.copy(rf"assets/{role.lower()}.png",f"broadcast/stats/icon1.png")
        with open(r"broadcast/stats/player1_team.txt","w") as f:
            f.write(player_name)
        with open(r"broadcast/stats/player1_tagline.txt","w") as f:
            f.write(f"as {hero_name} on {map_name}".upper())
        for idx,stat in enumerate(currated):
            with open(fr"broadcast/stats/player1_stat{idx+1}_name.txt","w") as f:
                f.write(stat.name.upper().replace("SCOPED CRITICAL HIT ACCURACY","CRITICAL HIT ACCURACY"))
            with open(fr"broadcast/stats/player1_stat{idx+1}_value.txt","w") as f:
                f.write(stat.format_value())
        with open(fr"broadcast/stats/player1_time_played.txt","w") as f:
            played = float([stat for stat in hero_stat.stats if stat.name == "Hero Time Played"][0].format_value())
            played = str(datetime.timedelta(seconds=played))
            played = played[2:-7]
            f.write(played)
        
    def roster_page_init(self):
        #Initial page grid setup
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.grid(column=1,row=0,sticky="nwes")
        self.content.columnconfigure(index=0,weight=1,uniform="fred")
        self.content.columnconfigure(index=1,weight=1,uniform="fred")
        self.content.rowconfigure(index=0,weight=1,uniform="fred")
        self.content.rowconfigure(index=1,weight=8)

        select1 = tk.Label(self.content,text="Select Team 1",font=(self.font,18))
        select1.grid(column=0,row=0,sticky="ws")
        select2 = tk.Label(self.content,text="Select Team 2",font=(self.font,18))
        select2.grid(column=1,row=0,sticky="ws")

        self.update_teams(self.content,0)
        self.update_teams(self.content,1)

    def update_teams(self,parent,side):
        menu = tk.Frame(parent)
        menu.columnconfigure(0,weight=1)
        files = os.listdir('broadcast/teams/')
        teamfiles = [file for file in files if file.endswith(".team")]
        for idx,item in enumerate(teamfiles):
            with open('broadcast/teams/'+item,'r') as f:
                team = json.loads(f.read())
            short = team['name']
            menu.rowconfigure(idx,weight=1)
            button = tk.Button(menu,text=short,font=(self.font,16),command=lambda team=team,side=side:self.select_team(team,side))
            if short == self.Team1 and side == 0:
                button = tk.Button(menu,bg='#ACE7F8',text=short,font=(self.font,16),command=lambda team=team,side=side:self.select_team(team,side))
            if short == self.Team2 and side == 1:
                button = tk.Button(menu,bg='#e5a3a3',text=short,font=(self.font,16),command=lambda team=team,side=side:self.select_team(team,side))
            button.grid(column=0,row=idx,sticky="news")
        button = tk.Button(menu,text="New Team",font=(self.font,16),command=lambda :self.new_team())
        button.grid(column=0,row=len(teamfiles)+1,sticky="news")        
        menu.grid(row=1,column=side,sticky="news")
    

        
    def select_team(self,team,side):
        if side == 0:
            self.Team1 = team['name']
        elif side == 1:
            self.Team2 = team['name']
        with open(f"broadcast/roster/team{side+1}.txt","w") as f:
            max_len = 10
            name = team['abbreviation']
            if len(name) < max_len:
                padding = round((max_len-len(name))/2)
                print(f"{padding} spaces generated for name of len {len(name)}")
                padding = "".join([" " for _ in range(padding)])
                name = padding+name
            f.write(name)
        for idx,player in enumerate(team['players']):
            shutil.copy(rf"assets/{player['role'].lower()}.png",f"broadcast/roster/team{side+1}role{idx+1}.png")
            with open(f"broadcast/roster/team{side+1}player{idx+1}.txt","w") as f:
                f.write(player['name'])
            with open(f"broadcast/roster/team{side+1}role{idx+1}.txt","w") as f:
                f.write(player['role'].replace("DPS","Damage"))
            hero = player['hero']
            if hero == "Soldier: 76":
                hero = "Soldier 76"
            shutil.copy(rf"assets/heroes/{hero}.png",f"broadcast/roster/team{side+1}hero{idx+1}.png")
        self.update_teams(self.content,side)

    def new_team(self):
        #Initial page grid setup
        print("new team")
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.grid(column=1,row=0,sticky="nwes")
        self.content.columnconfigure(index=0,weight=1,uniform="fred")
        self.content.columnconfigure(index=1,weight=1,uniform="fred")
        self.content.columnconfigure(index=2,weight=1,uniform="fred")
        self.content.rowconfigure(index=0,weight=1,uniform="fred")
        self.content.rowconfigure(index=1,weight=1,uniform="fred")
        self.content.rowconfigure(index=2,weight=1,uniform="fred")
        self.content.rowconfigure(index=3,weight=1,uniform="fred")
        self.content.rowconfigure(index=4,weight=1,uniform="fred")
        self.content.rowconfigure(index=5,weight=1,uniform="fred")
        self.content.rowconfigure(index=6,weight=1,uniform="fred")
        self.content.rowconfigure(index=7,weight=1,uniform="fred")
        self.content.rowconfigure(index=8,weight=1,uniform="fred")
        
        
        title = tk.Label(self.content,text="New Team Creation", font=(self.font,18))
        title.grid(row=0,column=0,columnspan=3,sticky="s")

        label1 = tk.Label(self.content,text="Team Name", font=(self.font,16))
        label1.grid(row=1,column=0,columnspan=1,sticky="sw")

        label2 = tk.Label(self.content,text="Short Name", font=(self.font,16))
        label2.grid(row=2,column=0,columnspan=1,sticky="sw")

        label3 = tk.Label(self.content,text="Tank ", font=(self.font,16))
        label3.grid(row=3,column=0,columnspan=1,sticky="sw")

        label4 = tk.Label(self.content,text="DPS 1", font=(self.font,16))
        label4.grid(row=4,column=0,columnspan=1,sticky="sw")

        label5 = tk.Label(self.content,text="DPS 2", font=(self.font,16))
        label5.grid(row=5,column=0,columnspan=1,sticky="sw")

        label6 = tk.Label(self.content,text="Support 1", font=(self.font,16))
        label6.grid(row=6,column=0,columnspan=1,sticky="sw")

        label7 = tk.Label(self.content,text="Support 2", font=(self.font,16))
        label7.grid(row=7,column=0,columnspan=1,sticky="sw")

        label8 = tk.Label(self.content,text="Society Name", font=(self.font,16))
        label8.grid(row=8,column=0,columnspan=1,sticky="sw")

        name = tk.StringVar(self.content)
        short = tk.StringVar(self.content)
        tank = tk.StringVar(self.content)
        dps1 = tk.StringVar(self.content)
        dps2 = tk.StringVar(self.content)
        sup1 = tk.StringVar(self.content)
        sup2 = tk.StringVar(self.content)
        soc = tk.StringVar(self.content)
        tankhero = tk.StringVar(self.content)
        dpshero1 = tk.StringVar(self.content)
        dpshero2 = tk.StringVar(self.content)
        suphero1 = tk.StringVar(self.content)
        suphero2 = tk.StringVar(self.content)
        

        e1 = tk.Entry(self.content, text="Team name",font=(self.font,16),textvariable=name).grid(row=1,column=1,columnspan=1,sticky="EWS")
        e2 = tk.Entry(self.content, text="Short name",font=(self.font,16),textvariable=short).grid(row=2,column=1,columnspan=1,sticky="esw")
        e3 = tk.Entry(self.content, text="Player name",font=(self.font,16),textvariable=tank).grid(row=3,column=1,columnspan=1,sticky="esw")
        e4 = tk.Entry(self.content, text="Player name",font=(self.font,16),textvariable=dps1).grid(row=4,column=1,columnspan=1,sticky="esw")
        e5 = tk.Entry(self.content, text="Player name",font=(self.font,16),textvariable=dps2).grid(row=5,column=1,columnspan=1,sticky="esw")
        e6 = tk.Entry(self.content, text="Player name",font=(self.font,16),textvariable=sup1).grid(row=6,column=1,columnspan=1,sticky="esw")
        e7 = tk.Entry(self.content, text="Player name",font=(self.font,16),textvariable=sup2).grid(row=7,column=1,columnspan=1,sticky="esw")
        e8 = tk.Entry(self.content, text="Society name",font=(self.font,16),textvariable=soc).grid(row=8,column=1,columnspan=1,sticky="esw")

        heroselect1 = tk.OptionMenu(self.content, tankhero, *tank_heroes).grid(row=3,column=2,columnspan=1,sticky="EWS")
        dpsselect1 = tk.OptionMenu(self.content, dpshero1, *dps_heroes).grid(row=4,column=2,columnspan=1,sticky="EWS")
        dpsselect2 = tk.OptionMenu(self.content, dpshero2, *dps_heroes).grid(row=5,column=2,columnspan=1,sticky="EWS")
        supselect1 = tk.OptionMenu(self.content, suphero1, *sup_heroes).grid(row=6,column=2,columnspan=1,sticky="EWS")
        supselect2 = tk.OptionMenu(self.content, suphero2, *sup_heroes).grid(row=7,column=2,columnspan=1,sticky="EWS")
        def export_values():
            print("SOC ="+soc.get())
            players = [{"name":tank.get(),"hero":tankhero.get(),"role":"Tank"},
                    {"name":dps1.get(),"hero":dpshero1.get(),"role":"DPS"},
                    {"name":dps2.get(),"hero":dpshero2.get(),"role":"DPS"},
                    {"name":sup1.get(),"hero":suphero1.get(),"role":"Support"},
                    {"name":sup2.get(),"hero":suphero2.get(),"role":"Support"},]

            team={"society":soc.get(),"name":name.get(),"abbreviation":str(short.get()),"players":players}
            self.submit_team(team)

        submit = tk.Button(self.content,text="Submit",font=(self.font,18),command=export_values)
        submit.grid(row=8,column=2,sticky="news")

    def submit_team(self,team):
        with open('broadcast/teams/'+team['abbreviation']+".team","w") as f:
            print(team)
            f.write(json.dumps(team,default=str))
        print("submitted")
        self.roster_page_init()

    def update_stats(self):
        files = os.listdir(self.dir)
        map_files = [file for file in files if file.endswith(".txt")]
        self.games = [GameStat(self.dir+"/"+file) for file in map_files]

    def generate_scoreboard(self):
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.grid(column=1,row=0,sticky="nwes")
        self.content.columnconfigure(index=0,weight=1,uniform="fred")
        self.content.columnconfigure(index=1,weight=1,uniform="fred")
        self.content.columnconfigure(index=2,weight=1,uniform="fred")
        self.content.rowconfigure(index=0,weight=1,uniform="fred")

        middle = tk.Frame(self.content)
        middle.grid(row=0,column=1,sticky="news")

        middle.columnconfigure(index=0,weight=1,uniform="fred")
        middle.rowconfigure(index=0,weight=1,uniform="fred")
        middle.rowconfigure(index=1,weight=1,uniform="fred")
        middle.rowconfigure(index=2,weight=1,uniform="fred")
        middle.rowconfigure(index=3,weight=1,uniform="fred")
        middle.rowconfigure(index=4,weight=1,uniform="fred")
        middle.rowconfigure(index=5,weight=1,uniform="fred")
        middle.rowconfigure(index=6,weight=1,uniform="fred")

        bo_label = tk.Label(middle,text="Best of ?",font=(self.font,18))
        bo_label.grid(row=0,column=0,sticky="s")

        bo = tk.StringVar(middle,self.scoreboard['bo'])
        bo_picker = tk.Spinbox(middle,from_=0, to=9,textvariable=bo,command = lambda bo=bo: self.update_bo(bo),font=(self.font,14))
        bo_picker.grid(row=1,column=0,sticky="news")

        map_label = tk.Label(middle,text="Current Map",font=(self.font,16))
        map_label.grid(row=2,column=0,sticky="s")

        current_map = tk.StringVar(middle,self.scoreboard['map'])
        map_picker = tk.Spinbox(middle,from_=0, to=bo.get(),textvariable=current_map,command = lambda current_map=current_map: self.update_map_scoreboard(current_map),font=(self.font,14))
        map_picker.grid(row=3,column=0,sticky="news")

        tag_label = tk.Label(middle,text="Tagline",font=(self.font,16))
        tag_label.grid(row=4,column=0,sticky="s")
        
        
        tagline = tk.StringVar(middle,self.scoreboard['tagline'])
        def update_tagline(var, index, mode):
            self.scoreboard['tagline'] = tagline.get()
        tagline_e = tk.Entry(middle,textvariable=tagline,font=(self.font,14),)
        tagline_e.grid(row=5,column=0,sticky="news")
        tagline.trace_add("write",update_tagline)

        swap = tk.Button(middle,text="Swap Teams",font=(self.font,16),command=self.swap_teams)
        swap.grid(column=0,row=6,sticky="news")

        update = tk.Button(self.content, text="Update",font=(self.font,16),command=self.update_scoreboard)
        update.grid(column=2,row=1,stick="news")

        reset = tk.Button(self.content, text="Reset",font=(self.font,16),command=self.reset_scoreboard)
        reset.grid(column=0,row=1,stick="news")
        self.generate_scoreboard_left()
        self.generate_scoreboard_right()

    def generate_scoreboard_left(self,swap=0):
        left = tk.Frame(self.content)
        left.grid(row=0,column=2*swap,sticky="news")
    
        left.columnconfigure(index=0,weight=1,uniform="fred")
        left.rowconfigure(index=0,weight=1,uniform="fred")
        left.rowconfigure(index=1,weight=1,uniform="fred")
        left.rowconfigure(index=2,weight=1,uniform="fred")
        left.rowconfigure(index=3,weight=1,uniform="fred")

        team_name = tk.Label(left,text=self.Team1,font=(self.font,16))
        team_name.grid(row=0,column=0,sticky="s")

        score_left = tk.StringVar(left,self.scoreboard['score1'])
        score_picker = tk.Spinbox(left,from_=0, to=self.scoreboard['bo'],textvariable=score_left,command = lambda score_left=score_left: self.update_score(score_left,0),font=(self.font,14))
        score_picker.grid(row=1,column=0,sticky="news")

    def generate_scoreboard_right(self,swap=0):
        right = tk.Frame(self.content)
        right.grid(row=0,column=2*(1-swap),sticky="news")
    
        right.columnconfigure(index=0,weight=1,uniform="fred")
        right.rowconfigure(index=0,weight=1,uniform="fred")
        right.rowconfigure(index=1,weight=1,uniform="fred")
        right.rowconfigure(index=2,weight=1,uniform="fred")
        right.rowconfigure(index=3,weight=1,uniform="fred")

        team_name = tk.Label(right,text=self.Team2,font=(self.font,16))
        team_name.grid(row=0,column=0,sticky="s")

        score_right = tk.StringVar(right,self.scoreboard['score2'])
        score_picker = tk.Spinbox(right,from_=0, to=self.scoreboard['bo'],textvariable=score_right,command = lambda score_right=score_right: self.update_score(score_right,1),font=(self.font,14))
        score_picker.grid(row=1,column=0,sticky="news")

    def swap_teams(self):
        self.scoreboard['swap'] = 1 if self.scoreboard['swap'] == 0 else 0
        self.generate_scoreboard_left(swap=self.scoreboard['swap'])
        self.generate_scoreboard_right(swap=self.scoreboard['swap'])
        pass
        
    def update_score(self, score,side):
        if side==0:
            self.scoreboard['score1']=score.get()
        elif side==1:
            self.scoreboard['score2']=score.get()

    def update_bo(self,bo):
        self.scoreboard['bo'] = bo.get()

    def update_map_scoreboard(self,current_map):
        self.scoreboard['map'] = current_map.get()

    def update_scoreboard(self):
        if self.scoreboard['swap'] == 0:
            with open("broadcast/scoreboard/team1_name.txt","w",encoding="utf8") as f:
                pad = 20-len(self.Team1)
                pad = ''.join(["⠀" for _ in range(pad)])
                f.write(pad+self.Team1)
            with open("broadcast/scoreboard/team2_name.txt","w") as f:
                f.write(self.Team2)
            with open("broadcast/scoreboard/score1.txt","w") as f:
                f.write(str(self.scoreboard['score1']))
            with open("broadcast/scoreboard/score2.txt","w") as f:
                f.write(str(self.scoreboard['score2']))
        elif self.scoreboard['swap'] == 1:
            with open("broadcast/scoreboard/team1_name.txt","w",encoding="utf8") as f:
                pad = 20-len(self.Team2)
                pad = ''.join(["⠀" for _ in range(pad)])
                f.write(pad+self.Team2)
            with open("broadcast/scoreboard/team2_name.txt","w") as f:
                f.write(self.Team1)
            with open("broadcast/scoreboard/score1.txt","w") as f:
                f.write(str(self.scoreboard['score2']))
            with open("broadcast/scoreboard/score2.txt","w") as f:
                f.write(str(self.scoreboard['score1']))
        with open("broadcast/scoreboard/map_line.txt","w") as f:
            f.write(f'Map {self.scoreboard["map"]} - Best of {self.scoreboard["bo"]}')
        with open("broadcast/scoreboard/tagline.txt","w",encoding="utf-8") as f:
            pad = 13-int(len(self.scoreboard['tagline'])/2)
            pad = ''.join(["⠀" for _ in range(pad)])
            tagline = pad+self.scoreboard['tagline']
            f.write(tagline)
                
        

    def reset_scoreboard(self):
        self.scoreboard={"bo":5,"map":0,"score1":0,"score2":0,"tagline":"","swap":0}
        self.generate_scoreboard()
    
    

StatGUI(r'C:\Users\david\OneDrive\Documents\Overwatch\Workshop\Youscrim')