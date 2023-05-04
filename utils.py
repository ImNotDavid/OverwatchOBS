import copy

def import_data(file):
    with open(file, "r") as f:
        text = f.readlines()
        text = [line.replace("LÃºcio","Lucio").replace("TorbjÃ¶rn","Torbjorn") for line in text]
    results = []
    for entry in text:
        row =  [e.strip() for e in entry.split(",")]
        time = row[0]
        eventType = row[1]
        data = row[3:]
        results.append({'time':time,'type':eventType,'data':data}) 
    return results

def get_player_stats(base_stats):
    player_stats = [result['data'] for result in base_stats if result['type'] == 'player_stat']
    return player_stats

def get_team_names(base_stats):
    match_start = [result['data'] for result in base_stats if result['type'] == 'match_start'][0]
    teams = [match_start[2],match_start[3]]
    return teams



def get_map_info(base_stats):
    match_info = [result['data'] for result in base_stats if result['type'] == 'match_start'][0]
    name = match_info[0]
    name = name.replace("EsperanÃ§a","Esperanca").replace("Paraíso","Paraiso")
    mode = match_info[1]
    return (name,mode)

def get_map_score(base_stats):
    match_score = [result for result in base_stats if result['type'] == 'match_end'][0]
    time = match_score['time'].replace("[","").replace("]","")
    score1 = int(match_score['data'][1])
    score2 = int(match_score['data'][2])
    if score1>score2:
        #team 1 wins
        winner = 1
    elif score2>score1:
        #team 2 wins
        winner = 2
    else:
        #draw
        winner = 0
    return {'time':time,'score':[score1,score2],'winner':winner}
