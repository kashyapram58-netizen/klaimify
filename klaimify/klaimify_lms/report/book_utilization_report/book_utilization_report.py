import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "book", "fieldtype": "Link", "label": "Book", "options": "Library Book", "width": 200},
        {"fieldname": "total_issues", "fieldtype": "Int", "label": "Total Issues", "width": 120}
    ]

    # Aggregating issues per book
    data = frappe.db.sql("""
        SELECT 
            book, 
            COUNT(name) as total_issues 
        FROM `tabLibrary Transaction` 
        GROUP BY book 
        ORDER BY total_issues DESC
    """, as_dict=True)

    return columns, data