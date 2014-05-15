#coding: utf-8
import requests
import uuid
import sys

from requests.cookies import create_cookie

import logging



class Tale_bot:

	def __init__(self, email, password):
		self.default_params = {'api_version': '1.0', 'api_client': 'thetaleapipy-0.1'}
		self.email = email
		self.password = password
		self.domain = 'the-tale.org'
		self.host = 'http://' + self.domain
		self.session = requests.Session()

		self.name = ''
		self.level = 0
		self.health = 0
		self.max_health = 100
		self.energy = 0
		self.max_energy = 100
		self.exp = 0
		self.max_exp = 100


	def update_info(self):
		pass

	def print_info(self):
		print('Account: ', self.login)
		pass

	# Выполняет действие, если необходимо сделать в текущий момент
	def decision(self):
		pass

	def get_game_info(self):
		return self.make_request('/game/api/info').json()

	def get_account_info(self):
		return self.get_game_info()['data']['account']

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
		# logger.debug('Getting %s', response.request.url)
		# logger.debug('response: %s', response.text)

		self.update_csrf()

		return response

	def update_csrf(self):
		csrf_value = self.session.cookies['csrftoken']
		self.session.headers.update({'X-CSRFToken': csrf_value})

	def login(self):
		csrf_token = uuid.uuid4().hex
		self.session.headers.update({'X-CSRFToken': csrf_token})
		cookie = create_cookie('csrftoken', csrf_token, domain=self.domain)
		self.session.cookies.set_cookie(cookie)

		response = self.make_request('/accounts/auth/api/login', 'post', data=dict(email=self.email, password=self.password))
		return response