# Copyright (c) 2023, Vivek and contributors
# For license information, please see license.txt
import datetime
from datetime import date
import frappe
from frappe import _

from datetime import date, timedelta
from frappe.model.document import Document


class DataCollection(Document):
    @frappe.whitelist()	
    def calculate_data(self):
        self.get_document()
        

	#To calculate Total Amount	
    def get_document(self):
        count=0
        doc = frappe.db.get_list('Rate Master')
        for d in doc:
            d1= frappe.get_doc("Rate Master",d.name)
            if(d.name==self.rate_group):
                for row in d1.get("rate_list"):
                    if ((self.snf == row.snf)):
                        if((self.fat == row.fat)):
                            self.rate = row.rate
                            self.on_save()
                            count+=1
                if(count==0):
                    # elif((self.snf != row.snf) and (self.fat != row.fat)):
                            frappe.msgprint("Please Enter Right SNF or Fat value")         

    def on_save(self):
        self.amount=self.litre * self.rate

    def before_save(self):
        self.get_document()
	#To calculate Total Amount	
    def get_document(self):
            count=0
            doc = frappe.db.get_list('Rate Master')
            for d in doc:
                d1= frappe.get_doc("Rate Master",d.name)
                if(d.name==self.rate_group):
                    for row in d1.get("rate_list"):
                        if ((self.snf == row.snf)):
                            if((self.fat == row.fat)):
                                self.rate = row.rate
                                self.on_save()
                                count+=1
                    if(count==0):
                        # elif((self.snf != row.snf) and (self.fat != row.fat)):
                                frappe.msgprint("Please Enter Right SNF or Fat value")     

    # To get Current shift
    @frappe.whitelist()
    def current_shift(self):
        now = datetime.datetime.now()
        p = now.strftime("%H%M%S")
        k = int(p)
        if 000000 <= k <= 115959:
            self.shift = "Morning"

        # elif 120000 <= k <= 155959:
        #     self.shift = "Afternoon"

        else:
            self.shift = "Evening"

    def on_submit(self):
        doc=frappe.new_doc('GL Entry')
        doc.posting_date=self.date
        doc.account=self.account_cr
        doc.party_type="Supplier"
        doc.party=self.supplier_id
        doc.cost_center="Main - QT"
        doc.credit=self.amount
        doc.credit_in_account_currency=self.amount
        doc.against=self.account_dr
        doc.voucher_type="Data Collection"
        doc.voucher_no=self.name
        doc.insert()

        doc=frappe.new_doc('GL Entry')
        doc.posting_date=self.date
        doc.account=self.account_dr
        doc.cost_center="Main - QT"
        doc.debit=self.amount
        doc.debit_in_account_currency=self.amount
        doc.against=self.supplier_id
        doc.voucher_type="Data Collection"
        doc.voucher_no=self.name
        doc.insert()




        

    
