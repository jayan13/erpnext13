import frappe

@frappe.whitelist()
def get_company_list():
    data = {}
    data["companys"] = frappe.get_list("Company", fields=['name'],limit_page_length=0, order_by="name",debug=0)
    return data
    
@frappe.whitelist()
def get_opening_stock():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C.";    
    cur_date=frappe.utils.today()
    oppeingstockqr=frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Layer' """.format(company),as_dict=1)
    oppeingstockwh=[]    
    for oppeingstoc in oppeingstockqr:
        oppeingstockwh.append(oppeingstoc.name)
     
    warehouse_conditions_sql = ''
    if oppeingstockwh:
        warehouse_conditions_sql = """ and warehouse in ('{}')""".format( "' ,'".join([str(elem) for elem in oppeingstockwh]))
        
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
    sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
            WHERE
                company = '{0}' 
                AND is_cancelled = 0 
                AND posting_date < '{1}'
                {2}
                {3}
            
            """.format(company,cur_date,item_conditions_sql,warehouse_conditions_sql),as_dict=1,debug=0)    
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                   
    data['fieldtype']='Float'
    return data
   
@frappe.whitelist()
def get_todays_production():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C.";    
    cur_date=frappe.utils.today()
    oppeingstockqr=frappe.db.sql("""select  project_name from tabProject p left join  `tabStock Ledger Entry`  s  on s.project=p.project_name  where (p.status='Open' OR p.status='Completed')  and s.actual_qty > 0  and voucher_type='Stock Entry'  and s.is_cancelled=0 and  s.posting_date='{0}'  and p.project_name LIKE 'LH%'  group by s.project having sum(s.actual_qty) >0 order by p.project_name """.format(cur_date),as_dict=1)
    oppeingstockwh=[]    
    for oppeingstoc in oppeingstockqr:
        oppeingstockwh.append(oppeingstoc.project_name)
     
    warehouse_conditions_sql = ''
    if oppeingstockwh:
        warehouse_conditions_sql = """ and `tabStock Ledger Entry`.project in ('{}')""".format( "' ,'".join([str(elem) for elem in oppeingstockwh]))
        
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and `tabStock Ledger Entry`.item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
    sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.actual_qty > 0 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                and `tabStock Ledger Entry`.company = '{0}' 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Entry`.stock_entry_type_option='Production' 
                AND `tabStock Ledger Entry`.posting_date = '{1}'
                {2}
                {3}
            
            """.format(company,cur_date,item_conditions_sql,warehouse_conditions_sql),as_dict=1,debug=0)    
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                   
    
    data['fieldtype']='Float'
    return data

@frappe.whitelist()
def get_stock_transfer_abu():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C."; 
    warehouse='ABU DHABI STORE - APF'
    cur_date=frappe.utils.today()       
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
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
                {2}
                AND warehouse='{3}'
            """.format(company,cur_date,item_conditions_sql,warehouse),as_dict=1,debug=0)
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                
    data['fieldtype']='Float'
    return data
    
@frappe.whitelist()
def get_stock_transfer_al():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C."; 
    warehouse='AL AIN STORE - APF'
    cur_date=frappe.utils.today()       
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
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
                {2}
                AND warehouse='{3}'
            """.format(company,cur_date,item_conditions_sql,warehouse),as_dict=1,debug=0)
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                
    data['fieldtype']='Float'
    return data    
    
