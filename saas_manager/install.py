from __future__ import unicode_literals

import json
import os

import frappe
from frappe.utils import get_bench_path, get_site_path
from saas_manager.permissions import set_saas_manager_permissions

def before_install():
    frappe.flags.skip_saas_check = True

def after_install():
    dont_skip_setup_wizerd()
    install_basic_docs()
    update_home_page()
    run_save_tirgger_for_all_users()
    frappe.flags.skip_saas_check = False
    

def dont_skip_setup_wizerd():
    # For new site use this defaults values
    frappe.db.set_default("desktop:home_page", "welcome-to-mosyr")
    frappe.db.set_value("System Settings", "System Settings", "setup_complete", 0)
    frappe.db.set_value("System Settings", "System Settings", "is_first_startup", 1)

def skip_setup_wizerd():
    # For new site use this defaults values
    frappe.db.set_default("desktop:home_page", "")
    frappe.db.set_value("System Settings", "System Settings", "setup_complete", 1)
    frappe.db.set_value("System Settings", "System Settings", "is_first_startup", 0)

def read_saas_config(site_name):
    """Update a value in site_config"""
    from pathlib import Path
    site_config = {}
    site_config_path = os.path.join(get_bench_path(), 'sites', f"{site_name}.config.json")
    _file = Path(site_config_path)
    if not _file.is_file():
        _file.touch()
        with open(site_config_path, "w") as f:
            f.write(json.dumps({}, indent=1, sort_keys=True))
    with open(site_config_path, "r") as f:
        site_config = json.loads(f.read())
    return site_config

def create_user(email, full_name, password):
    try:
        user = frappe.new_doc("User")
        user.update({
            "email": email,
            "first_name": full_name,
            "new_password": password,
            "send_welcome_email": 1
        })
        user.flags.no_welcome_mail = True
        user.flags.ignore_password_policy = True
        user.insert()
        frappe.db.commit()
        user.reload()
        create_employee(full_name, user.name)
        set_as_saas_manager(user.name)
        set_user_type(user.name)
        delete_restrictions(user.name)
        set_saas_manager_permissions()
    except Exception as e:
        pass

def set_as_saas_manager(user):
    user = frappe.get_doc("User", user)
    user.db_set("role_profile_name", "SaaS Manager")
    frappe.db.commit()
    
def set_user_type(user):
    user = frappe.get_doc("User", user)
    user.db_set("user_type", "System User")
    frappe.db.commit()
    
def delete_restrictions(user_id):
    for f in frappe.get_list("User Permission", filters={'user': user_id}):
        f = frappe.get_doc("User Permission", f.name)
        f.delete()
    frappe.db.commit()

def update_home_page():
    d = frappe.get_doc("Website Settings")
    d.db_set("home_page", "login")
    frappe.db.commit()

def create_employee(full_name, user_id):
    employee = frappe.new_doc("Employee")
    employee.first_name = full_name
    employee.full_name_en = full_name
    employee.e_gender = "Male"
    employee.user_id = user_id
    employee.flags.ignore_mandatory = True
    employee.flags.ignore_permissions = True
    employee.save()
    frappe.db.commit()
    employee.reload()
    set_user_for_employee(employee.name, user_id)

def set_user_for_employee(employee_name, user_id):
    employee = frappe.get_doc("Employee", employee_name)
    employee.user_id = user_id
    employee.flags.ignore_mandatory = True
    employee.save()
    frappe.db.commit()

def install_basic_docs():
    from frappe.desk.page.setup_wizard.setup_wizard import setup_complete
    site_name = get_site_path().split("/")
    
    if len(site_name) > 1:
        configs = read_saas_config(site_name[1])
    else:
        configs = {}

    country = configs.get('country', '')
    currency = configs.get('currency', '')
    company = configs.get('company', '')
    abbr = configs.get('abbr', '')
    email_address = "support@mosyr.io"
    admin_user_pass = configs.get('support_pass', email_address)
    full_name = "Mosyr Support"
    yar = frappe.utils.get_year_start(frappe.utils.nowdate()).year
    currency = configs.get('currency', '')
    args = {
        'country': country,
        'currency': currency,
        'full_name': full_name,
        'email': email_address,
        'password': admin_user_pass,
        'company_name': company,
        'company_abbr': abbr,
        'company_tagline': company,
        'language': 'English (United Kingdom)',
        'timezone': 'Asia/Riyadh',
        'domains': ['Services'],
        'bank_account': 'Bank Name',
        'chart_of_accounts': 'Standard',
        'fy_start_date': f'{yar}-01-01',
        'fy_end_date': f'{yar}-12-31'
    }
    frappe.logger("mosyr.saas").debug(args)
    setup_complete(args)
    frappe.db.commit()
    skip_setup_wizerd()
    saas_manager_email = configs.get('email_address', 'manager@email.com')
    saas_full_name = configs.get('customer', 'Manager')
    saas_password = configs.get('admin_user_pass', saas_manager_email)
    create_user(saas_manager_email, saas_full_name, saas_password)

    # make sure that company has been created successfully for arabic company name
    for company in frappe.get_list("Company"):
        company = frappe.get_doc("Company", company.name)
        company.save()
    frappe.db.commit()


def run_save_tirgger_for_all_users():
    for user in frappe.get_list("User", filters={'role_profile_name': "SaaS Manager"}):
        user = frappe.get_doc("User", user.name)
        user.save()
    frappe.db.commit()
    delete_restrictions_fo_managers()

def delete_restrictions_fo_managers():
    for user in frappe.get_list("User", filters={'role_profile_name': "SaaS Manager"}):
        delete_restrictions(user.name)
