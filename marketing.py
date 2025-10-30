import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Marketing Budget Calculator", page_icon="📊", layout="wide")

# Title
st.title("📊 Marketing Budget Calculator")
st.markdown("---")

# Input Parameters Section
st.header("Input Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    total_disbursal_target = st.number_input(
        "Total Disbursal Target (INR)",
        min_value=0,
        value=1500000000,
        step=10000000,
        format="%d"
    )
    
    repeat_customer_disbursals = st.number_input(
        "Expected Disbursals from Repeat Customers (INR)",
        min_value=0,
        value=900000000,
        step=10000000,
        format="%d"
    )
    
    campaign_duration = st.number_input(
        "Campaign Duration (Months)",
        min_value=1,
        value=3,
        step=1
    )

with col2:
    total_brands = st.number_input(
        "Total Brands Live",
        min_value=1,
        value=18,
        step=1
    )
    
    avg_loan_ticket_size = st.number_input(
        "Avg. Loan Ticket Size (INR)",
        min_value=0,
        value=20000,
        step=1000
    )
    
    agency_fee_per_brand = st.number_input(
        "Meta and Google Agency Fee (Per Brand/Month) (INR)",
        min_value=0,
        value=50000,
        step=5000
    )

with col3:
    avg_cpl = st.number_input(
        "Average Target CPL (INR)",
        min_value=1,
        value=140,
        step=10
    )
    
    target_cpd = st.number_input(
        "Target CPD (INR)",
        min_value=1,
        value=900,
        step=50
    )
    
    lead_to_disbursal_conversion = st.number_input(
        "Lead to Disbursement Conversion (%)",
        min_value=0.1,
        max_value=100.0,
        value=5.55,
        step=0.1,
        format="%.2f"
    )

st.markdown("---")

# Channel-wise Configuration
st.header("Channel Configuration")

col1, col2 = st.columns(2)

with col1:
    st.subheader("CPL by Channel")
    google_cpl = st.number_input("Google Ads CPL (INR)", min_value=1, value=50, step=5)
    meta_cpl = st.number_input("Meta Ads CPL (INR)", min_value=1, value=50, step=5)
    rcs_cpl = st.number_input("RCS & SMS CPL (INR)", min_value=1, value=200, step=10)
    whatsapp_cpl = st.number_input("WhatsApp CPL (INR)", min_value=1, value=200, step=10)
    email_cpl = st.number_input("Email CPL (INR)", min_value=1, value=200, step=10)

with col2:
    st.subheader("Conversion % by Channel")
    google_conv = st.number_input("Google Ads Conversion (%)", min_value=0.1, value=5.55, step=0.1, format="%.2f")
    meta_conv = st.number_input("Meta Ads Conversion (%)", min_value=0.1, value=5.55, step=0.1, format="%.2f")
    rcs_conv = st.number_input("RCS & SMS Conversion (%)", min_value=0.1, value=1.0, step=0.1, format="%.2f")
    whatsapp_conv = st.number_input("WhatsApp Conversion (%)", min_value=0.1, value=1.0, step=0.1, format="%.2f")
    email_conv = st.number_input("Email Conversion (%)", min_value=0.1, value=1.0, step=0.1, format="%.2f")

st.markdown("---")

