# RAM Quick Account Launch
This is a quick python script that utilizes the [Roblox Account Manager](https://github.com/ic3w0lf22/Roblox-Account-Manager) local web server api to quickly launch all accounts. I personally would never do this but I imagine it would be useful to combine this with an executor that auto loads a Roblox farming script!

# Requirements
In your `Roblox-Account-Loader` folder, `shift+right-click`, click `open in terminal` or similar and then run `pip install -r requirements.txt`

# Roblox Account Manager
* Install Roblox Account Manager, linked above
* * Add all of your accounts to the program...
* * Edit `RAMSettings.ini` to:
* * * `EnableWebServer=true`
* * * `WebServerPort=5151`
* * * `AllowGetAccounts=true`
* * * `AllowLaunchAccount=true`
* * In `main.py` edit `Roblox Alt Manager Settings` at the top as needed.

# SynapseX
* in `main.py` edit `SynapseX Settings` at the top as needed.
* Add your farming script to your SynapseX `autoexec` folder
* * We're assuming the farming script has all the proper settings saved to run on its own without human intervention.

# Running program
Run `quick_start.bat` or `python main.py`, etc