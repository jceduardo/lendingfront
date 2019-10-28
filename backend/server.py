import tornado.web
import tornado.gen
import tornado.ioloop

from tornado.options import define, options

import asyncio, selectors, sys, os

import http
from http import HTTPStatus

# Handler
import json, traceback, logging

define('PORT', default=8888)

logging.basicConfig(level = logging.DEBUG)
LOGGER = logging.getLogger('loan')

class LoanAppError(Exception):
	def __init__(self, message, error_code):
		self.message = message
		self.code = error_code
		super(Exception, self).__init__(message)

class InvalidData(LoanAppError):
	def __init__(self):
		LoanAppError.__init__(self, "Data (JSON) format not valid.", HTTPStatus.BAD_REQUEST)

class ActionNotFound(LoanAppError):
    def __init__(self, action):
        LoanAppError.__init__(self, "Action %s not found" % str(action), HTTPStatus.NOT_FOUND)

class ServerError(LoanAppError):
    def __init__(self):
        LoanAppError.__init__(self, "Internal server error", HTTPStatus.INTERNAL_SERVER_ERROR)

class HttpHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		# Tornado cors Options
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "Content-Type")
		self.set_header("Access-Control-Allow-Methods", "OPTIONS")

	@tornado.gen.coroutine
	def post(self, action):
		try:
			#Search action in LoanHandler
			LOGGER.debug("Action received: %s " % str(action))
			if not hasattr(self, str(action)):
				raise ActionNotFound(action)

			# Enviar la data al metodo encontrado
			handler = getattr(self, str(action))			
			handler(self.request.body)		
		except web.HTTPError or ServerError as error:
			LOGGER.debug("Server error trace: %s" % traceback.format_exc())
			self.send_response(error.message, error.code)
		except LoanAppError as error:
			LOGGER.debug("Error trace: %s" % traceback.format_exc())
			self.send_response(error.message, error.code)

	def send_response(self, data, status):
		#Construct and send a JSON response with appropriate status code.
		self.set_status(status)
		json_tosend = { "status": status, "data": data }
		self.write(json_tosend)
		self.finish()
		
class LoanHandler(HttpHandler):
	def loanDecision(self):
		return lambda requested_amount: "Approved" if (requested_amount > 0 and requested_amount < 50000) else "Declined" if requested_amount > 50000 else "Undecided" if requested_amount == 50000 else "BadRequest"
		
	def register(self, data):
		verifyLoanDecision = self.loanDecision()
		try:
			jsonData = json.loads(data)
			if ('business' in jsonData):
				if ( 'amount' in jsonData['business']):
					requested_amount = int(jsonData['business']['amount'])
					response = verifyLoanDecision(requested_amount)
					LOGGER.debug("Response: %s" % response)
					if 'BadRequest' != response:
						LOGGER.debug("Business name: %s " % jsonData['business']['businessName'])
						LOGGER.debug("Amount received: %d " % requested_amount)
						self.send_response(response, HTTPStatus.OK)
					else:
						response = "Bad request. Data sent with negative or zero loan value."
						self.send_response(response, HTTPStatus.BAD_REQUEST)
				else:
					response = "Bad request. Data sent without default value and no parameter with given name."
					self.send_response(response, HTTPStatus.BAD_REQUEST)
			else:
				response = "Bad request. Data sent without default value and no parameter with given name."
				self.send_response(response, HTTPStatus.BAD_REQUEST)
		except JSONDecodeError or ValueError as error:
			LOGGER.debug("Error trace: %s" % traceback.format_exc())
			raise InvalidData(error)
		except web.HTTPError as error:
			LOGGER.debug("Server error trace: %s" % traceback.format_exc())
			raise ServerError(error)

def main():
	if ('PROGRAMFILES(X86)' in os.environ):
		selector = selectors.SelectSelector()
		loop = asyncio.SelectorEventLoop(selector)
		asyncio.set_event_loop(loop)
	"""Construct and serve the loan application."""
	application = tornado.web.Application([(r"/loan/(?P<action>[A-Za-z]+)?", LoanHandler)], debug=True)
	application.listen(options.PORT)
	LOGGER.debug('Listening on port %i' % options.PORT)
	tornado.ioloop.IOLoop.current().start()
	
if __name__ == '__main__':
	main()