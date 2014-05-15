#! /usr/bin/env python
# coding: utf-8
import sys
from tale_bot import Tale_bot

print('Starting tale-bots:')

bots = []
for acc in accounts:
	bots.append(Tale_bot(acc['email'], acc['password']))

Insabot = bots[0]
Insabot.login()

print(Insabot.get_hero_info()['base'])
