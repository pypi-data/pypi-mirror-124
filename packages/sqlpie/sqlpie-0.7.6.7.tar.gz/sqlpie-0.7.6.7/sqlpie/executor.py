from concurrent.futures import ThreadPoolExecutor
from sqlpie.client import Sqlpie
from time import sleep
from datetime import datetime
import random
import time  
import requests
import string

class Executor:

	def __init__(self, version, logs_endpoint=None):
		self._run_id = version['_run_id']
		self.version = version
		self.queue = []
		self.results = {}
		print('pkg log', logs_endpoint)
		self.logs_endpoint = logs_endpoint
		ind_nodes = self.version['dag']['ind_nodes']
		self.append_to_queue(ind_nodes)
		print(self.queue)
		self.run()

	def run_task(self, payload):
		if payload['node'] not in self.results.keys():
			self.results[payload['node']] = {}
		self.results[payload['node']]['run_logs'] = []	
		self.results[payload['node']]['run_logs'].append(f"Running {payload['node']}")
		self.results[payload['node']]['run_logs'].append(f"Rendered Query")
		self.results[payload['node']]['run_logs'].append(f"{payload['rendered_query']}")
		self.results[payload['node']]['started_at'] = str(str(datetime.utcnow()))		
		self.set_results(payload, 'running', 0)
		print('='*50)
		print('running')
		print('node name - ', payload['node'])
		secs = random.randint(1,10)
		sleep(10) ##run_query
		db_response = 'query completed'
		self.results[payload['node']]['run_logs'].append(db_response)
		count = self.results[payload['node']]['count'] + 1
		self.results[payload['node']]['completed_at'] = str(datetime.utcnow())
		self.set_results(payload,'completed', count)
		print(f"took {secs} seconds")
		print('completed')
		print('='*50)
		print('Appending downstreams - ', payload['downstreams'])
		self.append_to_queue(payload['downstreams'])
		self.run()

	def get_upstream_statuses(self,payload):
		return list(filter(None,set(list(map(lambda upstream: self.results[upstream]['status'] if upstream in self.results.keys() else 'not started', payload['upstreams'])))))

	def execute_task(self, payload):
		if payload in self.queue:
			self.queue.remove(payload)
		print('node', payload['node'])
		print('upstreams', payload['upstreams'])
		# print('results - ', self.results.keys())			
		if payload['upstreams']:
			upstream_statuses =	self.get_upstream_statuses(payload)
			print('reduced upstream statuses', upstream_statuses)
			if upstream_statuses == ['completed']:
				print('dependecies completed - starting task')
				if payload['node'] in self.results.keys():
					print(f"Task {self.results[payload['node']]['status']}")
				else:
					self.run_task(payload)
				return True
			else:
				print('not starting - waiting for dependecies to complete')
				print('task statuses - ', self.results)
				if payload not in self.queue:
					self.queue.append(payload)
				return False																
		else:
			print('no dependecies - starting task')
			self.run_task(payload)
			return True

	def append_to_queue(self, nodes):		
		for node in nodes:
			print(node, self.version['table_index'][node]['source_type'])
			if self.version['table_index'][node]['source_type'] in ('model', 'prep'):
				self.queue.append(self.build_payload(node))
			else:
				downstream_nodes = self.version['dag']['dag_index'][node]['downstreams']
				self.append_to_queue(downstream_nodes)

	def build_payload(self, node):
		model_name = self.version['table_index'][node]['schema']
		print('model_name', model_name)
		if '_prep' in model_name:
			model_name = model_name.replace('_prep', '')
		payload = self.version['models'][model_name]['rendered_model'][node]
		payload['node'] = node
		payload['downstreams'] = self.version['dag']['dag_index'][node]['downstreams']
		payload['upstreams'] = self.version['dag']['dag_index'][node]['predecessors']
		return payload

	def set_results(self, payload, status, count=0):
		self.results[payload['node']]['status'] = status
		self.results[payload['node']]['count'] = count
		self.results[payload['node']]['query'] = payload['rendered_query']
		if self.logs_endpoint:
			data = {}
			data = {'logs_metadata': self.version['logs_metadata'], 'results': self.results}
			# print('logs-', data)
			response = requests.post(self.logs_endpoint, json=data)
			print(response)

	def run(self):
		print('queue lenght-', len(self.queue))		
		with ThreadPoolExecutor(max_workers = 5) as executor:
			results = executor.map(self.execute_task, self.queue)


