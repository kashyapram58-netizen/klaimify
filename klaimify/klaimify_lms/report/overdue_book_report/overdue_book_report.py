import frappe
from frappe.utils import getdate, today, date_diff

def execute(filters=None):
    columns = [
        {"fieldname": "transaction_id", "fieldtype": "Link", "label": "Transaction ID", "options": "Library Transaction", "width": 150},
        {"fieldname": "member", "fieldtype": "Link", "label": "Member", "options": "Library Member", "width": 150},
        {"fieldname": "book", "fieldtype": "Link", "label": "Book", "options": "Library Book", "width": 150},
        {"fieldname": "due_date", "fieldtype": "Date", "label": "Due Date", "width": 100},
        {"fieldname": "days_overdue", "fieldtype": "Int", "label": "Days Overdue", "width": 100}
    ]

    # Fetch data: Issued books where due date has passed
    data = frappe.db.sql("""
        SELECT name as transaction_id, member, book, due_date
        FROM `tabLibrary Transaction`
        WHERE status = 'Issued' 
        AND due_date < %s
    """, (today()), as_dict=True)

    # Calculate days overdue for each record
    for row in data:
        row['days_overdue'] = date_diff(today(), row['due_date'])

    return columns, data