from __future__ import unicode_literals

import subprocess

import frappe
from frappe.utils import flt, cint, date_diff, today

def db_size():
    """
    Getting DB Space
    """
    used_db_space = frappe.db.sql('''SELECT `table_schema` as `database_name`, SUM(`data_length` + `index_length`) / 1024 / 1024 AS `database_size` FROM information_schema.tables  GROUP BY `table_schema`''')[1][1]
    used_db_space = flt(used_db_space, 2)
    return used_db_space

def get_site_size():
    # all possible file locations
    site_path = frappe.get_site_path()
    private_files_path = site_path + '/private/files'
    public_files_path  = site_path + '/public/files'
    backup_files_path = site_path + '/private/backups'

    # Calculating Sizes
    total_size = get_directory_size(site_path)
    private_files_size = get_directory_size(private_files_path)
    public_files_size = get_directory_size(public_files_path)
    backup_files_size = get_directory_size(backup_files_path)

    return total_size

def get_directory_size(path):
    """
    returns total size of directory in MBs
    """
    output_string = subprocess.check_output(["du","-mcs","{}".format(path)])
    total_size = ''
    for char in output_string:
        if chr(char) == "\t": break
        else: total_size += chr(char)
    
    return flt(total_size, 2)

def is_suspended():
    is_saas = cint(frappe.local.conf.get('enable_saas', 0))
    is_suspended = cint(frappe.local.conf.get('is_suspended', 0))
    if is_saas == 0: return False
    if is_suspended == 1: return True
    return False

def has_free_space():
    if frappe.session.user == "Administrator": return True
    
    is_saas = cint(frappe.local.conf.get('enable_saas', 0))
    if is_saas == 0: return True

    site_size = get_site_size()

    storage_space = flt(frappe.local.conf.get('storage_space', 500))

    if not isinstance(storage_space, float) or storage_space < 500:
        storage_space = 500
    if site_size >= storage_space: return False
    return True


def is_out_of_date():
    # if frappe.session.user == "Administrator": return False
    
    is_saas = cint(frappe.local.conf.get('enable_saas', 0))
    if is_saas == 0: return False

    valid_till = frappe.local.conf.get("subscription_end_date")
    try:
        diff = date_diff(valid_till, today())
        if diff < 0: return True
    except:
        return False
    return False

def keep_process():
    return has_free_space() and not is_out_of_date()

# defining a decorators
def as_saas(func):
    # Check if system run as saas before call the methods
    is_saas = cint(frappe.local.conf.get('enable_saas', 0))
    def inner1(*args, **kwargs):
        if is_saas == 1: func(*args, **kwargs)
    return inner1

def is_expired(func):
    valid_till = frappe.local.conf.get("subscription_end_date")
    diff = date_diff(valid_till, today())
    def inner1(*args, **kwargs):
        if diff >= 0: func(*args, **kwargs)
    return inner1

def has_spaces(func):
    # Check DB Space and Site Space
    allowed = 2
    used = 2
    def inner1(*args, **kwargs):
        if used <= allowed: func(*args, **kwargs)
    return inner1
