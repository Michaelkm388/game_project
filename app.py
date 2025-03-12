from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import os

PLAY_COUNT_FILE = "play_count.txt"

# Function to get the current play count
def get_play_count():
    if not os.path.exists(PLAY_COUNT_FILE):
        return 0
    with open(PLAY_COUNT_FILE, "r") as file:
        return int(file.read())

# Function to update the play count
def update_play_count():
    count = get_play_count() + 1
    with open(PLAY_COUNT_FILE, "w") as file:
        file.write(str(count))
    return count

# Define the final scoring function ("State of the World")
def state_of_the_world(score):
    if score >= 40:
        return "State of the World: A Thriving Global Community"
    elif score >= 25:
        return "State of the World: Strong and Promising"
    elif score >= 10:
        return "State of the World: Stable but Room for Improvement"
    elif score >= 0:
        return "State of the World: Tense and Fragile"
    elif score >= -10:
        return "State of the World: Uncertain and Troubled"
    else:
        return "State of the World: Catastrophic"

# Expanded game events and choices for both U.S. and Russia

events = {
    "US": [
        # Pre-Soviet Era / Early 20th Century
        {
            "year": 1867,
            "event": "U.S. Buys Alaska from Russia",
            "choices": ["Buy Alaska", "Ignore the deal"],
            "scores": [10, -5],
            "effects": ["U.S. gains Alaska, setting a foundation for future expansion", 
                        "Russia keeps Alaska, leading to future territorial disputes"]
        },
        {
            "year": 1904,
            "event": "Russo-Japanese War Mediation",
            "choices": ["Mediate the conflict", "Stay out"],
            "scores": [8, -3],
            "effects": ["Successful mediation; U.S. earns global respect", 
                        "Missed opportunity for leadership in global peace"]
        },
        {
            "year": 1918,
            "event": "U.S. Intervention in Russian Civil War",
            "choices": ["Intervene militarily", "Withdraw quickly"],
            "scores": [4, 0],
            "effects": ["Intervention shows commitment to anti-communism (with mixed results)", 
                        "Avoids entanglement but loses influence"]
        },
        {
            "year": 1942,
            "event": "Wartime Cooperation in WWII",
            "choices": ["Coordinate closely", "Maintain distance"],
            "scores": [10, -5],
            "effects": ["Strong Allied cooperation contributes to victory", 
                        "Missed opportunity for a deeper U.S.–USSR alliance"]
        },
        # Cold War and Beyond
        {
            "year": 1947,
            "event": "Cold War Onset",
            "choices": ["Implement Truman Doctrine", "Stay neutral"],
            "scores": [7, -2],
            "effects": ["Begins containment of communism", 
                        "Potential for less immediate conflict but risks future instability"]
        },
        {
            "year": 1961,
            "event": "Berlin Crisis",
            "choices": ["Support West Berlin", "Avoid confrontation"],
            "scores": [9, -4],
            "effects": ["Boosts morale and international standing", 
                        "Risk of appearing indecisive on human rights"]
        },
        {
            "year": 1972,
            "event": "Nixon’s Moscow Summit and SALT I",
            "choices": ["Negotiate arms control", "Push for aggressive terms"],
            "scores": [10, -6],
            "effects": ["Reduced nuclear tension and improved dialogue", 
                        "Potentially escalates arms buildup"]
        },
        {
            "year": 1975,
            "event": "Helsinki Accords",
            "choices": ["Support the accords", "Reject them"],
            "scores": [8, -5],
            "effects": ["Improved human rights dialogue and East-West cooperation", 
                        "Increases ideological divisions"]
        },
        {
            "year": 1979,
            "event": "Soviet Invasion of Afghanistan",
            "choices": ["Impose sanctions", "Pursue diplomatic pressure"],
            "scores": [9, -4],
            "effects": ["Sanctions and pressure contribute to Soviet withdrawal", 
                        "Diplomatic channel less effective, prolonging conflict"]
        },
        {
            "year": 1983,
            "event": "Reagan’s 'Evil Empire' Speech",
            "choices": ["Maintain tough rhetoric", "Seek dialogue"],
            "scores": [5, 2],
            "effects": ["Rhetoric intensifies Cold War tensions", 
                        "Opens possibility for diplomatic engagement"]
        },
        {
            "year": 1987,
            "event": "INF Treaty",
            "choices": ["Sign the treaty", "Reject the treaty"],
            "scores": [10, -10],
            "effects": ["Eliminates a class of nuclear weapons and reduces tensions", 
                        "Continued arms buildup and risk of conflict"]
        },
        {
            "year": 1999,
            "event": "NATO Bombing of Yugoslavia",
            "choices": ["Support intervention", "Oppose intervention"],
            "scores": [4, -4],
            "effects": ["Asserts U.S. leadership but strains relations with Russia", 
                        "Avoids direct confrontation but loses global influence"]
        },
        {
            "year": 2002,
            "event": "U.S. Withdrawal from ABM Treaty",
            "choices": ["Withdraw from the treaty", "Remain in the treaty"],
            "scores": [-8, 6],
            "effects": ["Increases risk of arms race", 
                        "Maintains strategic stability"]
        },
        {
            "year": 2014,
            "event": "Ukraine Crisis and Crimea Annexation",
            "choices": ["Sanction Russia", "Engage diplomatically"],
            "scores": [-10, 3],
            "effects": ["Deepens Russian isolation and increases tensions", 
                        "May de-escalate conflict but risk appearing soft"]
        },
        {
            "year": 2016,
            "event": "U.S. Election Interference Allegations",
            "choices": ["Impose further sanctions", "Pursue diplomatic resolution"],
            "scores": [-7, 2],
            "effects": ["Further strains U.S.–Russia relations", 
                        "Attempt at dialogue but risk of perceived weakness"]
        }
    ],
    "Russia": [
        # Early 20th Century / Pre-Soviet Era
        {
            "year": 1867,
            "event": "Selling Alaska to the U.S.",
            "choices": ["Sell Alaska", "Keep Alaska"],
            "scores": [10, -5],
            "effects": ["Improves relations and gains cash", 
                        "Loss of territory hurts national pride"]
        },
        {
            "year": 1904,
            "event": "Russo-Japanese War: Lack of Mediation",
            "choices": ["Allow war to proceed", "Seek mediation"],
            "scores": [-6, 8],
            "effects": ["War continues, damaging Russia's image", 
                        "Mediation could have preserved resources and prestige"]
        },
        {
            "year": 1918,
            "event": "Russian Civil War: U.S. Intervention",
            "choices": ["Resist U.S. forces", "Cooperate with Allies"],
            "scores": [5, -2],
            "effects": ["Maintains revolutionary integrity", 
                        "Risk of prolonging internal conflict"]
        },
        {
            "year": 1942,
            "event": "Wartime Cooperation with Allies",
            "choices": ["Fully cooperate", "Keep military secrets"],
            "scores": [10, -5],
            "effects": ["Strengthens alliance and global position", 
                        "Limits strategic advantages"]
        },
        # Cold War and Beyond
        {
            "year": 1947,
            "event": "Cold War Onset",
            "choices": ["Adopt aggressive posture", "Seek détente"],
            "scores": [7, -3],
            "effects": ["Provokes confrontation", 
                        "Opens door to diplomatic engagement"]
        },
        {
            "year": 1961,
            "event": "Berlin Crisis",
            "choices": ["Support East Berlin", "Avoid escalation"],
            "scores": [8, -4],
            "effects": ["Solidifies influence in Eastern Europe", 
                        "Missed chance to reduce tensions"]
        },
        {
            "year": 1972,
            "event": "Nixon’s Moscow Summit and SALT I",
            "choices": ["Negotiate arms control", "Refuse concessions"],
            "scores": [10, -7],
            "effects": ["Reduces nuclear threat", 
                        "Missed opportunity to strengthen leverage"]
        },
        {
            "year": 1975,
            "event": "Helsinki Accords",
            "choices": ["Sign accords", "Reject accords"],
            "scores": [9, -6],
            "effects": ["Improves international image", 
                        "Leads to internal dissent"]
        },
        {
            "year": 1979,
            "event": "Soviet Invasion of Afghanistan",
            "choices": ["Maintain military presence", "Negotiate withdrawal"],
            "scores": [-8, 5],
            "effects": ["Drains resources and fuels dissent", 
                        "Shortens conflict but seen as a retreat"]
        },
        {
            "year": 1983,
            "event": "Reagan’s 'Evil Empire' Speech",
            "choices": ["Counter with rhetoric", "Engage quietly"],
            "scores": [-5, 3],
            "effects": ["Escalates tensions", 
                        "Opens possibility for dialogue"]
        },
        {
            "year": 1987,
            "event": "INF Treaty",
            "choices": ["Sign the treaty", "Reject the treaty"],
            "scores": [10, -10],
            "effects": ["Eliminates a class of nuclear weapons", 
                        "Continues arms race and isolation"]
        },
        {
            "year": 1999,
            "event": "NATO Bombing of Yugoslavia",
            "choices": ["Condemn NATO intervention", "Call for diplomatic resolution"],
            "scores": [6, -4],
            "effects": ["Strengthens ties with allies in the region", 
                        "Signals willingness to compromise"]
        },
        {
            "year": 2002,
            "event": "U.S. Withdrawal from ABM Treaty",
            "choices": ["Criticize U.S. decision", "Seek new strategic agreements"],
            "scores": [8, -3],
            "effects": ["Increases arms race tensions", 
                        "Opens door for modernized arms control"]
        },
        {
            "year": 2014,
            "event": "Ukraine Crisis and Crimea Annexation",
            "choices": ["Annex Crimea", "Engage diplomatically"],
            "scores": [10, -5],
            "effects": ["Boosts national pride and control", 
                        "Risks international isolation and sanctions"]
        },
        {
            "year": 2016,
            "event": "U.S. Election Interference Allegations",
            "choices": ["Deny involvement", "Acknowledge and adjust policy"],
            "scores": [-7, 2],
            "effects": ["Further strains relations", 
                        "Opens potential for rebalancing policies"]
        }
    ]
}


