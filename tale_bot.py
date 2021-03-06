#coding: utf-8
import requests
import uuid
import sys
import os
import logging
from datetime import datetime
import time

from requests.cookies import create_cookie

if not os.path.exists('./log'):
	os.mkdir('log')

actions= [
'безделие',
'задание',
'путешествие между городами',
'сражение 1x1 с монстром',
'воскрешение',
'действия в городе',
'отдых',
'экипировка',
'торговля',
'путешествие около города',
'всстановление энергии',
'действие без эффекта на игру',
'прокси-действия для взаимодействия героев',
'PvP 1x1',
'проверочное действие']

def get_time():
	cur_time = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']: '
	return cur_time

class Tale_bot:

	def __init__(self, email, password):
		self.default_params = {'api_version': '1.0', 'api_client': 'thetaleapipy-0.1'}
		self.email = email
		self.password = password
		self.domain = 'the-tale.org'
		self.host = 'http://' + self.domain
		self.session = requests.Session()

		self.log = ''
		self.name = ''
		self.level = 0
		self.health = 0
		self.max_health = 100
		self.health_perc = 50
		self.energy = 0
		self.max_energy = 100
		self.exp = 0
		self.max_exp = 100
		self.honor = 0
		self.peacefulness = 0
		self.items = 0
		self.max_items = 12
		self.power = 0
		self.action = 0
		self.action_desc = ''

	def update_info(self):
		time.sleep(1)
		hero_info = self.get_hero_info()

		self.name = hero_info['base']['name']
		self.log = './log/' + self.name.split()[0] + '.log'

		self.level = hero_info['base']['level']
		self.health = hero_info['base']['health']
		self.max_health =hero_info['base']['max_health']
		self.health_perc = self.health/self.max_health * 100
		self.honor = hero_info['habits']['honor']['raw']
		self.peacefulness = hero_info['habits']['peacefulness']['raw']
		self.max_exp = hero_info['base']['experience_to_level']
		self.exp = hero_info['base']['experience']
		self.is_alive = hero_info['base']['alive']
		self.items =  hero_info['secondary']['loot_items_count']
		self.max_items =  hero_info['secondary']['max_bag_size']
		self.energy =  hero_info['energy']['value']
		self.max_energy =  hero_info['energy']['max']
		self.action = hero_info['action']['type']
		self.action_desc = hero_info['action']['description']
		

	def get_info(self):
		self.update_info()
		info = ''
		info += 'Аккаунт: %s\n' % self.email
		info += 'Персонаж: %s(%i) ' % (self.name, self.level)
		info += 'HP: %i/%i(%i%%) ' % (self.health, self.max_health, self.health_perc)
		info += 'Energy: %i/%i ' % (self.energy, self.max_energy)
		info += 'Exp: %i/%i ' % (self.exp, self.max_exp)
		info += 'Items: %i/%i ' % (self.items, self.max_items)
		info += 'Honor/Peacef: %i/%i\n' % (self.honor, self.peacefulness)
		info += '%s: %s' % (actions[self.action], self.action_desc)
		info += '\n'
		return info

	def get_short_info(self):
		self.update_info()
		return 'HP: %i/%i(%i%%)' % (self.health, self.max_health, self.health_perc) + ' Energy: %i/%i' % (self.energy, self.max_energy) + ' Action: %s' % (actions[self.action])

	# Выполняет действие, если необходимо сделать в текущий момент
	def decision(self):
		self.update_info()

		if (self.energy >= 4):
			if (not self.is_alive):
				self.use_help()
				text = 'Help was used (Character is dead). ' + self.get_short_info()
				self.log_file(text)

			elif (int(self.health_perc) < 25 and self.action == 3 and self.energy >= 8):
				self.use_help()
				text = 'Help was used (HP < 25%%). ' + self.get_short_info()
				self.log_file(text)

			elif (self.energy == self.max_energy and self.items == self.max_items):
				self.use_ability('drop_item')
				text = 'Drop item was used (Max items). Items: %i/%i ' % (self.items, self.max_items) + self.get_short_info()
				self.log_file(text)

			elif (self.energy == self.max_energy):
				self.use_help()
				text = 'Help was used (Max energy): ' + self.get_short_info()
				self.log_file(text)

	def log_file(self, text):
		f = open(self.log, 'a')
		f.write(get_time())
		f.write(text + '\n')
		f.close()
		logging.info(get_time() + self.name + ' ' + text + '\n')

	def get_game_info(self):
		return self.make_request('/game/api/info').json()

	def get_account_info(self):
		return self.get_game_info()['data']['account']

	def get_quest_info(self):
		return self.get_game_info()['data']['account']['hero']['quests']

	def get_quest_text_choice(self):
		quests = self.get_quest_info()
		info = ''
		for quest in quests['quests']:
			info += 'Quest name %s: %s\n' % (quest['line'][0]['name'], quest['line'][0]['action'])
			info += 'Alternatives: %s ' % quest['line'][0]['choice_alternatives']
			info += 'Choice: %s ' % quest['line'][0]['choice']
			info += '\n\n'
		return info

	# def choose_quest(self, uid):
	# 	return self.make_request('/game/quests/api/choose/', 'post', data=dict(option_uid=uid)).json()

	def get_hero_info(self):
		return self.get_game_info()['data']['account']['hero']

	def use_ability(self, ability_name):
		return self.make_request('/game/abilities/{0}/api/use'.format(ability_name), 'post').json()

	def use_help(self):
		return self.use_ability('help')

	def make_request(self, path, method='get', params=None, **kwargs):
		params = params or {}
		actual_params = dict(self.default_params)
		actual_params.update(params)

		url = '{0}{1}'.format(self.host, path)
		method_callable = getattr(self.session, method)
		response = method_callable(url, params=actual_params, **kwargs)
		self.update_csrf()

		return response

	def update_csrf(self):
		csrf_value = self.session.cookies['csrftoken']
		self.session.headers.update({'X-CSRFToken': csrf_value})

	def send_friendship(self, id):
		response = self.make_request('/accounts/friends/request?friend=%s'%(id), 'post', data=dict(text='I want to friend you!'))
		return response

	def login(self):
		csrf_token = uuid.uuid4().hex
		self.session.headers.update({'X-CSRFToken': csrf_token})
		cookie = create_cookie('csrftoken', csrf_token, domain=self.domain)
		self.session.cookies.set_cookie(cookie)

		response = self.make_request('/accounts/auth/api/login', 'post', data=dict(email=self.email, password=self.password))
		return response


# check quest in list:
# quest['line'][0]['choice_alternatives'][0][1] in quest_evil
# id: first index
