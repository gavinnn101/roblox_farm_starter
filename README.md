# Roblox Bot Farm Starter
This is a quick python script that utilizes the [Roblox Account Manager](https://github.com/ic3w0lf22/Roblox-Account-Manager) local web server api to quickly launch all accounts. I personally would never do this but I imagine it would be useful to combine this with an executor that auto loads a Roblox farming script!

# Requirements
* In your `roblox_farm_starter` folder, `shift+right-click`, click `open in terminal` or similar and then run `pip install -r requirements.txt`
* Set Environment variables or edit variables in script:
* * `ram_password` - set this to the password you set in `RAMSettings.ini`
* account_data.json
* * You can add or remove entire groups as needed. You obviously need at least 1 group for it to function.
* * `server_code` - set this to your private server's code. (This comes from the end of the private server join link.)
* * `accounts` list - Add the accounts you want to join the private server to the list...

# Roblox Account Manager
* Install Roblox Account Manager, linked above
* * Add all of your accounts to the program...
* * Edit `RAMSettings.ini` to:
* * * `AccountJoinDelay=15` (Some accounts don't load correctly with lower/default time in my experience.)
* * * `EnableWebServer=true`
* * * `WebServerPort=5151` (This can be anything you want but change the port in `main.py` accordingly.)
* * * `AllowGetAccounts=true`
* * * `AllowLaunchAccount=true`
* * In `main.py` edit `Roblox Alt Manager Settings` at the top as needed.

# SynapseX
* In `main.py` edit `SynapseX Settings` at the top as needed.
* Add your farming script to your SynapseX `autoexec` folder
* * We're assuming the farming script has all the proper settings saved to run on its own without human intervention.

# Running program
Run `quick_start.bat` or `python main.py`, etc
