import frappe

def before_migrate():
    frappe.flags.skip_saas_check = True

def after_migrate():
    frappe.flags.skip_saas_check = False
