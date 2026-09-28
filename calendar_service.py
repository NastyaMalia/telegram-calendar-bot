from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events.readonly"
]

def authenticate_google():
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not credentials:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        credentials = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials

print("Google authentication successful!")

credentials = authenticate_google()
service = build("calendar", "v3", credentials=credentials)

events_result = service.events().list(
    calendarId="primary",
    maxResults=10,
    singleEvents=True,
    orderBy="startTime"
).execute()

events = events_result.get("items", [])

for event in events:
    print("TITLE:", event.get("summary"))
    print("START:", event.get("start"))
    print()