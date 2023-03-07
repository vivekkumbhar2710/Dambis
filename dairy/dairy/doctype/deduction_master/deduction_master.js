frappe.ui.form.on("Deduction Master", {
	onload: function(frm) {
			frm.set_query("supplier", function() {
			return {
				filters: [
					["Supplier","branch_id","in", [frm.doc.branch]]
				]
			};
		});
	}
});

frappe.ui.form.on('Deduction Master', {
	// avanti: function(frm) {
	// 	frm.call({
	// 		method:'avantii',//function name defined in python
	// 		doc:frm.doc, //current document
	// 	 });
	//  }
});
