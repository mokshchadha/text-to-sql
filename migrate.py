import csv
import psycopg2
from psycopg2 import sql
from psycopg2 import datetime

COLUMN_MAPPING = {
    'id': '_id',
    'order_number': 'orderno',
    'supplier_gst': 'supplierid',
    'supplier_name': 'supplier',
    'buyer_gst': 'buyerid',
    'buyer_name': 'buyer',
    'godown_id': 'godownid',
    'godown_name': 'godown',
    'single_quantity': 'singlequantity',
    'product_id': 'productid',
    'product_name': 'productname',
    'delivered_to_id': 'deliveredtoid',
    'delivered_to_name': 'deliveredto',
    'dispatch_date': 'dispatchdate',
    'due_date': 'duedate',
    'buyer_due_date': 'buyerduedate',
    'expected_delivery_date': 'expecteddeliverydate',
    'actual_delivery_date': 'actualdeliverydate',
    'supplier_due_date': 'supplierduedate',
    'order_status': 'status',
    'buyer_payment_terms': 'buyerpaymentterms',
    'delivery_address': 'deliverywholeaddress',
    'transporter_address': 'transportaddress',
    'is_eway_bill_created': 'isewaybillcreated',
    'buyer_po_number': 'buyerponumber',
    'delivery_buyer_payment_terms': 'deliverybuyerpaymentterms',
    'eway_bill_expiry_date': 'ewaybillexpirydate',
    'delay_days': 'delay',
    'logistic_delay_days': 'logisticdelay',
    'lr_number': 'lrno',
    'driver_mobile_number': 'drivermobileno',
    'transporter_name': 'transporter',
    'freight_cost': 'freight',
    'last_freight_cost': 'lastfreight',
    'freight_payment_status': 'freightpayment',
    'system_freight_cost': 'transit_distance',
    'max_possible_freight_cost': 'maxpossiblefreight',
    'transit_distance_in_km': 'transitdistance',
    'supplier_credit_note_value': 'suppliercreditnotevalue',
    'buyer_price': 'buyerprice',
    'buyer_credit_note_value': 'buyercreditnotevalue',
    'invoice_number': 'invoice',
    'supplier_price': 'supplierprice',
    'bill_number': 'bill',
    'purchase_order_number': 'purchaseorderno',
    'margin': 'margin',
    'total_amount': 'amount',
    'utr_number': 'utrno',
    'payment_made_to_supplier': 'paymentmadetosupplier',
    'freight_payment_application_status': 'freightpaymentapplicationstatus',
    'freight_bill_status': 'freightbillstatus',
    'freight_pod_status': 'freightpodstatus',
    'rejection_reason': 'rejectionreason',
    'reapply_reason': 'reapplyreason',
    'applied_for_freight_payment_at': 'appliedforfreightpaymentat', # this is being stored as unix timestamp
    'created_at': 'createdat', # this is being stored as unix timestamp
    'updated_at': 'updatedat', # this is being stored as unix timestamp
    'invoice_status': 'invoicestatus',
    'invoice_value': 'invoicevalue',
    'invoice_due_days': 'invoiceduedays',
    'invoice_balance': 'invoicebalance',
    'overdue_amount': 'overdueamount',
    'adjusted_system_distance': 'adjustedsystemdistance',
    'tracking_status': 'trackingstatus',
    'pod_reason': 'podreason',
    'bill_reason': 'billreason',
    'lr_reason': 'lrreason',
    'pod_remark': 'podremark',
    'bill_remark': 'billremark',
    'lr_remark': 'lrremark',
    'lr_status': 'lrstatus',
    'driver_coordinator_name': 'drivercoordinatorname',
    'transport_region': 'transportregion',
    'group_state_owner': 'groupstateowner',
    'buyer_account_manager': 'buyeraccountmanager',
    'supplier_account_manager': 'supplieraccountmanager',
    'is_return': 'isreturn',
    'return_order_created_from': 'returnordercreatedfrom',
    'buyer_poc': 'buyerpoc',
    'buyer_poc_name': 'buyerpocname',
    'supplier_poc': 'supplierpoc',
    'supplier_poc_name': 'supplierpocname',
    'tags': 'tags',
    'freight_quotes_count': 'freightquotescount',
    'loading_address': 'loadingwholeaddress',
    'vehicle_number': 'vehicleno',
    'delivered_to_with_parent': 'deliveredtowithparent',
    'warehouse_with_parent': 'godownwithparent',
    'created_at_date': 'createdatdate',
    'netback': 'netback',
    'buyer_group_id': 'buyergroupid',
    'supplier_group_id': 'suppliergroupid',
    'order_request_id': 'orderrequestid',
    'logistic_team_last_edit_by': 'logisticteam_lasteditby',
    'buyer_team_last_edit_by': 'buyerteam_lasteditby',
    'supplier_team_last_edit_by': 'supplierteam_lasteditby',
    'general_last_edit_by': 'general_lasteditby',
    'driver_last_edit_by': 'driver_lasteditby',
    'logistic_team_remarks_concatenated': 'logisticteam_concatenated',
    'buyer_team_remarks_concatenated': 'buyerteam_concatenated',
    'supplier_team_remarks_concatenated': 'supplierteam_concatenated',
    'general_remarks_concatenated': 'general_concatenated',
    'driver_remarks_concatenated': 'driver_concatenated',
    'netback_sf': 'netbacksf',
    'buyer_delivery_terms': 'buyerdeliveryterms',
    'state_abbreviation': 'state_abbreviation',
    'load': 'load',
    'freight_offset': 'freight_offset',
    'max_dispatch_date': 'maxdispatchdate',
    'min_dispatch_date': 'mindispatchdate',
    'last_order_days_ago': 'lastorderdaysago',
    'group_name': 'groupname',
    'group_limit': 'grouplimit',
    'group_blacklisted': 'groupblacklisted',
    'group_business_type': 'groupbusinesstype',
    'group_credit_interest': 'groupcreditinterest',
    'group_credit_limit': 'groupcreditlimit',
    'group_credit_tenor': 'groupcredittenor',
    'group_markup_value': 'groupmarkupvalue',
    'group_margin': 'groupmargin',
    'group_remarks': 'groupremarks',
    'group_unfulfilled_order_count': 'groupunfulfilledordercount',
    'group_waba_price_enabled': 'groupwabapriceenabled',
    'highest_gst_slab': 'highestgstslab',
    'orders_count': 'orderscount',
    'account_manager': 'accountmanager',
    'business_units': 'businessunits',
    'group_payment_category': 'grouppaymentcategory',
    'group_trade_reference_values': 'grouptradereferencevalues',
    'is_deleted': 'isdeleted',
    'application_type': 'applicationtype',
    'highest_pan': 'highestpan',
    'group_primary_location': 'groupprimarylocation',
    'last_ordered_date': 'lastordereddaysago',
    'coa_required': 'coarequired',
    'last_buyer_app_usage_days_ago': 'lastbuyerappusagedaysago',
    'payment_reminders': 'paymentreminders',
    'mobile_app_enabled': 'mobileappenabled',
    'supplier_payment_terms': 'supplierpaymentterms',
    'order_priority': 'priority',
    'listings_deactivation_timer': 'listingsdeactivationtimer',
    'repeat_reminders_after': 'repeatremindersafter',
    'special_offer_enabled': 'specialofferenabled',
    'supplier_orders_count': 'supplierorderscount',
    'group_available_limit': 'groupavailablelimit',
    'sub_application_types': 'subapplicationtypes',
    'pfp_status': 'pfpstatus',
    'group_creation_date': 'groupcreationdate',
    'regions': 'regions',
    'group_level_grade_groups': 'grouplevelgradegroups',
    'group_level_tags': 'groupleveltags',
    'group_hsns': 'grouphsns',
    'active_location': 'active_location',
    'inactive_location': 'inactive_location',
    'waba_status': 'wabastatus',
    'group_price_receipt': 'grouppricereceipt',
    'decision_maker_mapped': 'decisonmakermapped', #either YES or NO, need to map to boolean 
    'buyer_decision_maker': 'buyerdecisionmaker',
    'dgft_import': 'dgft_import',
    'dgft_import_mapped': 'dgft_import_mapped',
    'created_by': 'createdby',
    'last_correspondence_date': 'lastcorrespondancedate',
    'last_correspondence_days_ago': 'lastcorrespondencedaysago',
    'correspondence_range': 'correspondencerange',
    'first_note': 'first_note',
    'second_note': 'second_note',
    'credit_order': 'creditorder',
    'lifetime_volume': 'lifetimevolume',
    'liquidity_buyer_type': 'liquiditybuyertype',
    'outreach_buyer_type': 'outreachbuyertype',
    'days_passed': 'days_passed',
    'days_passed_label': 'days_passed_label',
    'opportunity': 'opportunity',
    'volume_supplied': 'volumesupplied',
    'supplier_activated': 'supplieractivated',
    'liquidity_type': 'liquiditytype',
    'liquidity_buyer_type_attrition_slab': 'liquiditybuyertype_attrition_slab',
    'finance_update_count': 'finance_update_count',
    'email_id_count': 'email_id_count',
    'parent_child_available': 'parent_child_available',
    'ceo': 'ceo',
    'coo': 'coo',
    'dm_owner': 'dm_owner',
    'dm_purchase_manager': 'dm_purchasemanager',
    'finance': 'finance',
    'gst': 'gst',
    'logistics': 'logistics',
    'md': 'md',
    'owner': 'owner',
    'purchase_head': 'purchase_head',
    'purchase_manager': 'purchase_manager',
    'sales_manager': 'sales_manager',
    'undefined_role': 'undefined_role',
    'tam': 'tam',
    'tag_category': 'tag_category',
    'buyer_decision_maker_person': 'buyerdecisionmakerperson',
    'buyer_decision_maker_email': 'buyerdecisionmakeremail',
    'ordered_grade_number': 'orderedgradenumber',
    'ordered_grade_group': 'orderedgradegroup',
    'pan': 'PAN',
    'total_mapped_qty': 'TotalMappedQty',
    'last_6mnt_lowest_not_adjusted': 'last_6mnt_lowest_notadjusted',
    'last_6mnt_lowest_not_adjusted_order_no': 'last_6mnt_lowest_notadjusted_orderno',
    'last_6mnt_lowest_adjusted': 'last_6mnt_lowest_adjusted',
    'last_6mnt_lowest_adjusted_order_no': 'last_6mnt_lowest_adjusted_orderno',
    'warehouse_parent_name': 'godown_parent_name',
    'destination_parent_name': 'destination_parent_name',
    'app_live_price': 'appliveprice',
    'l1_supplier_name': 'l1suppliername',
    'l1_netback': 'l1netback',
    'l2_supplier_name': 'l2suppliername',
    'l2_netback': 'l2netback',
    'l3_supplier_name': 'l3suppliername',
    'l3_netback': 'l3netback',
    'freight_quotes_l1': 'freight_quotes_l1',
    'freight_quotes_l2': 'freight_quotes_l2',
    'freight_quotes_l3': 'freight_quotes_l3',
    'change_time': 'change_time',
    'probable_supplier_group_id': 'probable_suppliergroupid',
    'probable_supplier_group_name': 'probable_suppliergroupname',
    'availability': 'availability',
    'buyer_type': 'buyerType',
    'company_gst': 'companygst',
    'order_created_by': 'ordercreatedby'
}


