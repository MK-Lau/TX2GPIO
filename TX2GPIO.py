import subprocess
from time import sleep



def pinConversion(pin):
	userPinsList = (7,11,12,13,15,16,18,19,21,22,23,24,29,31,32,33,35,37,38,40)
	backendPinsList = (396,466,392,397,255,296,481,429,428,254,427,430,398,298,297,389,395,467,388,394,393)
	PinsList =(userPinsList,backendPinsList)
	if pin in PinsList[0]:
		i = PinsList[0].index(pin)
		pin = PinsList[1][i]
	if pin not in backendPinsList:
		raise ValueError('{} is not a valid GPIO pin '.format(pin))
	return pin

class Pin:

	def __init__(self, pin,dir):
		self.Pin = pinConversion(pin)
		self.dir = dir
		self.CurrentState = 0
		self.PinDirectory = '/sys/class/gpio/gpio{}'.format(self.Pin)
		subprocess.call('echo {} > /sys/class/gpio/export'.format(self.Pin),shell=True)
		subprocess.call('echo {} > /sys/class/gpio/gpio{}/direction'.format(self.dir,self.Pin),shell=True)

	def output(self,state):
		if self.dir == 'out':
			if state == 'high':
				state = 1
			elif state == 'low':
				state = 0
			if state != 1 and state != 0:
				raise ValueError('invalid state')

			subprocess.call('echo {} > /sys/class/gpio/gpio{}/value'.format(state,self.Pin),shell=True)
			self.CurrentState = state
		else:
			raise UserWarning('this pin is not setup as an output pin... No action was taken')



	def pulse(self,*args):
		if self.dir == 'out':
			if len(args) > 1:
				raise SyntaxError('Too may arguments given')
			elif len(args) == 0:
				t = 0.1
			else:
				t = args[0]

			if self.CurrentState == 1: #pulsing to low if value already high
				self.output(0)
				sleep(t)
				self.output(1)
			elif self.CurrentState == 0: #pulsing to high if value already high
				self.output(1)
				sleep(t)
				self.output(0)
		else:
			raise UserWarning('this pin is not setup as an output pin... No action was taken')

	def read(self):
		with open('/sys/class/gpio/gpio{}/value'.format(self.Pin),'r') as valFile:
			currentPinState = valFile.read(1)
			return currentPinState

	def close(self):
		subprocess.call('echo {} > /sys/class/gpio/unexport '.format(self.Pin),shell=True)
