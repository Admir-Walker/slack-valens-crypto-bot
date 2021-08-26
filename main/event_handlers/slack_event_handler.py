from main.event_handlers.app_mention_service import AppMentionService

# If you want to add new command, just add new function with command name
# e.g. command help -> function help


class SlackEventHandler():
    def event_handler(self, event_data):
        message: str = event_data['event']['blocks'][0]['elements'][0]['elements'][1]['text']
        message_commands = list(
            filter(lambda x: x.strip() != '', message.split(' ')))

        command = message_commands[0].lower()
        operation = getattr(self, command, None)

        # Special case, when we specify list of currencies to display
        # @bot_name space-separated-crypto-symbols
        if operation is None:
            return AppMentionService.latest_listings(commands=message_commands, event_data=event_data)
        elif callable(operation):
            # We dont include name of command
            operation(commands=message_commands[1:], event_data=event_data)

    # @bot_name help
    def help(self, **kwargs):
        return AppMentionService.help(**kwargs)
    # @bot_name schedule hh:mm space-separated-crypto-symbols

    def schedule(self, **kwargs):
        return AppMentionService.schedule(**kwargs)

    def schedule_remove(self, **kwargs):
        return AppMentionService.schedule_remove(**kwargs)