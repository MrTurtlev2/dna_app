from flask import Flask, jsonify, render_template
import requests
import urllib3

# Wyłącz ostrzeżenia o SSL — przy testach
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Konfiguracja DNA Center (użyj swojego URL, username, password)
# DNAC_URL = "https://dnac.example.com"
#DNAC_URL = "https://sandboxapicdc.cisco.com"
#USERNAME = "admin"
#PASSWORD = "!v3G@!4@Y"

DNAC_URL = "https://sandboxdnac.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "Cisco123!"

def get_auth_token():
    """Uzyskaj token uwierzytelniania z DNA Center."""
    url = f"{DNAC_URL}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(USERNAME, PASSWORD), verify=False)
    response.raise_for_status()
    print("Token:", response.json().get("Token"))

    return response.json()["Token"]

def get_topology(token):
    """Pobierz topologię z DNA Center API."""
    url = f"{DNAC_URL}/dna/intent/api/v1/topology/physical-topology"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    print(response.json())
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/topology")
def topology():
    try:
        token = get_auth_token()
        topology_data = get_topology(token)
        return jsonify(topology_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
