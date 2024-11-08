
CREATE TABLE order_table (
    id VARCHAR(24) PRIMARY KEY,
    order_number VARCHAR(10), -- unique identifier for each order
    supplier_gst VARCHAR(15), -- GST number of the supplier
    supplier_name TEXT, -- name of the supplier entity
    buyer_gst VARCHAR(15), -- buyer GST number
    buyer_name TEXT, -- name of the buyer
    godown_id VARCHAR(24), -- location ID of the godown
    godown_name VARCHAR(30), -- location name of the godown
    quantity DECIMAL(6, 2), -- combined quantity for the order
    single_quantity DECIMAL(6, 2), -- actual quantity of the order
    product_id VARCHAR(24), -- unique ID of the product
    product_name TEXT, -- official grade name that was ordered
    delivery_location_id VARCHAR(24), -- location ID of the delivery location
    delivery_location_name VARCHAR(30), -- location name of the delivery location
    dispatch_date DATE, -- date of dispatch of the order
    due_date DATE, -- due date for the order
    buyer_due_date DATE, -- due date of the order for the buyer
    expected_delivery_date DATE, -- expected date of delivery by internal calculations
    actual_delivery_date DATE, -- actual date on which order was delivered
    supplier_due_date DATE, -- due date for the supplier for payment
    order_status VARCHAR(30) CHECK (order_status IN (
        'ENQUIRY SCHEDULED',
        'ENQUIRY SENT',
        'TRANSPORTER CONFIRMED',
        'VEHICLE CONFIRMED',
        'VEHICLE REACHED',
        'VEHICLE REACHED AT GODOWN',
        'LOADING IN PROGRESS',
        'VEHICLE LOADED',
        'SUPPLIER INVOICE RECEIVED',
        'INVOICE GENERATED',
        'VEHICLE DISPATCHED',
        'VEHICLE REACHED AT DESTINATION',
        'VEHICLE DELIVERED',
        'GENERATED',
        'NOT GENERATED',
        'UNPAID',
        'APPLIED FOR PAYMENT',
        'BILL GENERATED',
        'REJECTED',
        'PAID',
        'HOLD',
        'PENDING',
        'PENDING (LC)',
        'PENDING (TA,LIMIT)',
        'PENDING (TA,ADV)',
        'PENDING (LA)',
        'PENDING (TA)',
        'PENDING (TA,LA)',
        'PENDING (LIMIT)',
        'PENDING (LA,ADV)',
        'PENDING (ADV)'
    )), -- status of order
    buyer_payment_terms VARCHAR(30) CHECK (buyer_payment_terms IN (
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
    )), -- buyer payment terms based on dispatch
    delivery_address TEXT, -- complete delivery address for the order
    transporter_address TEXT, -- address shared with the transporter vendor for delivery
    is_eway_bill_created BOOLEAN, -- is eway bill created or not
    buyer_po_number TEXT, -- buyer PO number
    delivery_buyer_payment_terms VARCHAR(30) CHECK (delivery_buyer_payment_terms IN (
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
    )), -- buyer payment terms based on delivery
    eway_bill_expiry_date DATE, -- date on which eway bill will expire
    delay_score INTEGER DEFAULT 0, -- delay score, no delay means 0 delay days
    logistic_delay_score INTEGER DEFAULT 0, -- logistic delay score, can be minimum of -1
    lr_number VARCHAR(30), -- LR number of the transporter
    driver_mobile_number VARCHAR(10), -- mobile number of the driver
    transporter_name TEXT, -- name of the transporter vendor company
    freight_cost INTEGER, -- actual freight cost of the order
    last_freight_cost TEXT, -- freight cost of the last order placed between the same godown and delivery location
    freight_payment_status VARCHAR(30) CHECK (freight_payment_status IN (
        'UNPAID',
        'POD_UPLOADED',
        'APPLIED_FOR_PAYMENT',
        'REJECTED',
        'PAID',
        'BILL_GENERATED',
        'BILL_UPLOADED'
    )), -- payment status for the freight
    system_freight_cost INTEGER, -- freight cost generated by system automation logic
    max_possible_freight_cost INTEGER, -- upper threshold for freight cost for system generated cost
    transit_distance_in_km INTEGER, -- transit distance between godown and delivery location
    supplier_credit_note_value DECIMAL, -- credit note offered to supplier
    buyer_price DECIMAL, -- per kg price of the order confirmed by buyer
    buyer_credit_note_value DECIMAL, -- credit note offered to buyer
    invoice_number TEXT, -- unique identifier for invoices in the system
    supplier_price DECIMAL, -- per kg price of order confirmed by the supplier
    bill_number TEXT, -- bill ID generated for supplier
    purchase_order_number VARCHAR(30), -- purchase order number for the buyer
    margin INTEGER, -- internal profit margin in the order
    total_amount DECIMAL, -- total selling cost of the order for the buyer
    utr_number TEXT, -- transaction ID of payment made by buyer for order
    is_payment_made_to_supplier BOOLEAN, -- is payment made to supplier
    freight_payment_application_status VARCHAR(30) CHECK (freight_payment_application_status IN (
        'ACCEPTED',
        'REJECTED',
        'REAPPLIED_LOGISTICS',
        'REAPPLIED_TRANSPORTER',
        'BILL_GENERATED'
    )), -- status of freight payment application
    freight_bill_status VARCHAR(30) CHECK (freight_bill_status IN (
        'ACCEPTED',
        'UPLOADED',
        'REJECTED',
        'REUPLOADED'
    )), -- status of the freight bill
    freight_pod_status VARCHAR(30) CHECK (freight_pod_status IN (
        'PENDING',
        'UPLOADED',
        'REJECTED',
        'REUPLOADED',
        'ACCEPTED',
        'HARDCOPY_PENDING',
        'HARDCOPY_RECEIVED'
    )), -- status of proof of delivery for freight
    rejection_reason TEXT, -- reason for rejection
    reapply_reason TEXT, -- reason to reapply after rejection
    applied_for_freight_payment_at TIMESTAMP, -- timestamp when freight payment application was made
    created_at TIMESTAMP, -- order creation timestamp
    updated_at TIMESTAMP, -- order update timestamp
    invoice_status TEXT, -- status of invoice, can be paid or unpaid or void
    invoice_value TEXT, -- total cost on the invoices separated by comma
    invoice_due_days INTEGER, -- number of days due for the invoice
    invoice_balance TEXT, -- pending amount due against the buyer's each invoices separated by commas
    overdue_amount TEXT, -- overdue amount of the buyer invoices
    adjusted_system_distance INTEGER, -- system distance in kms later adjusted (DO NOT USE IT)
    tracking_status VARCHAR(30) CHECK (tracking_status IN (
        'Trip Completed',
        'Inactive',
        'Active',
        'Failed'
    )), -- tracking status from cargo exchange
    pod_reason TEXT, -- reason for proof of delivery
    bill_reason TEXT, -- reason for the bill
    lr_reason TEXT, -- reason for the LR
    pod_remark TEXT, -- remarks for proof of delivery
    bill_remark TEXT, -- remarks for the bill
    lr_remark TEXT, -- remarks for the LR
    lr_status VARCHAR(40) CHECK (lr_status IN (
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
    )), -- status of LR
    driver_coordinator_name TEXT, -- name of the driver coordinator
    transport_region VARCHAR(4) CHECK (transport_region IN (
        'TM_1',
        'TM_2',
        'TM_3',
        'TM_4'
    )), -- transporter region
    group_state_owner TEXT, -- group state owner
    buyer_account_manager TEXT, -- buyer account manager
    supplier_account_manager TEXT, -- supplier account manager
    is_return BOOLEAN, -- is this a returned order or not
    return_order_created_from VARCHAR(10), -- original order from which this return order is created
    buyer_poc VARCHAR(10), -- phone number of point of contact at buyer side
    buyer_poc_name TEXT, -- name of point of contact at buyer side
    supplier_poc VARCHAR(10), -- phone number of point of contact at supplier side
    supplier_poc_name TEXT, -- name of point of contact at supplier side
    tags TEXT, -- tags concatenated via comma-separated string
    freight_quotes_count INTEGER, -- number of freight quotes received
    loading_address TEXT, -- loading address for the order
    vehicle_number VARCHAR(10), -- vehicle number for transportation
    delivered_to_with_parent TEXT, -- concatenated string of the delivery location with its parent location
    godown_with_parent TEXT, -- concatenated string of the godown location with its parent location
    netback DECIMAL, -- netback received on every order, can be positive or negative
    buyer_group_id VARCHAR(24), -- group ID of the buyer entity group
    supplier_group_id VARCHAR(24), -- group ID of the supplier entity group
    order_request_id VARCHAR(24), -- order request ID from which this order was originally created
    logistic_team_last_edit_by TEXT, -- email of last person to update the logistic remarks
    buyer_team_last_edit_by VARCHAR(50), -- email of last person to update the buyer team remarks
    supplier_team_last_edit_by VARCHAR(50), -- email of last person to update the supplier team remarks
    general_last_edit_by VARCHAR(50), -- email of last person to update the general remarks
    driver_last_edit_by VARCHAR(50), -- email of last person to edit driver team remarks
    logistic_team_remarks_concatenated text, -- logistic team remarks concatenated with last time it was edited
    buyer_team_remarks_concatenated TEXT, -- buyer team remarks concatenated with last time it was edited
    supplier_team_remarks_concatenated TEXT, -- supplier team remarks concatenated with last time it was edited
    general_remarks_concatenated TEXT, -- general team remarks concatenated with last time it was edited
    driver_remarks_concatenated TEXT, -- driver team remarks concatenated with last time it was edited
    netback_sf DECIMAL, -- netback based on system freight
    buyer_delivery_terms VARCHAR(60) CHECK (buyer_delivery_terms IN (
        'F.O.R DELIVERED. Freight Cost is included in the Unit Price',
        'Ex-Godown'
    )), -- delivery terms for buyer
    state_abbreviation CHAR(2), -- state abbreviation
    load_amount INTEGER, -- load quantity
    freight_offset DECIMAL, 
    max_dispatch_date DATE, -- last order dispatch date for group entity
    min_dispatch_date DATE, -- first order dispatch date for group entity
    last_order_days_ago INTEGER, -- days since the last order was placed
    group_name TEXT, -- buyer group name 
    group_limit DECIMAL(15,2), -- limit of group for purchasing
    group_blacklisted BOOLEAN, -- is the buyer group blacklisted or not 
    group_business_type VARCHAR(15) CHECK (group_business_type IN (
        'Manufacturer',
        'Trader'
    )), -- business type of the buyer group
    group_credit_interest DECIMAL, -- interest in percentage offered to each buyer group
    group_credit_limit DECIMAL(15,2), -- credit limit of the buyer group
    group_credit_tenor VARCHAR(30) CHECK (group_credit_tenor IN (
        '0',
        'DELIVERY + 1 DAYS', 'DELIVERY + 2 DAYS', 'DELIVERY + 3 DAYS', 'DELIVERY + 4 DAYS', 'DELIVERY + 5 DAYS',
        'DELIVERY + 6 DAYS', 'DELIVERY + 7 DAYS', 'DELIVERY + 8 DAYS', 'DELIVERY + 9 DAYS', 'DELIVERY + 10 DAYS',
        'DELIVERY + 11 DAYS', 'DELIVERY + 12 DAYS', 'DELIVERY + 13 DAYS', 'DELIVERY + 14 DAYS', 'DELIVERY + 15 DAYS',
        'DELIVERY + 16 DAYS', 'DELIVERY + 17 DAYS', 'DELIVERY + 18 DAYS', 'DELIVERY + 19 DAYS', 'DELIVERY + 20 DAYS',
        'DELIVERY + 21 DAYS', 'DELIVERY + 22 DAYS', 'DELIVERY + 23 DAYS', 'DELIVERY + 24 DAYS', 'DELIVERY + 25 DAYS',
        'DELIVERY + 26 DAYS', 'DELIVERY + 27 DAYS', 'DELIVERY + 28 DAYS', 'DELIVERY + 29 DAYS', 'DELIVERY + 30 DAYS',
        'DELIVERY + 31 DAYS', 'DELIVERY + 32 DAYS', 'DELIVERY + 33 DAYS', 'DELIVERY + 34 DAYS', 'DELIVERY + 35 DAYS',
        'DELIVERY + 36 DAYS', 'DELIVERY + 37 DAYS', 'DELIVERY + 38 DAYS', 'DELIVERY + 39 DAYS', 'DELIVERY + 40 DAYS',
        'DELIVERY + 41 DAYS', 'DELIVERY + 42 DAYS', 'DELIVERY + 43 DAYS', 'DELIVERY + 44 DAYS', 'DELIVERY + 45 DAYS',
        'DELIVERY + 46 DAYS', 'DELIVERY + 47 DAYS', 'DELIVERY + 48 DAYS', 'DELIVERY + 49 DAYS', 'DELIVERY + 50 DAYS',
        'DELIVERY + 51 DAYS', 'DELIVERY + 52 DAYS', 'DELIVERY + 53 DAYS', 'DELIVERY + 54 DAYS', 'DELIVERY + 55 DAYS',
        'DELIVERY + 56 DAYS', 'DELIVERY + 57 DAYS', 'DELIVERY + 58 DAYS', 'DELIVERY + 59 DAYS', 'DELIVERY + 60 DAYS',
        'DELIVERY + 61 DAYS', 'DELIVERY + 62 DAYS', 'DELIVERY + 63 DAYS', 'DELIVERY + 64 DAYS', 'DELIVERY + 65 DAYS',
        'DELIVERY + 66 DAYS', 'DELIVERY + 67 DAYS', 'DELIVERY + 68 DAYS', 'DELIVERY + 69 DAYS', 'DELIVERY + 70 DAYS',
        'DELIVERY + 71 DAYS', 'DELIVERY + 72 DAYS', 'DELIVERY + 73 DAYS', 'DELIVERY + 74 DAYS', 'DELIVERY + 75 DAYS',
        'DELIVERY + 76 DAYS', 'DELIVERY + 77 DAYS', 'DELIVERY + 78 DAYS', 'DELIVERY + 79 DAYS', 'DELIVERY + 80 DAYS',
        'DELIVERY + 81 DAYS', 'DELIVERY + 82 DAYS', 'DELIVERY + 83 DAYS', 'DELIVERY + 84 DAYS', 'DELIVERY + 85 DAYS',
        'DELIVERY + 86 DAYS', 'DELIVERY + 87 DAYS', 'DELIVERY + 88 DAYS', 'DELIVERY + 89 DAYS', 'DELIVERY + 90 DAYS'
    )), -- it usually is 0 or of format delivery + X days
    group_markup_value DECIMAL, 
    group_margin DECIMAL, -- margin of money associated with the buyer group
    group_remarks TEXT, -- remarks for the buyer group
    group_unfulfilled_order_count INTEGER, -- orders for buyer group that were unfulfilled in the past
    group_waba_price_enabled BOOLEAN, -- whether WABA price is enabled or not for buyer group
    highest_gst_slab VARCHAR(20) CHECK (highest_gst_slab IN (
        '0',
        '0 to 40 lakhs',
        '40 lakhs to 1.5 Cr.',
        '1.5 Cr. to 5 Cr.',
        '5 Cr. to 25 Cr.',
        '25 Cr. to 100 Cr.',
        '100 Cr. to 500 Cr.',
        '500 Cr. and above'
    )), -- this is range for e.g., 5 Cr. to 25 Cr.
    orders_count INTEGER, -- count of orders for this particular buyer in the past
    account_manager VARCHAR(50), -- account manager of the buyer 
    business_units VARCHAR(25) CHECK (business_units IN (
        'Commodity',
        'Engineering',
        'Engineering, Commodity',
        'Commodity, Engineering',
        'Commodity, Bulk',
        'Bulk',
        'PVC',
        'PVC, Commodity'
    )), -- business unit refers to the commodity or engineering
    group_payment_category TEXT, -- default payment category of the buyer group
    group_trade_reference_values TEXT, -- buyer group trade references comma separated
    is_deleted BOOLEAN, -- is the buyer group deleted or not 
    application_type VARCHAR(50), -- application type of the grade ordered in the order
    highest_pan VARCHAR(10), -- PAN number with highest GST limit for buyer
    group_primary_location VARCHAR(50), -- name of the primary location for buyer group
    last_ordered_date DATE, -- date when the last order was placed by this group
    coa_required BOOLEAN, -- is COA certificate required or not for the buyer
    last_buyer_app_usage_days_ago INTEGER, -- the number of days since the buyer last used the app
    payment_reminders INTEGER,
    mobile_app_enabled BOOLEAN, -- mobile app enabled for the buyer or not
    supplier_payment_terms TEXT, -- payment terms selected by the supplier
    order_priority VARCHAR(10) CHECK (order_priority IN (
        'LOW', 
        'HIGH'
    )), -- priority of the order
    listings_deactivation_timer INTEGER, -- deactivation timer for the supplier selected for the order
    repeat_reminders_after INTEGER, -- number of hours after which we should send a reminder to the supplier for updating their offers
    special_offer_enabled BOOLEAN, -- is special offer enabled for the supplier of this order
    supplier_orders_count INTEGER, -- number of orders that this supplier has delivered in the past
    group_available_limit DECIMAL, -- available limit of money with the buyer group
    sub_application_types TEXT, -- sub application type of the grade ordered in the order separated by /
    pfp_status VARCHAR(50), -- custom field
    group_creation_date DATE, -- creation date of the buyer group
    regions TEXT, -- region from which the buyer group is associated
    group_level_grade_groups TEXT, -- grade groups associated with buyers comma separated
    group_level_tags TEXT, -- buyer group tags comma separated 
    group_hsns TEXT, -- buyer group HSN codes separated by comma
    active_locations TEXT, -- comma separated locations the buyer is active in 
    inactive_locations TEXT, -- comma separated locations that the buyer is inactive in 
    waba_status VARCHAR(10) CHECK (waba_status IN (
        'ACTIVE', 
        'INACTIVE', 
        'BLOCKED'
    )), -- WABA status of the buyer for this order
    group_price_receipt VARCHAR(10) CHECK (group_price_receipt IN (
        'ACTIVE', 
        'INACTIVE'
    )), -- buyer group price receipt is either active or inactive
    decision_maker_mapped BOOLEAN, -- is the decision maker for the order mapped or not 
    buyer_decision_maker VARCHAR(10), -- phone number of the person who makes decisions for the order from buyer side
    dgft_import DECIMAL, -- total count of DGFT imports for the buyer
    dgft_import_mapped DECIMAL, -- count of DGFT imports mapped for the buyer out of total imports
    created_by VARCHAR(50), -- email id of the person who created the order
    last_correspondence_date DATE, -- date of last correspondence 
    last_correspondence_days_ago INTEGER, -- days since last correspondence
    correspondence_range VARCHAR(15) CHECK (correspondence_range IN (
        'No Outreach',
        '0-30 Days',
        '31-60 Days',
        '61-90 Days',
        '90 Days Above'
    )), -- range for correspondence
    first_note TEXT, -- first note for the buyer 
    second_note TEXT, -- second note for the buyer 
    credit_order DECIMAL, -- percentage of order placed on credit by group entity
    lifetime_volume DECIMAL, -- lifetime volume of the buyer group associated with this order
    liquidity_buyer_type VARCHAR(15) CHECK (liquidity_buyer_type IN (
        'Attrition Buyer',
        'Regular Buyer',
        '0',
        '0-1 Buyer'
    )), -- type of buyer either attrition buyer or regular buyer
    outreach_buyer_type VARCHAR(15) CHECK (outreach_buyer_type IN (
        'Attrition Buyer',
        'Regular Buyer',
        '0',
        '0-1 Buyer'
    )), -- type of buyer either attrition buyer or regular buyer
    days_passed INTEGER,  -- how many days have passed since this order 
    days_passed_label VARCHAR(15) CHECK (days_passed_label IN (
        '0-30 Days',
        '31-60 Days',
        '61-90 Days',
        '91-120 Days',
        '121-180 Days',
        '181-365 Days',
        'Above 365 Days',
        '0',
        'No Order'
    )), -- label given to days passed 
    opportunity TEXT, -- type of business opportunity with the buyer 
    volume_supplied DECIMAL, -- total volume supplied by the supplier 
    is_supplier_activated BOOLEAN, -- is supplier activated or not 
    liquidity_type VARCHAR(20) CHECK (liquidity_type IN (
        '6 - orderActive',
        '2 - 0-30 Days',
        '4 - 60 Days Above',
        '3 - 31-60 Days',
        '1 - INACTIVE',
        '0',
        '5 - No Outreach'
    )), -- type of liquidity that the buyer has 
    liquidity_buyer_type_attrition_slab VARCHAR(20) CHECK (liquidity_buyer_type_attrition_slab IN (
        '2) Regular Buyer',
        '6) 181+',
        '5) 91 to 180',
        '4) 61 to 90',
        '1) INACTIVE',
        '0',
        '3) 0-1 Buyer'
    )), -- type of liquidity slab 
    finance_update_count INTEGER, -- number of persons recieving finance update
    email_id_count INTEGER, -- number of email id in group entity
    is_parent_child BOOLEAN, -- is the order a parent child order or not
    number_of_ceo INTEGER, -- number of ceo in group entity
    number_of_coo INTEGER, -- number of coo in group entity
    number_of_dm_owner INTEGER, -- number of decision maker in group entity
    number_of_dm_purchase_manager INTEGER, -- number of decision maker purchase manager in group entity
    number_of_finance INTEGER, -- number of person receiving financial update in group entity
    number_of_gst INTEGER, -- number of gst associated with group entity
    number_of_logistics INTEGER, -- number of persons associated with logistics in group entity
    number_of_md INTEGER, -- number of managing director in group entity
    number_of_owner INTEGER, -- number of owner in group entity
    number_of_purchase_head INTEGER, -- number of purchase head in group entity
    number_of_purchase_manager INTEGER, -- number of purchase manager in group entity
    number_of_sales_manager INTEGER, -- number of sales manager in group entity
    number_of_undefined_role INTEGER, -- number of persons in group entity whose role is undefined
    tam VARCHAR(20) CHECK (tam IN (
        'TAM_Manuf',
        'TAM_Trader',
        'Micro_Trader',
        'TAM_Trader_1',
        'Micro_Manuf',
        'NO',
        'TAM_Manuf_1',
        'PFP_Manuf',
        'PFP_Trader',
        'PFP_Manuf_1',
        'Micro_Manuf_1',
        'Micro_Trader_1',
        'PFP_Trader_1',
        'PFP_Trader_2'
    )), -- total addressable market filter
    tag_category VARCHAR(10) CHECK (tag_category IN (
        'Others',
        'PRODUCER',
        'COMPETITOR'
    )), -- category of tag can be 
    buyer_decision_maker_person TEXT, -- name of the person who makes decision for buyer group
    buyer_decision_maker_email TEXT, -- email of the person who makes decision for buyer group
    ordered_grade_number TEXT, -- grade number that was ordered in this order
    ordered_grade_group TEXT, -- grade group that was ordered in this order
    pan VARCHAR(10), -- PAN card of the associated buyer 
    total_mapped_qty DECIMAL, -- mapped dgft input
    last_6mnt_lowest_not_adjusted DECIMAL, -- last 6 months lowest not adjusted price
    last_6mnt_lowest_not_adjusted_order_no TEXT, -- order number of last 6 months lowest not adjusted price
    last_6mnt_lowest_adjusted DECIMAL, -- last 6 months lowest adjusted price
    last_6mnt_lowest_adjusted_order_no TEXT, -- order number of last 6 months lowest adjusted price
    godown_parent_name TEXT, -- name of the parent location of the godown location 
    destination_parent_name TEXT, -- name of the parent location of the delivery destination
    app_live_price DECIMAL, -- live price on buyer app of the selected grade during the time of purchase
    l1_supplier_name TEXT, -- supplier offering least price
    l1_netback DECIMAL, -- netback from l1 supplier
    l2_supplier_name TEXT, -- supplier offering second lowest price
    l2_netback DECIMAL, -- netback from l2 supplier
    l3_supplier_name TEXT, -- supplier offering third lowest price
    l3_netback DECIMAL, -- netback from l3 supplier
    freight_quotes_l1 DECIMAL(10,2), -- least freight quote
    freight_quotes_l2 DECIMAL(10,2), -- second lowest freight quote
    freight_quotes_l3 DECIMAL(10,2), -- third lowest freight quote
    change_time TIMESTAMP, -- time at which order was changed
    probable_supplier_group_id TEXT, -- id of possible suppliers for the order
    probable_supplier_group_name TEXT, -- name of possible suppliers for the order
    is_available boolean, 
    buyer_type VARCHAR(30) CHECK (buyer_type IN (
        'REGULAR BUYER',
        '0-1 BUYER',
        'ATTRITION(COMEBACK) BUYER'
    )), -- type of buyer
    company_gst VARCHAR(15) DEFAULT '27ABACS7251D1ZH' , -- GST of source.one
    order_created_by VARCHAR(50) -- person who created the order
);

