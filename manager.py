#! /usr/bin/env python
# coding: utf-8
import sys
import time

from tale_bot import Tale_bot, get_time
from accounts import accounts

print('Starting tale-bots:\n')

log = 'D:/Dropbox/general.log'

bots = []
for acc in accounts:
	bots.append(Tale_bot(acc['email'], acc['password']))

for bot in bots:
	bot.login()
	bot.update_info()
	print(bot.get_info())
	print(bot.get_quest_text_choice())



# Если были добавлены новые персонажы, активируйте на один запуск:
# for bot in bots:
# 	bot.send_friendship('12238')

# print(bots[5].get_quest_info())
# print(bots[5].get_quest_text_choice())

timer = 30
# 120 - час для таймера 30 сек. 
general_info_counter = 180
general_info_max = 180
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
		print(get_time() + " general info was updated\n")

	for bot in bots:
		bot.decision()

	time.sleep(timer)

print("The Tale-bots was stopped")