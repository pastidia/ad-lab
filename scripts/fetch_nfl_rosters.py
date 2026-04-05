import requests
import csv
import time

DIVISIONS = {
    "1": ("NFC", "NFC South", "Atlanta Falcons", "ATL"),
    "2": ("AFC", "AFC East", "Buffalo Bills", "BUF"),
    "3": ("NFC", "NFC North", "Chicago Bears", "CHI"),
    "4": ("AFC", "AFC North", "Cincinnati Bengals", "CIN"),
    "5": ("AFC", "AFC North", "Cleveland Browns", "CLE"),
    "6": ("NFC", "NFC East", "Dallas Cowboys", "DAL"),
    "7": ("AFC", "AFC West", "Denver Broncos", "DEN"),
    "8": ("NFC", "NFC North", "Detroit Lions", "DET"),
    "9": ("NFC", "NFC North", "Green Bay Packers", "GB"),
    "10": ("AFC", "AFC South", "Tennessee Titans", "TEN"),
    "11": ("AFC", "AFC South", "Indianapolis Colts", "IND"),
    "12": ("AFC", "AFC West", "Kansas City Chiefs", "KC"),
    "13": ("AFC", "AFC West", "Las Vegas Raiders", "LV"),
    "14": ("NFC", "NFC West", "Los Angeles Rams", "LAR"),
    "15": ("AFC", "AFC East", "Miami Dolphins", "MIA"),
    "16": ("NFC", "NFC North", "Minnesota Vikings", "MIN"),
    "17": ("AFC", "AFC East", "New England Patriots", "NE"),
    "18": ("NFC", "NFC South", "New Orleans Saints", "NO"),
    "19": ("NFC", "NFC East", "New York Giants", "NYG"),
    "20": ("AFC", "AFC East", "New York Jets", "NYJ"),
    "21": ("NFC", "NFC East", "Philadelphia Eagles", "PHI"),
    "22": ("NFC", "NFC West", "Arizona Cardinals", "ARI"),
    "23": ("AFC", "AFC North", "Pittsburgh Steelers", "PIT"),
    "24": ("AFC", "AFC West", "Los Angeles Chargers", "LAC"),
    "25": ("NFC", "NFC West", "San Francisco 49ers", "SF"),
    "26": ("NFC", "NFC West", "Seattle Seahawks", "SEA"),
    "27": ("NFC", "NFC South", "Tampa Bay Buccaneers", "TB"),
    "28": ("NFC", "NFC East", "Washington Commanders", "WSH"),
    "29": ("NFC", "NFC South", "Carolina Panthers", "CAR"),
    "30": ("AFC", "AFC South", "Jacksonville Jaguars", "JAX"),
    "33": ("AFC", "AFC North", "Baltimore Ravens", "BAL"),
    "34": ("AFC", "AFC South", "Houston Texans", "HOU") 
}

def generate_username(first, last, position):
    return f"{first[0].lower()}{last.lower().replace(' ', '').replace('-', '').replace("'", '').replace('jr.', 'jr')}_{position.lower()}"

def fetch_roster(team_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Faiuled to fetch team {team_id}")
        return []
    return response.json().get("athletes", [])

def main():
    rows = []
    for team_id, (conference, division, team_name, abbreviation) in DIVISIONS.items():
        print(f"Fetching {team_name}...")
        athlete_groups = fetch_roster(team_id)
        for group in athlete_groups:
            for player in group.get("items", []):
                first = player.get("firstName", "")
                last = player.get("lastName", "")
                position = player.get("position", {}).get("abbreviation", "")
                username = generate_username(first, last, position)
                rows.append({
                    "FirstName": first,
                    "LastName": last,
                    "Position": position,
                    "Team": team_name,
                    "Abbreviation": abbreviation,
                    "Division": division,
                    "Conference": conference,
                    "Username": username,
                    "Department": team_name,
                    "Company": "NFL"
                })
        time.sleep(0.5)
   
    with open("nfl_rosters.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "FirstName", "LastName", "Position", "Team", "Abbreviation",
            "Division", "Conference", "Username", "Department", "Company"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done! {len(rows)} players written to nfl_rosters.csv")

if __name__ == "__main__":
    main()


