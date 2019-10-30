import tornado.web
import tornado.gen
import tornado.ioloop
import asyncio, selectors, sys, os
import config.setting as SETUP
import adapters.handlers as HANDLER
import json, traceback, logging
import abc
from abc import ABCMeta, abstractmethod

logging.basicConfig(level = logging.DEBUG)
LOGGER = logging.getLogger('loanapp')

def main():
	# This selector allow Tornado works fine in windows
	if (SETUP.OS_WINDOWS in os.environ):
		selector = selectors.SelectSelector()
		loop = asyncio.SelectorEventLoop(selector)
		asyncio.set_event_loop(loop)
	# Construct and serve the loan application
	handler = HANDLER.LoanHandler_Adapter
	application = tornado.web.Application([(r"/", HANDLER.HttpDefaultHandler),(r"/loan_api/(?P<action>[A-Za-z]+)?", handler)], debug=True) 
	application.listen(SETUP.PORT)
	LOGGER.debug('Listening on port %i' % SETUP.PORT)
	tornado.ioloop.IOLoop.current().start()
	
if __name__ == '__main__':
	main()