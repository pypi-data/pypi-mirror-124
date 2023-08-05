from skylark.core.streams import StreamClient

import cv2
import time
import asyncio
from skylark.core.clients import RealTimeClient
import sys
from skylark.core.clients import Service
import json
import base64
import numpy as np


class NightDayStreamClient(StreamClient):
	def __init__(self, fps, batch_size, sampling_rate, token):
		self.fps = fps
		self.frames = []
		self.json = ""
		self.syncid = -1
		self.batch_size = batch_size
		self.sampling_rate = sampling_rate
		self.sample_length = int(fps / sampling_rate)
		self.delay_sec = 1 / self.fps
		self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		self.token = token
		self.client = RealTimeClient(Service.NIGHT_DAY, self.on_receive, batch_size, self.on_network_status_change, token)
		self.response_jsons = []
		self.createTasks()

	async def show_stream(self):
		# on message receive from websocket, we parse json response and show stream using cv2
		while True:
			if len(self.response_jsons) == 0:
				# if no responses then keep waiting for some message to be received
				print("waiting")
				await asyncio.sleep(1)
				continue
			# take out one of the response from beginning and apply the result to the frames
			response = self.response_jsons.pop(0)
			# syncid is used to maintain between sent and received frames
			self.syncid = self.syncid + self.batch_size
			syncids = response["sync"]
			if self.syncid != syncids[-1]:
				# if syncid sent and received for a particular response is not same then acheive sync
				print("not in sync:")
				print(self.syncid)
				print(syncids[-1])
				if self.syncid > syncids[-1]:
					# discarding results
					while self.syncid != syncids[-1]:
						syncids = response["sync"]
						self.response_jsons.pop(0)
				else:
					# discarding frames
					while self.syncid != syncids[-1]:
						self.frames.pop()
						self.syncid = self.syncid + 1
				continue
			else:
				# when in sync move further
				try:
					print("showing frame.......")

					# print(response["results"])
					result = response["results"]
					result = json.loads(result)
					for key in result:
						img = base64.b64decode(result[key])
						data = np.fromstring(img, dtype=np.uint8)
						img = cv2.imdecode(data, 1)
						cv2.imshow("outputStream", img)




				except Exception as e:
					exception_type, exception_object, exception_traceback = sys.exc_info()
					line_number = exception_traceback.tb_lineno
					print(e)
					print("Line number: ", line_number)
