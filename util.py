import psutil

def check_for_process(process_name) -> bool:
    """Returns True if process is open, otherwise returns False"""
    return process_name in (p.name() for p in psutil.process_iter())


def get_proc_count(proc_name: str) -> int:
	"""Returns the amount of Roblox proccess open"""
	client_count = 0
	for p in psutil.process_iter():
		proc = str(p).lower()
		if proc_name in proc and 'running' in proc:
			client_count += 1
	return client_count