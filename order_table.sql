
CREATE TYPE ORDER_STATUS_ENUM AS ENUM (
    'ENQUIRY_SCHEDULED',
    'ENQUIRY_SENT',
    'TRANSPORTER_CONFIRMED',
    'VEHICLE_CONFIRMED',
    'VEHICLE_REACHED',
    'VEHICLE_REACHED_AT_GODOWN',
    'LOADING_IN_PROGRESS',
    'VEHICLE_LOADED',
    'SUPPLIER_INVOICE_RECEIVED',
    'INVOICE_GENERATED',
    'VEHICLE_DISPATCHED',
    'VEHICLE_REACHED_AT_DESTINATION',
    'VEHICLE_DELIVERED',
    'GENERATED',
    'NOT_GENERATED',
    'UNPAID',
    'APPLIED_FOR_PAYMENT',
    'BILL_GENERATED',
    'REJECTED',
    'PAID',
    'HOLD'
);

CREATE TYPE delivery_buyer_payment_terms_enum AS ENUM (
    'ADVANCE',
    'PRE-ADVANCE',
    '30 DAYS FROM BILL OF EXCHANGE',
    '45 DAYS FROM BILL OF EXCHANGE',
    '60 DAYS FROM BILL OF EXCHANGE',
    '90 DAYS FROM BILL OF EXCHANGE',
    '120 DAYS FROM BILL OF EXCHANGE',
    'DELIVERY + 1 DAYS',
    'DELIVERY + 2 DAYS',
    'DELIVERY + 3 DAYS',
    'DELIVERY + 4 DAYS',
    'DELIVERY + 5 DAYS',
    'DELIVERY + 6 DAYS',
    'DELIVERY + 7 DAYS',
    'DELIVERY + 8 DAYS',
    'DELIVERY + 9 DAYS',
    'DELIVERY + 10 DAYS',
    'DELIVERY + 11 DAYS',
    'DELIVERY + 12 DAYS',
    'DELIVERY + 13 DAYS',
    'DELIVERY + 14 DAYS',
    'DELIVERY + 15 DAYS',
    'DELIVERY + 16 DAYS',
    'DELIVERY + 17 DAYS',
    'DELIVERY + 18 DAYS',
    'DELIVERY + 19 DAYS',
    'DELIVERY + 20 DAYS',
    'DELIVERY + 21 DAYS',
    'DELIVERY + 22 DAYS',
    'DELIVERY + 23 DAYS',
    'DELIVERY + 24 DAYS',
    'DELIVERY + 25 DAYS',
    'DELIVERY + 26 DAYS',
    'DELIVERY + 27 DAYS',
    'DELIVERY + 28 DAYS',
    'DELIVERY + 29 DAYS',
    'DELIVERY + 30 DAYS',
    'DELIVERY + 31 DAYS',
    'DELIVERY + 32 DAYS',
    'DELIVERY + 33 DAYS',
    'DELIVERY + 34 DAYS',
    'DELIVERY + 35 DAYS',
    'DELIVERY + 36 DAYS',
    'DELIVERY + 37 DAYS',
    'DELIVERY + 38 DAYS',
    'DELIVERY + 39 DAYS',
    'DELIVERY + 40 DAYS',
    'DELIVERY + 41 DAYS',
    'DELIVERY + 42 DAYS',
    'DELIVERY + 43 DAYS',
    'DELIVERY + 44 DAYS',
    'DELIVERY + 45 DAYS',
    'DELIVERY + 46 DAYS',
    'DELIVERY + 47 DAYS',
    'DELIVERY + 48 DAYS',
    'DELIVERY + 49 DAYS',
    'DELIVERY + 50 DAYS',
    'DELIVERY + 51 DAYS',
    'DELIVERY + 52 DAYS',
    'DELIVERY + 53 DAYS',
    'DELIVERY + 54 DAYS',
    'DELIVERY + 55 DAYS',
    'DELIVERY + 56 DAYS',
    'DELIVERY + 57 DAYS',
    'DELIVERY + 58 DAYS',
    'DELIVERY + 59 DAYS',
    'DELIVERY + 60 DAYS',
    'DELIVERY + 61 DAYS',
    'DELIVERY + 62 DAYS',
    'DELIVERY + 63 DAYS',
    'DELIVERY + 64 DAYS',
    'DELIVERY + 65 DAYS',
    'DELIVERY + 66 DAYS',
    'DELIVERY + 67 DAYS',
    'DELIVERY + 68 DAYS',
    'DELIVERY + 69 DAYS',
    'DELIVERY + 70 DAYS',
    'DELIVERY + 71 DAYS',
    'DELIVERY + 72 DAYS',
    'DELIVERY + 73 DAYS',
    'DELIVERY + 74 DAYS',
    'DELIVERY + 75 DAYS',
    'DELIVERY + 76 DAYS',
    'DELIVERY + 77 DAYS',
    'DELIVERY + 78 DAYS',
    'DELIVERY + 79 DAYS',
    'DELIVERY + 80 DAYS',
    'DELIVERY + 81 DAYS',
    'DELIVERY + 82 DAYS',
    'DELIVERY + 83 DAYS',
    'DELIVERY + 84 DAYS',
    'DELIVERY + 85 DAYS',
    'DELIVERY + 86 DAYS',
    'DELIVERY + 87 DAYS',
    'DELIVERY + 88 DAYS',
    'DELIVERY + 89 DAYS',
    'DELIVERY + 90 DAYS'
);


