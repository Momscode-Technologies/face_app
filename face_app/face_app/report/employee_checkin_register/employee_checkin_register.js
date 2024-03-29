// Copyright (c) 2023, Momscode Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Checkin Register"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From Date",
			"reqd":1,

		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To Date",
			"reqd":1,

		},
		{
			"fieldname": "location",
			"fieldtype": "Data",
			"label": "Location"
		},
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": "Employee",
			"options": "Employee",
		},

		{
			"fieldname": "office",
			"fieldtype": "Link",
			"label": "Office",
			"options": "Office",
		},
	],
		onload: function(report) {
            // dropdown for links to other financial statements


            // let fiscal_year = frappe.defaults.get_user_default("fiscal_year")
            // console.log("FISCAL YEAR")
            // frappe.model.with_doc("Fiscal Year", fiscal_year, function (r) {
            // var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
			frappe.query_report.set_filter_value({
				from_date: frappe.datetime.year_start(),
				to_date: frappe.datetime.year_end()
			});
            // });
        }
};
