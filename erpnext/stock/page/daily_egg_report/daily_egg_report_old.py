import frappe

@frappe.whitelist()
def get_company_list():
    data = {}
    data["companys"] = frappe.get_list("Company", fields=['name'],limit_page_length=0, order_by="name")
    return data
    
@frappe.whitelist()
def get_egg_report(company=None,posted_on=None):
    data = {}
    data['company']=company
    data['posted_on']=posted_on
    projects= frappe.db.sql("""select  project_name from tabProject where status='Open'and project_name<>'HERZ FARM 01-11-2021'  """,as_dict=1)
    data['items']=items= frappe.db.sql("""select  item_code,item_name from tabItem where item_group='EGGS' """,as_dict=1)
    data['warehouse']=warehouses= frappe.db.sql("""select  name,warehouse_name from tabWarehouse where company='{0}' and warehouse_type='Store' """.format(company),as_dict=1,debug=1)
    qtyarrays=[]
    for project in projects:

       # if project.project_name=='HERZ FARM 01-11-2021':
        #    continue
            
        itemqty=[]
        itemtot=0
        for item in items:
        
            sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
            WHERE
                company = '{0}' 
                and actual_qty > 0 
                and voucher_type='Stock Entry'
                AND is_cancelled = 0 
                AND posting_date ='{1}'
                AND item_code='{2}'
                AND project='{3}'
            GROUP BY
                item_code
            """.format(company,posted_on,item.item_code,project.project_name),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,sl_entry.qty)
                
            itemqty.append(itmqty)
            itemtot+=itmqty
            
        itemqty.append(itemtot)
        qtyarrays.append(itemqty)    
        project.update({'itemqty':itemqty})
    
    item_total=[]
    for k in itemqty:
        item_total.append(0)
    
    for i in range(len(qtyarrays)):
        for j in range(len(qtyarrays[i])):
            item_total[j]=item_total[j]+qtyarrays[i][j]
                
                
    data['item_total']=item_total
    data['projects']=projects
    return data

def get_item_ctn_qty(item_code,stock_qty):
    ctnqty=0   
    cv=frappe.db.get_value('UOM Conversion Detail', {'parent': item_code,'uom':'Ctn'}, 'conversion_factor', as_dict=1,debug=0)
    if stock_qty>0:
        ctnqty=round(stock_qty/cv.conversion_factor,2)
        
    return ctnqty
 
