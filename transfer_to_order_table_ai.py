import gc
gc.set_threshold(1000000, 5, 5)

import datetime
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import pandas as pd
import pytz
import os

from sqlalchemy import Column, String, Text, Integer, Date, Boolean, DECIMAL, TIMESTAMP, VARCHAR, CHAR, Index
from sqlalchemy import create_engine, Table, Column, insert, String, MetaData, Text, select, Float, BigInteger, text
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from sqlalchemy.dialects.mysql import insert as mysql_insert
import pandas as pd
from pymongo import MongoClient
import numpy as np
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
import re
metadata = MetaData()


def get_ist_now():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

runtime = get_ist_now()
print(runtime)


timestamp_epoch_ms = int(datetime.datetime.now().timestamp() * 1000)
print(timestamp_epoch_ms)

right_runtime_start = pd.Timestamp(datetime.datetime.now())


db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password= os.getenv('DB_PASSWORD')
db_host= os.getenv('DB_HOST')
db_port =int(os.getenv('DB_PORT'))


engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')


# Read the last runtime from scripts_runtime table
scripts_runtime = Table('scripts_runtime', metadata, autoload_with=engine)
with engine.connect() as connection:
    stmt = select(scripts_runtime.c.runtime).where(scripts_runtime.c.script_name == 'order_table_ai')
    result = connection.execute(stmt).fetchone()
    last_runtime = int(result[0]) if result and result[0] else 0
  

last_runtime = last_runtime-(2*60*1000)
# print(last_runtime)


order_table = text("SELECT * FROM order_table_superset WHERE updatedat > :last_runtime")

with engine.connect() as connection:
    order_table = pd.read_sql(order_table, connection, params={"last_runtime": last_runtime})

if order_table.empty:
    print("No new data in order_table_superset. Script execution stopped.")

