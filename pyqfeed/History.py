import datetime, threading, logging
import OldClient, dispatcher

class HistoryClient(dispatcher.Dispatcher):
	def __init__(self, (host, port) = ("127.0.0.1", 9100)):
		dispatcher.Dispatcher.__init__(self)
		self.host = host
		self.port = port
		self.instrument = None
		self.exit_thread = threading.Event()

	def getHistory(self, instrument, date, num_days=1):
		self.exit_thread.clear()
		self.instrument = instrument

		self.client = OldClient.Client((self.host, self.port))
		self.client.set_listener('', self)
		self.client.start()
		#self.client.send("HTD,%s,%i,,,,1" % (self.instrument, num_days))
		logging.debug("HDX,%s,%i,1"% (self.instrument, num_days))
#		self.client.send("HID,%s,60,%i,,,,1" % (self.instrument, num_days))
		#self.client.send("HDX,%s,%i,1"% (self.instrument, num_days))
		self.client.join()

		import time
		time.sleep(1)

	def stop(self):
		self.disconnect()

	def disconnect(self):
		logging.debug("Trying to disconnect...")
		self.client.stop()

	def on_message(self, data):
		if data.startswith("E,!"):
			map(lambda l: l.on_error(data), self._listeners.values())
			self.disconnect()
		elif data.startswith("!ENDMSG!"):
			map(lambda l: l.on_data_end(), self._listeners.values())
			self.disconnect()
		else:
			map(lambda l: l.on_message(data), self._listeners.values())
						
	
