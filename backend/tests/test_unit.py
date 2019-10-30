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
			"bsn_tax_id": "173554531",
			"bsn_name": "MoneyExpress INC",
			"bsn_address": "Street 34 #27-19",
			"bsn_city": "Medellin",
			"bsn_state": "Antioquia",
			"bsn_postal_code": "30000",
			"bsn_requested_amount": 49999,
			"owr_social_security_number": "S1836647",
			"owr_name": "Juan",
			"owr_email": "juan@gmail.com",
			"owr_address": "Street 45B #24-180",
			"owr_city": "Medellin",
			"owr_state": "Antioquia",
			"owr_postal_code": "30001"
		}
		
		try:
			result = self.post("/loan/register", loan_register)
			
			self.assertIn("loan_decision", result)			
			self.assertEqual(result["loan_decision"], "Approved")
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_undecided(self):
		loan_register = {
			"bsn_tax_id": "173554532",
			"bsn_name": "High Business INC",
			"ban_Address": "Street 34 #27-19",
			"bsn_city": "Medellin",
			"bsn_state": "Antioquia",
			"bsn_postal_code": "30002",
			"bsn_requested_amount": 50000,
			"owr_social_security_number": "S1836648",
			"owr_name": "Ana",
			"owr_email": "ana@hotmail.com",
			"owr_address": "Street 105B #30-51",
			"owr_city": "Medellin",
			"owr_state": "Antioquia",
			"owr_postal_code": "30003"
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("loan_decision", result)
			self.assertEqual(result["loan_decision"], "Undecided")
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_declined(self):
		loan_register = {
			"bsn_tax_id": "173554533",
			"bsn_name": "Conexmy INC",
			"bsn_address": "Street 10 #15-63",
			"bsn_city": "Medellin",
			"bsn_state": "Antioquia",
			"bsn_postal_code": "30004",
			"bsn_requested_amount": 50001,
			"owr_social_security_number": "S1836649",
			"owr_name": "Lucas",
			"owr_email": "lucas@hotmail.com",
			"owr_address": "Street 30 #19-76",
			"owr_city": "Medellin",
			"owr_state": "Antioquia",
			"owr_postal_code": "30005"
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("loan_decision", result)
			self.assertEqual(result["loan_decision"], "Declined")
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_zero_amount(self):
		loan_register = {
			"bsn_tax_id": "173554534",
			"bsn_name": "BusinessStreet INC",
			"bsn_address": "Street 10 #15-63",
			"bsn_city": "Medellin",
			"bsn_state": "Antioquia",
			"bsn_postal_code": "30006",
			"bsn_requested_amount": 0,
			"owr_social_security_number": "S1836625",
			"owr_name": "David",
			"owr_email": "david@hotmail.com",
			"owr_address": "Street 31 #109-10",
			"owr_city": "Medellin",
			"owr_state": "Antioquia",
			"owr_postal_code": "30007"
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("loan_status", result)
			self.assertEqual(result["loan_status"], "Inactive")
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_negative_amount(self):
		loan_register = {
			"bsn_tax_id": "173554535",
			"bsn_name": "BankOfAmerica INC",
			"bsn_address": "Street 10 #15-63",
			"bsn_city": "Medellin",
			"bsn_state": "Antioquia",
			"bsn_postal_code": "30008",
			"bsn_requested_amount": -1,
			"owr_social_security_number": "S1836626",
			"owr_name": "Pedro",
			"owr_email": "pedro@hotmail.com",
			"owr_address": "Street 33 #79-12",
			"owr_city": "Medellin",
			"owr_state": "Antioquia",
			"owr_postal_code": "30009"
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("loan_status", result)

			self.assertIn("Inactive", result["loan_status"])
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_without_requested_amount(self):
		loan_register = {
			"bsn_tax_id": "173554536",
			"bsn_name": "BankOfAmerica INC",
			"bsn_address": "Street 80 #65-82",
			"bsn_city": "Medellin",
			"bsn_state": "Antioquia",
			"bsn_postal_code": "30010",
			"owr_social_security_number": "S1836626",
			"owr_name": "Ana",
			"owr_email": "ana@gmail.com",
			"owr_address": "Street 55 #90-28",
			"owr_city": "Medellin",
			"owr_state": "Antioquia",
			"owr_postal_code": "30011"
		}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("loan_decision", result)
			self.assertEqual(result["loan_decision"], "Requested amount parameter does not exists")
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())
			
	def test_internal_server_error(self):
		loan_register = {}
		try:
			result = self.post("/loan/register", loan_register)
					
			self.assertIn("loan_decision", result)
			self.assertEqual(result["loan_decision"], "Requested amount parameter does not exists")
		except JSONDecodeError as error:
			console("Error trace: %s" % traceback.format_exc())

if __name__ == "__main__":
	unittest.main()