import csv
import mysql.connector
import datetime
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


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
    'delivery_location_id': 'deliveredtoid',
    'delivery_location_name': 'deliveredto',
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
    'delay_score': 'delay',
    'logistic_delay_score': 'logisticdelay',
    'lr_number': 'lrno',
    'driver_mobile_number': 'drivermobileno',
    'transporter_name': 'transporter',
    'freight_cost': 'freight',
    'last_freight_cost': 'lastfreight',
    'freight_payment_status': 'freightpayment',
    'system_freight_cost': 'systemfreight',
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
    'is_payment_made_to_supplier': 'paymentmadetosupplier',
    'freight_payment_application_status': 'freightpaymentapplicationstatus',
    'freight_bill_status': 'freightbillstatus',
    'freight_pod_status': 'freightpodstatus',
    'rejection_reason': 'rejectionreason',
    'reapply_reason': 'reapplyreason',
    'applied_for_freight_payment_at': 'appliedforfreightpaymentat',
    'created_at': 'createdat', 
    'updated_at': 'updatedat',
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
    'godown_with_parent': 'godownwithparent',
    'created_at': 'createdatdate',
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
    'load_amount': 'load',
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
    'gst_slab_greater_than': 'highestgstslab',
    'gst_slab_less_than': 'highestgstslab',
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
    'active_locations': 'active_location',
    'inactive_locations': 'inactive_location',
    'waba_status': 'wabastatus',
    'group_price_receipt': 'grouppricereceipt',
    'decision_maker_mapped': 'decisonmakermapped', 
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
    'is_supplier_activated': 'supplieractivated', 
    'liquidity_type': 'liquiditytype',
    'liquidity_buyer_type_attrition_slab': 'liquiditybuyertype_attrition_slab',
    'finance_update_count': 'finance_update_count',
    'email_id_count': 'email_id_count',
    'is_parent_child': 'parent_child_available',
    'number_of_ceo': 'ceo',
    'number_of_coo': 'coo',
    'number_of_dm_owner': 'dm_owner',
    'number_of_dm_purchase_manager': 'dm_purchasemanager',
    'number_of_finance': 'finance',
    'number_of_gst': 'gst',
    'number_of_logistics': 'logistics',
    'number_of_md': 'md',
    'number_of_owner': 'owner',
    'number_of_purchase_head': 'purchase_head',
    'number_of_purchase_manager': 'purchase_manager',
    'number_of_sales_manager': 'sales_manager',
    'number_of_undefined_role': 'undefined_role',
    'tam': 'tam',
    'tag_category': 'tag_category',
    'buyer_decision_maker_person': 'buyerdecisionmakerperson',
    'buyer_decision_maker_email': 'buyerdecisionmakeremail',
    'grade_number': 'orderedgradenumber',
    'grade_group': 'orderedgradegroup',
    'pan': 'PAN',
    'total_mapped_qty': 'TotalMappedQty',
    'last_6mnt_lowest_not_adjusted': 'last_6mnt_lowest_notadjusted',
    'last_6mnt_lowest_not_adjusted_order_no': 'last_6mnt_lowest_notadjusted_orderno',
    'last_6mnt_lowest_adjusted': 'last_6mnt_lowest_adjusted',
    'last_6mnt_lowest_adjusted_order_no': 'last_6mnt_lowest_adjusted_orderno',
    'godown_parent_name': 'godown_parent_name',
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
    'is_available': 'availability',
    'buyer_type': 'buyerType',
    'company_gst': 'companygst',
    'order_created_by': 'ordercreatedby',
    'buyer_threshold_payment_date':'buyerthresholdpaymentdate',
    'supplier_threshold_payment_date':'supplierthresholdpaymentdate'
}



