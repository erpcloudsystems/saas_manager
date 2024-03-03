import frappe
from frappe.permissions import add_permission, update_permission_property


def set_saas_manager_permissions():
    docs = [
        'Company',
        'User',
        'Users Permission Manager',
        'Department',
        'Branch',
        'Employee Group',
        'Designation',
        'Employee Grade',
        'Employment Type',
        'Shift Type',
        'Shift Builder',
        'Staffing Plan',
        'Holiday List',
        'Leave Type',
        'Leave Period',
        'Leave Policy',
        'Leave Policy Assignment',
        'Leave Allocation',
        'Leave Encashment',
        'Employee Health Insurance',
        'Leave Block List',
        'Employee',
        'End Of Service',
        'Leave Application',
        'Shift Request',
        'Contact Details',
        'Educational Qualification',
        'Emergency Contact',
        'Health Insurance',
        'Lateness Permission',
        'Personal Details',
        'Salary Details',
        'Exit Permission',
        'Mosyr Form',
        'Attendance',
        'Employee Attendance Tool',
        'Attendance Request',
        'Upload Attendance',
        'Employee Checkin',
        'Payroll Settings',
        'Salary Component',
        'Salary Structure',
        'Salary Structure Assignment',
        'Employee Benefit',
        'Employee Deduction',
        'Payroll Entry',
        'Salary Slip',
        'Retention Bonus',
        'Employee Incentive',
        'Appraisal',
        'Appraisal Template',
        'Leave Application',
        'Compensatory Leave Request',
        'Travel Request',
        'Leave Encashment',
        'Loan Type',
        'Loan',
        'Loan Application',
        'Vehicle',
        'Vehicle Log',
        'Vehicle Service',
        'Document Manager',
        'Document Type',
        'Custody',
        'Cash Custody',
        'Cash Custody Expense',
        'Return Custody',
        'Role Profile',
        'Currency',
        'Address',
        'Domain',
        'Bank',
        'Email Account',
        'Module Profile',
        'Skill',
        'Purpose of Travel',
        'Identification Document Type',
        'Attendance',
        'Letter Head',
        'Account',
        'Supplier',
        'UOM',
        'Mode of Payment',
        'User Permission',
        'Workflow State',
        'Workflow',
        'Custom DocPerm',
        'System Controller'
    ]

    reports = [
        'Insurances and Risk',
        'Employee Attendance Sheet',
        'Biomitric Devices',
        'Exit Permissions Summary',
        'Files in Saudi banks format',
        'Employee Leave Balance'
    ]

    role = "SaaS Manager"

    set_doctype_permissions(docs, role)
    set_reports_permissions(reports, role)


def set_doctype_permissions(docs, role):
    for doc in docs:
        if frappe.db.get_value("Custom DocPerm", {"parent": doc, "role": role}):
            frappe.db.sql(
                f"DELETE FROM `tabCustom DocPerm` WHERE role='{role}' and parent='{doc}'")
            frappe.db.commit()

        frappe.get_doc(
            {
                "doctype": "Custom DocPerm",
                "role": role,
                "select": 1,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 1,
                "cancel": 1,
                "amend": 1,
                "report": 1,
                "parent": doc,
            }
        ).insert(ignore_permissions=True)

        if doc == 'User':
            add_permission(doc, role, permlevel=1)
            update_permission_property(
                doc, role, permlevel=1, ptype="write", value=1)

        if doc == 'Attendance':
            update_permission_property(
                doc, role, permlevel=0, ptype="report", value=1)


def set_reports_permissions(reports, role):
    for d in reports:
        name = frappe.db.get_value("Custom Role", {"report": d}, "name")
        if name:
            custom_role = frappe.get_doc("Custom Role", name)
            roles_lst = [d.role for d in custom_role.roles]
            if not role in roles_lst:
                custom_role.append("roles", {"role": role})
                custom_role.save(ignore_permissions=True)
                update_permission_property(
                    custom_role.ref_doctype, role, permlevel=0, ptype="report", value=1)
        else:
            custom_role = frappe.get_doc({
                "doctype": "Custom Role",
                "roles": [{"role": role, "parenttype": "Custom Role"}],
                "report": d,
            }).insert(ignore_permissions=1)
            update_permission_property(
                custom_role.ref_doctype, role, permlevel=0, ptype="report", value=1)


def set_self_service_permissions():
    allowed_docs = frappe.db.get_list(
        "Custom DocPerm", fields="*",  filters={"role": "Employee Self Service"})
    role = "Self Service"
    
    for d in allowed_docs:
        doc = d.get("parent")
        if frappe.db.get_value("Custom DocPerm", {"parent": doc, "role": role}):
            frappe.db.sql(
                f"DELETE FROM `tabCustom DocPerm` WHERE role='{role}' and parent='{doc}'")
            frappe.db.commit()

        frappe.get_doc(
            {
                "doctype": "Custom DocPerm",
                "role": role,
                "select": d.get("select"),
                "read": d.get("read"),
                "write": d.get("write"),
                "create": d.get("create"),
                "delete": d.get("delete"),
                "submit": d.get("submit"),
                "cancel": d.get("cancel"),
                "amend": d.get("amend"),
                "parent": d.get("parent"),
            }
        ).insert(ignore_permissions=True)


    extra_docs = [
        "Loan Application"
    
        ]
    
    set_doctype_permissions(extra_docs, role)
    
    updates_docs = [
        "Vehicle",
        "Loan Type",
        "Loan Application"
    ]

    for doc in updates_docs:
        update_permission_property(doc, role, permlevel=0, ptype="read", value=1)
        if doc in ["Loan Application"]:
            update_permission_property(doc, role, permlevel=0, ptype="if_owner", value=1)
    frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": role,
            "select": 1,
            "read": 1,
            "write": 0,
            "create": 0,
            "delete": 0,
            "submit": 0,
            "cancel": 0,
            "amend": 0,
            "parent": "Workflow State",
        }
    ).insert(ignore_permissions=True)

    frappe.db.commit()