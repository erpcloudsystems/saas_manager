from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import cint
from .utils import (
    as_saas,
    has_free_space,
    is_out_of_date,
    is_suspended,
    get_directory_size,
)


def validate_doc_based_on_package(doc, method):
    if frappe.flags.skip_saas_check:
        return
    if frappe.session.user == "Administrator":
        return
    enable_saas = as_saas("enable_saas")
    if not enable_saas:
        return

    # if is_out_of_date():
    #     frappe.throw(
    #         _(
    #             "Your subscription Package is <b>out of date</b>,<br>Please contact Sales to renew the package"
    #         ),
    #         title=_("Your site is suspended."),
    #     )
    #     frappe.local.login_manager.logout()
    #     return

    if is_suspended():
        frappe.throw(
            _("Your subscription is <b>Suspended</b>,<br>Please contact Sales"),
            title=_("Your site is suspended."),
        )
        return
    if not has_free_space():
        site_path = frappe.get_site_path()
        private_files_path = site_path + "/private/files"
        public_files_path = site_path + "/public/files"
        backup_files_path = site_path + "/private/backups"

        private_files_size = get_directory_size(private_files_path)
        public_files_size = get_directory_size(public_files_path)
        backup_files_size = get_directory_size(backup_files_path)

        msg = "<div>You have exceeded your files space limit. Delete some files from file manager or to increase the limit please contact sales</div>"
        msg += "<div><ul><li>Private Files: {}MB</li><li>Public Files: {}MB</li><li>Backup Files: {}MB</li></ul></div>".format(
            private_files_size, public_files_size, backup_files_size
        )
        frappe.throw(_(msg), title=_("Your site is suspended."))
        return
    if frappe.db.exists(doc.doctype, doc.name):
        return
    if doc.doctype == "Company":
        company_limit(doc, method)

    if doc.doctype == "Department":
        check_departments(doc, method)

    if doc.doctype == "Branch":
        check_branchs(doc, method)

    if doc.doctype == "Employee":
        check_employees(doc, method)

    if doc.doctype == "User":
        user_limit(doc, method)


def check_departments(doc, method):
    if frappe.session.user == "Administrator":
        return
    can_defined = cint(frappe.local.conf.get("define_departments", 0))
    if can_defined == 0:
        frappe.throw(
            _("Not Allowed to Create/Update Departments"),
            title=_("Package Limitations."),
        )


def check_employees(doc, method):
    if frappe.session.user == "Administrator":
        return
    can_defined = cint(
        frappe.local.conf.get("define_employees_and_personal_details", 0)
    )
    if can_defined == 0:
        frappe.throw(
            _("Not Allowed to Create/Update Employees"), title=_("Package Limitations.")
        )


def check_branchs(doc, method):
    if frappe.session.user == "Administrator":
        return
    can_defined = frappe.local.conf.get("define_branch", 0)
    if can_defined == 0:
        frappe.throw(
            _("Not Allowed to Create/Update Branches"), title=_("Package Limitations.")
        )


def company_limit(doc, method):
    if frappe.session.user == "Administrator":
        return
    allow_create = cint(frappe.local.conf.get("manage_more_than_one_company", 0))
    if allow_create == 0:
        frappe.throw(
            _(
                "Only one <b>company</b> allowed.<br>To increase the limit please contact sales Please"
            ),
            title=_("Package Limitations."),
        )

    allow_no = cint(frappe.local.conf.get("available_companies", 1))
    current_no = frappe.get_list("Company")

    if allow_no == 0:
        allow_no = 1

    current_no = len(current_no)
    if current_no > allow_no:
        frappe.throw(
            _(
                "Only <b>{}</b> Active companies allowed.<br>Please delete companeis or to increase the limit please contact sales".format(
                    allow_no
                )
            ),
            title=_("Package Limitations."),
        )


def user_limit(doc, method):
    if frappe.session.user == "Administrator":
        return
    if frappe.flags.skip_saas_check == 1:
        return
    allow_create = cint(frappe.local.conf.get("allow_to_add_users", 0))
    if allow_create == 0:
        frappe.throw(
            _(
                "your not Allowed to manage users.<br><br>To increase the limit please contact sales Please"
            ),
            title=_("Package Limitations."),
        )

    allow_no = cint(frappe.local.conf.get("available_users", 1))
    current_no = frappe.get_list(
        "User", filters={"name": ["not in", ["Administrator", "Guest"]]}
    )

    if allow_no == 0 or allow_no == 1:
        allow_no = 2

    current_no = len(current_no)
    if current_no > allow_no:
        frappe.throw(
            _(
                "Only {} active users allowed and you have {} active users.<br>Please delete users or to increase the limit please contact sales".format(
                    allow_no, allow_no
                )
            ),
            title=_("Package Limitations."),
        )


# def validate_space_package(doc, method):
#     '''
#     Validates files space limit
#     '''
#     db_space = db_space_limit(doc, method)
#     files_space = files_space_limit(doc, method)
#     total_used_space = flt(db_space) + flt(files_space)

#     if total_used_space < 500:
#         total_used_space = 500

#     allowed_storage_space = flt(frappe.conf.storage_space)
#     if total_used_space > allowed_storage_space:
#         frappe.throw(_("Company Count {} > {} not allowed".format(total_used_space, allowed_storage_space)))


