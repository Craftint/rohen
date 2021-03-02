from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe import utils
from frappe.utils import date_diff


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_record(filters)

    return columns, data


def get_columns():
    return [
        {
            "fieldname": "date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 150
        },
        {
            "fieldname": "delivery_note",
            "label": _("Delivery Note"),
            "fieldtype": "Link",
			"options":"Delivery Note",
            "width": 150
        },

 
	


        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 150
        },

        {
            "fieldname": "qty",
            "label": _("Quantity"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "amount",
            "label": _("Amount"),
            "fieldtype": "Currency",
            "width": 150
        },

    ]


def get_record(filters):
    data = []
    conditions = get_conditions(filters)
    deliveryitems = frappe.db.sql(
        '''select pa.posting_date,pa.name,pa.customer,pa.vehicle_plate_number,pa.order_confirmation,pa.rbi_number,pa.docstatus,pa.company,ch.item_code,ch.item_name,ch.qty,ch.total_amount,ch.parent,ch.warehouse
        
            from `tabDelivery Note` as pa
            inner join `tabDelivery Note Item` as ch
            on pa.name=ch.parent {} and pa.docstatus!=2 '''.format(conditions), as_dict=1)
    print(deliveryitems)
    for items in deliveryitems:
        row = {
            "date": items.posting_date,
            "delivery_note": items.name,
			"item_code":items.item_code,
			"qty":items.qty,
            "item_name":items.item_name,
            "customer": items.customer,
			"vehicle_plate":items.vehicle_plate_number,
			"amount":items.total_amount,
            "order":items.order_confirmation,
			"rbi":items.rbi_number

        }
        data.append(row)
    return data


def get_conditions(filters):
    conditions = ''

    if filters.get('from_date') and filters.get('to_date'):
        conditions += "where date(posting_date) between '{}' and '{}'".format(
            filters.get('from_date'), filters.get('to_date'))

    if filters.get('customer'):
        conditions += "and customer = '{}'".format(filters.get('customer'))
    if filters.get('vehicle_plate'):
        conditions += "and vehicle_plate_number = '{}'".format(
            filters.get('vehicle_plate'))
    return conditions
