import os
import pusher
import yaml


class BismarkPusher(object):

    # The pusher object.
    pusher = {}

    def __init__(self):
        """
        Process the readme file.

        :return:
        """
        stream = open(os.getcwd() + "/settings.yml")
        pusher_settings = yaml.load(stream)

        print(pusher_settings)

        self.pusher = pusher.Pusher(
            app_id=pusher_settings['pusher']['app_id'],
            key=pusher_settings['pusher']['key'],
            secret=pusher_settings['pusher']['secret'],
            cluster=pusher_settings['pusher']['cluster'],
            ssl=pusher_settings['pusher']['ssl']
        )

    def send_message(self, channel, event, message):
        """
        Sending a message to pusher.

        :param channel:
            The channel of the message.
        :param event:
            The event of the message.
        :param message:
            The message.

        :return:
        """
        self.pusher.trigger(channel, event, message)
