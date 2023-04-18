import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.google import generate_google_meet_link
from src.port import create_entity, get_entity, get_owners_of_entities_emails, get_team, update_run_status
from src.slack import create_incident_channel_invite_relevant_people

from src.util import generate_short_uuid


def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    short_id = generate_short_uuid()

    print("Got request body: ", event['body'])

    services = request_body['payload']['properties']['services']
    severity = request_body['payload']['properties']['severity']
    description = request_body['payload']['properties']['description']

    try:
        all_user_emails, on_call_emails = get_owners_of_entities_emails(
            'service', services)

        google_meet_url = generate_google_meet_link(
            description=description, severity=severity, emails=on_call_emails
        )

        new_channel_id = create_incident_channel_invite_relevant_people(
            short_id, all_user_emails, on_call_emails, severity, services, google_meet_url)

        create_entity('incident', {"identifier": f"incident-{short_id}", "title": f"Incident {short_id}", "properties": {
            "slackChannel": f"https://getport.slack.com/archives/{new_channel_id}",
            "severity": severity,
            "commanders": list(on_call_emails),
            "status": "In Progress",
            "description": description
        },
            "relations": {
            "services": services
        }}, request_body['context']['runId'])

        update_run_status(request_body['context']['runId'], "SUCCESS")

        return {
            'statusCode': 200,
        }
    except Exception as e:
        print(f"Error: {e}")

        update_run_status(request_body['context']['runId'], "FAILURE")

        return {
            'statusCode': 500,
        }
