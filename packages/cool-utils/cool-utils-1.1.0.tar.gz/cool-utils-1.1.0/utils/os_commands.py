import sys

def get_command(command: str):
	PYTHON = {
		'linux': 'python3',
		'win32': 'python',
		'macos': 'python3'
	}

	PIP = {
		'linux': 'python3 -m pip',
		'win32': 'pip',
		'macos': 'python3 -m pip'
	}

	CLEAR = {
		'linux': 'clear',
		'win32': 'cls',
		'macos': 'clear'
	}

	LS = {
		'linux': 'ls',
		'win32': 'dir',
		'macos': 'ls'
	}
	command = command.lower()
	if command == "python":
		return PYTHON[sys.platform]

	elif command == "pip":
		return PIP[sys.platfrom]

	elif command == "clear":
		return CLEAR[sys.platfrom]

	elif command == "ls":
		return LS[sys.platfrom]

	else:
		return command