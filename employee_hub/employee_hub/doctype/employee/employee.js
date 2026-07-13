// Copyright (c) 2026, Raj and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
    department(frm) {
        // Clear selected designation
        frm.set_value("designation", "");

        // Filter designation based on selected department
        frm.set_query("designation", function () {
            return {
                filters: {
                    department: frm.doc.department
                }
            };
        });
    },
    first_name(frm) {
        set_full_name(frm);
    },
    last_name(frm) {
        set_full_name(frm);
    },
    refresh(frm) {
        frm.add_custom_button(__("Create Leave Request"), function () {
            frappe.route_options = {
                employee: frm.doc.name
            };
            frappe.new_doc("Leave Request");
        });

        frm.dashboard.clear_headline();
        // Dashboard Indicator
        if (frm.doc.employee_status == "Active") {
            frm.dashboard.set_headline_alert(__("Employee Status: Active"), "green");
        } else if (frm.doc.employee_status == "On Leave") {
            frm.dashboard.set_headline_alert(__("Employee Status: On Leave"), "orange");
        } else if (frm.doc.employee_status == "Terminated") {
            frm.dashboard.set_headline_alert(__("Employee Status: Terminated"), "red");
        }


        frm.add_custom_button(__("View Skills Summary"), function () {

            let summary = "";

            if (frm.doc.skills && frm.doc.skills.length) {
                frm.doc.skills.forEach(function (row, index) {
                    summary +=
                        (index + 1) + ". " +
                        row.skill +
                        " | " +
                        row.proficiency +
                        " | " +
                        row.years_of_experience +
                        " Years\n";
                });
            } else {
                summary = "No Skills Added";
            }

            let d = new frappe.ui.Dialog({
                title: "Skills Summary",
                fields: [
                    {
                        label: "Summary",
                        fieldname: "summary",
                        fieldtype: "Small Text",
                        read_only: 1
                    }
                ]
            });

            d.set_value("summary", summary);
            d.show();
        });

    }
});
function set_full_name(frm) {
    frm.set_value(
        "full_name",
        `${frm.doc.first_name || ""} ${frm.doc.last_name || ""}`.trim()
    );
}
