// Copyright (c) 2026, Raj and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Leave Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Leave Request", {
    employee(frm) {
        if (frm.doc.employee) {
            frappe.db.get_value(
                "Employee",
                frm.doc.employee,
                "annual_leave_balance"
            ).then((r) => {
                if (r.message) {
                    frm.set_intro(
                        `Remaining Leave Balance: ${r.message.annual_leave_balance} Days`,
                        "blue"
                    );
                }
            });
        } else {
            frm.set_intro("");
        }
    },
    from_date(frm) {
        calculate_total_days(frm);
    },
    to_date(frm) {
        calculate_total_days(frm);
    },

    before_submit(frm) {
        frappe.confirm(
            `Are you sure you want to submit this Leave Request?
            Employee: ${frm.doc.employee_name}
            Leave Type: ${frm.doc.leave_type}
            From Date: ${frm.doc.from_date}
            To Date: ${frm.doc.to_date}
            Total Days: ${frm.doc.total_days}`,
            function () {
                frm.save("Submit");
            },
            function () {
                frappe.show_alert({
                    message: __("Submission Cancelled"),
                    indicator: "red"
                });
            }
        );

        return false;
    },


    total_days(frm) {
		if (!frm.doc.total_days) {
			return;
		}
		frappe.db.get_single_value(
			"Leave Configuration",
			"max_leave_days_per_request"
		).then((max_days) => {
			if (frm.doc.total_days > max_days) {
				frappe.show_alert({
					message: __("Maximum {0} leave days are allowed per request.", [max_days]),
					indicator: "orange"
				});
			}
		});
	}
});
function calculate_total_days(frm) {

    if (frm.doc.from_date && frm.doc.to_date) {

        let days = frappe.datetime.get_day_diff(
            frm.doc.to_date,
            frm.doc.from_date
        ) + 1;

        if (days >= 0) {
            frm.set_value("total_days", days);
        }
    }
}