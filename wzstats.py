import asyncio
import json
import callofduty
import csv
import re
import config

from callofduty import Mode, Platform, Title

async def main():

    ## credentials for https://my.callofduty.com/login
    email = config.email
    password = config.password

    client = await callofduty.Login(email, password)

    myTeamSummary = []

    while True:
        playerName = input("Enter your activision name (case sensitive): ")
        playerId = input ("Enter your activision id (press enter if none): ")
        username = playerName

        if len(playerId):
            username = playerName + "#" + playerId

        player = await client.GetPlayer(Platform.Activision, username)

        ## repeats user input prompt if user not found
        try:
            await (player.profile(Title.ModernWarfare, Mode.Warzone))
        except Exception:
            print("User not found. Please try again")
            continue
        else:
            break
    
    print ("fetching warzone team summary...")

    ## getting most recent WZ match
    recentGameIndex = 0
    isBattleRoyale = False

    ## only want Battle Royale matches
    ## breaks if not duos/trios/quads, hence this mode check
    while (not(isBattleRoyale)):
        match = (await player.matches(Title.ModernWarfare, Mode.Warzone, limit = 100))[recentGameIndex] ## limit set to 100 in case the player went on a non-BR binge
        match = await client.GetFullMatch(Platform.Activision, Title.ModernWarfare, Mode.Warzone, match.id)
        
        gameMode = match["allPlayers"][0]["mode"]
        if (re.search("^br_br.*", gameMode)):
            break
        else:
            recentGameIndex += 1

    ## fetching the team placement of the desired player
    ## tedious workaround because the teams() method doesn't work for wz
    teamPlacement = None
    for player in match["allPlayers"]:
        if (player["player"]["username"]) == playerName:
            teamPlacement = player["playerStats"]["teamPlacement"]
            break

    ## fetching players in the squad that got the teamPlacement from above
    for player in match["allPlayers"]:
        if (player["playerStats"]["teamPlacement"]) == teamPlacement:
            member = {
                "player": player["player"]["username"],
                "kills": int(player["playerStats"]["kills"]),
                "damage": int(player["playerStats"]["damageDone"])
            }
            myTeamSummary.append(member)

    with open('warzonesummary.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Team', 'Kills', 'Damage'])

        for member in myTeamSummary:
            player = member["player"]
            kills = member["kills"]
            damage = member["damage"]

            writer.writerow([player, kills, damage])
        
        writer.writerow(['Placement', teamPlacement])
    
    print ("Done! Please check the warzonesummary.csv file")

asyncio.get_event_loop().run_until_complete(main())