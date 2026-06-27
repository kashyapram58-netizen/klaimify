frappe.query_reports["Book Utilization Report"] = {
    "filters": [
        {
            "fieldname": "book",
            "label": __("Book"),
            "fieldtype": "Link",
            "options": "Library Book"
        }
    ]
};