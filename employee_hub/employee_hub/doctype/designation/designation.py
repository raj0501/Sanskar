# Copyright (c) 2026, Raj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Designation(Document):
	def validate(self):
		self.designation_name = self.designation_name.strip()
		self.validate_duplicate_designation()

	def validate_duplicate_designation(self):
		duplicate = frappe.db.sql(
            """
            SELECT name
            FROM `tabDesignation`
            WHERE LOWER(designation_name)=LOWER(%s)
            AND name!=%s
            """,
            (self.designation_name, self.name),
        )

		if duplicate:
			frappe.throw("Designation Name already exists.")
