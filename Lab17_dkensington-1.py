from operator import itemgetter

import requests

# Make an API call and check the response.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Make a new API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    submission_dict = {                                                         # type: ignore
        'title': response_dict['title'],
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}"
    }
    try:
        submission_dict['comments'] = response_dict['descendants']
    except KeyError:
        submission_dict['comments'] = 0
    submission_dicts.append(submission_dict)                                    # type: ignore

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),         # type: ignore
                            reverse=True)

for submission_dict in submission_dicts:                                        # type: ignore
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")