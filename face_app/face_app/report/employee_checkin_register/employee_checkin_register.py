# Copyright (c) 2023, Momscode Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
def get_columns():
	return [
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": "Employee",
			"options": "Employee",
			"width": 200

		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"width": 200
		},
		{
			"label": _("Office ID"),
			"fieldname": "office_id",
			"fieldtype": "Link",
			"options": "Office",
			"width": 180,
		},
		{
			"fieldname": "location",
			"fieldtype": "Data",
			"label": "Location",
			"width": 210

		},
		{
			"fieldname": "latitude",
			"fieldtype": "Date",
			"label": "Latitude",
			"width": 100
		},
		{
			"fieldname": "longitude",
			"fieldtype": "Data",
			"label": "Longitude",
			"width": 100
		},
		{
			"fieldname": "shift",
			"fieldtype": "Link",
			"label": "Shift",
			"options": "Shift Type",
			"width": 80
		},
		{
			"fieldname": "attendance_date",
			"fieldtype": "Date",
			"label": "Date",
			"width": 120
		},
		{
			"fieldname": "in_time",
			"fieldtype": "Data",
			"label": "In Time",
			"width": 100
		},
		{
			"fieldname": "out_time",
			"fieldtype": "Data",
			"label": "Out Time",
			"width": 100
		},

		{
			"fieldname": "standard_working_hour",
			"fieldtype": "Float",
			"label": "Standard Working Hour",
			"width": 200
		},
		{
			"fieldname": "overtime",
			"fieldtype": "Float",
			"label": "Overtime",
			"width": 130
		},
	]

def get_conditions(filters):
	conditions = " time BETWEEN '{0}' and '{1}'".format(str(filters.get("from_date")) + " " + "00:00:00",str(filters.get("to_date")) + " " + "23:59:59")

	if filters.get("employee"):
		conditions += " and employee='{0}'".format(filters.get("employee"))
	if filters.get("location"):
		conditions += " and location like '{0}%'".format(filters.get("location"))

	if filters.get("office"):
		conditions += " and office_id='{0}'".format(filters.get("office"))
	return conditions
def execute(filters=None):
	columns, data = get_columns(), []
	conditions = get_conditions(filters)
	# employees = frappe.db.sql(""" SELECT * FROM `tabEmployee` WHERE status='Active' """,as_dict=1)

	# for x in employees:
	query = """ SELECT * FROM `tabEmployee Checkin` WHERE {0} ORDER BY employee,time ASC""".format(conditions)
	data = frappe.db.sql(query,as_dict=1)
	f_data = []
	current_employee = ""
	current_date = ""
	prev_object = {}
	standard_working_hours = frappe.db.get_single_value("HR Settings", "standard_working_hours")
	for x in data:
		date_ = frappe.utils.getdate(x.time)
		x['standard_working_hour'] = standard_working_hours
		x['attendance_date'] = date_
		if not current_employee:
			x['in_time'] = str(frappe.utils.get_datetime(x.time).time())
			f_data.append(x)
			current_employee = x.employee
			prev_object = x
			current_date =  frappe.utils.getdate(x.time)
			continue

		if current_employee and current_employee == x.employee and current_date and current_date == frappe.utils.getdate(x.time):
			prev_object = x
			continue

		# f_data.append(prev_object)
		f_data[-1]["out_time"] = str(frappe.utils.get_datetime(prev_object['time']).time())
		# difference_normal_time = frappe.utils.time_diff_in_hours(str(f_data[-1]["attendance_date"])+ " " + str(f_data[-1]["out_time"]),str(f_data[-1]["attendance_date"]) + " " + str(f_data[-1]["in_time"]))
		difference_normal_time = frappe.utils.time_diff_in_hours(str(f_data[-1]["attendance_date"])+ " " + str(f_data[-1]["out_time"]),str(f_data[-1]["attendance_date"]) + " " + str(f_data[-1]["in_time"]))

		# f_data[-1]['normal_time'] = difference_normal_time if difference_normal_time <= 8 else 8

		f_data[-1]['overtime'] = difference_normal_time - x['standard_working_hour'] if (difference_normal_time - x['standard_working_hour']) > 0 else 0

		x['in_time'] = str(frappe.utils.get_datetime(x.time).time())
		f_data.append(x)
		prev_object = x

		current_employee = x.employee
		current_date = frappe.utils.getdate(x.time)
	if prev_object:
		f_data[-1]["out_time"] = str(frappe.utils.get_datetime(prev_object['time']).time())
		# difference_normal_time = frappe.utils.time_diff_in_hours(str(f_data[-1]["attendance_date"])+ " " + str(f_data[-1]["out_time"]),str(f_data[-1]["attendance_date"]) + " " + str(f_data[-1]["in_time"]))

        # f_data[-1]['overtime'] = difference_normal_time - f_data[-1]['standard_working_hour'] if difference_normal_time - f_data[-1]['standard_working_hour'] > 8 else 0

	# prev_object['in_time'] = frappe.utils.get_datetime(prev_object['time']).time()
	# f_data.append(prev_object)
	print(f_data)
	return columns, f_data
