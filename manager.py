#! /usr/bin/env python
# coding: utf-8

import os
import sys
import time

import logging
from tale_bot import Tale_bot, get_time
from accounts import accounts


cur_dir = os.path.dirname(__file__)
if (cur_dir == ""):
	cur_dir = "."

log = cur_dir + "/general.log"

def manager_start():
	logging.info('Starting tale-bots:\n')

	bots = []
	for acc in accounts:
		bots.append(Tale_bot(acc['email'], acc['password']))

	for bot in bots:
		bot.login()
		bot.update_info()
		logging.info(bot.get_info())
		logging.info(bot.get_quest_text_choice())

	# Если были добавлены новые персонажы, активируйте на один запуск:
	# for bot in bots:
	# 	bot.send_friendship('12238')

	timer = 30
	# 120 - час для таймера 30 сек. 
	general_info_counter = 180
	general_info_max = 180
	logging.info("start the loop of decisions")
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
			logging.info(get_time() + " general info was updated\n")

		for bot in bots:
			bot.decision()

		time.sleep(timer)
	logging.info("The Tale-bots was stopped")

if __name__=="__main__":
	try:
		arg = sys.argv[1]
	except IndexError:
		arg = ""

	filename = None
	if ("l" in arg):
		filename=cur_dir+"/log/ManagerStream.log"

	logging.basicConfig(filename=filename, level=logging.INFO,
					format = '[%(asctime)s] %(levelname)s: %(message)s',
					datefmt = '%Y-%m-%d %I:%M:%S')

	manager_start()