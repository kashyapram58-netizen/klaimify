frappe.query_reports["Member Activity Report"] = {
    "filters": [
        {
            "fieldname": "member",
            "label": __("Member"),
            "fieldtype": "Link",
            "options": "Library Member",
            "reqd": 0
        }
    ]
};