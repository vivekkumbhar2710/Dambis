# Copyright (c) 2023, Vivek and contributors
# For license information, please see license.txt
import frappe
from frappe import _

# import pandas as pd
from datetime import date 

from datetime import date, timedelta
from frappe.model.document import Document
from datetime import datetime
from datetime import timedelta



class DeductionProcess(Document):
    # Show Supplier List
    @frappe.whitelist()
    def showlist(self):
        doc = frappe.db.get_list('Supplier',
                                 fields=['supplier_name','branch_id','name']
                                 )
        for d in doc:
            total=0
            if(self.branch_id==d.branch_id):
                doc1 = frappe.db.get_list('Total Deduction Amount',
                                 fields=['supplier_name','total_deduction_amount']
                                 )
            
                for d1 in doc1:
                    if(d1.supplier_name==d.name):
                        total+=float(d1.total_deduction_amount)
                if(total):   
                    self.append("supplier_list", {
                        "supplier_name": d.name,
                        "supplier_id":d.supplier_name
                        })


    @frappe.whitelist()
    def checkall(self):
        children = self.get('supplier_list')
        if not children:
            return
        all_selected = all([child.check for child in children])  
        value = 0 if all_selected else 1 
        for child in children:
            child.check = value 
                # To Collect Data from D                   




                   
        
    @frappe.whitelist()
    def get_document(self):
        for i in self.get("supplier_list"):  # first child table
            if (i.check):
                doc = frappe.db.get_list('Supplier',
                                         fields=['milk_type','supplier_name','name']
                                         )
                 
                for d in doc:
                    if (i.supplier_name == d.name):                                         
                        a = d.milk_type
                        break
                if (self.type == 'Litre Wise'):
                    doc1 = frappe.db.get_list('Data Collection',
                                              fields=['litre', 'supplier_id','bill_status','date']
                                              )
                    abc = 0
                    x = 0
                    for d1 in doc1:
                        if (i.supplier_name == d1.supplier_id and d1.bill_status=="Not Proceed" and str(self.first_date)<=str(d1.date) and str(self.last_date)>=str(d1.date) ): 
                            abc += d1.litre
                            if (a == 'Cow'):
                                
                                x = abc * self.cow
                            else:
                                x = abc*self.buffalo
                if (self.type == 'Percentage Wise'):
                    doc = frappe.db.get_list('Data Collection',
                                             fields=['amount', 'supplier_id','bill_status','date']
                                             )
                    abc = 0
                    x = 0
                    for d in doc:
                         if (i.supplier_name == d.supplier_id and d.bill_status=="Not Proceed" and str(self.first_date)<=str(d.date) and str(self.last_date)>=str(d.date)):
                            abc += d.amount
                            if (a == 'Cow'):
                                x = (abc*self.cow)/100
                            else:
                                x = (abc*self.buffalo)/100
                if (self.type == 'Bill Wise'):
                    doc = frappe.db.get_list('Data Collection',
                                             fields=['supplier_id','bill_status','date']
                                             )
                    x = 0
                    for d in doc:
                         if (i.supplier_name == d.supplier_id and d.bill_status=="Not Proceed" and str(self.first_date)<=str(d.date) and str(self.last_date)>=str(d.date)):
                            if (a == 'cow'):
                                x = self.cow
                            else:
                                x = self.buffalo

                total=0
                doc1 = frappe.db.get_list('Total Deduction Amount',
                                 fields=['supplier_name','total_deduction_amount']
                                 )
                for d1 in doc1:
                    if(d1.supplier_name==i.supplier_name):
                        total+=float(d1.total_deduction_amount)
               
                if(total<=x):
                     self.append("deduction_list", {  # second child table
                        "supplier_name": i.supplier_name,
                        "total_deduction_amt":total,
                        "cutting": self.type,
                        "cowbuffalo": a,
                        "current_deduction_amt": total
                    })
                else:
                    self.append("deduction_list", {  # second child table
                        "supplier_name": i.supplier_name,
                        "total_deduction_amt":total,
                        "cutting": self.type,
                        "cowbuffalo": a,
                        "current_deduction_amt": round(x, 2)
                    })


    #To set Date between two period
    @frappe.whitelist()
    def set_date(self):
        billperiod = ""
        doc = frappe.db.get_list("Dairy Branch", fields=["bill_period", "branch_name"])
        for d in doc:
            if d.branch_name == self.branch_name:
                billperiod = d.bill_period
        if billperiod == "7":
            x = self.first_date.split("-")
            if int(x[2]) >= 1 and int(x[2]) <= 7:
                self.first_date = date(int(x[0]), int(x[1]), int(1))
                Begindatestring = self.first_date
                Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                billperiod = int(billperiod) - 1
                Enddate = Begindate + timedelta(days=int(str(billperiod)))
                self.last_date = Enddate
            elif int(x[2]) >= 8 and int(x[2]) <= 14:
                self.first_date = date(int(x[0]), int(x[1]), int(8))
                Begindatestring = self.first_date
                Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                billperiod = int(billperiod) - 1
                Enddate = Begindate + timedelta(days=int(str(billperiod)))
                self.last_date = Enddate
            elif int(x[2]) >= 15 and int(x[2]) <= 21:
                self.first_date = date(int(x[0]), int(x[1]), int(15))
                Begindatestring = self.first_date
                Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                billperiod = int(billperiod) - 1
                Enddate = Begindate + timedelta(days=int(str(billperiod)))
                self.last_date = Enddate
            elif int(x[2]) >= 22 and int(x[2]) <= 28 or 29 or 30 or 31:
                year = int(x[0])
                if (year % 4 == 0 and year % 100 != 0) or (
                    year % 400 == 0 and year % 100 == 0
                ):
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 29,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(22))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) + 2
                            elif d[i] == 29:
                                billperiod = int(billperiod) + 0
                            elif d[i] == 30:
                                billperiod = int(billperiod) + 1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate

                else:
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 28,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(22))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) + 2
                            elif d[i] == 28:
                                billperiod = int(billperiod) - 1
                            elif d[i] == 30:
                                billperiod = int(billperiod) + 1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate
        elif billperiod == "10":
            x = self.first_date.split("-")
            if int(x[2]) >= 1 and int(x[2]) <= 10:
                self.first_date = date(int(x[0]), int(x[1]), int(1))
                Begindatestring = self.first_date
                Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                billperiod = int(billperiod) - 1
                Enddate = Begindate + timedelta(days=int(str(billperiod)))
                self.last_date = Enddate
            elif int(x[2]) >= 11 and int(x[2]) <= 20:
                self.first_date = date(int(x[0]), int(x[1]), int(11))
                Begindatestring = self.first_date
                Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                billperiod = int(billperiod) - 1
                Enddate = Begindate + timedelta(days=int(str(billperiod)))
                self.last_date = Enddate
            elif int(x[2]) >= 21 and int(x[2]) <= 28 or 29 or 30 or 31:
                year = int(x[0])
                if (year % 4 == 0 and year % 100 != 0) or (
                    year % 400 == 0 and year % 100 == 0
                ):
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 29,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(21))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) -0
                            elif d[i] == 29:
                                billperiod = int(billperiod) -2
                            elif d[i] == 30:
                                billperiod = int(billperiod) -1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate

                else:
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 28,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(21))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) +0
                            elif d[i] == 28:
                                billperiod = int(billperiod) - 3
                            elif d[i] == 30:
                                billperiod = int(billperiod) -1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate

        elif billperiod == "15":
            x = self.first_date.split("-")
            if int(x[2]) >= 1 and int(x[2]) <= 15:
                self.first_date = date(int(x[0]), int(x[1]), int(1))
                Begindatestring = self.first_date
                Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                billperiod = int(billperiod) - 1
                Enddate = Begindate + timedelta(days=int(str(billperiod)))
                self.last_date = Enddate
            elif int(x[2]) >= 16 and int(x[2]) <= 28 or 29 or 30 or 31:
                year = int(x[0])
                if (year % 4 == 0 and year % 100 != 0) or (
                    year % 400 == 0 and year % 100 == 0
                ):
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 29,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(16))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) - 0
                            elif d[i] == 29:
                                billperiod = int(billperiod) -2
                            elif d[i] == 30:
                                billperiod = int(billperiod) -1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate

                else:
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 28,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(16))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) -0
                            elif d[i] == 28:
                                billperiod = int(billperiod)  -3
                            elif d[i] == 30:
                                billperiod = int(billperiod) -1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate

        elif billperiod == "30":
            x = self.first_date.split("-")
            if int(x[2]) >= 1 and int(x[2]) <= 28 or 29 or 30 or 31:
                year = int(x[0])
                if (year % 4 == 0 and year % 100 != 0) or (
                    year % 400 == 0 and year % 100 == 0
                ):
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 29,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(1))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) -0
                            elif d[i] == 29:
                                billperiod = int(billperiod) - 2
                            elif d[i] == 30:
                                billperiod = int(billperiod) -1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate

                else:
                    p = int(x[1])
                    d = {
                        1: 31,
                        2: 28,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31,
                    }
                    for i in d:
                        if p == i:
                            self.first_date = date(int(x[0]), int(x[1]), int(1))
                            Begindatestring = self.first_date
                            Begindate = datetime.strptime(
                                str(Begindatestring), "%Y-%m-%d"
                            )
                            if d[i] == 31:
                                billperiod = int(billperiod) - 0
                            elif d[i] == 28:
                                billperiod = int(billperiod) - 3
                            elif d[i] == 30:
                                billperiod = int(billperiod) - 1
                            Enddate = Begindate + timedelta(days=int(str(billperiod)))
                            self.last_date = Enddate