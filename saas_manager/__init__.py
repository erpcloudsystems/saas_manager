
__version__ = '0.0.1'

STANDARD_SAAS_USERS = ["support@mosyr.io"]

from frappe.core.doctype.user import user
STANDARD_SAAS_USERS.extend(list(user.STANDARD_USERS))
user.STANDARD_USERS = STANDARD_SAAS_USERS
