import json, unittest, asyncio, selectors, sys, os, traceback, json.decoder
import tornado.web

from tornado.testing import AsyncHTTPTestCase
from server import LoanHandler
from json.decoder import JSONDecodeError 

import http
from http import HTTPStatus

class ServerTest(AsyncHTTPTestCase):
	def get_app(self):
		return tornado.web.Application([(r"/loan/(?P<action>[A-Za-z]+)?", LoanHandler)], debug=True)

	def post(self, route, data):
		result = self.fetch(route,method="POST",body=json.dumps(data)).body
		try:
			return json.loads(result)
		except ValueError:
			raise ValueError(result)

class LoanTest(ServerTest):	
	
	def test_approved(self):
		loan_register = {
			"business": {
				"taxId": "T173554531",
				"businessName": "MoneyExpress INC",
				"businessAddress": "Street 34 #27-19",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30000",
				"amount": 49999
			},
			"owner": {
				"socialSecurity": "S1836647",
				"name": "Juan",
				"email": "juan@gmail.com",
				"address": "Street 45B #24-180",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30001"
			}
		}
		
		try:
			result = self.post("/loan/register", loan_register)
			
			self.assertIn("status", result)
			self.assertIn("data", result)
			
			self.assertEqual(result["data"], "Approved")
			self.assertEqual(result["status"], HTTPStatus.OK)
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_undecided(self):
		loan_register = {
			"business": {
				"taxId": "T173554532",
				"businessName": "High Business INC",
				"businessAddress": "Street 34 #27-19",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30002",
				"amount": 50000
			},
			"owner": {
				"socialSecurity": "S1836648",
				"name": "Ana",
				"email": "ana@hotmail.com",
				"address": "Street 105B #30-51",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30003"
			}
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("status", result)
			self.assertIn("data", result)

			self.assertEqual(result["data"], "Undecided")
			self.assertEqual(result["status"], HTTPStatus.OK)
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_declined(self):
		loan_register = {
			"business": {
				"taxId": "T173554533",
				"businessName": "Conexmy INC",
				"businessAddress": "Street 10 #15-63",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30004",
				"amount": 50001
			},
			"owner": {
				"socialSecurity": "S1836649",
				"name": "Lucas",
				"email": "lucas@hotmail.com",
				"address": "Street 30 #19-76",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30005"
			}
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("status", result)
			self.assertIn("data", result)

			self.assertEqual(result["data"], "Declined")
			self.assertEqual(result["status"], HTTPStatus.OK)
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_zero_amount(self):
		loan_register = {
			"business": {
				"taxId": "T173554534",
				"businessName": "BusinessStreet INC",
				"businessAddress": "Street 10 #15-63",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30006",
				"amount": 0
			},
			"owner": {
				"socialSecurity": "S1836625",
				"name": "David",
				"email": "david@hotmail.com",
				"address": "Street 31 #109-10",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30007"
			}
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("status", result)
			self.assertIn("data", result)

			self.assertEqual(result["data"], "Bad request. Data sent with negative or zero loan value.")
			self.assertEqual(result["status"], HTTPStatus.BAD_REQUEST)
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_negative_amount(self):
		loan_register = {
			"business": {
				"taxId": "T173554535",
				"businessName": "BankOfAmerica INC",
				"businessAddress": "Street 10 #15-63",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30008",
				"amount": -1
			},
			"owner": {
				"socialSecurity": "S1836626",
				"name": "Pedro",
				"email": "pedro@hotmail.com",
				"address": "Street 33 #79-12",
				"city": "Medellin",
				"state": "Antioquia",
				"postalCode": "30009"
			}
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("status", result)
			self.assertIn("data", result)

			self.assertEqual(result["data"], "Bad request. Data sent with negative or zero loan value.")
			self.assertEqual(result["status"], HTTPStatus.BAD_REQUEST)
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_internal_server_error(self):
		loan_register = {}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("status", result)
			self.assertIn("data", result)

			self.assertEqual(result["data"], "Bad request. Data sent without default value and no parameter with given name.")
			self.assertEqual(result["status"], HTTPStatus.BAD_REQUEST)
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())

if __name__ == "__main__":
	unittest.main()