# Budget Split
st.header("Budget Split by Channel (%)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    google_split = st.number_input("Google Ads %", min_value=0, max_value=100, value=45, step=1)
with col2:
    meta_split = st.number_input("Meta Ads %", min_value=0, max_value=100, value=40, step=1)
with col3:
    rcs_split = st.number_input("RCS & SMS %", min_value=0, max_value=100, value=5, step=1)
with col4:
    whatsapp_split = st.number_input("WhatsApp %", min_value=0, max_value=100, value=5, step=1)
with col5:
    email_split = st.number_input("Email %", min_value=0, max_value=100, value=5, step=1)

total_split = google_split + meta_split + rcs_split + whatsapp_split + email_split

if total_split != 100:
    st.error(f"⚠️ Budget split must total 100%. Current total: {total_split}%")

st.markdown("---")

# Calculations
st.header("📈 Calculated Results")

# Calculate key metrics
new_leads_disbursal_target = total_disbursal_target - repeat_customer_disbursals
required_disbursals_total = new_leads_disbursal_target / avg_loan_ticket_size
required_disbursals_per_brand_month = required_disbursals_total / (total_brands * campaign_duration)
required_leads_per_brand_month = required_disbursals_per_brand_month / (lead_to_disbursal_conversion / 100)
required_media_budget_per_brand_month = required_leads_per_brand_month * avg_cpl

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("New Leads Disbursal Target", f"₹{new_leads_disbursal_target:,.0f}")
    st.metric("Required Disbursals (Total)", f"{required_disbursals_total:,.0f}")

with col2:
    st.metric("Required Disbursals (Per Brand/Month)", f"{required_disbursals_per_brand_month:,.2f}")
    st.metric("Required Leads (Per Brand/Month)", f"{required_leads_per_brand_month:,.2f}")

with col3:
    st.metric("Required Media Budget (Per Brand/Month)", f"₹{required_media_budget_per_brand_month:,.2f}")
    total_agency_fees = agency_fee_per_brand * total_brands * campaign_duration
    st.metric("Total Agency Fees (All Brands, Campaign)", f"₹{total_agency_fees:,.0f}")

with col4:
    total_media_spend = required_media_budget_per_brand_month * total_brands * campaign_duration
    st.metric("Total Media Spend (Campaign)", f"₹{total_media_spend:,.2f}")
    grand_total = total_media_spend + total_agency_fees
    st.metric("Grand Total Budget", f"₹{grand_total:,.2f}")

st.markdown("---")

# Channel-wise Budget Breakdown
st.header("💰 Channel-wise Budget Breakdown (Per Brand/Month)")

if total_split == 100:
    channels_data = []
    
    channels = [
        ("Google Ads", google_split, google_cpl, google_conv),
        ("Meta Ads", meta_split, meta_cpl, meta_conv),
        ("RCS & SMS", rcs_split, rcs_cpl, rcs_conv),
        ("WhatsApp", whatsapp_split, whatsapp_cpl, whatsapp_conv),
        ("Email", email_split, email_cpl, email_conv)
    ]
    
    for channel_name, split_pct, cpl, conv_pct in channels:
        budget = required_media_budget_per_brand_month * (split_pct / 100)
        leads = budget / cpl if cpl > 0 else 0
        disbursals = leads * (conv_pct / 100)
        
        channels_data.append({
            "Channel": channel_name,
            "Budget Split %": f"{split_pct}%",
            "Media Spend (INR)": f"₹{budget:,.2f}",
            "Leads Expected": f"{leads:,.0f}",
            "Disbursals Expected": f"{disbursals:,.0f}",
            "CPL": f"₹{cpl}",
            "Conversion %": f"{conv_pct}%"
        })
    
    # Add total row
    total_budget = required_media_budget_per_brand_month
    total_leads = sum([row["Leads Expected"] for row in channels_data])
    total_leads_num = sum([(required_media_budget_per_brand_month * (ch[1] / 100)) / ch[2] for ch in channels])
    total_disbursals = sum([(required_media_budget_per_brand_month * (ch[1] / 100)) / ch[2] * (ch[3] / 100) for ch in channels])
    
    channels_data.append({
        "Channel": "TOTAL",
        "Budget Split %": "100%",
        "Media Spend (INR)": f"₹{total_budget:,.2f}",
        "Leads Expected": f"{total_leads_num:,.0f}",
        "Disbursals Expected": f"{total_disbursals:,.0f}",
        "CPL": "-",
        "Conversion %": "-"
    })
    
    df_channels = pd.DataFrame(channels_data)
    st.dataframe(df_channels, use_container_width=True, hide_index=True)
    
    # Campaign totals
    st.markdown("---")
    st.header("📊 Campaign Totals (All Brands, Full Duration)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        campaign_total_spend = total_media_spend
        st.metric("Total Media Spend", f"₹{campaign_total_spend:,.2f}")
        
    with col2:
        campaign_total_leads = total_leads_num * total_brands * campaign_duration
        st.metric("Total Leads Expected", f"{campaign_total_leads:,.0f}")
        
    with col3:
        campaign_total_disbursals = total_disbursals * total_brands * campaign_duration
        st.metric("Total Disbursals Expected", f"{campaign_total_disbursals:,.0f}")

st.markdown("---")
st.info("💡 **Note:** Affiliate agency costs (INR 1,000-2,000 per disbursal) are additional to the media spend shown above.")

# Export functionality
st.markdown("---")
st.header("📥 Export Results")

if st.button("Generate Summary Report"):
    summary_data = {
        "Metric": [
            "Total Disbursal Target",
            "Expected Repeat Customer Disbursals",
            "New Leads Disbursal Target",
            "Campaign Duration (Months)",
            "Total Brands",
            "Avg Loan Ticket Size",
            "Required Disbursals (Total)",
            "Required Disbursals (Per Brand/Month)",
            "Required Leads (Per Brand/Month)",
            "Required Media Budget (Per Brand/Month)",
            "Total Media Spend (Campaign)",
            "Total Agency Fees",
            "Grand Total Budget"
        ],
        "Value": [
            f"₹{total_disbursal_target:,.0f}",
            f"₹{repeat_customer_disbursals:,.0f}",
            f"₹{new_leads_disbursal_target:,.0f}",
            campaign_duration,
            total_brands,
            f"₹{avg_loan_ticket_size:,.0f}",
            f"{required_disbursals_total:,.0f}",
            f"{required_disbursals_per_brand_month:,.2f}",
            f"{required_leads_per_brand_month:,.2f}",
            f"₹{required_media_budget_per_brand_month:,.2f}",
            f"₹{total_media_spend:,.2f}",
            f"₹{total_agency_fees:,.0f}",
            f"₹{grand_total:,.2f}"
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    
    st.subheader("Summary Report")
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # Convert to CSV for download
    csv = df_summary.to_csv(index=False)
    st.download_button(
        label="Download Summary as CSV",
        data=csv,
        file_name="marketing_budget_summary.csv",
        mime="text/csv"
    )
