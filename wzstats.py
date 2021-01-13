import asyncio
import json
import callofduty

from callofduty import Mode, Platform, Title

async def main():
    client = await callofduty.Login("eye-cream@hotmail.com", "KxwWthqr3LxG2fD")

    myTeamSummary = []

    # playerName = "Kobe Bryant"
    # playerId = "3528767"

    playerName = input("Enter your in-game name (case sensitive): ")
    playerId = input("Enter your unique playerID beside your in-game name: ")
    username = playerName + "#" + playerId

    player = await client.GetPlayer(Platform.Activision, username)

    ## getting most recent WZ match
    match = (await player.matches(Title.ModernWarfare, Mode.Warzone, limit = 1))[0]
    match = await client.GetFullMatch(Platform.Activision, Title.ModernWarfare, Mode.Warzone, match.id)

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
    
    ## this extra print statement just for better visibility in the terminal
    print ()
    print ('Placement:', int(teamPlacement), '\n')
    for member in myTeamSummary:
        print ('Player:', member["player"])
        print ('Kills:', member["kills"], 'Damage:', member["damage"], '\n')

asyncio.get_event_loop().run_until_complete(main())

