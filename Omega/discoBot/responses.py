import lookup, requests
from difflib import get_close_matches

def get_response(message: str) -> str:
    p_message = message.lower()
    playerid = message.split() # split message into a list of words

    if p_message == '!omega whois':
        return 'Omega Bot - Flamingo Services\nOmega is a bot software written by Flamingo and zer0 and is used to calculate player probabilities on them hitting their target. Currently we support NBA and have future plans to add NFL, MLS, MLB, PGA'

    if p_message == '!omega':
        return '`Omega Bot - Flamingo Services\nType "!omega" to access Omega Commands\nType "!omega whois" to access description of the Omega Bot\nType "!omega nba playerids (jayson tatum)" to access playerid\nType "!omega nba stats " for access to all available player stats\nType "!omega nba (playerID) (stat)" to see players stat averages/standard deviations\nType "!omega nba (playerID) (stat(ex: "trb" for rebounds)) (target goal (ex: "11.5"))" to access specific player stats`'
    if p_message == '!omega nba stats':
        return 'stats to choose from include (3p,ft,trb,ast,stl,blk,tov,pts (COMING SOON: ast+trb,pts+ast,pts+trb,pts+trb+ast) '


#nba
    if p_message.startswith('!omega nba '):
        if len(playerid) > 3 and len(playerid) <= 5:
            player_id = playerid[2] # get the third word of the message
            if player_id == 'playerids':
                request = requests.get('https://zerscrpt.cfd/omega/playerID.txt')
                response = request.text
                newResponse = response[:-1]
                ids = []
                names = []

                for line in newResponse.split(sep="\n"):
                    id_, name = line.split(":", 1)
                    ids.append(id_)
                    names.append(name.lower())

                # join the player ID words using a space separator
                player_id_words = ' '.join(playerid[3:])
                player_id_words = player_id_words.replace(' ', '') # remove spaces
                match = get_close_matches(player_id_words.lower(), names, n=1, cutoff=0.8)
                if match:
                    index = names.index(match[0])
                    return f"Player ID of {names[index].title()}: {ids[index]}"
                else:
                    return f"Sorry, could not find a player with name {player_id_words.title()}"

            elif len(playerid) == 3:  # handle basic player average request
                return 'All Target Statistics for player '+player_id+' (Coming Soon)'.format(player_id)
            elif len(playerid) == 4:  # handle player stat average request
                player_stat = playerid[3]
                if player_stat == '3p':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)
                if player_stat == 'ft':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)
                if player_stat == 'trb':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)
                if player_stat == 'ast':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)
                if player_stat == 'blk':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)
                if player_stat == 'tov':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)
                if player_stat == 'pts':
                    var1,var2 = lookup.doLookupMean(player_id,player_stat)
                    return str(player_id) +' average for '+str(player_stat) +' is '+ str(var1) +' and has a standard deviation of '+str(var2)

#target specific probabilities
    if p_message.startswith('!omega nba ') and len(playerid) == 5:
        player_id = playerid[2] # get the target player
        player_stat = playerid[3] # get the player target stat
        player_target = playerid[4] # get the target stat 
        if player_stat == 'stat':
            return player_id+' stats to choose from include (3p,ft,trb,ast,stl,blk,tov,pts - COMING SOON ast+trb,pts+ast,pts+trb,pts+trb+ast) '.format(player_id)
        if player_stat == '3p':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'ft':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'trb':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'ast':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'blk':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'tov':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'pts':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'   
        if player_stat == 'ast+trb':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'pts+ast':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'pts+trb':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        if player_stat == 'pts+trb+ast':
            var1,var2 = lookup.doLookup(player_id,player_stat,player_target)
            return 'the probability of '+str(player_id) +' hitting the target '+str(player_target) +' for '+player_stat + ' is:\nOver: ' + str(var1) + '%\nUnder: ' + str(var2) +'%'
        elif player_stat != '':
            return 'Faulty input try again'

   

    return 