def handle_decimal(value, column_name):
    decimal_columns = {
        'group_credit_interest': (5, 2),
        'group_markup_value': (5, 2),
        'group_margin': (5, 2),
        'quantity': (10, 2),
        'single_quantity': (10, 2),
        'supplier_credit_note_value': (10, 2),
        'buyer_price': (10, 2),
        'buyer_credit_note_value': (10, 2),
        'supplier_price': (10, 2),
        'total_amount': (10, 2),
        'netback': (10, 2),
        'netback_sf': (10, 2),
        'freight_offset': (10, 2),
        'group_limit': (15, 2),
        'group_credit_limit': (15, 2),
        'group_available_limit': (15, 2),
        'dgft_import': (10, 2),
        'dgft_import_mapped': (10, 2),
        'credit_order': (10, 2),
        'lifetime_volume': (10, 2),
        'volume_supplied': (10, 2),
        'total_mapped_qty': (10, 2),
        'last_6mnt_lowest_not_adjusted': (10, 2),
        'last_6mnt_lowest_adjusted': (10, 2),
        'app_live_price': (10, 2),
        'l1_netback': (10, 2),
        'l2_netback': (10, 2),
        'l3_netback': (10, 2),
        'freight_quotes_l1': (10, 2),
        'freight_quotes_l2': (10, 2),
        'freight_quotes_l3': (10, 2)
    }

    if column_name not in decimal_columns:
        return Decimal('0')

    try:
        if value in ['', 'N/A', 'NA', 'null', 'NULL', 'None', '0.0', 'NaN']:
            return Decimal('0')

        dec_value = Decimal(value)
        precision, scale = decimal_columns[column_name]
        max_value = Decimal('9' * precision) / (Decimal('10') ** scale)
        min_value = -max_value
        
        if dec_value > max_value or dec_value < min_value:
            print(f"Warning: Value {dec_value} for column {column_name} exceeds allowed range. Clamping to allowed range.")
            dec_value = max(min(dec_value, max_value), min_value)
        
        return dec_value.quantize(Decimal('0.' + '0' * scale), rounding=ROUND_HALF_UP)
    except InvalidOperation:
        print(f"Warning: Invalid decimal value '{value}' for column {column_name}. Using 0 instead.")
        return Decimal('0')


