from asyncio import events

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from datetime import datetime, time
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events.readonly"
]

timezone = ZoneInfo("America/Los_Angeles")

now = datetime.now(timezone)

start_of_day = datetime.combine(
    now.date(),
    time.min,
    tzinfo=timezone
)

end_of_day = datetime.combine(
    now.date(),
    time.max,
    tzinfo=timezone
)


def format_event_time(event):
    start = event.get("start", {})

    if "dateTime" in start:
        event_time = datetime.fromisoformat(start["dateTime"])
        return event_time.strftime("%-I:%M %p")

    return "All day"

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

def get_today_events():
    credentials = authenticate_google()
    service = build("calendar", "v3", credentials=credentials)

    events_result = service.events().list(
    calendarId="primary",
    timeMin=start_of_day.isoformat(),
    timeMax=end_of_day.isoformat(),
    singleEvents=True,
    orderBy="startTime"
).execute()

    events = events_result.get("items", [])

    return events

def create_daily_message(events):   
    message = "Good morning, Anastasiya!\n\n"

    if not events:
        message += "You don't have anything scheduled today."
        return message

    message += "Today you have:\n"

    for event in events:
        title = event.get("summary", "Untitled event")
        event_time = format_event_time(event)

        message += f"• {event_time} — {title}\n"

    return message

events = get_today_events()
message = create_daily_message(events)
