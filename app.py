from main import app, slack_events_adapter
from main.event_handlers.slack_event_handler import SlackEventHandler

slack_event_handler = SlackEventHandler()


@slack_events_adapter.on('app_mention')
def handle(event_data):
    return slack_event_handler.event_handler(event_data)


@app.route('/')
def index():
    return 'Valens Crypto Bot'


if __name__ == '__main__':
    app.run()