def convert_to_database_type(value, column_name):

    # Decimal columns
    decimal_columns = [
        'quantity', 'single_quantity', 'supplier_credit_note_value', 'buyer_price',
        'buyer_credit_note_value', 'supplier_price', 'margin', 'total_amount',
          'netback', 'netback_sf',
        'freight_offset', 'group_limit', 'group_credit_interest', 'group_credit_limit',
        'group_markup_value', 'group_margin', 'group_available_limit', 'dgft_import',
        'dgft_import_mapped', 'credit_order', 'lifetime_volume', 'volume_supplied',
        'total_mapped_qty', 'last_6mnt_lowest_not_adjusted', 'last_6mnt_lowest_adjusted',
        'app_live_price', 'l1_netback', 'l2_netback', 'l3_netback', 'freight_quotes_l1',
        'freight_quotes_l2', 'freight_quotes_l3'
    ]

    if (value in ['', 'N/A', 'NA', 'na', 'null', 'NULL', 'None', '0.0'] or value.strip() == '') and (column_name not in decimal_columns):
        return None
    
    if column_name == 'gst_slab_greater_than':
        if value == '0':
            return 0
        elif value == '0 to 40 lakhs':
            return 0
        elif value == '40 lakhs to 1.5 Cr.':
            return 40
        elif value == '1.5 Cr. to 5 Cr.':
            return 150
        elif value == '5 Cr. to 25 Cr.':
            return 500
        elif value == '25 Cr. to 100 Cr.':
            return 2500
        elif value == '100 Cr. to 500 Cr.':
            return 10000
        elif value == '500 Cr. and above':
            return 50000 
        else:
            return None  
    
    if column_name == 'gst_slab_less_than':
        if value == '0':
            return 0
        elif value == '0 to 40 lakhs':
            return 40
        elif value == '40 lakhs to 1.5 Cr.':
            return 150
        elif value == '1.5 Cr. to 5 Cr.':
            return 500
        elif value == '5 Cr. to 25 Cr.':
            return 2500
        elif value == '25 Cr. to 100 Cr.':
            return 10000
        elif value == '100 Cr. to 500 Cr.':
            return 50000
        elif value == '500 Cr. and above':
            return None
        else:
            return None
    
    if column_name == 'is_payment_made_to_supplier':
        if value == 'N':
            return False
        elif value == 'Y':
            return True
        else:
            return None
    
    # Special handling for dispatch_date
    if column_name == 'dispatch_date':
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format for column {column_name}: {value}")


    if column_name in [ 'last_ordered_date', 'min_dispatch_date', 'max_dispatch_date']:
        if value.strip() == '0' or value.strip() == '0.0':
            return None
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format for column {column_name}: {value}")

    if column_name in [ 'buyer_threshold_payment_date', 'supplier_threshold_payment_date']:
        if value.strip() == '0' or value.strip() == '0.0' or value.strip() == 'NA':
            return None
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format for column {column_name}: {value}")

    if column_name == 'group_creation_date' or column_name == 'last_correspondence_date':
        if value.strip() == '0':
            return None
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
            except ValueError:
                try:
                    return datetime.datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError(f"Invalid date format for column {column_name}: {value}")
    
    
    if column_name == 'group_waba_price_enabled':
         try:
            is_enabled = value == 'ENABLED'
            return is_enabled
         except ValueError:
            raise ValueError(f"Invalid date format for column {column_name}: {value}")
    
    # Special handling for due_date
    if column_name in ['due_date', 'buyer_due_date', 'actual_delivery_date', 'supplier_due_date']:
        try:
            return datetime.datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format for column {column_name}: {value}")
            
    if column_name == 'expected_delivery_date':
        try:
            if value == '20924-09-06':
                return datetime.date(2024, 9, 6)
            return datetime.datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format for column {column_name}: {value}")
    
    # Other date conversions
    if column_name.endswith('_date') or column_name in ['buyer_due_date', 'eway_bill_expiry_date']:
        if value.strip() == '0':
            return None
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(f"Invalid date format for column {column_name}: {value}")
    
    # Timestamp conversions
    if column_name in ['applied_for_freight_payment_at', 'created_at', 'updated_at', 'change_time']:
        try:
            # First, try to parse as a float (Unix timestamp)
           timestamp = int(value)
           if timestamp > 1000000000000:  # If timestamp is in milliseconds
                return datetime.datetime.fromtimestamp(timestamp / 1000)
           else:  # If timestamp is in seconds
                return datetime.datetime.fromtimestamp(timestamp)
        except ValueError:
            # If that fails, try to parse as a datetime string
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                try:
                    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    raise ValueError(f"Invalid timestamp for column {column_name}: {value}")

    if column_name  == 'transit_distance_in_km':
        if value.strip() == '' or  'ERR' in value or 'undefined' in value:
            return None
        try:
            distance = value.replace("km", "").strip()
            return int(float(distance))
        except ValueError:
            raise ValueError(f"Invalid value for column {column_name}: {value}")

    integer_columns = [
        'delay_score', 'logistic_delay_score', 'freight_cost', 'margin'
        'system_freight_cost', 'max_possible_freight_cost',
         'adjusted_system_distance', 'freight_quotes_count',
        'last_order_days_ago', 'group_unfulfilled_order_count', 'orders_count',
        'last_buyer_app_usage_days_ago', 'listings_deactivation_timer',
        'repeat_reminders_after', 'supplier_orders_count', 'last_correspondence_days_ago',
        'days_passed', 'finance_update_count', 'email_id_count', 'number_of_ceo', 'number_of_coo',
        'number_of_dm_owner', 'number_of_dm_purchase_manager', 'number_of_finance', 'number_of_gst', 'number_of_logistics', 'number_of_md',
        'number_of_owner', 'number_of_purchase_head', 'number_of_purchase_manager', 'number_of_sales_manager', 'number_of_undefined_role',
        'load_amount', 'payment_reminders', 'system_freight_cost'
    ]

    if column_name in integer_columns:
        try:
            return int(float(value))
        except ValueError:
            raise ValueError(f"Invalid integer for column {column_name}: {value}")


    if column_name in decimal_columns:
        return handle_decimal(value, column_name)

    
    # Boolean conversions
    if column_name in ['is_eway_bill_created', 'is_return', 'group_blacklisted', 'group_waba_price_enabled', 'is_deleted', 'coa_required', 'mobile_app_enabled', 'special_offer_enabled', 'decision_maker_mapped', 'is_supplier_activated', 'is_parent_child']:
        if value.lower() in ['true', '1', 'yes']:
            return True
        elif value.lower() in ['false', '0', 'no']:
            return False
        else:
            raise ValueError(f"Invalid boolean for column {column_name}: {value}")
    
    # Handle payment_reminders as JSONB
    if column_name == 'payment_reminders':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON for column {column_name}: {value}")
        
    
    if column_name == 'invoice_due_days':
        if not value.strip() or all(char == ',' for char in value.strip()):
            return None
        parts = [part.strip() for part in value.split(',') if part.strip()]
        unique_numbers = {part for part in parts if part.isdigit()}
        return int(unique_numbers.pop()) if unique_numbers else None

    
    if column_name == 'is_available':
        try:
            is_avail = False
            if value == "Available":
                is_avail = True
            return is_avail
        except ValueError:
            raise ValueError(f"Invalid date format for column {column_name}: {value}")

        
    if column_name == 'buyer_type':
        buyer_type_mapping = {
            'Regular Buyer': 'REGULAR BUYER',
            '0-1 Buyer': '0-1 BUYER',
            'Attrition(Comeback) Buyer': 'ATTRITION(COMEBACK) BUYER'
        }
        
        if value in buyer_type_mapping:
            return buyer_type_mapping[value]
        else:
            raise ValueError(f"Invalid buyer type for column {column_name}: {value}")
        
    if column_name == 'freight_payment_application_status':
        if value == '0':
            return None
        

    if column_name in ['driver_mobile_number', 'buyer_poc', 'buyer_decision_maker']:
        try:
            if value == '0':
                return None
            digits = ''.join(filter(str.isdigit, value))
            
            return digits[-10:] if len(digits) >= 10 else digits
        
        except ValueError:
            raise ValueError(f"Invalid mobile number for column {column_name}: {value}")
        
    if column_name in ['lr_status', 'business_units','tam', 'order_priority', 'tam_enum', 'delivery_buyer_payment_terms', 'group_business_type','waba_status', 'tag_category', 'group_price_receipt','correspondence_range']:
        try:
            if value == '0':
                return None
        
        except ValueError:
            raise ValueError(f"Invalid mobile number for column {column_name}: {value}")
        
    if column_name == 'buyer_delivery_terms':
        try:
            if value in ['0', 'dummy']:
                return None
            if value.lower() == 'f.o.r delivered. freight cost is included in the unit price':
                return 'F.O.R DELIVERED. Freight Cost is included in the Unit Price' 

        except ValueError:
            raise ValueError(f"Invalid mobile number for column {column_name}: {value}")
        
    if column_name == 'order_status':
        try:
            if value is None or not value.strip():
                return None

            value = value.strip().upper()
            return value
        except ValueError:
            raise ValueError(f"Invalid order status for column {column_name}: {value}")

    
    # Default case: return the value as is
    return value


