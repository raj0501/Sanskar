// Copyright (c) 2026, Raj and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	setup(frm) {
        frm.set_query("designation", function () {
            return {
                filters: {
                    department: frm.doc.department
                }
            };
        });
    }
});
