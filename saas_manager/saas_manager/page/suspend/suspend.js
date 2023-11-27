frappe.pages['suspend'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Suspended Account',
		single_column: true
	});
}