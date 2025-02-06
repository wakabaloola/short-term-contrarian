import requests

def i_am_online():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
        """
        if response.status_code == 200:
            return True
        else:
            return False
        """
    except (requests.ConnectionError, requests.Timeout) as e:
        return False