csv_file_path = 'orders_table.csv'


db_params = {
    'host': 'your_host',
    'database': 'your_database',
    'user': 'your_username',
    'password': 'your_password'
}

 
def convert_to_postgres_type(value, column_name):
    if value == '':
        return None
    if column_name.endswith('_date') or column_name in ['createdat', 'updatedat', 'appliedforfreightpaymentat']:
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return None
    if column_name in ['delay', 'logisticdelay', 'freightquotescount', 'orderscount', 'supplierorderscount']:
        try:
            return int(value)
        except ValueError:
            return None
    if column_name in ['freight', 'lastfreight', 'systemfreight', 'maxpossiblefreight', 'suppliercreditnotevalue',
                       'buyerprice', 'buyercreditnotevalue', 'supplierprice', 'amount', 'invoicevalue', 'invoicebalance',
                       'overdueamount', 'adjustedsystemdistance', 'netback', 'netbacksf', 'freight_offset']:
        try:
            return float(value)
        except ValueError:
            return None
    if column_name in ['isewaybillcreated', 'isreturn', 'isdeleted', 'coarequired', 'mobileappenabled',
                       'specialofferenabled', 'dgft_import', 'dgft_import_mapped', 'parent_child_available']:
        return value.lower() == 'true'
    return value

def insert_data_to_postgres(csv_file_path, db_params, table_name):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                columns = []
                values = []
                for pg_col, csv_col in COLUMN_MAPPING.items():
                    if csv_col in row:
                        columns.append(pg_col)
                        values.append(convert_to_postgres_type(row[csv_col], pg_col))
                
                insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(', ').join(map(sql.Identifier, columns)),
                    sql.SQL(', ').join(sql.Placeholder() * len(values))
                )
                
                cur.execute(insert_query, values)
        
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

# Usage
table_name = 'your_table_name'
insert_data_to_postgres(csv_file_path, db_params, table_name)