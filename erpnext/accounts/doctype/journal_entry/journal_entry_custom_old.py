import math
import frappe
from frappe.utils import flt

@frappe.whitelist()
def get_outstanding_customer_invoices(customer_group,from_posting_date_p,to_posting_date_p,account, company, party_type,total_debit=0):
	precision = frappe.get_precision("Sales Invoice", "outstanding_amount")
	totdebit=get_total_outstanding_debit(customer_group,from_posting_date_p,to_posting_date_p,company) or 0
	totcredit=0
	granddebittot=float(total_debit)+float(abs(flt(totdebit,2)))
	#frappe.msgprint(""" gtot {0} + {1} = {2}""".format(float(total_debit),float(abs(truncate(totdebit,2))),granddebittot))	
	allocation=[]

	invoice= frappe.db.sql("""select name,outstanding_amount,customer
				from `tabSales Invoice` where docstatus = 1 and customer in(select name from `tabCustomer` where customer_group='{0}')
				and outstanding_amount <> 0  and posting_date between '{1}' and '{2}' and company='{3}' order by outstanding_amount,posting_date """.format(customer_group,from_posting_date_p,to_posting_date_p,company), as_dict=True,debug=0)
	for inv in invoice:	
		
		amount=float(truncate(abs(inv.outstanding_amount),2))*1
		#frappe.msgprint(""" {0} """.format(amount))	
		inv.update({
					'acbalance': get_account_balance_customer(account,company,inv.customer,party_type)
				})
		if (inv.outstanding_amount < 0):
			if (amount > 0):
				inv.update({
						'debit': abs(inv.outstanding_amount),
						'credit': '0'
					})
				allocation.append(inv)
		else:
			if (amount > 0):
				totcredit2=totcredit+inv.outstanding_amount
				if (totcredit < granddebittot) :
					if (totcredit < granddebittot and totcredit2 <= granddebittot):					
						inv.update({
										'credit': amount,
										'debit':'0'
									})
						allocation.append(inv)			
					else:					
						cre=inv.outstanding_amount-(totcredit2-granddebittot)
						#frappe.msgprint(""" {0} - {1} - {2} - {3} - {4}""".format(totcredit2,totcredit,flt(inv.outstanding_amount,precision),granddebittot,cre))
						inv.update({
										'credit': truncate(cre,2),
										'debit':'0'
									})
						allocation.append(inv)			
						break			
				
				totcredit=totcredit+inv.outstanding_amount

	return allocation

def get_account_balance_customer(account,company,customer,party_type):
	balance= frappe.db.sql("""select sum(debit) - sum(credit) as acbalance from `tabGL Entry` where party='{0}' and party_type='{1}' and company='{2}' and account='{3}' """.format(customer,party_type,company,account),as_dict=1,debug=0)
	return balance[0].acbalance

def get_total_outstanding_debit(customer_group,from_posting_date_p,to_posting_date_p,company):
	totdebit= frappe.db.sql("""select sum(outstanding_amount) as totdebit
				from `tabSales Invoice` where docstatus = 1 and customer in(select name from `tabCustomer` where customer_group='{0}')
				and outstanding_amount < 0  and posting_date between '{1}' and '{2}' and company='{3}' """.format(customer_group,from_posting_date_p,to_posting_date_p,company), as_dict=True,debug=1)
	return totdebit[0].totdebit

def truncate(number, decimals=0):
    
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

