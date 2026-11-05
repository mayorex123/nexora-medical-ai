from collections import defaultdict
from nexora.memory.store import CASES_FILE
import json

def detect_bruteforce(threshold=3):
    if not CASES_FILE.exists():
        return []
    ip_counts = defaultdict(int)
    ip_users = defaultdict(set)

    with open(CASES_FILE, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                if event.get("type") == "failed_login":
                    ip = event["ip"]
                    ip_counts[ip] += 1
                    ip_users[ip].add(event["user"])
            except json.JSONDecodeError:
                continue

    findings = []
    for ip, count in ip_counts.items():
        if count >= threshold:
            users = list(ip_users[ip])
            findings.append({
                "rule": "bruteforce_detected",
                "ip": ip,
                "count": count,
                "users_targeted": users,
                "explanation": f"IP {ip} failed login {count} times targeting users: {', '.join(users)}"
            })
    return findings

def detect_new_users():
    """Flags if a new user is created (adduser or useradd)."""
    if not CASES_FILE.exists():
        return []
    findings = []
    with open(CASES_FILE, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                if event.get("type") == "new_user":
                    findings.append({
                        "rule": "new_user_created",
                        "ip": event.get("ip", "localhost"),
                        "count": 1,
                        "users_targeted": [event.get("user")],
                        "explanation": f"New user '{event.get('user')}' was created on the system."
                    })
            except json.JSONDecodeError:
                continue
    return findings

def detect_sudo_abuse(threshold=2):
    """Flags repeated failed sudo attempts."""
    if not CASES_FILE.exists():
        return []
    sudo_counts = defaultdict(int)
    sudo_users = defaultdict(set)
    with open(CASES_FILE, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                if event.get("type") == "failed_sudo":
                    user = event.get("user")
                    sudo_counts[user] += 1
                    sudo_users[user].add(user)
            except json.JSONDecodeError:
                continue

    findings = []
    for user, count in sudo_counts.items():
        if count >= threshold:
            findings.append({
                "rule": "sudo_abuse_detected",
                "ip": "localhost",
                "count": count,
                "users_targeted": [user],
                "explanation": f"User '{user}' failed sudo password {count} times."
            })
    return findings

def run_all_rules():
    """Runs every detection rule and returns a combined list."""
    return detect_bruteforce() + detect_new_users() + detect_sudo_abuse()
