import math
import frappe
import erpnext
from frappe.utils import flt

@frappe.whitelist()
def get_outstanding_customer_invoices(customer_group,from_posting_date_p,to_posting_date_p,account, company, party_type,total_debit=0):
	precision = frappe.get_precision("Sales Invoice", "outstanding_amount")
	totcredit=0
	granddebittot=float(total_debit)	
	allocation=[]

	invoice= frappe.db.sql("""select name,outstanding_amount,customer
				from `tabSales Invoice` where docstatus = 1 and customer in(select name from `tabCustomer` where customer_group='{0}')
				and outstanding_amount <> 0  and posting_date between '{1}' and '{2}' and company='{3}' order by outstanding_amount,posting_date """.format(customer_group,from_posting_date_p,to_posting_date_p,company), as_dict=True,debug=0)
	for inv in invoice:	
		amount=float(truncate(abs(inv.outstanding_amount),2))*1
		inv.update({
					'acbalance': get_account_balance_customer(account,company,inv.customer,party_type)
				})
		if (inv.outstanding_amount < 0):
			if (amount > 0):
				inv.update({
						'debit': amount,
						'credit': '0'
					})
				granddebittot=granddebittot+amount
				allocation.append(inv)
		else:
			if (amount > 0):
				totcredit2=totcredit+amount
				if (totcredit < granddebittot) :
					if (totcredit < granddebittot and totcredit2 <= granddebittot):					
						inv.update({
										'credit': amount,
										'debit':'0'
									})
						allocation.append(inv)			
					else:					
						cre=amount-(totcredit2-granddebittot)
						inv.update({
										'credit': truncate(cre,2),
										'debit':'0'
									})
						allocation.append(inv)			
						break			
				
				totcredit=totcredit+amount

	return allocation

def get_account_balance_customer(account,company,customer,party_type):
	values = {"party": customer,"party_type":party_type,"company":company,"account":account}
	balance= frappe.db.sql("""select sum(debit) - sum(credit) as acbalance from `tabGL Entry` where party=%(party)s and party_type=%(party_type)s and company=%(company)s and account=%(account)s """,values=values,as_dict=1,debug=0)
	return balance[0].acbalance

def truncate(number, decimals=0):
    
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_income_account(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.controllers.queries import get_match_cond

	# income account can be any Credit account,
	# but can also be a Asset account with account_type='Income Account' in special circumstances.
	# Hence the first condition is an "OR"
	if not filters: filters = {}

	condition = ""
	if filters.get("company"):
		condition += "and tabAccount.company = %(company)s"

	return frappe.db.sql("""select tabAccount.name from `tabAccount`
			where  tabAccount.is_group=0
				and tabAccount.`{key}` LIKE %(txt)s
				{condition} {match_condition}
			order by idx desc, name"""
			.format(condition=condition, match_condition=get_match_cond(doctype), key=searchfield), {
				'txt': '%' + txt + '%',
				'company': filters.get("company", "")
			})
