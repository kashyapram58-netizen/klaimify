frappe.query_reports["Overdue Books Report"] = {
    "filters": [
        {
            "fieldname": "member_type",
            "label": __("Member Type"),
            "fieldtype": "Select",
            "options": "\nStudent\nStaff\nPublic"
        }
    ]
};