import os
import requests


API_URL = 'https://api.getport.io/v1'
PORT_CREDENTIALS = {
    'clientId': os.environ["PORT_CLIENT_ID"],
    'clientSecret': os.environ["PORT_CLIENT_SECRET"]
}


def get_access_token():
    print(f"Getting port access_token")

    token_response = requests.post(
        f'{API_URL}/auth/access_token', json=PORT_CREDENTIALS)

    return token_response.json()['accessToken']


def create_entity(blueprint, entity, run_id):
    access_token = get_access_token()
    response = requests.post(
        f'{API_URL}/blueprints/{blueprint}/entities?run_id={run_id}',
        headers={'Authorization': f'Bearer {access_token}'},
        json=entity
    )

    return response.json()


def update_run_status(run_id, status):
    access_token = get_access_token()
    response = requests.patch(
        f'{API_URL}/actions/runs/{run_id}',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'status': status}
    )

    return response.json()


def get_team(team_id, fields="users.email"):
    access_token = get_access_token()
    response = requests.get(
        f'{API_URL}/teams/{team_id}?fields={fields}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    return response.json()['team']


def get_entity(blueprint, entity_identifier):
    access_token = get_access_token()
    response = requests.get(
        f'{API_URL}/blueprints/{blueprint}/entities/{entity_identifier}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    return response.json()['entity']


def get_owners_of_entities_emails(blueprint, entities_identifiers):
    print("Getting teams of the services that the incident was deployed for")

    all_teams = set()
    on_call_emails = set()
    all_user_emails = set()

    for entity_identifier in entities_identifiers:
        entity = get_entity(blueprint, entity_identifier)

        for team in entity['team']:
            all_teams.add(team)

        on_call_emails.add(
            entity['properties']['on-call'])

    print(f"Got owning teams: {all_teams}")

    for team in all_teams:
        team = get_team(team)

        for user in team['users']:
            all_user_emails.add(user['email'])

    print(
        f"Got user emails: {all_user_emails}")

    return all_user_emails, on_call_emails
