from . import __version__ as app_version

app_name = "saas_manager"
app_title = "Saas Manager"
app_publisher = "Abdullah A. Zaqout"
app_description = "SaaS Manager App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "aazaqout@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/saas_manager/css/saas_manager.css"
app_include_js = "/assets/saas_manager/js/manager.js"

# include js, css files in header of web template
# web_include_css = "/assets/saas_manager/css/saas_manager.css"
# web_include_js = "/assets/saas_manager/js/saas_manager.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "saas_manager/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Employee" : "public/js/employee.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Migration
# ------------

before_migrate = "saas_manager.migrate.before_migrate"
after_migrate = "saas_manager.migrate.after_migrate"

# Installation
# ------------

before_install = "saas_manager.install.before_install"
after_install = "saas_manager.install.after_install"
on_login = 'saas_manager.manager.successful_login'
# Uninstallation
# ------------

# before_uninstall = "saas_manager.uninstall.before_uninstall"
# after_uninstall = "saas_manager.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "saas_manager.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
#  'User': {
#    'validate': 'saas_manager.manager.check_if_manager',
 #   'on_trash': 'saas_manager.manager.check_if_manager',
  #  'before_naming': 'saas_manager.manager.check_if_manager',
 # },
  #'Employee': {
    #'validate':'saas_manager.manager.check_if_manager',
    #'on_trash':'saas_manager.manager.check_if_manager'
  #},
  "User Permission": {
    "after_insert": "saas_manager.manager.delete_restrictions_from_managers",
  }
}
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"saas_manager.tasks.all"
# 	],
# 	"daily": [
# 		"saas_manager.tasks.daily"
# 	],
	# "hourly": [
	# 	"saas_manager.tasks.hourly"
	# ],
# 	"weekly": [
# 		"saas_manager.tasks.weekly"
# 	]
# 	"monthly": [
# 		"saas_manager.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "saas_manager.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "saas_manager.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "saas_manager.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"saas_manager.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

# fixtures = [
#     {"dt": "Role", "filters": [
#         [
#             "name", "in", [
#                 "Complete Tech Support"
#             ]
#         ]
#     ]}
# ]

# standard_queries = {"User": "saas_manager.whitelists.user_query"}