CREATE TYPE buyer_payment_terms_enum AS ENUM (
    'ADVANCE',
    'PRE-ADVANCE',
    '30 DAYS FROM BILL OF EXCHANGE',
    '45 DAYS FROM BILL OF EXCHANGE',
    '60 DAYS FROM BILL OF EXCHANGE',
    '90 DAYS FROM BILL OF EXCHANGE',
    '120 DAYS FROM BILL OF EXCHANGE',
    'DISPATCH + 1 DAYS',
    'DISPATCH + 2 DAYS',
    'DISPATCH + 3 DAYS',
    'DISPATCH + 4 DAYS',
    'DISPATCH + 5 DAYS',
    'DISPATCH + 6 DAYS',
    'DISPATCH + 7 DAYS',
    'DISPATCH + 8 DAYS',
    'DISPATCH + 9 DAYS',
    'DISPATCH + 10 DAYS',
    'DISPATCH + 11 DAYS',
    'DISPATCH + 12 DAYS',
    'DISPATCH + 13 DAYS',
    'DISPATCH + 14 DAYS',
    'DISPATCH + 15 DAYS',
    'DISPATCH + 16 DAYS',
    'DISPATCH + 17 DAYS',
    'DISPATCH + 18 DAYS',
    'DISPATCH + 19 DAYS',
    'DISPATCH + 20 DAYS',
    'DISPATCH + 21 DAYS',
    'DISPATCH + 22 DAYS',
    'DISPATCH + 23 DAYS',
    'DISPATCH + 24 DAYS',
    'DISPATCH + 25 DAYS',
    'DISPATCH + 26 DAYS',
    'DISPATCH + 27 DAYS',
    'DISPATCH + 28 DAYS',
    'DISPATCH + 29 DAYS',
    'DISPATCH + 30 DAYS',
    'DISPATCH + 31 DAYS',
    'DISPATCH + 32 DAYS',
    'DISPATCH + 33 DAYS',
    'DISPATCH + 34 DAYS',
    'DISPATCH + 35 DAYS',
    'DISPATCH + 36 DAYS',
    'DISPATCH + 37 DAYS',
    'DISPATCH + 38 DAYS',
    'DISPATCH + 39 DAYS',
    'DISPATCH + 40 DAYS',
    'DISPATCH + 41 DAYS',
    'DISPATCH + 42 DAYS',
    'DISPATCH + 43 DAYS',
    'DISPATCH + 44 DAYS',
    'DISPATCH + 45 DAYS',
    'DISPATCH + 46 DAYS',
    'DISPATCH + 47 DAYS',
    'DISPATCH + 48 DAYS',
    'DISPATCH + 49 DAYS',
    'DISPATCH + 50 DAYS',
    'DISPATCH + 51 DAYS',
    'DISPATCH + 52 DAYS',
    'DISPATCH + 53 DAYS',
    'DISPATCH + 54 DAYS',
    'DISPATCH + 55 DAYS',
    'DISPATCH + 56 DAYS',
    'DISPATCH + 57 DAYS',
    'DISPATCH + 58 DAYS',
    'DISPATCH + 59 DAYS',
    'DISPATCH + 60 DAYS',
    'DISPATCH + 61 DAYS',
    'DISPATCH + 62 DAYS',
    'DISPATCH + 63 DAYS',
    'DISPATCH + 64 DAYS',
    'DISPATCH + 65 DAYS',
    'DISPATCH + 66 DAYS',
    'DISPATCH + 67 DAYS',
    'DISPATCH + 68 DAYS',
    'DISPATCH + 69 DAYS',
    'DISPATCH + 70 DAYS',
    'DISPATCH + 71 DAYS',
    'DISPATCH + 72 DAYS',
    'DISPATCH + 73 DAYS',
    'DISPATCH + 74 DAYS',
    'DISPATCH + 75 DAYS',
    'DISPATCH + 76 DAYS',
    'DISPATCH + 77 DAYS',
    'DISPATCH + 78 DAYS',
    'DISPATCH + 79 DAYS',
    'DISPATCH + 80 DAYS',
    'DISPATCH + 81 DAYS',
    'DISPATCH + 82 DAYS',
    'DISPATCH + 83 DAYS',
    'DISPATCH + 84 DAYS',
    'DISPATCH + 85 DAYS',
    'DISPATCH + 86 DAYS',
    'DISPATCH + 87 DAYS',
    'DISPATCH + 88 DAYS',
    'DISPATCH + 89 DAYS',
    'DISPATCH + 90 DAYS'
);


