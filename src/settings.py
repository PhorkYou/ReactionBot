#!/usr/bin/env python
# -*- coding: utf-8



#from sqlalchemy import create_engine
#DATABASE_ENGINE = create_engine('sqlite:///:memory:')

# set all your connections here
CONNECTIONS = (
        ('irc.freenode.net', 6667, 'test_bot', 'twistedbot'),
        #('irc.freenode.net', 6667, 'test_bot_2', 'twistedbot2'),
        )

# set plugins that should be loaded
PLUGINS = (
        #'plugins.reminder',

        #'plugins.demo.periodic',
        #'plugins.demo.logger',
        #'plugins.demo.echo.handler',
        )
