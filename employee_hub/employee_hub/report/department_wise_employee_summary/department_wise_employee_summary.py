# Copyright (c) 2026, Raj and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)

    return columns, data, None, chart


def get_columns():

    return [
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 180,
        },
        {
            "label": "Total Employees",
            "fieldname": "total_employees",
            "fieldtype": "Int",
            "width": 150,
        },
        {
            "label": "Active Employees",
            "fieldname": "active_employees",
            "fieldtype": "Int",
            "width": 150,
        },
        {
            "label": "Inactive / Terminated",
            "fieldname": "inactive_employees",
            "fieldtype": "Int",
            "width": 170,
        },
        {
            "label": "Avg Leave Balance",
            "fieldname": "avg_leave_balance",
            "fieldtype": "Float",
            "width": 160,
        },
        {
            "label": "Top Skill",
            "fieldname": "top_skill",
            "fieldtype": "Data",
            "width": 180,
        },
    ]


def get_data(filters):

    conditions = ""

    if filters.get("department"):
        conditions += " AND e.department = %(department)s"

    if filters.get("employee_status"):
        conditions += " AND e.employee_status = %(employee_status)s"

    data = frappe.db.sql(
        f"""
        SELECT
            e.department AS department,

            COUNT(e.name) AS total_employees,

            SUM(
                CASE
                    WHEN e.employee_status='Active'
                    THEN 1
                    ELSE 0
                END
            ) AS active_employees,

            SUM(
                CASE
                    WHEN e.employee_status IN ('Inactive','Terminated')
                    THEN 1
                    ELSE 0
                END
            ) AS inactive_employees,

            ROUND(
                AVG(e.annual_leave_balance),
                2
            ) AS avg_leave_balance,

            (
                SELECT es.skill
                FROM `tabEmployee Skill` es
                INNER JOIN `tabEmployee` emp
                    ON emp.name = es.parent
                WHERE emp.department = e.department
                GROUP BY es.skill
                ORDER BY COUNT(*) DESC
                LIMIT 1
            ) AS top_skill

        FROM `tabEmployee` e

        WHERE 1=1
        {conditions}

        GROUP BY e.department

        ORDER BY e.department
        """,
        filters,
        as_dict=True,
    )

    return data


def get_chart(data):

    return {
        "data": {
            "labels": [d.department for d in data],
            "datasets": [
                {
                    "name": "Employees",
                    "values": [d.total_employees for d in data],
                }
            ],
        },
        "type": "bar",
    }