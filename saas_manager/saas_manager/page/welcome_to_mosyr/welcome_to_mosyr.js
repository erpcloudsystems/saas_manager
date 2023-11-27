frappe.pages['welcome-to-mosyr'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Welcome to Mosyr SaaS System',
		single_column: true
	});
	$(wrapper).html(frappe.render_template("welcome_to_mosyr", {}));
	$('header').remove()
	$(wrapper).find('.start-system').click(ev => {
		frappe.call({
			method: 'saas_manager.manager.start_system',
			args:{},
			callback: function(r){location.reload()},
			freeze: true,
			freeze_message: __("wait while Setup complete")
		})
	})
}