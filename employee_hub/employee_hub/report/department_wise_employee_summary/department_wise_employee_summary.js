// Copyright (c) 2026, Raj and contributors
// For license information, please see license.txt

frappe.query_reports["Department Wise Employee Summary"] = {
	filters: [
		// {
		// 	"fieldname": "my_filter",
		// 	"label": __("My Filter"),
		// 	"fieldtype": "Data",
		// 	"reqd": 1,
		// },
		{
			fieldname: "department",
			label: "Department",
			fieldtype: "Link",
			options: "Department"
		},
		{
			fieldname: "employee_status",
			label: "Employee Status",
			fieldtype: "Select",
			options: "\nActive\nInactive\nOn Leave\nTerminated"
		}
	],
};