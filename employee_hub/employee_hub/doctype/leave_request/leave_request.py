# Copyright (c) 2026, Raj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, date_diff, now_datetime


class LeaveRequest(Document):
    def validate(self):
        self.calculate_total_days()
        self.validate_dates()
        self.validate_leave_balance()
        self.validate_overlap()
    
    def calculate_total_days(self):
        self.total_days = (
            date_diff(self.to_date, self.from_date) + 1
        )

    def validate_dates(self):
        if getdate(self.to_date) < getdate(self.from_date):
            frappe.throw("To Date cannot be before From Date.")
        if getdate(self.from_date) < getdate(today()):
            frappe.throw("From Date cannot be in the past.")

    def validate_leave_balance(self):
        balance = frappe.db.get_value(
            "Employee",
            self.employee,
            "annual_leave_balance"
        )

        if self.total_days > balance:
            frappe.throw(
                f"Only {balance} leave days are available."
            )

    def validate_overlap(self):
        overlap = frappe.db.exists(
            "Leave Request",
            {
                "employee": self.employee,
                "docstatus": 1,
                "approval_status": "Approved",
                "from_date": ["<=", self.to_date],
                "to_date": [">=", self.from_date],
                "name": ["!=", self.name],
            },
        )

        if overlap:
            frappe.throw("Employee already has approved leave for these dates")

    def on_submit(self):
        self.db_set("approval_status", "Approved")
        self.db_set("approved_by", frappe.session.user)
        self.db_set("approval_date", now_datetime())

        employee = frappe.get_doc("Employee", self.employee)
        employee.annual_leave_balance -= self.total_days
        employee.save(ignore_permissions=True)
        employee.employee_status = "On Leave"

    def on_cancel(self):
        if self.rejection_reason:
            self.db_set("approval_status", "Rejected")

        employee = frappe.get_doc("Employee", self.employee)
        employee.annual_leave_balance += self.total_days
        employee.employee_status = "Active"
        employee.save(ignore_permissions=True)
