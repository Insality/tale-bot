#! /usr/bin/env python
# coding: utf-8
import sys
import time

from tale_bot import Tale_bot, get_time
from accounts import accounts

print('Starting tale-bots:\n')

log = './log/general.log'



bots = []
for acc in accounts:
	bots.append(Tale_bot(acc['email'], acc['password']))

for bot in bots:
	bot.login()
	bot.update_info()
	print(bot.get_info())


# Если были добавлены новые персонажы, активируйте на один запуск:
# for bot in bots:
# 	bot.send_friendship('12238')

timer = 30
general_info_counter = 30
general_info_max = 30
print("start the loop of decisions")
while True:
	general_info_counter += 1
	if (general_info_counter >= general_info_max):
		general_info_counter = 0;
		f = open(log, 'a')
		f.write(get_time() + '\n\n')
		for bot in bots:
			f.write(bot.get_info() + '\n')
		f.write('===============================\n\n')
		f.close()

	for bot in bots:
		bot.decision()

	# print(get_time() + " pause " + str(timer) + "sec")
	time.sleep(timer)

print("The bots was stopped")