CREATE TYPE buyer_type_enum AS ENUM (
    'REGULAR BUYER',
    '0-1 BUYER',
    'ATTRITION(COMEBACK) BUYER'
);

CREATE TYPE freight_payment_status_enum AS ENUM (
    'UNPAID',
    'POD_UPLOADED',
    'APPLIED_FOR_PAYMENT',
    'REJECTED',
    'PAID',
    'BILL_GENERATED'
);

CREATE TYPE freight_payment_application_status_enum AS ENUM (
  'ACCEPTED',
  'REJECTED',
  'REAPPLIED_LOGISTICS',
  'REAPPLIED_TRANSPORTER',
  'BILL_GENERATED'
);

CREATE TYPE freight_bill_status_enum AS ENUM (
  'ACCEPTED',
  'UPLOADED',
  'REJECTED'
);

CREATE TYPE freight_pod_status_enum AS ENUM (
  'PENDING',
  'UPLOADED',
  'REJECTED',
  'REUPLOADED',
  'ACCEPTED',
  'HARDCOPY_PENDING',
  'HARDCOPY_RECEIVED'
);

CREATE TYPE tracking_status_enum AS ENUM (
  'Trip Completed',
  'Inactive',
  'Active',
  'Failed'
);

CREATE TYPE lr_status_enum AS ENUM (
    'ACCEPTED',
    'UPLOADED',
    'HARDCOPY_PENDING',
    'HARDCOPY_RECEIVED',
    'PENDING',
    'REUPLOADED',
    'REJECTED',
    'LR_UPLOADED',
    'LR_POD_HARDCOPY_RECEIVED',
    'LR_SOFTCOPY_APPROVED_HARDCOPY_PENDING'
);

CREATE TYPE transport_region_enum AS ENUM (
    'TM_1',
    'TM_2',
    'TM_3',
    'TM_4'
);

CREATE TYPE buyer_delivery_terms_enum AS ENUM (
    'F.O.R DELIVERED. Freight Cost is included in the Unit Price',
    'Ex-Godown'
);

CREATE TYPE group_business_type_enum AS ENUM (
    'Manufacturer',
    'Trader'
);

CREATE TYPE highest_gst_slab_enum AS ENUM (
	'0',
    '0 to 40 lakhs',
    '40 lakhs to 1.5 Cr.',
    '1.5 Cr. to 5 Cr.',
    '5 Cr. to 25 Cr.',
    '25 Cr. to 100 Cr.',
    '100 Cr. to 500 Cr.',
    '500 Cr. and above'
);

