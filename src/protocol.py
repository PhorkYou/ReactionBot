# -*- coding: utf-8


from twisted.words.protocols import irc

from core.plugins.manager import plugin_manager
from core.plugins.interface import IInitialize, IFinalize, IStorable
from core.storage.database import storage


"""
more info:
  http://twistedmatrix.com/documents/current/api/twisted.words.protocols.irc.IRCClient.html
"""


class PluggableBotProto(irc.IRCClient):

    def signedOn(self):
        "called when succesfully signed on to server"
        self.join(self.factory.channel)
        plugins = plugin_manager.filter(
                channel=self.channel, interface=IInitialize)
        for plugin in plugins:
            plugin.initialize()
        plugins = plugin_manager.filter(
                channel=self.channel, interface=IStorable)
        for plugin in plugins:
            data = storage.get(plugin.name)
            if data:
                plugin.load(data)

    def connectionLost(self, reason):
        plugins = plugin_manager.filter(
                channel=self.channel, interface=IFinalize)
        for plugin in plugins:
            plugin.finalize()
        plugins = plugin_manager.filter(
                channel=self.channel, interface=IStorable)
        for plugin in plugins:
            storage.set(plugin.name, plugin.dump())
        storage.dump()
        irc.IRCClient.connectionLost(self, reason)

    def handleCommand(self, command, prefix, params):
        """Call approppriate plugins with given command"""
        irc.IRCClient.handleCommand(self, command, prefix, params)
        if len(params) < 2:
            return
        plugins = plugin_manager.filter(
                channel=self.channel, action=command.lower())
        for plugin in plugins:
            plugin.handle_action(protocol=self, action=command.lower(),
                    user=prefix, message=params[1])

    @property
    def nickname(self):
        return self.factory.nickname

    @property
    def channel(self):
        return self.factory.channel
