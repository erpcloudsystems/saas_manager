frappe.ui.form.on('Employee', {
    refresh: function (frm) {
		frm.set_query("user_id", function() {
			return {
				query: 'saas_manager.manager.user_query',
			};
		});
	},
})