CREATE TYPE business_units_enum AS ENUM (
    'Commodity',
    'Engineering',
    'Engineering, Commodity',
    'Commodity, Engineering',
    'Commodity, Bulk',
    'Bulk',
    'PVC',
    'PVC, Commodity'
);

CREATE TYPE order_priority_enum AS ENUM (
	'LOW', 
	'HIGH'
);

CREATE TYPE waba_status_enum AS ENUM (
    'ACTIVE', 
    'INACTIVE', 
    'BLOCKED'
);

CREATE TYPE group_price_receipt_enum AS ENUM (
    'ACTIVE', 
    'INACTIVE'
);

CREATE TYPE correspondence_range_enum AS ENUM (
    'No Outreach',
    '0-30 Days',
    '31-60 Days',
    '61-90 Days',
    '90 Days Above'
);

CREATE TYPE liquidity_buyer_type_enum AS ENUM (
    'Attrition Buyer',
    'Regular Buyer',
    '0',
    '0-1 Buyer'
);

CREATE TYPE outreach_buyer_type_enum AS ENUM (
    'Attrition Buyer',
    'Regular Buyer',
    '0',
    '0-1 Buyer'
);

CREATE TYPE days_passed_label_enum AS ENUM (
    '0-30 Days',
    '31-60 Days',
    '61-90 Days',
    '91-120 Days',
    '121-180 Days',
    '181-365 Days',
    'Above 365 Days',
    '0',
    'No Order'
);

CREATE TYPE liquidity_type_enum AS ENUM (
    '6 - orderActive',
    '2 - 0-30 Days',
    '4 - 60 Days Above',
    '3 - 31-60 Days',
    '1 - INACTIVE',
    '0',
    '5 - No Outreach'
);

CREATE TYPE liquidity_buyer_type_attrition_slab_enum AS ENUM (
    '2) Regular Buyer',
    '6) 181+',
    '5) 91 to 180',
    '4) 61 to 90',
    '1) INACTIVE',
    '0',
    '3) 0-1 Buyer'
);

CREATE TYPE tag_category_enum AS ENUM (
    'Others',
    'PRODUCER',
    'COMPETITOR'
);


