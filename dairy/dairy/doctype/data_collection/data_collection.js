// Copyright (c) 2023, Vivek and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Collection", {
	onload: function(frm) {
			frm.set_query("supplier_id", function() {
			return {
				filters: [
					["Supplier","branch_id","in", [frm.doc.branch_id]]
				]
			};
		});
	}
});

// --------------------------------------------------------------------------------------------------------
frappe.ui.form.on('Data Collection', {
	supplier_id: function(frm) {
		frm.call({
			method:'current_shift',//function name defined in python
			doc:frm.doc, //current document
		 });
	 }
});


// frappe.ui.form.on('Data Collection', {
// 	supplier_id: function(frm) {
// 		frm.call({
// 			method:'get_data',//function name defined in python
// 			doc:frm.doc, //current document
// 		 });
// 	 }
// });

frappe.ui.form.on('Data Collection', {
	calculate: function(frm) {
		frm.call({
			method:'calculate_data',//function name defined in python
			doc:frm.doc, //current document
		 });
	 }
});

// frappe.ui.form.on('Data Collection', {
// 	branch_id: function(frm) {
// 		frm.call({
// 			method:'today',//function name defined in python
// 			doc:frm.doc, //current document
// 		 });
// 	 }
// });

