import urllib.request as req
import json as js

# Retrieve the latest public activity for a user on GitHub
def fetch_github_activity(user_handle):
    api_url = f"https://api.github.com/users/{user_handle}/events"
    
    try:
        with req.urlopen(api_url) as response:
            if response.status == 200:
                raw_data = response.read()
                parsed_data = js.loads(raw_data)
                return parsed_data
            else:
                print(f"Failed to fetch data. Status code: {response.status}")
                return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Analyze the activity and generate summary
def summarize_activity(events):
    if not events:
        print("No activities found.")
        return
    
    activity_details = {}

    for event in events:
        event_kind = event.get("type")
        repository_name = event.get("repo", {}).get("name")
        
        if event_kind and repository_name:
            if event_kind == "PushEvent":
                commit_list = event.get("payload", {}).get("commits", [])
                num_commits = len(commit_list)
                activity_details[f"Pushed {num_commits} commits to {repository_name}"] = True

            elif event_kind == "IssuesEvent" and event.get("payload", {}).get("action") == "opened":
                activity_details[f"Opened a new issue in {repository_name}"] = True

            elif event_kind == "WatchEvent" and event.get("payload", {}).get("action") == "star":
                activity_details[f"Starred {repository_name}"] = True

    # Display the activity summary
    for summary in activity_details:
        print(summary)

def main():
    user = input("Enter GitHub username: ")
    activity_data = fetch_github_activity(user)
    summarize_activity(activity_data)

if __name__ == "__main__":
    main()