@frappe.whitelist()
def get_stock_transfer_sha():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C."; 
    warehouse='SHARJAH STORE - APF'
    cur_date=frappe.utils.today()       
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
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
                {2}
                AND warehouse='{3}'
            """.format(company,cur_date,item_conditions_sql,warehouse),as_dict=1,debug=0)
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                
    data['fieldtype']='Float'
    return data  

@frappe.whitelist()
def get_total_loading():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C."; 
    cur_date=frappe.utils.today()
    oppeingstockqr=frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Store' """.format(company),as_dict=1)
    oppeingstockwh=[]    
    for oppeingstoc in oppeingstockqr:
        oppeingstockwh.append(oppeingstoc.name)
     
    warehouse_conditions_sql = ''
    if oppeingstockwh:
        warehouse_conditions_sql = """ and warehouse in ('{}')""".format( "' ,'".join([str(elem) for elem in oppeingstockwh]))
        
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
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
                {2}
                {3}
            """.format(company,cur_date,item_conditions_sql,warehouse_conditions_sql),as_dict=1,debug=0)
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                
    data['fieldtype']='Float'
    return data
    
@frappe.whitelist()
def get_repacking():
    data = {}
    company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C."; 
    cur_date=frappe.utils.today()
    oppeingstockqr=frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Layer' """.format(company),as_dict=1)
    oppeingstockwh=[]    
    for oppeingstoc in oppeingstockqr:
        oppeingstockwh.append(oppeingstoc.name)
     
    warehouse_conditions_sql = ''
    if oppeingstockwh:
        warehouse_conditions_sql = """ and `tabStock Ledger Entry`.warehouse in ('{}')""".format( "' ,'".join([str(elem) for elem in oppeingstockwh]))
    items= frappe.db.sql("""select  item_code from tabItem where item_group='EGGS' """,as_dict=1)
    itemsar=[]
    
    for item in items:
        itemsar.append(item.item_code)
    
    item_conditions_sql = ''
    if itemsar:
        item_conditions_sql = """ and `tabStock Ledger Entry`.item_code in ('{}')""".format( "' ,'".join([str(elem) for elem in itemsar]))
        
    sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.company = '{0}' 
                and `tabStock Ledger Entry`.actual_qty > 0 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                AND `tabStock Entry`.stock_entry_type_option in('Repacking','GRV Repacking','Old Stock Repacking','Organic Packing') 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Ledger Entry`.posting_date ='{1}'
                {2}
                {3}
            """.format(company,cur_date,item_conditions_sql,warehouse_conditions_sql),as_dict=1,debug=0)
    data['value']=0
    for sl_entry in sl_entrys:
        if sl_entry.qty:
            data['value']=round(sl_entry.qty/360,2)
                
    data['fieldtype']='Float'
    return data

@frappe.whitelist()
def get_closing_stock():
    data = {}
    op=get_opening_stock() 
    pd=get_todays_production()
    re=get_repacking()
    tl=get_total_loading()
    val=op['value']+pd['value']+re['value']-tl['value']
    data['value']=round(val, 2)
    data['fieldtype']='Float'
    return data    
    
@frappe.whitelist()
def get_egg_report(company=None,posted_on=None):
    data = {}
    if not company:
        company="ABU DHABI POULTRY FARM - SOLE PROPRIETORSHIP L.L.C.";
        
    data['company']=company
    data['posted_on']=posted_on
    projects= frappe.db.sql("""select  project_name from tabProject p left join  `tabStock Ledger Entry`  s  on s.project=p.project_name  where (p.status='Open' OR p.status='Completed')  and s.actual_qty > 0  and voucher_type='Stock Entry'  and s.is_cancelled=0 and  s.posting_date='{0}'  and p.project_name LIKE 'LH%'  group by s.project having sum(s.actual_qty) >0 order by p.project_name """.format(posted_on),as_dict=1)
    data['items']=items= frappe.db.sql("""select  item_code,item_name from tabItem where item_group='EGGS' """,as_dict=1)
    warehouses= frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Store' """.format(company),as_dict=1)
    retwarehouses= frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='RETURN STORE' """.format(company),as_dict=1)
    oppeingstockqr=frappe.db.sql("""select  name from tabWarehouse where company='{0}' and warehouse_type='Layer' """.format(company),as_dict=1)
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
    #================= repacking =========================
    itemqty=[]
    grvitemqty=[]
    olditemqty=[]
    orgitemqty=[]

    item_conditions_sql = ''
    if oppeingstockwh:
        item_conditions_sql = """ and `tabStock Ledger Entry`.warehouse in ('{}')""".format( "' ,'".join([str(elem) for elem in oppeingstockwh]))
        
        itemtot=0
        for item in items:
            sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.company = '{0}' 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                AND `tabStock Entry`.stock_entry_type_option='Repacking' 
                and `tabStock Ledger Entry`.actual_qty > 0 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Ledger Entry`.posting_date = '{1}'
                AND `tabStock Ledger Entry`.item_code='{2}'
                {3}
            GROUP BY
                `tabStock Ledger Entry`.item_code
            """.format(company,posted_on,item.item_code,item_conditions_sql),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,sl_entry.qty)
                
            itemqty.append(itmqty)
            itemtot+=itmqty
            
        itemqty.append(round(itemtot,2))
        #=================================================
        itemtot=0
        for item in items:
            sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.company = '{0}' 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                AND `tabStock Entry`.stock_entry_type_option='GRV Repacking' 
                and `tabStock Ledger Entry`.actual_qty > 0 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Ledger Entry`.posting_date = '{1}'
                AND `tabStock Ledger Entry`.item_code='{2}'
                {3}
            GROUP BY
                `tabStock Ledger Entry`.item_code
            """.format(company,posted_on,item.item_code,item_conditions_sql),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,sl_entry.qty)
                
            grvitemqty.append(itmqty)
            itemtot+=itmqty
            
        grvitemqty.append(round(itemtot,2))
        #=================================================
        itemtot=0
        for item in items:
            sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.company = '{0}' 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                AND `tabStock Entry`.stock_entry_type_option='Old Stock Repacking' 
                and `tabStock Ledger Entry`.actual_qty > 0 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Ledger Entry`.posting_date = '{1}'
                AND `tabStock Ledger Entry`.item_code='{2}'
                {3}
            GROUP BY
                `tabStock Ledger Entry`.item_code
            """.format(company,posted_on,item.item_code,item_conditions_sql),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,sl_entry.qty)
                
            olditemqty.append(itmqty)
            itemtot+=itmqty
            
        olditemqty.append(round(itemtot,2))
        #=================================================
        itemtot=0
        for item in items:
            sl_entrys= frappe.db.sql("""
            SELECT
                sum(actual_qty) as qty
            FROM
                `tabStock Ledger Entry` 
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.company = '{0}' 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                AND `tabStock Entry`.stock_entry_type_option='Organic Packing' 
                and `tabStock Ledger Entry`.actual_qty > 0 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Ledger Entry`.posting_date = '{1}'
                AND `tabStock Ledger Entry`.item_code='{2}'
                {3}
            GROUP BY
                `tabStock Ledger Entry`.item_code
            """.format(company,posted_on,item.item_code,item_conditions_sql),as_dict=1,debug=0)
            itmqty=0         
            for sl_entry in sl_entrys:
                itmqty=get_item_ctn_qty(item.item_code,sl_entry.qty)
                
            orgitemqty.append(itmqty)
            itemtot+=itmqty
            
        orgitemqty.append(round(itemtot,2))
        
    data['store_repacking_total']=store_repacking_total=itemqty 
    data['grv_repacking_total']=grv_repacking_total=grvitemqty
    data['old_repacking_total']=old_repacking_total=olditemqty
    data['org_repacking_total']=org_repacking_total=orgitemqty
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
                left join   `tabStock Entry`  on  `tabStock Entry`.name=`tabStock Ledger Entry`.voucher_no
            WHERE
                `tabStock Ledger Entry`.company = '{0}' 
                and `tabStock Ledger Entry`.actual_qty > 0 
                and `tabStock Ledger Entry`.voucher_type='Stock Entry'
                AND `tabStock Entry`.stock_entry_type_option='Production' 
                AND `tabStock Ledger Entry`.is_cancelled = 0 
                AND `tabStock Ledger Entry`.posting_date ='{1}'
                AND `tabStock Ledger Entry`.item_code='{2}'
                AND `tabStock Ledger Entry`.project='{3}'
            GROUP BY
                `tabStock Ledger Entry`.item_code
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
        active_stock[k]=round(store_oppenning_total[k]+item_total[k]+store_repacking_total[k]+grv_repacking_total[k]+old_repacking_total[k]+org_repacking_total[k],2)
        
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
    #=================  store return qty ======================
    storqtyarrays=[]
    for warehouse in retwarehouses:
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
    
    retstore_item_total=[]
    for k in itemqty:
        retstore_item_total.append(0)
    
    for i in range(len(storqtyarrays)):
        for j in range(len(storqtyarrays[i])):
            retstore_item_total[j]=round(retstore_item_total[j]+storqtyarrays[i][j],2)
                
        
    data['retstore_item_total']=retstore_item_total
    data['retwarehouses']=retwarehouses
     #===============sore closing stock============
    for z in range(len(active_stock)):       
        closing_stock[z]=round(active_stock[z]-store_item_total[z])
        
    data['closing_stock']=closing_stock    
    #===============sore closing stock============
    
    return data

def get_item_ctn_qty(item_code,stock_qty):
    ctnqty=0   
    cv=frappe.db.get_value('UOM Conversion Detail', {'parent': item_code,'uom':'Ctn'}, 'conversion_factor', as_dict=1,debug=0)
    if stock_qty>0:
        ctnqty=round(stock_qty/cv.conversion_factor,2)
        
    return ctnqty
       
    

    
    
