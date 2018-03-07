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
        settings = yaml.load(stream)

        self.pusher = pusher.Pusher(
            app_id=settings['pusher']['app_id'],
            key=settings['pusher']['key'],
            secret=settings['pusher']['secret'],
            cluster=settings['pusher']['cluster'],
            ssl=settings['pusher']['ssl']
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
