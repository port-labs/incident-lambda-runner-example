<img align="right" width="100" height="74" src="https://user-images.githubusercontent.com/8277210/183290025-d7b24277-dfb4-4ce1-bece-7fe0ecd5efd4.svg" />

# Incident lambda runner example

[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/devex-community/shared_invite/zt-1bmf5621e-GGfuJdMPK2D8UN58qL4E_g)


# Instructions for using the Incident Management Lambda Function

This Lambda function is designed to automate the creation of an incident and corresponding Slack channel in response to an incident. This function uses the Google Calendar API to generate a Google Meet link for the incident and the Port API to create and update the incident entity in the Port system.

## Prerequisites

Before using this function, you must ensure that you have the following:

- An AWS account with the Lambda service enabled.
- A Google Cloud Platform account with the Calendar API enabled.
- A Port account with access to the API.
- The following blueprints are installed in your Port account:
   - `Incident`: This blueprint contains the incident entity and the incident management workflow.
   ```json
    {
    "identifier": "incident",
    "title": "Incident",
    "icon": "TwoUsers",
    "schema": {
        "properties": {
        "slackChannel": {
            "type": "string",
            "format": "url",
            "title": "Slack"
        },
        "status": {
            "type": "string",
            "enum": [
            "In Progress",
            "Complete",
            "Decliend"
            ],
            "enumColors": {
            "In Progress": "darkGray",
            "Complete": "green",
            "Decliend": "red"
            }
        },
        "severity": {
            "title": "Severity",
            "type": "string",
            "enum": [
            "Critical",
            "Significant",
            "Minor",
            "Low"
            ],
            "enumColors": {
            "Critical": "red",
            "Significant": "orange",
            "Minor": "yellow",
            "Low": "green"
            }
        },
        "commanders": {
            "icon": "DefaultProperty",
            "title": "Commanders",
            "type": "array",
            "items": {
            "type": "string",
            "format": "user"
            }
        },
        "description": {
            "type": "string",
            "title": "Description"
        }
        },
        "required": []
    },
    "mirrorProperties": {},
    "calculationProperties": {},
    "relations": {
        "services": {
        "title": "Impacted Services",
        "target": "service",
        "required": false,
        "many": true
        }
    }
    }
   ```
   - `Service`: This blueprint contains the Services.
   ```json
    {
    "identifier": "service",
    "description": "This blueprint represents service in our software catalog",
    "title": "Service",
    "icon": "Microservice",
    "schema": {
        "properties": {
        "on-call": {
            "type": "string",
            "icon": "pagerduty",
            "title": "On Call",
            "format": "user",
            "default": "develoepr@getport.io"
        },
        "language": {
            "type": "string",
            "icon": "Git",
            "title": "Language",
            "default": "Node",
            "enum": [
            "GO",
            "Python",
            "Node",
            "React"
            ],
            "enumColors": {
            "GO": "red",
            "Python": "green",
            "Node": "blue",
            "React": "yellow"
            }
        },
        "monitor-links": {
            "title": "Monitor Tooling",
            "type": "array",
            "items": {
            "type": "string",
            "format": "url"
            },
            "default": [
            "https://grafana.com",
            "https://prometheus.com",
            "https://datadog.com"
            ]
        },
        "readme": {
            "format": "markdown",
            "type": "string",
            "title": "Readme",
            "icon": "Github"
        },
        "communication_method": {
            "type": "string",
            "title": "Communication Method",
            "enum": [
            "REST API",
            "GraphQL",
            "gRPC",
            "NATS",
            "Message Queue",
            "WebSocket"
            ]
        },
        "lifecycle": {
            "type": "string",
            "title": "Lifecycle",
            "enum": [
            "Production",
            "Experimental",
            "Deprecated"
            ],
            "enumColors": {
            "Production": "green",
            "Experimental": "orange",
            "Deprecated": "red"
            }
        },
        "swagger": {
            "type": "string",
            "format": "url",
            "spec": "open-api",
            "icon": "Swagger",
            "title": "Swagger"
        },
        "type": {
            "title": "Type",
            "type": "string",
            "enum": [
            "Lambda",
            "CronJob",
            "Deployment"
            ]
        },
        "tier": {
            "type": "string",
            "title": "Tier",
            "description": "How mission-critical the service is",
            "enum": [
            "Mission Critical",
            "Customer Facing",
            "Internal Service",
            "Other"
            ],
            "enumColors": {
            "Mission Critical": "turquoise",
            "Customer Facing": "green",
            "Internal Service": "darkGray",
            "Other": "yellow"
            }
        },
        "internetFacing": {
            "type": "boolean",
            "title": "Internet Facing"
        }
        },
        "required": []
    },
    "mirrorProperties": {},
    "calculationProperties": {
        "github-url": {
        "title": "Github URL",
        "icon": "Github",
        "calculation": "\"https://github.com/port-labs/\" + .title",
        "type": "string",
        "format": "url"
        }
    },
    "relations": {}
    }
   ```
- The following Create action on the incident 
```json
    [
    {
        "id": "action_BqI7CwTqfJa9nzja",
        "identifier": "create",
        "title": "Open new incident",
        "icon": "Slack",
        "userInputs": {
        "properties": {
            "services": {
            "title": "Impacted Services",
            "type": "array",
            "items": {
                "type": "string",
                "blueprint": "service",
                "format": "entity"
            },
            "description": "Which services are impacted by this incident"
            },
            "severity": {
            "title": "Severity",
            "type": "string",
            "enum": [
                "Critical",
                "Significant",
                "Minor",
                "Low"
            ]
            },
            "description": {
            "type": "string",
            "title": "Description"
            }
        },
        "required": [
            "description",
            "severity",
            "services"
        ]
        },
        "invocationMethod": {
        "type": "WEBHOOK",
        "url": "YOUR_LAMBDA_URL"
        },
        "trigger": "CREATE",
        "description": "This action will open up a new slack channel with the team owning the selected microservice, and assign the on call as the commander",
        "requiredApproval": false
    }
    ]
```

## Setup

1. Clone this repository to your local machine.
2. Install the required packages listed in the `requirements.txt` file in the `lambda_layer` library - you may use `deploy-layers.sh` helper script to deploy the layers.
3. Create a new Lambda function in the AWS console. - you may use `deploy-function.sh` helper script to deploy the function.
4. Adjust the function's timeout to 5 minutes.
5. Connect the layers to the function.
6. Upload the `src` folder to your Lambda function.
7. Set the environment variables required for the function to run. These variables include:
   - `GOOGLE_CREDENTIALS_JSON_ENCODED`: This is a base64-encoded string representing the service account JSON file for your Google Cloud Platform project.
   - `PORT_CLIENT_ID`: The Client ID for your Port account.
   - `PORT_CLIENT_SECRET`: The Client Secret for your Port account.
   - `SLACK_TOKEN`: The API token for your Slack workspace. You can get this token by creating a new Slack app.