else:

    COLUMN_MAPPING = {
        '_id': 'id',
        'orderno': 'order_number',
        'supplierid': 'supplier_gst',
        'supplier': 'supplier_name',
        'buyerid': 'buyer_gst',
        'buyer': 'buyer_name',
        'godownid': 'godown_id',
        'godown': 'godown_name',
        'quantity': 'quantity',
        'singlequantity': 'single_quantity',
        'productid': 'product_id',
        'productname': 'product_name',
        'deliveredtoid': 'delivery_location_id',
        'deliveredto': 'delivery_location_name',
        'dispatchdate': 'dispatch_date',
        'duedate': 'due_date',
        'buyerduedate': 'buyer_due_date',
        'expecteddeliverydate': 'expected_delivery_date',
        'actualdeliverydate': 'actual_delivery_date',
        'supplierduedate': 'supplier_due_date',
        'status': 'order_status',
        'buyerpaymentterms': 'buyer_payment_terms',
        'deliverywholeaddress': 'delivery_address',
        'transportaddress': 'transporter_address',
        'isewaybillcreated': 'is_eway_bill_created',
        'buyerponumber': 'buyer_po_number',
        'deliverybuyerpaymentterms': 'delivery_buyer_payment_terms',
        'ewaybillexpirydate': 'eway_bill_expiry_date',
        'delay': 'delay_score',
        'logisticdelay': 'logistic_delay_score',
        'lrno': 'lr_number',
        'drivermobileno': 'driver_mobile_number',
        'transporter': 'transporter_name',
        'freight': 'freight_cost',
        'lastfreight': 'last_freight_cost',
        'freightpayment': 'freight_payment_status',
        'systemfreight': 'system_freight_cost',
        'maxpossiblefreight': 'max_possible_freight_cost',
        'transitdistance': 'transit_distance_in_km',
        'suppliercreditnotevalue': 'supplier_credit_note_value',
        'buyerprice': 'buyer_price',
        'buyercreditnotevalue': 'buyer_credit_note_value',
        'invoice': 'invoice_number',
        'supplierprice': 'supplier_price',
        'bill': 'bill_number',
        'purchaseorderno': 'purchase_order_number',
        'margin': 'margin',
        'amount': 'total_amount',
        'utrno': 'utr_number',
        'paymentmadetosupplier': 'is_payment_made_to_supplier',
        'freightpaymentapplicationstatus': 'freight_payment_application_status',
        'freightbillstatus': 'freight_bill_status',
        'freightpodstatus': 'freight_pod_status',
        'rejectionreason': 'rejection_reason',
        'reapplyreason': 'reapply_reason',
        'appliedforfreightpaymentat': 'applied_for_freight_payment_at',
        'createdat': 'created_at',
        'updatedat': 'updated_at',
        'invoicestatus': 'invoice_status',
        'invoicevalue': 'invoice_value',
        'invoiceduedays': 'invoice_due_days',
        'invoicebalance': 'invoice_balance',
        'overdueamount': 'overdue_amount',
        'adjustedsystemdistance': 'adjusted_system_distance',
        'trackingstatus': 'tracking_status',
        'podreason': 'pod_reason',
        'billreason': 'bill_reason',
        'lrreason': 'lr_reason',
        'podremark': 'pod_remark',
        'billremark': 'bill_remark',
        'lrremark': 'lr_remark',
        'lrstatus': 'lr_status',
        'drivercoordinatorname': 'driver_coordinator_name',
        'transportregion': 'transport_region',
        'groupstateowner': 'group_state_owner',
        'buyeraccountmanager': 'buyer_account_manager',
        'supplieraccountmanager': 'supplier_account_manager',
        'isreturn': 'is_return',
        'returnordercreatedfrom': 'return_order_created_from',
        'buyerpoc': 'buyer_poc',
        'buyerpocname': 'buyer_poc_name',
        'supplierpoc': 'supplier_poc',
        'supplierpocname': 'supplier_poc_name',
        'tags': 'tags',
        'freightquotescount': 'freight_quotes_count',
        'loadingwholeaddress': 'loading_address',
        'vehicleno': 'vehicle_number',
        'deliveredtowithparent': 'delivered_to_with_parent',
        'godownwithparent': 'godown_with_parent',
        'netback': 'netback',
        'buyergroupid': 'buyer_group_id',
        'suppliergroupid': 'supplier_group_id',
        'orderrequestid': 'order_request_id',
        'logisticteam_lasteditby': 'logistic_team_last_edit_by',
        'buyerteam_lasteditby': 'buyer_team_last_edit_by',
        'supplierteam_lasteditby': 'supplier_team_last_edit_by',
        'general_lasteditby': 'general_last_edit_by',
        'driver_lasteditby': 'driver_last_edit_by',
        'logisticteam_concatenated': 'logistic_team_remarks_concatenated',
        'buyerteam_concatenated': 'buyer_team_remarks_concatenated',
        'supplierteam_concatenated': 'supplier_team_remarks_concatenated',
        'general_concatenated': 'general_remarks_concatenated',
        'driver_concatenated': 'driver_remarks_concatenated',
        'netbacksf': 'netback_sf',
        'buyerdeliveryterms': 'buyer_delivery_terms',
        'state_abbreviation': 'state_abbreviation',
        'load': 'load_amount',
        'freight_offset': 'freight_offset',
        'maxdispatchdate': 'max_dispatch_date',
        'mindispatchdate': 'min_dispatch_date',
        'lastorderdaysago': 'last_order_days_ago',
        'groupname': 'group_name',
        'grouplimit': 'group_limit',
        'groupblacklisted': 'group_blacklisted',
        'groupbusinesstype': 'group_business_type',
        'groupcreditinterest': 'group_credit_interest',
        'groupcreditlimit': 'group_credit_limit',
        'groupcredittenor': 'group_credit_tenor',
        'groupmarkupvalue': 'group_markup_value',
        'groupmargin': 'group_margin',
        'groupremarks': 'group_remarks',
        'groupunfulfilledordercount': 'group_unfulfilled_order_count',
        'groupwabapriceenabled': 'group_waba_price_enabled',
        'highestgstslab': 'highest_gst_slab',
        'orderscount': 'orders_count',
        'accountmanager': 'account_manager',
        'businessunits': 'business_units',
        'grouppaymentcategory': 'group_payment_category',
        'grouptradereferencevalues': 'group_trade_reference_values',
        'isdeleted': 'is_deleted',
        'applicationtype': 'application_type',
        'highestpan': 'highest_pan',
        'groupprimarylocation': 'group_primary_location',
        'lastordereddaysago': 'last_ordered_date',
        'coarequired': 'coa_required',
        'lastbuyerappusagedaysago': 'last_buyer_app_usage_days_ago',
        'paymentreminders': 'payment_reminders',
        'mobileappenabled': 'mobile_app_enabled',
        'supplierpaymentterms': 'supplier_payment_terms',
        'priority': 'order_priority',
        'listingsdeactivationtimer': 'listings_deactivation_timer',
        'repeatremindersafter': 'repeat_reminders_after',
        'specialofferenabled': 'special_offer_enabled',
        'supplierorderscount': 'supplier_orders_count',
        'groupavailablelimit': 'group_available_limit',
        'subapplicationtypes': 'sub_application_types',
        'pfpstatus': 'pfp_status',
        'groupcreationdate': 'group_creation_date',
        'regions': 'regions',
        'grouplevelgradegroups': 'group_level_grade_groups',
        'groupleveltags': 'group_level_tags',
        'grouphsns': 'group_hsns',
        'active_location': 'active_locations',
        'inactive_location': 'inactive_locations',
        'wabastatus': 'waba_status',
        'grouppricereceipt': 'group_price_receipt',
        'decisonmakermapped': 'decision_maker_mapped',
        'buyerdecisionmaker': 'buyer_decision_maker',
        'dgft_import': 'dgft_import',
        'dgft_import_mapped': 'dgft_import_mapped',
        'createdby': 'created_by',
        'lastcorrespondancedate': 'last_correspondence_date',
        'lastcorrespondencedaysago': 'last_correspondence_days_ago',
        'correspondencerange': 'correspondence_range',
        'first_note': 'first_note',
        'second_note': 'second_note',
        'creditorder': 'credit_order',
        'lifetimevolume': 'lifetime_volume',
        'liquiditybuyertype': 'liquidity_buyer_type',
        'outreachbuyertype': 'outreach_buyer_type',
        'days_passed': 'days_passed',
        'days_passed_label': 'days_passed_label',
        'opportunity': 'opportunity',
        'volumesupplied': 'volume_supplied',
        'supplieractivated': 'is_supplier_activated',
        'liquiditytype': 'liquidity_type',
        'liquiditybuyertype_attrition_slab': 'liquidity_buyer_type_attrition_slab',
        'finance_update_count': 'finance_update_count',
        'email_id_count': 'email_id_count',
        'parent_child_available': 'is_parent_child',
        'ceo': 'number_of_ceo',
        'coo': 'number_of_coo',
        'dm_owner': 'number_of_dm_owner',
        'dm_purchasemanager': 'number_of_dm_purchase_manager',
        'finance': 'number_of_finance',
        'gst': 'number_of_gst',
        'logistics': 'number_of_logistics',
        'md': 'number_of_md',
        'owner': 'number_of_owner',
        'purchase_head': 'number_of_purchase_head',
        'purchase_manager': 'number_of_purchase_manager',
        'sales_manager': 'number_of_sales_manager',
        'undefined_role': 'number_of_undefined_role',
        'tam': 'tam',
        'tag_category': 'tag_category',
        'buyerdecisionmakerperson': 'buyer_decision_maker_person',
        'buyerdecisionmakeremail': 'buyer_decision_maker_email',
        'orderedgradenumber': 'ordered_grade_number',
        'orderedgradegroup': 'ordered_grade_group',
        'PAN': 'pan',
        'TotalMappedQty': 'total_mapped_qty',
        'last_6mnt_lowest_notadjusted': 'last_6mnt_lowest_not_adjusted',
        'last_6mnt_lowest_notadjusted_orderno': 'last_6mnt_lowest_not_adjusted_order_no',
        'last_6mnt_lowest_adjusted': 'last_6mnt_lowest_adjusted',
        'last_6mnt_lowest_adjusted_orderno': 'last_6mnt_lowest_adjusted_order_no',
        'godown_parent_name': 'godown_parent_name',
        'destination_parent_name': 'destination_parent_name',
        'appliveprice': 'app_live_price',
        'l1suppliername': 'l1_supplier_name',
        'l1netback': 'l1_netback',
        'l2suppliername': 'l2_supplier_name',
        'l2netback': 'l2_netback',
        'l3suppliername': 'l3_supplier_name',
        'l3netback': 'l3_netback',
        'freight_quotes_l1': 'freight_quotes_l1',
        'freight_quotes_l2': 'freight_quotes_l2',
        'freight_quotes_l3': 'freight_quotes_l3',
        'change_time': 'change_time',
        'probable_suppliergroupid': 'probable_supplier_group_id',
        'probable_suppliergroupname': 'probable_supplier_group_name',
        'availability': 'is_available',
        'buyerType': 'buyer_type',
        'companygst': 'company_gst',
        'ordercreatedby': 'order_created_by'
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
        value = str(value)
        if value in ['', 'N/A', 'NA', 'na', 'nan', 'null', 'NULL', 'None', '0.0'] or value.strip() == '':
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
                    try:
                        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
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
                timestamp = float(value)
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
                if value in ['nan']:
                    return None
                return int(float(value))
            except ValueError:
                raise ValueError(f"Invalid integer for column {column_name}: {value}")

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



    def preprocess_dataframe(df):
        df = df.rename(columns = COLUMN_MAPPING)
        for column in df.columns:
            df[column] = df[column].apply(lambda value: convert_to_database_type(value, column))

        return df
    

    def get_gst_slab_greater_than(value):
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

    def get_gst_slab_less_than(value):
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

    # Apply the functions to create the new columns
    order_table['gst_slab_greater_than'] = order_table['highestgstslab'].apply(get_gst_slab_greater_than)
    order_table['gst_slab_less_than'] = order_table['highestgstslab'].apply(get_gst_slab_less_than)

    columns_to_remove = ['groupappenabled', 'createdatdate','highestgstslab']
    order_table = order_table.drop(columns=columns_to_remove)




    columns = [
        Column('id', String(24), primary_key=True),
        Column('order_number', String(10), unique=True),
        Column('supplier_gst', String(15)),
        Column('supplier_name', Text),
        Column('buyer_gst', String(15)),
        Column('buyer_name', Text),
        Column('godown_id', String(24)),
        Column('godown_name', String(30)),
        Column('quantity', DECIMAL(10, 2)),
        Column('single_quantity', DECIMAL(10, 2)),
        Column('product_id', String(24)),
        Column('product_name', Text),
        Column('delivery_location_id', String(24)),
        Column('delivery_location_name', String(30)),
        Column('dispatch_date', Date),
        Column('due_date', Date),
        Column('buyer_due_date', Date),
        Column('expected_delivery_date', Date),
        Column('actual_delivery_date', Date),
        Column('supplier_due_date', Date),
        Column('order_status', String(30)),
        Column('buyer_payment_terms', String(30)),
        Column('delivery_address', Text),
        Column('transporter_address', Text),
        Column('is_eway_bill_created', Boolean),
        Column('buyer_po_number', Text),
        Column('delivery_buyer_payment_terms', String(30)),
        Column('eway_bill_expiry_date', Date),
        Column('delay_score', Integer, default=0),
        Column('logistic_delay_score', Integer, default=0),
        Column('lr_number', String(30)),
        Column('driver_mobile_number', String(10)),
        Column('transporter_name', Text),
        Column('freight_cost', Integer),
        Column('last_freight_cost', Text),
        Column('freight_payment_status', String(30)),
        Column('system_freight_cost', Integer),
        Column('max_possible_freight_cost', Integer),
        Column('transit_distance_in_km', Integer),
        Column('supplier_credit_note_value', DECIMAL(10, 2)),
        Column('buyer_price', DECIMAL(10, 2)),
        Column('buyer_credit_note_value', DECIMAL(10, 2)),
        Column('invoice_number', Text),
        Column('supplier_price', DECIMAL(10, 2)),
        Column('bill_number', Text),
        Column('purchase_order_number', String(30)),
        Column('margin', Integer),
        Column('total_amount', DECIMAL(10, 2)),
        Column('utr_number', Text),
        Column('is_payment_made_to_supplier', Boolean),
        Column('freight_payment_application_status', String(30)),
        Column('freight_bill_status', String(30)),
        Column('freight_pod_status', String(30)),
        Column('rejection_reason', Text),
        Column('reapply_reason', Text),
        Column('applied_for_freight_payment_at', TIMESTAMP),
        Column('created_at', TIMESTAMP),
        Column('updated_at', TIMESTAMP),
        Column('invoice_status', Text),
        Column('invoice_value', Text),
        Column('invoice_due_days', Integer),
        Column('invoice_balance', Text),
        Column('overdue_amount', Text),
        Column('adjusted_system_distance', Integer),
        Column('tracking_status', String(30)),
        Column('pod_reason', Text),
        Column('bill_reason', Text),
        Column('lr_reason', Text),
        Column('pod_remark', Text),
        Column('bill_remark', Text),
        Column('lr_remark', Text),
        Column('lr_status', String(40)),
        Column('driver_coordinator_name', Text),
        Column('transport_region', String(4)),
        Column('group_state_owner', Text),
        Column('buyer_account_manager', Text),
        Column('supplier_account_manager', Text),
        Column('is_return', Boolean),
        Column('return_order_created_from', String(10)),
        Column('buyer_poc', String(10)),
        Column('buyer_poc_name', Text),
        Column('supplier_poc', String(10)),
        Column('supplier_poc_name', Text),
        Column('tags', Text),
        Column('freight_quotes_count', Integer),
        Column('loading_address', Text),
        Column('vehicle_number', String(10)),
        Column('delivered_to_with_parent', Text),
        Column('godown_with_parent', Text),
        Column('netback', DECIMAL(10, 2)),
        Column('buyer_group_id', String(24)),
        Column('supplier_group_id', String(24)),
        Column('order_request_id', String(24)),
        Column('logistic_team_last_edit_by', Text),
        Column('buyer_team_last_edit_by', String(50)),
        Column('supplier_team_last_edit_by', String(50)),
        Column('general_last_edit_by', String(50)),
        Column('driver_last_edit_by', String(50)),
        Column('logistic_team_remarks_concatenated', Text),
        Column('buyer_team_remarks_concatenated', Text),
        Column('supplier_team_remarks_concatenated', Text),
        Column('general_remarks_concatenated', Text),
        Column('driver_remarks_concatenated', Text),
        Column('netback_sf', DECIMAL(10, 2)),
        Column('buyer_delivery_terms', String(60)),
        Column('state_abbreviation', String(2)),
        Column('load_amount', Integer),
        Column('freight_offset', DECIMAL(10, 2)),
        Column('max_dispatch_date', Date),
        Column('min_dispatch_date', Date),
        Column('last_order_days_ago', Integer),
        Column('group_name', Text),
        Column('group_limit', DECIMAL(15, 2)),
        Column('group_blacklisted', Boolean),
        Column('group_business_type', String(15)),
        Column('group_credit_interest', DECIMAL(5, 2)),
        Column('group_credit_limit', DECIMAL(15, 2)),
        Column('group_credit_tenor', String(30)),
        Column('group_markup_value', DECIMAL(5, 2)),
        Column('group_margin', DECIMAL(5, 2)),
        Column('group_remarks', Text),
        Column('group_unfulfilled_order_count', Integer),
        Column('group_waba_price_enabled', Boolean),
        Column('gst_slab_greater_than', Integer),
        Column('gst_slab_less_than', Integer),
        Column('orders_count', Integer),
        Column('account_manager', String(50)),
        Column('business_units', String(25)),
        Column('group_payment_category', Text),
        Column('group_trade_reference_values', Text),
        Column('is_deleted', Boolean),
        Column('application_type', String(50)),
        Column('highest_pan', String(10)),
        Column('group_primary_location', String(50)),
        Column('last_ordered_date', Date),
        Column('coa_required', Boolean),
        Column('last_buyer_app_usage_days_ago', Integer),
        Column('payment_reminders', Integer),
        Column('mobile_app_enabled', Boolean),
        Column('supplier_payment_terms', Text),
        Column('order_priority', String(10)),
        Column('listings_deactivation_timer', Integer),
        Column('repeat_reminders_after', Integer),
        Column('special_offer_enabled', Boolean),
        Column('supplier_orders_count', Integer),
        Column('group_available_limit', DECIMAL(15, 2)),
        Column('sub_application_types', Text),
        Column('pfp_status', String(50)),
        Column('group_creation_date', Date),
        Column('regions', Text),
        Column('group_level_grade_groups', Text),
        Column('group_level_tags', Text),
        Column('group_hsns', Text),
        Column('active_locations', Text),
        Column('inactive_locations', Text),
        Column('waba_status', String(10)),
        Column('group_price_receipt', String(10)),
        Column('decision_maker_mapped', Boolean),
        Column('buyer_decision_maker', String(10)),
        Column('dgft_import', DECIMAL(10, 2)),
        Column('dgft_import_mapped', DECIMAL(10, 2)),
        Column('created_by', String(50)),
        Column('last_correspondence_date', Date),
        Column('last_correspondence_days_ago', Integer),
        Column('correspondence_range', String(15)),
        Column('first_note', Text),
        Column('second_note', Text),
        Column('credit_order', DECIMAL(10, 2)),
        Column('lifetime_volume', DECIMAL(10, 2)),
        Column('liquidity_buyer_type', String(15)),
        Column('outreach_buyer_type', String(15)),
        Column('days_passed', Integer),
        Column('days_passed_label', String(15)),
        Column('opportunity', Text),
        Column('volume_supplied', DECIMAL(10, 2)),
        Column('is_supplier_activated', Boolean),
        Column('liquidity_type', String(20)),
        Column('liquidity_buyer_type_attrition_slab', String(20)),
        Column('finance_update_count', Integer),
        Column('email_id_count', Integer),
        Column('is_parent_child', Boolean),
        Column('number_of_ceo', Integer),
        Column('number_of_coo', Integer),
        Column('number_of_dm_owner', Integer),
        Column('number_of_dm_purchase_manager', Integer),
        Column('number_of_finance', Integer),
        Column('number_of_gst', Integer),
        Column('number_of_logistics', Integer),
        Column('number_of_md', Integer),
        Column('number_of_owner', Integer),
        Column('number_of_purchase_head', Integer),
        Column('number_of_purchase_manager', Integer),
        Column('number_of_sales_manager', Integer),
        Column('number_of_undefined_role', Integer),
        Column('tam', String(20)),
        Column('tag_category', String(10)),
        Column('buyer_decision_maker_person', Text),
        Column('buyer_decision_maker_email', Text),
        Column('ordered_grade_number', Text),
        Column('ordered_grade_group', Text),
        Column('pan', String(10)),
        Column('total_mapped_qty', DECIMAL(10, 2)),
        Column('last_6mnt_lowest_not_adjusted', DECIMAL(10, 2)),
        Column('last_6mnt_lowest_not_adjusted_order_no', Text),
        Column('last_6mnt_lowest_adjusted', DECIMAL(10, 2)),
        Column('last_6mnt_lowest_adjusted_order_no', Text),
        Column('godown_parent_name', Text),
        Column('destination_parent_name', Text),
        Column('app_live_price', DECIMAL(10, 2)),
        Column('l1_supplier_name', Text),
        Column('l1_netback', DECIMAL(10, 2)),
        Column('l2_supplier_name', Text),
        Column('l2_netback', DECIMAL(10, 2)),
        Column('l3_supplier_name', Text),
        Column('l3_netback', DECIMAL(10, 2)),
        Column('freight_quotes_l1', DECIMAL(10, 2)),
        Column('freight_quotes_l2', DECIMAL(10, 2)),
        Column('freight_quotes_l3', DECIMAL(10, 2)),
        Column('change_time', TIMESTAMP),
        Column('probable_supplier_group_id', Text),
        Column('probable_supplier_group_name', Text),
        Column('is_available', Boolean),
        Column('buyer_type', String(30)),
        Column('company_gst', String(15), default='27ABACS7251D1ZH'),
        Column('order_created_by', String(50))
    ]


    # Define the table
    table = Table('order_table_ai', metadata, *columns)

    Index('idx_order_number', table.c.order_number)
    Index('idx_supplier_gst', table.c.supplier_gst)
    Index('idx_buyer_gst', table.c.buyer_gst)
    Index('idx_product_id', table.c.product_id)
    Index('idx_status', table.c.order_status)
    Index('idx_dispatch_date', table.c.dispatch_date)
    Index('idx_due_date', table.c.due_date)
    Index('idx_created_at', table.c.created_at)
    
    Index('idx_fulltext_supplier_name', table.c.supplier_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_buyer_name', table.c.buyer_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_godown_name', table.c.godown_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_product_name', table.c.product_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_delivery_location_name', table.c.delivery_location_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_delivery_address', table.c.delivery_address, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_transporter_address', table.c.transporter_address, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_buyer_po_number', table.c.buyer_po_number, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_transporter_name', table.c.transporter_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_last_freight_cost', table.c.last_freight_cost, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_invoice_number', table.c.invoice_number, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_bill_number', table.c.bill_number, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_utr_number', table.c.utr_number, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_rejection_reason', table.c.rejection_reason, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_reapply_reason', table.c.reapply_reason, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_invoice_status', table.c.invoice_status, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_invoice_value', table.c.invoice_value, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_invoice_balance', table.c.invoice_balance, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_overdue_amount', table.c.overdue_amount, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_pod_reason', table.c.pod_reason, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_bill_reason', table.c.bill_reason, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_lr_reason', table.c.lr_reason, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_pod_remark', table.c.pod_remark, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_bill_remark', table.c.bill_remark, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_lr_remark', table.c.lr_remark, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_driver_coordinator_name', table.c.driver_coordinator_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_group_remarks', table.c.group_remarks, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_group_payment_category', table.c.group_payment_category, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_group_trade_reference_values', table.c.group_trade_reference_values, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_supplier_payment_terms', table.c.supplier_payment_terms, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_sub_application_types', table.c.sub_application_types, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_regions', table.c.regions, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_group_level_grade_groups', table.c.group_level_grade_groups, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_group_level_tags', table.c.group_level_tags, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_group_hsns', table.c.group_hsns, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_active_locations', table.c.active_locations, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_inactive_locations', table.c.inactive_locations, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_first_note', table.c.first_note, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_second_note', table.c.second_note, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_opportunity', table.c.opportunity, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_buyer_decision_maker_person', table.c.buyer_decision_maker_person, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_buyer_decision_maker_email', table.c.buyer_decision_maker_email, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_last_6mnt_lowest_not_adjusted_order_no', table.c.last_6mnt_lowest_not_adjusted_order_no, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_last_6mnt_lowest_adjusted_order_no', table.c.last_6mnt_lowest_adjusted_order_no, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_godown_parent_name', table.c.godown_parent_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_destination_parent_name', table.c.destination_parent_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_l1_supplier_name', table.c.l1_supplier_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_l2_supplier_name', table.c.l2_supplier_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_l3_supplier_name', table.c.l3_supplier_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_probable_supplier_group_id', table.c.probable_supplier_group_id, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_probable_supplier_group_name', table.c.probable_supplier_group_name, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_buyer_type', table.c.buyer_type, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_company_gst', table.c.company_gst, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_order_created_by', table.c.order_created_by, mysql_prefix='FULLTEXT')
    Index('idx_fulltext_tags', table.c.tags, mysql_prefix='FULLTEXT')

    # Create the table in the database
    try:
        metadata.create_all(engine)
    except OperationalError as e:
        print(f"Error creating table: {e}")

    # Function to convert row to dictionary with None values for NaNs
    def row_to_dict_with_none(row):
        return {key: (None if pd.isna(value) else value) for key, value in row.items()}

    # Insert or update the DataFrame in the database using bulk operations
    def insert_or_update_orders(df, table):
        with engine.connect() as connection:
            try:
                # Start a transaction
                with connection.begin() as transaction:
                    df = preprocess_dataframe(df)
                    rows = df.to_dict(orient='records')
                    
                    # Convert NaN to None
                    rows = [row_to_dict_with_none(row) for row in rows]

                    for chunk in [rows[i:i + 1000] for i in range(0, len(rows), 1000)]:
                        insert_stmt = mysql_insert(table).values(chunk)

                        # Update statement to handle conflicts
                        update_stmt = insert_stmt.on_duplicate_key_update(
                            {key: insert_stmt.inserted[key] for key in df.columns if key != 'id'}
                        )

                        # Execute the upsert statement
                        connection.execute(update_stmt)

                    # Commit the transaction
                    transaction.commit()
            except OperationalError as e:
                print(f"OperationalError updating or inserting record: {e}")
            except SQLAlchemyError as e:
                print(f"SQLAlchemyError updating or inserting record: {e}")
            except Exception as e:
                print(f"Unexpected error updating or inserting record: {e}")

    insert_or_update_orders(order_table, table)
    
    # Insert or update the script runtime in the database
    with engine.connect() as connection:
        insert_update_query = text("""
            INSERT INTO scripts_runtime (script_name, runtime)
            VALUES (:script_name, :runtime)
            ON DUPLICATE KEY UPDATE runtime = :runtime
        """)

        try:
            # Start a transaction
            with connection.begin() as transaction:
                timestamp_epoch_ms = int(datetime.datetime.now().timestamp() * 1000)  # Generate a timestamp
                # Update for ordertable
                connection.execute(insert_update_query, {"script_name": "order_table_ai", "runtime": timestamp_epoch_ms})
                
                # Commit the transaction
                transaction.commit()

        except ProgrammingError as e:
            print(f"ProgrammingError inserting/updating script runtime: {e}")
        except OperationalError as e:
            print(f"OperationalError inserting/updating script runtime: {e}")
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError inserting/updating script runtime: {e}")
        except Exception as e:
            print(f"Unexpected error inserting/updating script runtime: {e}")

    right_runtime_end = pd.Timestamp(datetime.datetime.now())
    print("Runtime:", right_runtime_end - right_runtime_start)
