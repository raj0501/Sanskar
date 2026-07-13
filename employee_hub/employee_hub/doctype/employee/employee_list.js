// Copyright (c) 2026, Raj and contributors
// For license information, please see license.txt

frappe.listview_settings["Employee"] = {

	add_fields: [
		"full_name",
		"department",
		"designation",
		"employee_status",
		"date_of_joining"
	],

	get_indicator(doc) {

		if (doc.employee_status === "Active") {
			return [__("Active"), "green", "employee_status,=,Active"];
		}

		if (doc.employee_status === "On Leave") {
			return [__("On Leave"), "orange", "employee_status,=,On Leave"];
		}

		if (doc.employee_status === "Inactive") {
			return [__("Inactive"), "gray", "employee_status,=,Inactive"];
		}

		if (doc.employee_status === "Terminated") {
			return [__("Terminated"), "red", "employee_status,=,Terminated"];
		}
	}
};