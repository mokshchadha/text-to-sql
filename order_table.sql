CREATE TABLE order_table (
  id VARCHAR(100) PRIMARY KEY, 
  order_number VARCHAR(10) , -- unique identifier for each order
  supplier_gst VARCHAR(30) , -- gst number of the supplier 
  supplier_name VARCHAR(255), -- name of the supplier entity
  buyer_gst VARCHAR(30) , -- buyer gst number 
  buyer_name VARCHAR(100) , -- name of the buyer
  godown_id VARCHAR(100), -- location id of the godown location
  godown_name VARCHAR(100), -- location name of the godown
  quantity DECIMAL , -- combined quantity for the order
  single_quantity DECIMAL , -- actual quantity of the order 
  product_id VARCHAR(100) , -- unique id of product
  product_name VARCHAR(100) , -- official grade name that was ordered
  delivery_location_id VARCHAR(100),  -- location id of the delivery location
  delivery_location_name VARCHAR(100) , -- location name of the delivery location
  dispatch_date DATE, -- date of dispatch of the order
  due_date DATE, -- due date for the order
  buyer_due_date DATE, -- due date of the order for the buyer
  expected_delivery_date DATE, -- expected date of delivery by our internal calculations
  actual_delivery_date DATE, -- actual date on which order was delivered
  supplier_due_date DATE, -- due date for the supplier for supplier payment
  order_status VARCHAR(100)  , -- status of order
  buyer_payment_terms VARCHAR(100), -- payment terms opted by the buyer for paying 
  delivery_address TEXT, -- complete delivery address for the order
  transporter_address TEXT, -- address that is shared with the transporter vendor for delivery
  is_eway_bill_created BOOLEAN, -- is eway bill created or no
  buyer_po_number VARCHAR(100), -- buyer po number
  delivery_buyer_payment_terms VARCHAR(255), -- TODO:
  eway_bill_expiry_date DATE, -- date on which eway bill will get expired 
  delay_score INTEGER DEFAULT 0, -- delay score, no delay means 0 delay days
  logistic_delay_score INTEGER DEFAULT 0, -- logistic delay score can be minimum of -1 
  lr_number VARCHAR(100), -- lr number of the transporter
  driver_mobile_number VARCHAR(100), -- mobile number of person driving
  transporter_name VARCHAR(100), -- name of the transporter vendor company
  freight_cost INTEGER, -- actual freight cost of the order
  last_freight_cost VARCHAR(255), -- freight cost of the last order that placed between the same godown and delivery location along with load and order No eg:-  3500 (30mt-40164)
  freight_payment_status VARCHAR(100), -- payment status for the freight
  system_freight_cost INTEGER, -- freight cost generated by system automation logic
  max_possible_freight_cost INTEGER, -- upper threshold for freight cost for system generated cost
  transit_distance_in_km INTEGER, -- transit distance between godown and delivery location
  supplier_credit_note_value DECIMAL, -- credit note offered to supplier
  buyer_price DECIMAL, -- per kg price of the order confirmed by buyer
  buyer_credit_note_value DECIMAL, -- credit note offered to buyer
  invoice_number VARCHAR(100), -- unique identifier for invoices in zoho books
  supplier_price DECIMAL,-- per kg price of order confirmed by the supplier
  bill_number VARCHAR(100), -- bill id generated for supplier
  purchase_order_number VARCHAR(100), -- purchase order number for the buyer
  margin INTEGER, -- internal profit margin in the order
  total_amount DECIMAL, -- total selling cost of the order for the buyer
  utr_number text, -- transaction id of payment made by buyer for order
  is_payment_made_to_supplier BOOLEAN, -- is payment made to supplier 
  freight_payment_application_status VARCHAR(100),
  freight_bill_status VARCHAR(100),
  freight_pod_status VARCHAR(100),
  rejection_reason TEXT, -- reason for freight request rejection
  reapply_reason TEXT, -- reason to reapply after freight rejection 
  applied_for_freight_payment_at TIMESTAMP,
  created_at TIMESTAMP, -- order created at time
  updated_at TIMESTAMP, -- order updated at time 
  invoice_status VARCHAR(100), -- status of invoice , can be paid or unpaid or void
  invoice_value VARCHAR(255), -- total cost on the invoices seperated by comma 
  invoice_due_days text,  -- FIXME: convert this into integer
  invoice_balance text, -- FIXME: convert this into intger ,Pending amount due against the buyer's invoice
  overdue_amount text, -- FIXME: convert this into decimal  Over due of the buyer invoice -- //TODO:
  adjusted_system_distance INTEGER, -- system distance in kms later adjusted DO NOT USE IT
  tracking_status VARCHAR(100), -- tracking status from cargo exchange 
  pod_reason TEXT,
  bill_reason TEXT,
  lr_reason TEXT,
  pod_remark TEXT,
  bill_remark TEXT,
  lr_remark TEXT,
  lr_status VARCHAR(100), -- status of lr, can be UPLOADED, ACCEPTED, REJECTED, REUPLOADED
  driver_coordinator_name VARCHAR(100), -- driver coordinate name 
  transport_region VARCHAR(100), -- transporter region 
  group_state_owner VARCHAR(100), -- group state owner 
  buyer_account_manager VARCHAR(100), -- buyer account manager 
  supplier_account_manager VARCHAR(100), -- supplier account manager
  is_return BOOLEAN, -- is this is returned order or not
  return_order_created_from VARCHAR(100), -- original order from which this return order is created from 
  buyer_poc VARCHAR(100), -- Phone number Point of contact at buyer side 
  buyer_poc_name VARCHAR(100), -- Name of point of contact at buyer side
  supplier_poc VARCHAR(100), -- Phone number point of contact at supplier side 
  supplier_poc_name VARCHAR(100), -- Name of point of contact at supplier side
  tags text, -- tags concatenated via comma separated string 
  freight_quotes_count INTEGER,
  loading_address TEXT,
  vehicle_number VARCHAR(100),
  delivered_to_with_parent VARCHAR(100), -- concatenated string of the delivery location with its parent location 
  godown_with_parent VARCHAR(100), -- concatenated string of the godown location with its parent location 
  netback DECIMAL, -- decimal netback received on every order can be positive or negative 
  buyer_group_id VARCHAR(100), -- group id of the buyer entity group 
  supplier_group_id VARCHAR(100), -- group id of the supplier entity group 
  order_request_id VARCHAR(100), -- order request id from which this order was originally created
  logistic_team_last_edit_by VARCHAR(100), -- email of last person to update the logistic remarks 
  buyer_team_last_edit_by VARCHAR(100), -- email of the last person to update the buyer team remarks
  supplier_team_last_edit_by VARCHAR(100), -- email of the last person to update the supplier team remarks
  general_last_edit_by VARCHAR(100), -- email of last person to update the general remarks
  driver_last_edit_by VARCHAR(100), -- email of last person to edit driver team remarks
  logistic_team_remarks_concatenated TEXT, -- logistic team remarks concatenated with last time it was edited
  buyer_team_remarks_concatenated TEXT, -- buyer team remarks concatenated with last time it was edited
  supplier_team_remarks_concatenated TEXT,-- supplier team remarks concatenated with last time it was edited
  general_remarks_concatenated TEXT,-- general team remarks concatenated with last time it was edited
  driver_remarks_concatenated TEXT,-- driver team remarks concatenated with last time it was edited
  netback_sf DECIMAL, -- TODO:
  buyer_delivery_terms VARCHAR(100), -- 
  state_abbreviation CHAR(2),
  load INTEGER,
  freight_offset DECIMAL, -- TODO:
  max_dispatch_date DATE,
  min_dispatch_date DATE,
  last_order_days_ago INTEGER,
  group_name VARCHAR(100), --  buyer group name 
  group_limit DECIMAL(15,2),-- TODO:
  group_blacklisted BOOLEAN, -- is the buyer group blacklisted or not 
  group_business_type VARCHAR(100), -- business type of the buyer group
  group_credit_interest DECIMAL, -- interest in percentage offered to each buyer group
  group_credit_limit DECIMAL(15,2), -- credit limit of the buyer group
  group_credit_tenor VARCHAR(100), -- it usually of formate delivery + X days
  group_markup_value DECIMAL, -- TODO:
  group_margin DECIMAL, -- margin of money associated with the buyer group
  group_remarks TEXT, -- remarks for the buyer group
  group_unfulfilled_order_count INTEGER, -- orders for buyer group that were unfulfilled in past
  group_waba_price_enabled BOOLEAN, -- weather waba price is enabled or not for buyer group
  highest_gst_slab VARCHAR(100), -- this is range for eg:- 5 Cr. to 25 Cr.
  orders_count INTEGER, -- count of orders for this particular buyer in the past
  account_manager VARCHAR(100), -- account manager of the buyer 
  business_units VARCHAR(255), -- business unit refers to the commodity or Engineering
  group_payment_category VARCHAR(100), -- default payment category of the buyer group
  group_trade_reference_values VARCHAR(255), -- buyer group trade references comma separated
  is_deleted BOOLEAN, -- is the buyer group deleted or not 
  application_type VARCHAR(100), -- application type of the grade ordered in the order
  highest_pan VARCHAR(10), -- PAN number with highest gst limit for buyer
  group_primary_location VARCHAR(100), -- name of the primary location for buyer group
  last_ordered_date DATE, -- date when the last ordered by placed by this group
  coa_required BOOLEAN, -- is COA certificate required or not for the buyer
  last_buyer_app_usage_days_ago INTEGER, -- 
  payment_reminders text, -- TODO: this is always empty or 0
  mobile_app_enabled BOOLEAN, -- mobile app enabled for the buyer or not
  supplier_payment_terms VARCHAR(100), -- payment terms selected by the supplier
  order_priority VARCHAR(100), -- priority of the order
  listings_deactivation_timer INTEGER, -- deactivation timer for the supplier selected for the order
  repeat_reminders_after INTEGER, -- no of hours after which we should send a reminder to the supplier for updating their offers
  special_offer_enabled BOOLEAN, -- is special offer enabled for the supplier of this order
  supplier_orders_count INTEGER, -- no of orders that this supplier has delivered in the past
  group_available_limit DECIMAL, -- available limit of money with the buyer group
  sub_application_types VARCHAR(255), -- sub application type of the grade ordered in the order separated by /
  pfp_status VARCHAR(100), -- TODO:
  group_creation_date DATE, -- creation date of the buyer group
  regions VARCHAR(100), -- region from which the buyer group is associated
  group_level_grade_groups TEXT, -- grade groups associated with buyers comma separated
  group_level_tags TEXT, -- buyer group tags comma separated 
  group_hsns TEXT, -- buyer group hsn codes separated by comma
  active_locations TEXT, -- comma separated locations the buyer is active in 
  inactive_locations TEXT, -- comma separated locations that the buyer is inactive in 
  waba_status VARCHAR(100), -- waba status of the buyer for this order
  group_price_receipt VARCHAR(100), -- buyer group price receipt is either active or inactive
  decision_maker_mapped BOOLEAN, -- is the decision maker for the order mapped or not TODO:
  buyer_decision_maker VARCHAR(100), -- phone number of the person who makes decisions for the order from buyer side
  dgft_import DECIMAL,-- total count of dgft imports for the buyer
  dgft_import_mapped DECIMAL, --  count of dgft imports mapped for the buyer out of total imports
  created_by VARCHAR(100), -- email id of the person who created the order
  last_correspondence_date DATE, -- date of last correspondence TODO:
  last_correspondence_days_ago INTEGER, -- last correspondence days ago
  correspondence_range VARCHAR(255),
  first_note TEXT, -- first note for the buyer 
  second_note TEXT, -- second note for the buyer 
  credit_order DECIMAL, -- credit associated with the order TODO:
  lifetime_volume DECIMAL, -- lifetime volume of the buyer group associated with this order
  liquidity_buyer_type VARCHAR(100), -- type of buyer either he is attrition buyer or regular buyer FIXME: can be refactored
  outreach_buyer_type VARCHAR(100), -- type of buyer either he is attrition buyer or regular buyer FIXME: can be refactored
  days_passed INTEGER,  -- how many days have passed since this order TODO:
  days_passed_label VARCHAR(100), -- label given to days passed 
  opportunity TEXT, -- type of business opportunity with the buyer 
  volume_supplied DECIMAL, -- total volume supplied by the supplier 
  is_supplier_activated BOOLEAN, -- is supplier activated or not 
  liquidity_type VARCHAR(255), -- type of liquidity that the buyer has 
  liquidity_buyer_type_attrition_slab VARCHAR(100), -- type of liquidity slap FIXME:
  finance_update_count INTEGER, -- number of times the finance updated TODO:
  email_id_count INTEGER, -- TODO:
  is_parent_child BOOLEAN, -- is the order a parent child order or not TODO:
  ceo INTEGER, -- TODO:
  coo INTEGER, -- TODO:
  dm_owner INTEGER, -- TODO:
  dm_purchase_manager INTEGER, -- TODO:
  finance INTEGER, -- TODO:
  gst INTEGER, -- TODO: why is this an integer?
  logistics INTEGER, -- this is an integer why ? TODO:
  md INTEGER, -- TODO: this is an integer why?
  owner INTEGER, -- TODO: this is an integer why?
  purchase_head INTEGER,-- TODO: this is an integer why?
  purchase_manager INTEGER,-- TODO: this is an integer why?
  sales_manager INTEGER, -- TODO: this is an integer why?
  undefined_role INTEGER, -- TODO: this is an integer why?
  tam VARCHAR(100), -- 
  tag_category VARCHAR(100), -- category of tag can be 
  buyer_decision_maker_person VARCHAR(100), -- name of the person who makes decision for buyer group
  buyer_decision_maker_email VARCHAR(100),-- email of the person who makes decision for buyer group
  ordered_grade_number VARCHAR(100), -- grade number that was ordered in this order
  ordered_grade_group VARCHAR(100), -- grade group that was ordered in this order
  pan VARCHAR(10), -- pan card of the associated buyer 
  total_mapped_qty DECIMAL, -- TODO:
  last_6mnt_lowest_not_adjusted DECIMAL,
  last_6mnt_lowest_not_adjusted_order_no VARCHAR(100),
  last_6mnt_lowest_adjusted DECIMAL,
  last_6mnt_lowest_adjusted_order_no VARCHAR(100),
  godown_parent_name VARCHAR(100), -- name of the parent location of the godown location 
  destination_parent_name VARCHAR(100),
  app_live_price DECIMAL, -- live price on buyer app of the selected grade during the time of purchase
  l1_supplier_name VARCHAR(100),
  l1_netback DECIMAL,
  l2_supplier_name VARCHAR(100),
  l2_netback DECIMAL,
  l3_supplier_name VARCHAR(100),
  l3_netback DECIMAL,
  freight_quotes_l1 DECIMAL,
  freight_quotes_l2 DECIMAL,
  freight_quotes_l3 DECIMAL,
  change_time TIMESTAMP,
  probable_supplier_group_id VARCHAR(100),
  probable_supplier_group_name VARCHAR(100),
  availability VARCHAR(100),
  buyer_type VARCHAR(100),
  company_gst VARCHAR(15),
  order_created_by VARCHAR(100)
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
CREATE INDEX idx_gin_delivery_buyer_payment_terms ON order_table USING gin (delivery_buyer_payment_terms gin_trgm_ops);
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
CREATE INDEX idx_gin_transport_region ON order_table USING gin (transport_region gin_trgm_ops);
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
CREATE INDEX idx_gin_buyer_delivery_terms ON order_table USING gin (buyer_delivery_terms gin_trgm_ops);
CREATE INDEX idx_gin_group_name ON order_table USING gin (group_name gin_trgm_ops);
CREATE INDEX idx_gin_group_business_type ON order_table USING gin (group_business_type gin_trgm_ops);
CREATE INDEX idx_gin_group_credit_tenor ON order_table USING gin (group_credit_tenor gin_trgm_ops);
CREATE INDEX idx_gin_group_remarks ON order_table USING gin (group_remarks gin_trgm_ops);
CREATE INDEX idx_gin_highest_gst_slab ON order_table USING gin (highest_gst_slab gin_trgm_ops);
CREATE INDEX idx_gin_account_manager ON order_table USING gin (account_manager gin_trgm_ops);
CREATE INDEX idx_gin_business_units ON order_table USING gin (business_units gin_trgm_ops);
CREATE INDEX idx_gin_group_payment_category ON order_table USING gin (group_payment_category gin_trgm_ops);
CREATE INDEX idx_gin_group_trade_reference_values ON order_table USING gin (group_trade_reference_values gin_trgm_ops);
CREATE INDEX idx_gin_application_type ON order_table USING gin (application_type gin_trgm_ops);
CREATE INDEX idx_gin_group_primary_location ON order_table USING gin (group_primary_location gin_trgm_ops);
CREATE INDEX idx_gin_supplier_payment_terms ON order_table USING gin (supplier_payment_terms gin_trgm_ops);
CREATE INDEX idx_gin_order_priority ON order_table USING gin (order_priority gin_trgm_ops);
CREATE INDEX idx_gin_pfp_status ON order_table USING gin (pfp_status gin_trgm_ops);
CREATE INDEX idx_gin_regions ON order_table USING gin (regions gin_trgm_ops);
CREATE INDEX idx_gin_group_level_grade_groups ON order_table USING gin (group_level_grade_groups gin_trgm_ops);
CREATE INDEX idx_gin_group_level_tags ON order_table USING gin (group_level_tags gin_trgm_ops);
CREATE INDEX idx_gin_group_hsns ON order_table USING gin (group_hsns gin_trgm_ops);
CREATE INDEX idx_gin_active_locations ON order_table USING gin (active_locations gin_trgm_ops);
CREATE INDEX idx_gin_inactive_locations ON order_table USING gin (inactive_locations gin_trgm_ops);
CREATE INDEX idx_gin_waba_status ON order_table USING gin (waba_status gin_trgm_ops);
CREATE INDEX idx_gin_group_price_receipt ON order_table USING gin (group_price_receipt gin_trgm_ops);
CREATE INDEX idx_gin_buyer_decision_maker ON order_table USING gin (buyer_decision_maker gin_trgm_ops);
CREATE INDEX idx_gin_created_by ON order_table USING gin (created_by gin_trgm_ops);
CREATE INDEX idx_gin_correspondence_range ON order_table USING gin (correspondence_range gin_trgm_ops);
CREATE INDEX idx_gin_first_note ON order_table USING gin (first_note gin_trgm_ops);
CREATE INDEX idx_gin_second_note ON order_table USING gin (second_note gin_trgm_ops);
CREATE INDEX idx_gin_liquidity_buyer_type ON order_table USING gin (liquidity_buyer_type gin_trgm_ops);
CREATE INDEX idx_gin_outreach_buyer_type ON order_table USING gin (outreach_buyer_type gin_trgm_ops);
CREATE INDEX idx_gin_days_passed_label ON order_table USING gin (days_passed_label gin_trgm_ops);
CREATE INDEX idx_gin_opportunity ON order_table USING gin (opportunity gin_trgm_ops);
CREATE INDEX idx_gin_liquidity_type ON order_table USING gin (liquidity_type gin_trgm_ops);
CREATE INDEX idx_gin_liquidity_buyer_type_attrition_slab ON order_table USING gin (liquidity_buyer_type_attrition_slab gin_trgm_ops);
CREATE INDEX idx_gin_tam ON order_table USING gin (tam gin_trgm_ops);
CREATE INDEX idx_gin_tag_category ON order_table USING gin (tag_category gin_trgm_ops);
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
CREATE INDEX idx_gin_availability ON order_table USING gin (availability gin_trgm_ops);
CREATE INDEX idx_gin_buyer_type ON order_table USING gin (buyer_type gin_trgm_ops);
CREATE INDEX idx_gin_order_created_by ON order_table USING gin (order_created_by gin_trgm_ops);
CREATE INDEX idx_gin_utr_number ON order_table USING gin(utr_number gin_trgm_ops );