################################################
################ System API's
################################################
# @as_saas
def successful_login(login_manager):
    """
    on_login verify if site is not expired
    """
    # if login_manager.user == "Administrator": return
    msg = _("Error in login")
    title = _("Error in login")
    _exit = False
    if is_out_of_date():
        msg = _(
            "Your subscription Package is <b>out of date</b>,<br>Please contact Sales to renew the package"
        )
        title = _("Your site is suspended.")
        _exit = True

    elif is_suspended():
        msg = _("Your subscription is <b>Suspended</b>,<br>Please contact Sales")
        title = _("Your site is suspended.")
        _exit = True
    if _exit:
        try:
            if login_manager:
                login_manager.logout()
            else:
                frappe.local.login_manager.logout()
            frappe.msgprint(msg, title=title)
        except Exception as e:
            frappe.throw(msg, title=title)


@frappe.whitelist()
def start_system():
    # frappe.db.set_single_value("System Settings", "setup_complete", 0)
    from saas_manager.install import install_basic_docs

    install_basic_docs()
    frappe.db.set_value("System Settings", "System Settings", "is_first_startup", 0)
    frappe.db.set_single_value("System Settings", "setup_complete", 1)


def check_if_manager(doc, method):
    from frappe.core.doctype.user.user import STANDARD_USERS

    managers = [
        t[0]
        for t in frappe.db.sql(
            "SELECT name FROM `tabUser` WHERE role_profile_name='SaaS Manager' ORDER BY creation asc"
        )
    ]
    STANDARD_USERS.extend(list(managers))

    if method == "before_naming" and doc.doctype == "User":
        if doc.name in STANDARD_USERS:
            frappe.throw(_("Cannot Rename {0} {1}").format(doc.doctype, doc.name))
        return

    if method == "on_trash":
        user_id = (
            doc.name
            if doc.doctype == "User"
            else doc.user_id
            if doc.doctype == "Employee"
            else None
        )
        if not user_id or user_id is None:
            return
        frappe.clear_cache(user=user_id)
        if user_id in STANDARD_USERS:
            frappe.throw(_("Cannot Delete {0} {1}").format(doc.doctype, doc.name))
        return

    if method == "validate":
        old_doc = doc.get_doc_before_save()
        if doc.is_new() or not old_doc or old_doc is None:
            return

        if doc.doctype == "User":
            if doc.name not in STANDARD_USERS:
                return
            if cint(doc.enabled) == 0:
                frappe.throw(_("User {0} cannot be disabled").format(doc.name))
            if old_doc.email != doc.email:
                frappe.throw(_("User Email {0} cannot be updated").format(doc.name))

        if doc.doctype == "Employee":
            if old_doc.user_id != doc.user_id and old_doc.user_id in STANDARD_USERS:
                frappe.throw(
                    _("Mosyr User {0} cannot be updated for this employee").format(
                        doc.name
                    )
                )


@frappe.whitelist()
def user_query(doctype, txt, searchfield, start, page_len, filters):
    from frappe.desk.reportview import get_filters_cond, get_match_cond
    from frappe.core.doctype.user.user import STANDARD_USERS

    # Manager not linked to any employee
    used_users = [
        t[0]
        for t in frappe.db.sql(
            """SELECT name
               FROM `tabUser`
               WHERE name IN (SELECT user_id as name FROM `tabEmployee`)"""
        )
    ]
    STANDARD_USERS.extend(list(used_users))

    doctype = "User"
    conditions = []

    user_type_condition = "and user_type != 'Website User'"
    if filters and filters.get("ignore_user_type"):
        user_type_condition = ""
        filters.pop("ignore_user_type")

    txt = "%{}%".format(txt)
    return frappe.db.sql(
        """SELECT `name`, CONCAT_WS(' ', first_name, middle_name, last_name)
        FROM `tabUser`
        WHERE `enabled`=1
            {user_type_condition}
            AND `docstatus` < 2
            AND `name` NOT IN ({standard_users})
            AND ({key} LIKE %(txt)s
                OR CONCAT_WS(' ', first_name, middle_name, last_name) LIKE %(txt)s)
            {fcond} {mcond}
        ORDER BY
            CASE WHEN `name` LIKE %(txt)s THEN 0 ELSE 1 END,
            CASE WHEN concat_ws(' ', first_name, middle_name, last_name) LIKE %(txt)s
                THEN 0 ELSE 1 END,
            NAME asc
        LIMIT %(page_len)s OFFSET %(start)s
    """.format(
            user_type_condition=user_type_condition,
            standard_users=", ".join([frappe.db.escape(u) for u in STANDARD_USERS]),
            key=searchfield,
            fcond=get_filters_cond(doctype, filters, conditions),
            mcond=get_match_cond(doctype),
        ),
        dict(start=start, page_len=page_len, txt=txt),
    )

def delete_restrictions_from_managers(doc, method):
    for user in frappe.get_list("User", filters={'role_profile_name': "SaaS Manager"}):
        delete_restrictions(user.name)

def delete_restrictions(user_id):
    for f in frappe.get_list("User Permission", filters={'user': user_id, 'allow': ["!=", "Company"]}):
        f = frappe.get_doc("User Permission", f.name)
        f.delete()
    frappe.db.commit()