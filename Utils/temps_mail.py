import tls_client
import requests
import html2text
import time
import random
import string


session = tls_client.Session(
    client_identifier="chrome_112", random_tls_extension_order=True)


def get_AvailableDomains():
    domains = requests.get(
        "https://www.1secmail.com/api/v1/?action=getDomainList").json()

    return domains


def get_ValidDomains():
    domains = get_AvailableDomains()
    valid_domains = []

    headers = {
        'Host': 'kick.com',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Language': 'fr_FR',
        'User-Agent': 'Kick/71 CFNetwork/1404.0.5 Darwin/22.3.0',
    }

    for domain in domains:

        json_data = {
            'email': 'yy1zk4ftf3@' + domain,
        }

        response = session.post(
            'https://kick.com/api/v1/signup/verify/email',  headers=headers, json=json_data)

        if response.status_code != 403:
            valid_domains.append(domain)

    return valid_domains


domains_available = get_ValidDomains()


def generateRandomUsername():
    username = ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(8))
    domain = random.choice(domains_available)
    return username, domain


def getEmail(username, domain):
    start_time = time.time()
    end_time = start_time + 300

    while time.time() < end_time:
        response = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}", timeout=6).json()

        if response:

            email_id = response[0]["id"]
            response_msg = requests.get(
                f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={email_id}", timeout=6).json()
            email_subject = response_msg["subject"]
            return email_subject.split(" ")[0]

        time.sleep(3)

    return "Not_found"
