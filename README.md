# Warzone Recent Match Summary

Creates a CSV file to show your team, respective kills, respective damage, and placement for your most recent match.

### Setup

#### For those that are not familiar with CLI commands
Download my repo and simply navigate to the `dist` folder and run the `.exe` file. Your antivirus may detect it as a virus. <b> DO NOT WORRY. IT IS NOT A VIRUS. </b>

#### Familiar with CLI commands (and don't trust my exe file)
1. Clone my repo
2. Get Python 3.9 or later.
3. Run `pip install callofduty.py` to install the CoD API library.
4. Run `py wzstats.py` in the project directory.
5. Follow prompts.

### Issues
If the terminal displays a `User not found` message, due to my lazy error handling it could either mean you entered a user that does not exist for that specific platform (activision, battlenet, psn, xbox) or the API is not allowing you to search for that player's data.

In the event that it's due to the API restricting you from searching that player's data, make sure the player you're searching for has updated their privacy settings in their https://my.callofduty.com/login to allow their data to be searched for.

#### Credits
https://pypi.org/project/callofduty.py/
