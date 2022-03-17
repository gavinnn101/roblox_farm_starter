import os
import time
import psutil
import requests
import subprocess
from loguru import logger
from util import check_for_process, get_proc_count, kill_process

# Roblox Alt Manager Settings
ram_ip = 'http://localhost'
ram_port = '5151'
ram_fqdn = f'{ram_ip}:{ram_port}'
ram_pass = os.getenv('ram_password')
ram_dir = 'C:\\Users\\Gavin\\Desktop\\roblox stuff\\roblox alt manager'
ram_path = f'{ram_dir}\\RBX Alt Manager.exe'

# SynapseX Settings
synapse_dir = 'C:\\Users\\Gavin\\Desktop\\roblox stuff\\synapse-launcher-11-17-21'
synapse_path = f'{synapse_dir}\\Synapse Launcher.exe'

# Pet Sim X private server code
private_server_code = os.getenv('rbx_prv_svr_code')


def start_synapse():
    """Will start SynapseX if not already. Expects a specific path - see below."""
    ram_running = check_for_process("RBX Alt Manager.exe")
    cefsharp_count = get_proc_count('cefsharp')
    logger.debug(f'Starting cefsharp_count: {cefsharp_count}')
    if cefsharp_count >= 4:
        logger.info("4+ cefsharp process found, we're assuming SynapseX is already open.")
    elif (cefsharp_count == 2 and ram_running) or cefsharp_count == 0:  # SynapseX isn't loaded (or some other program that uses cefsharp but im utilizing this as a hack because synapse loads with a random string for its proc name)
        try:
            if os.curdir != synapse_dir:
                logger.info("Changing to the SynapseX directory.")
                os.chdir(synapse_dir)
            logger.info('Launching SynapseX')
            subprocess.Popen([synapse_path], stdin=None, stdout=None, stderr=None)
        except Exception as e:
            logger.error('Error starting SynapseX')
            logger.error(e)
        while get_proc_count('cefsharp') != cefsharp_count+2:
            logger.info(f'Sleeping until SynapseX is open.. Count: {cefsharp_count}')
            time.sleep(1)
        logger.success('SynapseX has launched!')


def start_ram():
    """Will start RAM if not already. Set paths at top of file."""

    ram_running = check_for_process("RBX Alt Manager.exe")
    if not ram_running:
        try:
            if os.curdir != ram_dir:
                logger.info("Changing to the RAM directory.")
                os.chdir(ram_dir)  # RAM needs to be launched from the directory it lives in or else the settings/accounts won't load..
            logger.info("Launching RAM")
            subprocess.Popen([ram_path], stdin=None, stdout=None, stderr=None)
            while not ram_running:
                logger.info('Sleeping until RAM is open..')
                time.sleep(1)
                ram_running = check_for_process("RBX Alt Manager.exe")
        except Exception as e:
            logger.error('Error starting RAM')
            logger.error(e)
        else:
            logger.success('Successfully Started RAM.')


def api_call(api_func: str, api_params: dict) -> requests.Response:
    """Makes a request to the RAM API with some error handling.
    params:
        api_func: Function of the RAM API - https://ic3w0lf22.gitbook.io/roblox-account-manager
            Note: This 
        api_params: the parameters to pass to the API function
    
    returns:
        requests.Response
    """
    bad_response_text = ['Empty Account', 'Invalid Password']  # List of strings that would indicate a bad response but could still get a successful response code..
    launch_cmd = f'{ram_fqdn}/{api_func}'
    with requests.session() as session:
        try:
            r = session.get(launch_cmd, params=api_params)
            logger.debug(r.url)
        except ConnectionError:
            logger.error('Connection error to API. Make sure RAM is open.')
        if not r.ok or any(text in r.text for text in bad_response_text):
            logger.error("Bad response code or bad response contents. Check details below.")
        logger.debug(f"Response Code: {r.status_code}")
        logger.info(r.text)
        return r


def get_accounts() -> list:
    """Makes a GetAccounts request to RAM API and returns accounts in a list.
    params:
        none
    
    returns:
        Parsed List[] of accounts.
    """
    accs_list = []
    accs_string = api_call('GetAccounts', {'Password': ram_pass}).text
    try:
        accs_list = accs_string.split(',')  # API returns accounts in a comma seperated list
    except Exception as e:
        logger.error(f'Error Getting accounts: {e}')
        logger.error(f'Response text: {accs_string}')
    else:
        logger.success(f'Accounts: {accs_list}')
    return accs_list


def launch_account(account_name: str) -> None:
    """Loads account into Roblox server.
    params:
        account_name: username of account in RAM to load into game
        client_count: Amount of clients currently running

    returns:
        none
    """
    starting_client_count = get_proc_count('roblox')
    client_count = 0
    # RAM API 'LaunchAccount' parameters
    # https://ic3w0lf22.gitbook.io/roblox-account-manager/#launchaccount
    acc_launch_params = {
        'Account': account_name,
        'Password': ram_pass, # 
        'PlaceId': 6284583030,  # Pet Sim X
        'JobId': f'https://www.roblox.com/games/6284583030?privateServerLinkCode={private_server_code}',
    }
    # API call to launch game
    api_call('LaunchAccount', acc_launch_params)
    while client_count != starting_client_count+2:  # Roblox seems to open 2 proccess per client
        logger.debug(f'Waiting for {account_name} to finish launching (proc count: {client_count})')
        time.sleep(2)
        client_count = get_proc_count('roblox')
    logger.success(f'{account_name} launch finished!')


def main():
    logger.info('Ending Roblox processes')
    kill_process('RobloxPlayerBeta.exe')
    start_synapse()
    start_ram()
    accs = get_accounts()
    if accs:
        for acc in accs:
            logger.info(f"Launching account: {acc}")
            launch_account(acc)


main()
