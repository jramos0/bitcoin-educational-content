import yaml
from datetime import datetime, timedelta
import os

# Custom Dumper to ensure strings are dumped without quotes
class CustomDumper(yaml.SafeDumper):
    def represent_str(self, data):
        if data.startswith('202'):
            return self.represent_scalar('tag:yaml.org,2002:timestamp', data)
        return self.represent_scalar('tag:yaml.org,2002:str', data)

# Register custom dumper for strings
yaml.add_representer(str, CustomDumper.represent_str, Dumper=CustomDumper)

# Path to the file
file_path = '/home/jramos/sovereign-university-data/resources/conference/pleblab-tuesday-2024/events.yml'

# Create the directory if it does not exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Read the existing file or initialize an empty list if it does not exist
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        existing_events = yaml.safe_load(file) or []
else:
    existing_events = []

# Remove all events that have a start date before today
today = datetime.now()

existing_events = [
    event for event in existing_events
    if isinstance(event['start_date'], str) and datetime.strptime(event['start_date'], '%Y-%m-%d %H:%M:%S') >= today
]

# Recurring event configuration
days_interval = 7  # Every week
today = datetime.now().date()

# Start date for the event
start_date = datetime(2024, 7, 23).date()

# Find the next Tuesday
if today > start_date:
    days_until_next_tuesday = (1 - today.weekday() + 7) % 7
    if days_until_next_tuesday == 0:
        days_until_next_tuesday = 7
    next_tuesday = today + timedelta(days=days_until_next_tuesday)
else:
    next_tuesday = start_date

# Check if an event for the next Tuesday already exists
existing_event = next((event for event in existing_events if event['start_date'] == next_tuesday.strftime('%Y-%m-%d 14:00:00')), None)

if not existing_event:
    # Create a new event if it does not exist
    new_event = {
        'start_date': next_tuesday.strftime('%Y-%m-%d 14:00:00'),
        'end_date': next_tuesday.strftime('%Y-%m-%d 22:00:00'),
        'address_line_1': 'Austin, USA',
        'address_line_2': '',
        'address_line_3': '',
        'name': 'Open Hackerspace Day',
        'builder': 'PlebLab',
        'type': 'course',
        'book_online': False,
        'book_in_person': False,
        'price_dollars': 0,
        'description': 'Every Tuesday, we open our doors to the Bitcoin Builders, from simple projects and creators to forward-thinking developers. It is a collaborative space where your Bitcoin project or startup takes center stage.',
        'language': ['en'],
        'links': {
            'website': 'https://www.meetup.com/pleb-lab/events/302290112/?utm_medium=referral&utm_campaign=share-btn_savedevents_share_modal&utm_source=link',
            'replay_url': '',
            'live_url': ''
        },
        'tags': ['bitcoiner', 'general', 'hacker'],
        'timezone': 'America/Chicago'
    }

    # Only keep the next event
    existing_events = [new_event]

    # Save the updated events using the custom dumper
    with open(file_path, 'w') as file:
        yaml.dump(existing_events, file, default_flow_style=False, Dumper=CustomDumper)

    print(f'An event has been added for the date {new_event["start_date"]}')
else:
    print(f'The event for the date {next_tuesday.strftime("%Y-%m-%d 14:00:00")} already exists')
