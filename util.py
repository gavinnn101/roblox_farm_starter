import psutil
import win32gui, win32process, win32con
from loguru import logger

def check_for_process(process_name) -> bool:
	"""Returns True if process is open, otherwise returns False"""
	return process_name in (p.name() for p in psutil.process_iter())


def get_proc_count(process_name: str) -> int:
	"""Returns the amount of Roblox proccess open"""
	client_count = 0
	for p in psutil.process_iter():
		proc = str(p).lower()
		if process_name in proc and 'running' in proc:
			client_count += 1
	return client_count


def kill_process(process_name):
	""""Kills all processes with the given name"""
	for p in psutil.process_iter():
		if p.name() == process_name:
			p.kill()


def minimize_clients():
	"""Mimimizes all Roblox clients.
	This is useful because Roblox doesn't render graphics while minimized. Saves resources.
	https://stackoverflow.com/a/2323367
	"""
	def enumHandler(hwnd, lParam):
		if win32gui.IsWindowVisible(hwnd):
			if 'Roblox' in win32gui.GetWindowText(hwnd) and not win32gui.IsIconic(hwnd):
				logger.debug('Minimizing Roblox client')
				win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

	win32gui.EnumWindows(enumHandler, None)
