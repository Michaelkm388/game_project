import itertools

# Define events for the U.S. side with scores assigned for each decision.
us_events = [
    {
        "year": 1867,
        "event": "U.S. Buys Alaska from Russia",
        "choices": ["Buy Alaska", "Ignore the deal"],
        "scores": [10, -5]
    },
    {
        "year": 1917,
        "event": "Bolshevik Revolution",
        "choices": ["Support White Army", "Stay Neutral"],
        "scores": [5, 0]
    },
    {
        "year": 1939,
        "event": "Nazi-Soviet Pact",
        "choices": ["Fund Anti-Nazi Resistance", "Stay Neutral"],
        "scores": [8, -2]
    },
    {
        "year": 1962,
        "event": "Cuban Missile Crisis",
        "choices": ["Negotiate secretly", "Publicly confront"],
        "scores": [10, -10]
    },
    {
        "year": 2022,
        "event": "Ukraine Conflict",
        "choices": ["Force peace talks", "Fund Ukraine indefinitely"],
        "scores": [12, -8]
    }
]

# Function to compute the total score and detail of each decision path.
def compute_score(events, decision_path):
    total_score = 0
    details = []
    for event, decision in zip(events, decision_path):
        score = event["scores"][decision]
        total_score += score
        details.append((event["year"], event["event"], event["choices"][decision], score))
    return total_score, details

# Function to classify the final outcome based on the total score.
def classify_score(score):
    if score >= 40:
        return "Best"
    elif score >= 25:
        return "Better"
    elif score >= 10:
        return "Good"
    elif score >= 0:
        return "Bad"
    elif score >= -10:
        return "Worse"
    else:
        return "Catastrophe"

# Generate all possible decision combinations.
# Each event has 2 choices (0 or 1). For n events, there are 2^n combinations.
all_combinations = list(itertools.product([0, 1], repeat=len(us_events)))

# Evaluate each combination.
for path in all_combinations:
    score, details = compute_score(us_events, path)
    classification = classify_score(score)
    print(f"Path: {path} -> Total Score: {score} -> Classification: {classification}")
    for year, event, choice, s in details:
        print(f"  {year}: {event} -> {choice} (Score: {s})")
    print("-" * 40)