import os
import pusher
import yaml


class BismarkPusher(object):

    # The pusher object.
    pusher = {}

    # The channel name.
    channel = ''

    def __init__(self, channel):
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
        self.channel = channel

    def send_message(self, event, message):
        """
        Sending a message to pusher.

        :param event:
            The event of the message.
        :param message:
            The message.

        :return:
        """
        self.pusher.trigger(self.channel, event, message)