# Track game progress (each decision stores its numeric score)
game_progress = []
player_country = None  # Will store the player's selected country

@app.route("/")
def index():
    return render_template("choose_nation.html")

@app.route("/choose")
def choose_nation():
    return render_template("choose_nation.html")

@app.route("/start_game", methods=["POST"])
def start_game():
    global player_country
    data = request.get_json()

    print("🔹 Received request data:", data)  # ✅ Debugging output

    if not data or "country" not in data:
        print("❌ Error: No country provided")
        return jsonify({"error": "Invalid selection"}), 400

    player_country = data["country"]

    if player_country not in events:
        print("❌ Error: Invalid country selection:", player_country)
        return jsonify({"error": "Invalid country selection"}), 400

    # Update play count
    play_count = update_play_count()

    print(f"✅ Game started as {player_country}, play count: {play_count}")  # ✅ Debugging output

    return jsonify({
        "message": f"Game started as {player_country}!",
        "redirect": "/game",
        "events": events[player_country],
        "play_count": play_count
    })

@app.route("/game")
def game():
    global player_country
    if not player_country:
        return "Error: No country selected. Go back and choose a nation.", 400
    return render_template("index.html", events=events[player_country], player_country=player_country)

@app.route("/play", methods=["POST"])
def play():
    global player_country
    data = request.get_json()
    choice_index = data.get("choice_index")
    event_index = data.get("event_index")

    # If no more events, compute final score and state of the world.
    if player_country not in events or event_index >= len(events[player_country]):
        total_score = sum(item.get("score", 0) for item in game_progress)
        final_state = state_of_the_world(total_score)
        return jsonify({
            "game_over": True,
            "summary": game_progress,
            "final_score": total_score,
            "state_of_the_world": final_state
        })

    event = events[player_country][event_index]
    score = event["scores"][choice_index]
    result = event["effects"][choice_index]

    game_progress.append({
        "year": event["year"],
        "event": event["event"],
        "choice": event["choices"][choice_index],
        "result": result,
        "score": score
    })

    return jsonify({"next_event": event_index + 1, "result": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)