def insert_data_to_database(csv_file_path, db_params, table_name, max_rows=5, min_row=0):
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_params)
        cur = conn.cursor()

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row_num, row in enumerate(csv_reader, start=1):
                if row_num < min_row:
                    continue
                if row_num > max_rows:
                    break
                
                # print("csv_row: ", row)
                columns = []
                values = []

                for db_col, csv_col in COLUMN_MAPPING.items():
                    if csv_col in row:
                        columns.append(db_col)
                        try:
                            converted_value = convert_to_database_type(row[csv_col], db_col)
                            values.append(converted_value)
                        except ValueError as ve:
                            print(f"Error on row {row_num}: {str(ve)}")
                            break
                else:
                    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

                    
                    try:
                        cur.execute(insert_query, values)
                        print(f"Inserted row {row_num}")
                    except Exception as e:
                        print(f"Database error on row {row_num}: {str(e)}")
                        print(values)
                        conn.rollback()
                    continue
                                
                # If we're here, it means we broke out of the for loop due to an error
                conn.rollback()

        conn.commit()
        print(f"Data insertion completed. Attempted to insert {min(row_num, max_rows)} rows.")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"An unexpected error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# Usage
if __name__ == "__main__":
    table_name = 'order_table_ai'

    db_params = {
        'host': 'localhost',
        'database': 'mydb',
        'user': 'myuser',
        'password': 'mypassword',
        'port':'5454',
        'charset': 'utf8mb4', 
        'collation': 'utf8mb4_general_ci'
    }

    csv_file_path = 'orders_table.csv'

    insert_data_to_database(csv_file_path, db_params, table_name, max_rows=50000, min_row=1)