import re
from pathlib import Path

# Changed \s to \s+ to handle variable spaces from echo
AUTH_REGEX = re.compile(
    r"(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}).*?"
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)"
)
NEW_USER_REGEX = re.compile(
    r"(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}).*?new user: name=(?P<user>\w+)"
)
SUDO_REGEX = re.compile(
    r"(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}).*?sudo:.*?user=(?P<user>\w+).*?NOT in sudoers"
)

def parse_auth_log(filepath: str):
    path = Path(filepath)
    if not path.exists():
        return
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            # 1. Check Brute-force
            match = AUTH_REGEX.search(line)
            if match:
                yield {**match.groupdict(), "type": "failed_login"}
                continue
            
            # 2. Check New User Creation
            match = NEW_USER_REGEX.search(line)
            if match:
                yield {**match.groupdict(), "type": "new_user", "ip": "localhost"}
                continue

            # 3. Check Sudo Abuse
            match = SUDO_REGEX.search(line)
            if match:
                yield {**match.groupdict(), "type": "failed_sudo", "ip": "localhost"}
                continue