CREATE INDEX idx_order_number ON order_table(order_number);
CREATE INDEX idx_supplier_gst ON order_table(supplier_gst);
CREATE INDEX idx_buyer_gst ON order_table(buyer_gst);
CREATE INDEX idx_product_id ON order_table(product_id);
CREATE INDEX idx_status ON order_table(order_status);
CREATE INDEX idx_dispatch_date ON order_table(dispatch_date);
CREATE INDEX idx_due_date ON order_table(due_date);
CREATE INDEX idx_created_at ON order_table(created_at);

CREATE FULLTEXT INDEX idx_fulltext_supplier_name ON new_temp_order_table (supplier_name);
CREATE FULLTEXT INDEX idx_fulltext_buyer_name ON new_temp_order_table (buyer_name);
CREATE FULLTEXT INDEX idx_fulltext_godown_name ON new_temp_order_table (godown_name);
CREATE FULLTEXT INDEX idx_fulltext_product_name ON new_temp_order_table (product_name);
CREATE FULLTEXT INDEX idx_fulltext_delivery_location_name ON new_temp_order_table (delivery_location_name);
CREATE FULLTEXT INDEX idx_fulltext_delivery_address ON new_temp_order_table (delivery_address);
CREATE FULLTEXT INDEX idx_fulltext_transporter_address ON new_temp_order_table (transporter_address);
CREATE FULLTEXT INDEX idx_fulltext_buyer_po_number ON new_temp_order_table (buyer_po_number);
CREATE FULLTEXT INDEX idx_fulltext_transporter_name ON new_temp_order_table (transporter_name);
CREATE FULLTEXT INDEX idx_fulltext_last_freight_cost ON new_temp_order_table (last_freight_cost);
CREATE FULLTEXT INDEX idx_fulltext_invoice_number ON new_temp_order_table (invoice_number);
CREATE FULLTEXT INDEX idx_fulltext_bill_number ON new_temp_order_table (bill_number);
CREATE FULLTEXT INDEX idx_fulltext_utr_number ON new_temp_order_table (utr_number);
CREATE FULLTEXT INDEX idx_fulltext_rejection_reason ON new_temp_order_table (rejection_reason);
CREATE FULLTEXT INDEX idx_fulltext_reapply_reason ON new_temp_order_table (reapply_reason);
CREATE FULLTEXT INDEX idx_fulltext_invoice_status ON new_temp_order_table (invoice_status);
CREATE FULLTEXT INDEX idx_fulltext_invoice_value ON new_temp_order_table (invoice_value);
CREATE FULLTEXT INDEX idx_fulltext_invoice_balance ON new_temp_order_table (invoice_balance);
CREATE FULLTEXT INDEX idx_fulltext_overdue_amount ON new_temp_order_table (overdue_amount);
CREATE FULLTEXT INDEX idx_fulltext_pod_reason ON new_temp_order_table (pod_reason);
CREATE FULLTEXT INDEX idx_fulltext_bill_reason ON new_temp_order_table (bill_reason);
CREATE FULLTEXT INDEX idx_fulltext_lr_reason ON new_temp_order_table (lr_reason);
CREATE FULLTEXT INDEX idx_fulltext_pod_remark ON new_temp_order_table (pod_remark);
CREATE FULLTEXT INDEX idx_fulltext_bill_remark ON new_temp_order_table (bill_remark);
CREATE FULLTEXT INDEX idx_fulltext_lr_remark ON new_temp_order_table (lr_remark);
CREATE FULLTEXT INDEX idx_fulltext_driver_coordinator_name ON new_temp_order_table (driver_coordinator_name);
CREATE FULLTEXT INDEX idx_fulltext_group_remarks ON new_temp_order_table (group_remarks);
CREATE FULLTEXT INDEX idx_fulltext_group_payment_category ON new_temp_order_table (group_payment_category);
CREATE FULLTEXT INDEX idx_fulltext_group_trade_reference_values ON new_temp_order_table (group_trade_reference_values);
CREATE FULLTEXT INDEX idx_fulltext_supplier_payment_terms ON new_temp_order_table (supplier_payment_terms);
CREATE FULLTEXT INDEX idx_fulltext_sub_application_types ON new_temp_order_table (sub_application_types);
CREATE FULLTEXT INDEX idx_fulltext_regions ON new_temp_order_table (regions);
CREATE FULLTEXT INDEX idx_fulltext_group_level_grade_groups ON new_temp_order_table (group_level_grade_groups);
CREATE FULLTEXT INDEX idx_fulltext_group_level_tags ON new_temp_order_table (group_level_tags);
CREATE FULLTEXT INDEX idx_fulltext_group_hsns ON new_temp_order_table (group_hsns);
CREATE FULLTEXT INDEX idx_fulltext_active_locations ON new_temp_order_table (active_locations);
CREATE FULLTEXT INDEX idx_fulltext_inactive_locations ON new_temp_order_table (inactive_locations);
CREATE FULLTEXT INDEX idx_fulltext_first_note ON new_temp_order_table (first_note);
CREATE FULLTEXT INDEX idx_fulltext_second_note ON new_temp_order_table (second_note);
CREATE FULLTEXT INDEX idx_fulltext_opportunity ON new_temp_order_table (opportunity);
CREATE FULLTEXT INDEX idx_fulltext_buyer_decision_maker_person ON new_temp_order_table (buyer_decision_maker_person);
CREATE FULLTEXT INDEX idx_fulltext_buyer_decision_maker_email ON new_temp_order_table (buyer_decision_maker_email);
CREATE FULLTEXT INDEX idx_fulltext_last_6mnt_lowest_not_adjusted_order_no ON new_temp_order_table (last_6mnt_lowest_not_adjusted_order_no);
CREATE FULLTEXT INDEX idx_fulltext_last_6mnt_lowest_adjusted_order_no ON new_temp_order_table (last_6mnt_lowest_adjusted_order_no);
CREATE FULLTEXT INDEX idx_fulltext_godown_parent_name ON new_temp_order_table (godown_parent_name);
CREATE FULLTEXT INDEX idx_fulltext_destination_parent_name ON new_temp_order_table (destination_parent_name);
CREATE FULLTEXT INDEX idx_fulltext_l1_supplier_name ON new_temp_order_table (l1_supplier_name);
CREATE FULLTEXT INDEX idx_fulltext_l2_supplier_name ON new_temp_order_table (l2_supplier_name);
CREATE FULLTEXT INDEX idx_fulltext_l3_supplier_name ON new_temp_order_table (l3_supplier_name);
CREATE FULLTEXT INDEX idx_fulltext_probable_supplier_group_id ON new_temp_order_table (probable_supplier_group_id);
CREATE FULLTEXT INDEX idx_fulltext_probable_supplier_group_name ON new_temp_order_table (probable_supplier_group_name);
CREATE FULLTEXT INDEX idx_fulltext_buyer_type ON new_temp_order_table (buyer_type);
CREATE FULLTEXT INDEX idx_fulltext_company_gst ON new_temp_order_table (company_gst);
CREATE FULLTEXT INDEX idx_fulltext_order_created_by ON new_temp_order_table (order_created_by);
