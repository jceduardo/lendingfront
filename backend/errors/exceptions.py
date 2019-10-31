import tornado.web
import tornado.ioloop
import asyncio, selectors, sys, os

from resources import messages as MESSAGE

import http
from http import HTTPStatus

# Handle general exception
class LoanAppError(Exception):
	def __init__(self, message, error_code):
		self.message = message
		self.code = error_code
		super(Exception, self).__init__(message)

# Handle JSON invalid format
class InvalidData(LoanAppError):
	def __init__(self):
		LoanAppError.__init__(self, MESSAGE.JSON_INVALID, HTTPStatus.BAD_REQUEST)

# Handle action or context method incorrect
class ActionNotFound(LoanAppError):
    def __init__(self, action):
        LoanAppError.__init__(self, MESSAGE.ACTION_NOT_FOUND % str(action), HTTPStatus.NOT_FOUND)

# Handle internal server errors
class ServerError(LoanAppError):
    def __init__(self):
        LoanAppError.__init__(self, MESSAGE.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR)
	
