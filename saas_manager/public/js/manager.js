$(document).on("page-change", function(e){
    if(frappe.boot.is_first_startup==1){
        if(frappe.get_route_str() != ''){
            location.href = '/app'
        }
    }
})