CREATE TABLE order_table (
    id VARCHAR(24) PRIMARY KEY,
    order_number VARCHAR(10),
    supplier_gst VARCHAR(15),
    supplier_name VARCHAR(100),
    buyer_gst VARCHAR(15),
    buyer_name VARCHAR(100),
    godown_id VARCHAR(24),
    godown_name VARCHAR(30),
    quantity DECIMAL(6, 2),
    single_quantity DECIMAL(6, 2),
    product_id VARCHAR(24), 
    product_name VARCHAR(50), 
    delivery_location_id VARCHAR(24), 
    delivery_location_name VARCHAR(30), 
    dispatch_date DATE, 
    due_date DATE, 
    buyer_due_date DATE, 
    expected_delivery_date DATE, 
    actual_delivery_date DATE, 
    supplier_due_date DATE,
    order_status ORDER_STATUS_ENUM  , 
    buyer_payment_terms buyer_payment_terms_enum, 
    delivery_address TEXT,
    transporter_address TEXT,
    is_eway_bill_created BOOLEAN, 
    buyer_po_number VARCHAR(50), 
    delivery_buyer_payment_terms delivery_buyer_payment_terms_enum,
    eway_bill_expiry_date DATE, 
    delay_score INTEGER DEFAULT 0,
    logistic_delay_score INTEGER DEFAULT 0 ,
    lr_number VARCHAR(30),
    driver_mobile_number VARCHAR(10),
    transporter_name VARCHAR(100),
    freight_cost INTEGER,
    last_freight_cost text, 
    freight_payment_status freight_payment_status_enum,
    system_freight_cost INTEGER,
    max_possible_freight_cost INTEGER,
    transit_distance_in_km INTEGER,
    supplier_credit_note_value DECIMAL,
    buyer_price DECIMAL,
    buyer_credit_note_value DECIMAL,
    invoice_number TEXT,
    supplier_price DECIMAL,
    bill_number TEXT,
    purchase_order_number VARCHAR(30),
    margin INTEGER,
    total_amount DECIMAL,
    utr_number TEXT,
    is_payment_made_to_supplier BOOLEAN,
    freight_payment_application_status freight_payment_application_status_enum,
    freight_bill_status freight_bill_status_enum,
    freight_pod_status freight_pod_status_enum,
    rejection_reason TEXT,
    reapply_reason TEXT,
    applied_for_freight_payment_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    invoice_status TEXT,
    invoice_value TEXT,
    invoice_due_days INTEGER,
    invoice_balance INTEGER,
    overdue_amount INTEGER,
    adjusted_system_distance INTEGER,
    tracking_status tracking_status_enum,
    pod_reason TEXT,
    bill_reason TEXT,
    lr_reason TEXT,
    pod_remark TEXT,
    bill_remark TEXT,
    lr_remark TEXT,
    lr_status lr_status_enum,
    driver_coordinator_name VARCHAR(50),
    transport_region transport_region_enum,
    group_state_owner VARCHAR(100),
    buyer_account_manager VARCHAR(50),
    supplier_account_manager VARCHAR(50),
    is_return BOOLEAN,
    return_order_created_from VARCHAR(10),
    buyer_poc VARCHAR(10),
    buyer_poc_name VARCHAR(100),
    supplier_poc VARCHAR(10),
    supplier_poc_name VARCHAR(100),
    tags TEXT,
    freight_quotes_count INTEGER,
    loading_address TEXT,
    vehicle_number VARCHAR(10),
    delivered_to_with_parent VARCHAR(100),
    godown_with_parent VARCHAR(100),
    netback DECIMAL,
    buyer_group_id VARCHAR(24),
    supplier_group_id VARCHAR(24),
    order_request_id VARCHAR(24),
    logistic_team_last_edit_by VARCHAR(50),
    buyer_team_last_edit_by VARCHAR(50),
    supplier_team_last_edit_by VARCHAR(50),
    general_last_edit_by VARCHAR(50),
    driver_last_edit_by VARCHAR(50),
    logistic_team_remarks_concatenated TEXT,
    buyer_team_remarks_concatenated TEXT,
    supplier_team_remarks_concatenated TEXT,
    general_remarks_concatenated TEXT,
    driver_remarks_concatenated TEXT,
    netback_sf DECIMAL,
    buyer_delivery_terms buyer_delivery_terms_enum,
    state_abbreviation CHAR(2),
    load INTEGER,
    freight_offset DECIMAL,
    max_dispatch_date DATE,
    min_dispatch_date DATE,
    last_order_days_ago INTEGER,
    group_name VARCHAR(100),
    group_limit DECIMAL(15,2),
    group_blacklisted BOOLEAN,
    group_business_type group_business_type_enum,
    group_credit_interest DECIMAL,
    group_credit_limit DECIMAL(15,2),
    group_credit_tenor VARCHAR,
    group_markup_value DECIMAL,
    group_margin DECIMAL,
    group_remarks TEXT,
    group_unfulfilled_order_count INTEGER,
    group_waba_price_enabled BOOLEAN,
    highest_gst_slab highest_gst_slab_enum,
    orders_count INTEGER,
    account_manager VARCHAR(50),
    business_units business_units_enum,
    group_payment_category VARCHAR(100),
    group_trade_reference_values TEXT,
    is_deleted BOOLEAN,
    application_type VARCHAR(50),
    highest_pan VARCHAR(10),
    group_primary_location VARCHAR(50),
    last_ordered_date DATE,
    coa_required BOOLEAN,
    last_buyer_app_usage_days_ago INTEGER,
    payment_reminders INTEGER,
    mobile_app_enabled BOOLEAN,
    supplier_payment_terms VARCHAR(100),
    order_priority order_priority_enum,
    listings_deactivation_timer INTEGER,
    repeat_reminders_after INTEGER,
    special_offer_enabled BOOLEAN,
    supplier_orders_count INTEGER,
    group_available_limit DECIMAL,
    sub_application_types VARCHAR(100),
    pfp_status VARCHAR(50),
    group_creation_date DATE,
    regions VARCHAR(100),
    group_level_grade_groups TEXT,
    group_level_tags TEXT,
    group_hsns TEXT,
    active_locations TEXT,
    inactive_locations TEXT,
    waba_status waba_status_enum,
    group_price_receipt group_price_receipt_enum,
    decision_maker_mapped BOOLEAN,
    buyer_decision_maker VARCHAR(10),
    dgft_import DECIMAL,
    dgft_import_mapped DECIMAL,
    created_by VARCHAR(50), 
    last_correspondence_date DATE, 
    last_correspondence_days_ago INTEGER, 
    correspondence_range correspondence_range_enum,
    first_note TEXT, 
    second_note TEXT, 
    credit_order DECIMAL, 
    lifetime_volume DECIMAL, 
    liquidity_buyer_type liquidity_buyer_type_enum, 
    outreach_buyer_type outreach_buyer_type_enum, 
    days_passed INTEGER,  
    days_passed_label days_passed_label_enum, 
    opportunity TEXT, 
    volume_supplied DECIMAL, 
    is_supplier_activated BOOLEAN, 
    liquidity_type liquidity_type_enum, 
    liquidity_buyer_type_attrition_slab liquidity_buyer_type_attrition_slab_enum, 
    finance_update_count INTEGER, 
    email_id_count INTEGER, 
    is_parent_child BOOLEAN,
    number_of_ceo INTEGER,
    number_of_coo INTEGER,
    number_of_dm_owner INTEGER,
    number_of_dm_purchase_manager INTEGER,
    number_of_finance INTEGER,
    number_of_gst INTEGER,
    number_of_logistics INTEGER,
    number_of_md INTEGER,
    number_of_owner INTEGER,
    number_of_purchase_head INTEGER,
    number_of_purchase_manager INTEGER,
    number_of_sales_manager INTEGER,
    number_of_undefined_role INTEGER,
    tam VARCHAR(100),
    tag_category tag_category_enum, 
    buyer_decision_maker_person VARCHAR(100), 
    buyer_decision_maker_email VARCHAR(100), 
    ordered_grade_number VARCHAR(100), 
    ordered_grade_group VARCHAR(100), 
    pan VARCHAR(10), 
    total_mapped_qty DECIMAL,
    last_6mnt_lowest_not_adjusted DECIMAL,
    last_6mnt_lowest_not_adjusted_order_no VARCHAR(10),
    last_6mnt_lowest_adjusted DECIMAL,
    last_6mnt_lowest_adjusted_order_no VARCHAR(10),
    godown_parent_name VARCHAR(30),
    destination_parent_name VARCHAR(100),
    app_live_price DECIMAL, 
    l1_supplier_name VARCHAR(100),
    l1_netback DECIMAL,
    l2_supplier_name VARCHAR(100),
    l2_netback DECIMAL,
    l3_supplier_name VARCHAR(100),
    l3_netback DECIMAL,
    freight_quotes_l1 DECIMAL(10,2), 
    freight_quotes_l2 DECIMAL(10,2),
    freight_quotes_l3 DECIMAL(10,2),
    change_time TIMESTAMP,
    probable_supplier_group_id TEXT,
    probable_supplier_group_name TEXT,
    is_available boolean,
    buyer_type buyer_type_enum,
    company_gst VARCHAR(15) DEFAULT '27ABACS7251D1ZH' ,
    order_created_by VARCHAR(50)
);

