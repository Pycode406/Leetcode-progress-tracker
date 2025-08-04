import requests
import matplotlib.pyplot as plt

def get_leetcode_data(username):
    query = {
        "query": """
        query userStats($username: String!) {
          matchedUser(username: $username) {
            submitStats {
              acSubmissionNum {
                difficult\
                count
              }
            }
            languageProblemCount {
              languageName
              problemsSolved
            }
            profile {
              ranking
              reputation
              solutionCount
            }
          }
        }
        """,
        "variables": {"username": username}
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post("https://leetcode.com/graphql", json=query, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

def plot_difficulty_bar(stats):
    difficulties = [item['difficulty'] for item in stats]
    counts = [item['count'] for item in stats]

    bars = plt.bar(difficulties, counts, color=['purple', 'green', 'orange', 'red'])
    plt.title("Problems Solved by Difficulty")
    plt.xlabel("Difficulty")
    plt.ylabel("Count")
    plt.bar_label(bars)
    plt.tight_layout()
    plt.show()

def plot_language_pie(lang_data):
    labels = [item['languageName'] for item in lang_data]
    values = [item['problemsSolved'] for item in lang_data]

    if not values:
        print("No language data available.")
        return

    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("Languages Used")
    plt.show()

def show_profile(profile):
    print("\n User Profile Summary:")
    print(f" Ranking: {profile.get('ranking', 'N/A')}")
    print(f" Reputation: {profile.get('reputation', 'N/A')}")
    print(f" Solutions Submitted: {profile.get('solutionCount', 'N/A')}")

def menu():
    print("\nChoose an option:")
    print("1. Bar Chart - Problems Solved by Difficulty")
    print("2. Pie Chart - Languages Used")
    print("3. Show User Profile Summary")
    print("0. Exit")

def main():
    username = input("Enter LeetCode username: ").strip()
    try:
        data = get_leetcode_data(username)
    except requests.exceptions.HTTPError as err:
        print(" HTTP error:", err)
        print("Response:", err.response.text)
        return
    except Exception as e:
        print(" Error fetching data:", e)
        return

    user = data.get("matchedUser")
    if not user:
        print("User not found.")
        return

    stats = user["submitStats"]["acSubmissionNum"]
    lang_data = user.get("languageProblemCount", [])
    profile = user.get("profile", {})

    while True:
        menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            plot_difficulty_bar(stats)
        elif choice == '2':
            plot_language_pie(lang_data)
        elif choice == '3':
            show_profile(profile)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
