import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.register_plugin('xep_0045') # Multi-User Chat

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self['xep_0045'].joinMUC('room@conference.jabber.site', 'your_name', wait=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    xmpp = EchoBot('your_user@conference.jabber.site', 'your_password')
    xmpp.connect()
    xmpp.process(block=True)
