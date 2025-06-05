import requests
import matplotlib.pyplot as plt

username = "Pycode406"

query = {
    "query": """
    query($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """,
    "variables": {"username": username}
}

response = requests.post("https://leetcode.com/graphql", json=query)
result = response.json()

if result['data']['matchedUser']:
    stats = result['data']['matchedUser']['submitStats']['acSubmissionNum']

    difficulties = [item['difficulty'] for item in stats]
    counts = [item['count'] for item in stats]

    bars = plt.bar(difficulties, counts, color=['purple', 'green', 'orange','red'])
    plt.title(f"{username}'s Solved Problems")
    plt.xlabel("Difficulty")
    plt.ylabel("Count")

    
    plt.bar_label(bars, padding=3)

    plt.show()
else:
    print("User not found or no data available.")
