frappe.query_reports["Outstanding Fines Summary"] = {
    "filters": [
        {
            "fieldname": "member",
            "label": __("Member"),
            "fieldtype": "Link",
            "options": "Library Member"
        }
    ]
};