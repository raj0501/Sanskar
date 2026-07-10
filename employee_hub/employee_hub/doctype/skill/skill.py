# Copyright (c) 2026, Raj and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class Skill(Document):
	def validate(self):
		self.skill_name = self.skill_name.strip()
		self.validate_duplicate_skill()

	def validate_duplicate_skill(self):
		duplicate = frappe.db.sql(
            """
            SELECT name
            FROM `tabSkill`
            WHERE LOWER(skill_name)=LOWER(%s)
            AND name!=%s
            """,
            (self.skill_name, self.name),
        )

		if duplicate:
			frappe.throw("Skill Name already exists.")