CREATE INDEX idx_order_number ON order_table(order_number);
CREATE INDEX idx_supplier_gst ON order_table(supplier_gst);
CREATE INDEX idx_buyer_gst ON order_table(buyer_gst);
CREATE INDEX idx_product_id ON order_table(product_id);
CREATE INDEX idx_status ON order_table(order_status);
CREATE INDEX idx_dispatch_date ON order_table(dispatch_date);
CREATE INDEX idx_due_date ON order_table(due_date);
CREATE INDEX idx_created_at ON order_table(created_at);

-- gin indexes with pgtgrm 
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_gin_supplier_name ON order_table USING gin (supplier_name gin_trgm_ops);
CREATE INDEX idx_gin_buyer_name ON order_table USING gin (buyer_name gin_trgm_ops);
CREATE INDEX idx_gin_godown_name ON order_table USING gin (godown_name gin_trgm_ops);
CREATE INDEX idx_gin_product_name ON order_table USING gin (product_name gin_trgm_ops);
CREATE INDEX idx_gin_delivery_location_name ON order_table USING gin (delivery_location_name gin_trgm_ops);
CREATE INDEX idx_gin_delivery_address ON order_table USING gin (delivery_address gin_trgm_ops);
CREATE INDEX idx_gin_transport_address ON order_table USING gin (transporter_address gin_trgm_ops);
CREATE INDEX idx_gin_buyer_po_number ON order_table USING gin (buyer_po_number gin_trgm_ops);
CREATE INDEX idx_gin_transporter_name ON order_table USING gin (transporter_name gin_trgm_ops);
CREATE INDEX idx_gin_invoice_number ON order_table USING gin (invoice_number gin_trgm_ops);
CREATE INDEX idx_gin_bill_number ON order_table USING gin (bill_number gin_trgm_ops);
CREATE INDEX idx_gin_purchase_order_number ON order_table USING gin (purchase_order_number gin_trgm_ops);
CREATE INDEX idx_gin_rejection_reason ON order_table USING gin (rejection_reason gin_trgm_ops);
CREATE INDEX idx_gin_reapply_reason ON order_table USING gin (reapply_reason gin_trgm_ops);
CREATE INDEX idx_gin_pod_reason ON order_table USING gin (pod_reason gin_trgm_ops);
CREATE INDEX idx_gin_bill_reason ON order_table USING gin (bill_reason gin_trgm_ops);
CREATE INDEX idx_gin_lr_reason ON order_table USING gin (lr_reason gin_trgm_ops);
CREATE INDEX idx_gin_pod_remark ON order_table USING gin (pod_remark gin_trgm_ops);
CREATE INDEX idx_gin_bill_remark ON order_table USING gin (bill_remark gin_trgm_ops);
CREATE INDEX idx_gin_lr_remark ON order_table USING gin (lr_remark gin_trgm_ops);
CREATE INDEX idx_gin_driver_coordinator_name ON order_table USING gin (driver_coordinator_name gin_trgm_ops);
CREATE INDEX idx_gin_group_state_owner ON order_table USING gin (group_state_owner gin_trgm_ops);
CREATE INDEX idx_gin_buyer_account_manager ON order_table USING gin (buyer_account_manager gin_trgm_ops);
CREATE INDEX idx_gin_supplier_account_manager ON order_table USING gin (supplier_account_manager gin_trgm_ops);
CREATE INDEX idx_gin_buyer_poc_name ON order_table USING gin (buyer_poc_name gin_trgm_ops);
CREATE INDEX idx_gin_supplier_poc_name ON order_table USING gin (supplier_poc_name gin_trgm_ops);
CREATE INDEX idx_gin_tags ON order_table USING gin (tags gin_trgm_ops);
CREATE INDEX idx_gin_loading_address ON order_table USING gin (loading_address gin_trgm_ops);
CREATE INDEX idx_gin_delivered_to_with_parent ON order_table USING gin (delivered_to_with_parent gin_trgm_ops);
CREATE INDEX idx_gin_godown_with_parent ON order_table USING gin (godown_with_parent gin_trgm_ops);
CREATE INDEX idx_gin_logistic_team_remarks_concatenated ON order_table USING gin (logistic_team_remarks_concatenated gin_trgm_ops);
CREATE INDEX idx_gin_buyer_team_remarks_concatenated ON order_table USING gin (buyer_team_remarks_concatenated gin_trgm_ops);
CREATE INDEX idx_gin_supplier_team_remarks_concatenated ON order_table USING gin (supplier_team_remarks_concatenated gin_trgm_ops);
CREATE INDEX idx_gin_general_remarks_concatenated ON order_table USING gin (general_remarks_concatenated gin_trgm_ops);
CREATE INDEX idx_gin_driver_remarks_concatenated ON order_table USING gin (driver_remarks_concatenated gin_trgm_ops);
CREATE INDEX idx_gin_group_name ON order_table USING gin (group_name gin_trgm_ops);
CREATE INDEX idx_gin_group_credit_tenor ON order_table USING gin (group_credit_tenor gin_trgm_ops);
CREATE INDEX idx_gin_group_remarks ON order_table USING gin (group_remarks gin_trgm_ops);
CREATE INDEX idx_gin_account_manager ON order_table USING gin (account_manager gin_trgm_ops);
CREATE INDEX idx_gin_group_payment_category ON order_table USING gin (group_payment_category gin_trgm_ops);
CREATE INDEX idx_gin_group_trade_reference_values ON order_table USING gin (group_trade_reference_values gin_trgm_ops);
CREATE INDEX idx_gin_application_type ON order_table USING gin (application_type gin_trgm_ops);
CREATE INDEX idx_gin_group_primary_location ON order_table USING gin (group_primary_location gin_trgm_ops);
CREATE INDEX idx_gin_supplier_payment_terms ON order_table USING gin (supplier_payment_terms gin_trgm_ops);
CREATE INDEX idx_gin_pfp_status ON order_table USING gin (pfp_status gin_trgm_ops);
CREATE INDEX idx_gin_regions ON order_table USING gin (regions gin_trgm_ops);
CREATE INDEX idx_gin_group_level_grade_groups ON order_table USING gin (group_level_grade_groups gin_trgm_ops);
CREATE INDEX idx_gin_group_level_tags ON order_table USING gin (group_level_tags gin_trgm_ops);
CREATE INDEX idx_gin_group_hsns ON order_table USING gin (group_hsns gin_trgm_ops);
CREATE INDEX idx_gin_active_locations ON order_table USING gin (active_locations gin_trgm_ops);
CREATE INDEX idx_gin_inactive_locations ON order_table USING gin (inactive_locations gin_trgm_ops);
CREATE INDEX idx_gin_buyer_decision_maker ON order_table USING gin (buyer_decision_maker gin_trgm_ops);
CREATE INDEX idx_gin_created_by ON order_table USING gin (created_by gin_trgm_ops);
CREATE INDEX idx_gin_first_note ON order_table USING gin (first_note gin_trgm_ops);
CREATE INDEX idx_gin_second_note ON order_table USING gin (second_note gin_trgm_ops);
CREATE INDEX idx_gin_opportunity ON order_table USING gin (opportunity gin_trgm_ops);
CREATE INDEX idx_gin_tam ON order_table USING gin (tam gin_trgm_ops);
CREATE INDEX idx_gin_buyer_decision_maker_person ON order_table USING gin (buyer_decision_maker_person gin_trgm_ops);
CREATE INDEX idx_gin_buyer_decision_maker_email ON order_table USING gin (buyer_decision_maker_email gin_trgm_ops);
CREATE INDEX idx_gin_ordered_grade_number ON order_table USING gin (ordered_grade_number gin_trgm_ops);
CREATE INDEX idx_gin_ordered_grade_group ON order_table USING gin (ordered_grade_group gin_trgm_ops);
CREATE INDEX idx_gin_godown_parent_name ON order_table USING gin (godown_parent_name gin_trgm_ops);
CREATE INDEX idx_gin_destination_parent_name ON order_table USING gin (destination_parent_name gin_trgm_ops);
CREATE INDEX idx_gin_l1_supplier_name ON order_table USING gin (l1_supplier_name gin_trgm_ops);
CREATE INDEX idx_gin_l2_supplier_name ON order_table USING gin (l2_supplier_name gin_trgm_ops);
CREATE INDEX idx_gin_l3_supplier_name ON order_table USING gin (l3_supplier_name gin_trgm_ops);
CREATE INDEX idx_gin_probable_supplier_group_name ON order_table USING gin (probable_supplier_group_name gin_trgm_ops);
CREATE INDEX idx_gin_order_created_by ON order_table USING gin (order_created_by gin_trgm_ops);
CREATE INDEX idx_gin_utr_number ON order_table USING gin(utr_number gin_trgm_ops );
