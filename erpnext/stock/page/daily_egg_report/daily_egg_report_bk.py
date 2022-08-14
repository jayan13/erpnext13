import frappe

@frappe.whitelist()
def get_company_list():
    data = {}
    data["companys"] = frappe.get_list("Company", fields=['name'],limit_page_length=0, order_by="name")
    return data
    
@frappe.whitelist()
def get_egg_report(company=None,posted_on=None):
    data = {}
    if not company:
        company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C.";
        
    data['company']=company
    data['posted_on']=posted_on
    projects= frappe.db.sql("""select  project_name from tabProject p left join  `tabStock Ledger Entry`  s  on s.project=p.project_name  where (p.status='Open' OR p.status='Completed') and s.actual_qty > 0  and voucher_type='Stock Entry' and s.is_cancelled=0 and  s.posting_date='{0}'  and p.project_name LIKE 'LH%'  group by s.project having sum(s.actual_qty) >0 order by p.project_name """.format(posted_on),as_dict=1)   
    data['items']=items= frappe.db.sql("""select  item_code,item_name from tabItem where item_group='EGGS' """,as_dict=1)
    warehouses= frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Store' """.format(company),as_dict=1)    
    oppeingstockqr=frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Layer' """.format(company),as_dict=1,debug=0)
    oppeingstockwh=[]
    wareh=[]
    for oppeingstoc in oppeingstockqr:
        oppeingstockwh.append(oppeingstoc.name)
        
    #===============store oppenning stock============
    data['oppeingstockwh']=oppeingstockwh
    itemqty=[]
    data['colum_count']=len(items)+2  
    item_conditions_sql = ''
    if oppeingstockwh:
        item_conditions_sql = """ and warehouse in ('{}')""".format( "' ,'".join([str(elem) for elem in oppeingstockwh]))
        
        itemtot=0
        for item in items:
            sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
            WHERE
                company = '{0}' 
                AND is_cancelled = 0 
                AND posting_date < '{1}'
                AND item_code='{2}'
                {3}
            GROUP BY
                item_code
            """.format(company,posted_on,item.item_code,item_conditions_sql),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,sl_entry.qty)
                
            itemqty.append(itmqty)
            itemtot+=itmqty
            
        itemqty.append(round(itemtot,2))
        
    data['store_oppenning_total']=store_oppenning_total=itemqty      
    
    #=================  layer stock qty ======================
    qtyarrays=[]
    for project in projects:
        itemqty=[]
        itemtot=0
        lay=project.project_name.split('-')
        if lay:
            layer=lay[0].replace("LH", "Layer Shed No. ").replace("RH", "Rearing Sheds No. ")
        else:
            layer=project.project_name
        
        project.update({'layers':layer})
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
    active_stock=[]
    closing_stock=[]
    for k in itemqty:
        item_total.append(0)
        active_stock.append(0)
        closing_stock.append(0)
    
    for i in range(len(qtyarrays)):
        for j in range(len(qtyarrays[i])):
            item_total[j]=round(item_total[j]+qtyarrays[i][j],2)
                
                
    data['item_total']=item_total
     #===============Active stock============
    for k in range(len(store_oppenning_total)):
        active_stock[k]=round(store_oppenning_total[k]+item_total[k],2)
        
    data['projects']=projects
    data['active_stock']=active_stock
    #=================  store qty ======================
    storqtyarrays=[]
    for warehouse in warehouses:
        itemqty=[]
        itemtot=0
        wareh.append(warehouse.name)
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
                AND warehouse='{3}'
            GROUP BY
                item_code
            """.format(company,posted_on,item.item_code,warehouse.name),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,abs(sl_entry.qty))
                
            itemqty.append(itmqty)
            itemtot+=itmqty
            
        itemqty.append(itemtot)
        storqtyarrays.append(itemqty)    
        warehouse.update({'itemqty':itemqty})
    
    store_item_total=[]
    for k in itemqty:
        store_item_total.append(0)
    
    for i in range(len(storqtyarrays)):
        for j in range(len(storqtyarrays[i])):
            store_item_total[j]=round(store_item_total[j]+storqtyarrays[i][j],2)
                
        
    data['store_item_total']=store_item_total
    data['warehouses']=warehouses
     #===============sore closing stock============
    for z in range(len(active_stock)):       
        closing_stock[z]=round(active_stock[z]-store_item_total[z],2)
        
    data['closing_stock']=closing_stock    
    #===============sore closing stock============
    
    return data

def get_item_ctn_qty(item_code,stock_qty):
    ctnqty=0   
    cv=frappe.db.get_value('UOM Conversion Detail', {'parent': item_code,'uom':'Ctn'}, 'conversion_factor', as_dict=1,debug=0)
    if stock_qty>0:
        ctnqty=round(stock_qty/cv.conversion_factor,2)
        
    return ctnqty
       
    

    
    
