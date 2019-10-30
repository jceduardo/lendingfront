import tornado.web
import tornado.gen
import tornado.ioloop
import json, traceback, logging
import errors.error
import config.setting as SETUP
import resources.messages as MESSAGE
import abc
from abc import ABC, abstractmethod

import http
from http import HTTPStatus

# Logger 
logging.basicConfig(level = logging.DEBUG)
LOGGER = logging.getLogger('handler')

# Abtract class provides un handler adapter
# HttpDefaultHandler extends RequestHandler and respond to HTTP requests with GET method
class HttpDefaultHandler(tornado.web.RequestHandler):

	# GET method when from the browser send a request entering server domain and port
    @tornado.gen.coroutine
    def get(self):
        self.write(SETUP.SERVER_UP)
        self.finish()

# HttpHandler extends RequestHandler that respond to HTTP requests that match particular criteria
class HttpHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Origin, Authorization, X-Requested-With')

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
		except HTTPError or ServerError as error:
			LOGGER.debug("Server error trace: %s" % traceback.format_exc())
			self.send_response(error.message, error.code)
		except LoanAppError as error:
			LOGGER.debug("Error trace: %s" % traceback.format_exc())
			self.send_response(error.message, error.code)

	def send_response(self, data, status):
		#Construct and send a JSON response with appropriate status code.
		self.set_status(status)
		if status == HTTPStatus.BAD_REQUEST:
			json_tosend = { "loan_decision": data, "loan_status": SETUP.LOAN_STATUS_INACTIVE }
		else:
			json_tosend = { "loan_decision": data, "loan_status": SETUP.LOAN_STATUS_ACTIVE }
		self.write(json_tosend)
		self.finish()
	
# Abtract class provides un handler adapter
class AbstractHandler(HttpHandler):		
	__metaclass__ = abc.ABCMeta
	
	# Loan decision abstract method
	@abstractmethod
	def loanDecision(self):
		pass
 
	# Register a loan abstract method
	@abstractmethod
	def register(self, data):
		pass
		
# LoanHandler class extends HttpHandler. Receives logging messages from request and makes loan decision	
class LoanHandler_Adapter(AbstractHandler):

	# Makes loan decision
	def loanDecision(self):
		return lambda requested_amount: SETUP.LOAN_DECISION_APPROVED if (requested_amount > 0 and requested_amount < 50000) else SETUP.LOAN_DECISION_DECLINED if requested_amount > 50000 else SETUP.LOAN_DECISION_UNDECIDED if requested_amount == 50000 else SETUP.LOAN_REQUEST_INVALID
	
	# Action method that allow register a loan 
	def register(self, data):
		verifyLoanDecision = self.loanDecision()
		try:
			jsonData = json.loads(data)
			if ( 'bsn_requested_amount' in jsonData):
				if (jsonData['bsn_requested_amount'] == '' or jsonData['bsn_requested_amount'] == None):
					response = SETUP.LOAN_REQUEST_INVALID
					LOGGER.debug("Response: %s" % response)
					self.set_status(HTTPStatus.OK,)
					json_tosend = { "loan_decision": SETUP.LOAN_STATUS_NONE, "loan_status": SETUP.LOAN_STATUS_INACTIVE }
					self.write(json_tosend)
					self.finish()
				else:
					requested_amount = float(jsonData['bsn_requested_amount'])
					response = verifyLoanDecision(requested_amount)
					LOGGER.debug("Response: %s" % response)
					if 'BadRequest' != response:
						LOGGER.debug("Business name: %s " % jsonData['bsn_name'])
						LOGGER.debug("Amount received: %d " % requested_amount)
						self.send_response(response, HTTPStatus.OK)
					else:
						response = SETUP.LOAN_STATUS_INACTIVE
						self.set_status(HTTPStatus.OK,)
						json_tosend = { "loan_decision": SETUP.LOAN_STATUS_NONE, "loan_status": SETUP.LOAN_STATUS_INACTIVE }
						self.write(json_tosend)
						self.finish()
			else:
				response = MESSAGE.PARAMETER_NOT_EXISTS
				self.send_response(response, HTTPStatus.BAD_REQUEST)

		except JSONDecodeError or ValueError as error:
			LOGGER.debug("Error trace: %s" % traceback.format_exc())
			raise InvalidData(error)
		except web.HTTPError as error:
			LOGGER.debug("Server error trace: %s" % traceback.format_exc())
			raise ServerError(error)

