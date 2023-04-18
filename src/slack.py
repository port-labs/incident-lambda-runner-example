import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def find_channel_id(channel_name):
    client = WebClient(token=os.environ["SLACK_TOKEN"])
    try:
        cursor = None

        while True:
            response = client.conversations_list(
                types="public_channel,private_channel",
                cursor=cursor
            )
            for channel in response["channels"]:
                if channel['name'] == channel_name:
                    return channel['id']
            cursor = response.get("response_metadata", {}).get("next_cursor")

            if not cursor:
                break

    except SlackApiError as e:
        print(f"Error: {e}")


def create_incident_channel_invite_relevant_people(short_id, all_user_emails, on_call_emails, severity, services, google_meet_url):
    client = WebClient(token=os.environ["SLACK_TOKEN"])

    response = client.conversations_create(name=f"incident-{short_id}")
    new_channel_id = response["channel"]["id"]

    for email in all_user_emails:
        user_response = client.users_lookupByEmail(email=email)
        client.conversations_invite(
            channel=new_channel_id, users=[user_response['user']['id']])

        print(f"User {email} added to channel")

    print(f"Channel created: {new_channel_id}")

    print(f"Posting message to the NEW slack channel")
    response = client.chat_postMessage(
        channel=response['channel']['id'],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":bust_in_silhouette: *Incident Commanders:*"
                },
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Emails:*\n{', '.join(on_call_emails)}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": ":video_camera: *Google Meet:*"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                            "type": "plain_text",
                            "text": "Join Meeting"
                    },
                    "url": google_meet_url,
                    "style": "primary"
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": f":exclamation: *Severity:* {severity}"
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": f":chart_with_downwards_trend: *Impacted Services:* {', '.join(services)}"
                }
            }
        ]
    )

    print(f"Message posted: {response['ts']}")

    print(f"Getting channel id of #attn-incidents")

    attn_incidents_channel_id = find_channel_id("attn-incidents")

    print("Posting message to #attn-incidents")

    response = client.chat_postMessage(
        channel=attn_incidents_channel_id,
        blocks=[
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": f":alert: #incident-{short_id} created"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": ":video_camera: *Google Meet:*"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                            "type": "plain_text",
                            "text": "Join Meeting"
                    },
                    "url": google_meet_url,
                    "style": "primary"
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": f":exclamation: *Severity:* {severity}"
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": f":chart_with_downwards_trend: *Impacted Services:* {', '.join(services)}"
                }
            }
        ]
    )

    print(f"Message posted: {response['ts']}")

    return new_channel_id
