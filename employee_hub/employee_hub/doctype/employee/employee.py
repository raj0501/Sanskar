# Copyright (c) 2026, Raj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.utils import validate_email_address

class Employee(Document):
	def before_save(self):
		self.set_full_name()

	def validate(self):
		self.validate_age()
		self.validate_joining_date()
		self.validate_email()
		self.validate_dob_and_joining()
	
	def set_full_name(self):
		self.full_name = f"{self.first_name} {self.last_name}"

	def validate_age(self):
		dob = getdate(self.date_of_birth)
		current_date = getdate(today())

		age = (
            current_date.year
            - dob.year
            - ((current_date.month, current_date.day) < (dob.month, dob.day))
        )

		if age < 18:
			frappe.throw("Employee must be at least 18 years old.")

	def validate_joining_date(self):
		if getdate(self.date_of_joining) > getdate(today()):
			frappe.throw("Date of Joining cannot be in the future.")

	def validate_email(self):
		if self.employee_email:
			validate_email_address(self.employee_email, throw=True)

	def validate_dob_and_joining(self):
		if getdate(self.date_of_joining) <= getdate(self.date_of_birth):
			frappe.throw("Date of Joining must be after Date of Birth.")