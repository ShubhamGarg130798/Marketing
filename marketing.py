import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Marketing Budget Calculator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .calculated-value {
        background-color: #e8f4f8;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>📊 Marketing Budget Calculator</h1>", unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("Input Parameters")
st.sidebar.markdown("*All amounts are in Lakhs (₹)*")

# New Input parameters
target = st.sidebar.number_input(
    "Target (₹ Lakhs)", 
    min_value=0.0, 
    max_value=200000000.0, 
    value=250.0, 
    step=10.0,
    help="Total target disbursement amount in lakhs"
)

reloan = st.sidebar.number_input(
    "Reloan (₹ Lakhs)", 
    min_value=0.0, 
    max_value=200000000.0, 
    value=150.0, 
    step=10.0,
    help="Expected reloan amount in lakhs"
)

# Calculate Target from Marketing
target_from_marketing = target - reloan

# Display calculated value
st.sidebar.markdown("### 📊 Calculated Value")
st.sidebar.markdown(f"""
<div class='calculated-value'>
    <strong>Target from Marketing</strong><br>
    <span style='font-size: 1.5rem; color: #1f77b4;'>₹{target_from_marketing:.2f} L</span><br>
    <small style='color: #666;'>Target ({target:.0f}) - Reloan ({reloan:.0f})</small>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

avg_ticket_size = st.sidebar.number_input(
    "Average Ticket Size (₹ Lakhs)", 
    min_value=0.1, 
    max_value=10.0, 
    value=0.25, 
    step=0.05,
    help="Average loan amount per customer in lakhs"
)

# Channel configuration
st.sidebar.header("Channel Configuration")

# Default channel data
default_channels = {
    'Channel': ['Google Ads', 'Meta Ads', 'RCS & SMS', 'WhatsApp', 'Email'],
    'CPL': [27.5, 16.07, 200, 200, 200],
    'Conversion %': [9.25, 3.60, 2.00, 2.00, 2.00],
    'Budget Split %': [45, 40, 5, 5, 5]
}

# Create editable dataframe
channel_df = pd.DataFrame(default_channels)

# Allow users to edit channel parameters
st.sidebar.markdown("### Edit Channel Parameters")

edited_data = []
for idx, row in channel_df.iterrows():
    st.sidebar.markdown(f"**{row['Channel']}**")
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        cpl = st.number_input(
            "CPL", 
            min_value=1.0, 
            max_value=1000.0, 
            value=float(row['CPL']), 
            step=0.1,
            key=f"cpl_{idx}"
        )
    
    with col2:
        conv = st.number_input(
            "Conv %", 
            min_value=0.1, 
            max_value=100.0, 
            value=float(row['Conversion %']), 
            step=0.1,
            key=f"conv_{idx}"
        )
    
    with col3:
        budget = st.number_input(
            "Budget %", 
            min_value=0.0, 
            max_value=100.0, 
            value=float(row['Budget Split %']), 
            step=1.0,
            key=f"budget_{idx}"
        )
    
    edited_data.append({
        'Channel': row['Channel'],
        'CPL': cpl,
        'Conversion %': conv,
        'Budget Split %': budget
    })

# Update channel dataframe
channel_df = pd.DataFrame(edited_data)

# Validate budget split
total_budget_split = channel_df['Budget Split %'].sum()
if total_budget_split != 100:
    st.sidebar.error(f"⚠️ Budget split must equal 100%. Current: {total_budget_split:.1f}%")

# Calculate derived values using target_from_marketing
disbursal_leads_required = int(target_from_marketing / avg_ticket_size)

# Main calculations
results = []
for idx, row in channel_df.iterrows():
    channel_target = target_from_marketing * (row['Budget Split %'] / 100)
    leads_to_disburse = int(channel_target / avg_ticket_size)
    leads_required = int(leads_to_disburse / (row['Conversion %'] / 100))
    amount_to_spend = (leads_required * row['CPL']) / 100000  # Convert to lakhs
    
    results.append({
        'Channel': row['Channel'],
        'Amount to Disburse (₹ Lakhs)': channel_target,
        'Leads to Disburse': leads_to_disburse,
        'Leads Required': leads_required,
        'Amount to Spend (₹ Lakhs)': amount_to_spend,
        'CPL (₹)': row['CPL'],
        'Conversion %': row['Conversion %']
    })

results_df = pd.DataFrame(results)

# Main content area - Updated metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Target", f"₹{target:.0f} L", delta=None)

with col2:
    st.metric("Reloan", f"₹{reloan:.0f} L", delta=None)

with col3:
    st.metric("Target from Marketing", f"₹{target_from_marketing:.0f} L", delta=None, 
              help="Target - Reloan")

with col4:
    st.metric("Total Leads Required", f"{results_df['Leads Required'].sum():,}", delta=None)

with col5:
    st.metric("Total Marketing Spend", f"₹{results_df['Amount to Spend (₹ Lakhs)'].sum():.1f} L", delta=None)

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📈 Charts", "📋 Detailed Results", "💡 Insights"])

with tab1:
    st.header("Channel Performance Summary")
    
    # Summary metrics
    summary_df = results_df[['Channel', 'Amount to Disburse (₹ Lakhs)', 'Leads Required', 'Amount to Spend (₹ Lakhs)']].copy()
    summary_df['ROI'] = (summary_df['Amount to Disburse (₹ Lakhs)'] / summary_df['Amount to Spend (₹ Lakhs)']).round(2)
    summary_df['Cost per Disbursed Lead'] = ((summary_df['Amount to Spend (₹ Lakhs)'] * 100000) / (summary_df['Amount to Disburse (₹ Lakhs)'] / avg_ticket_size)).round(2)
    
    st.dataframe(summary_df.style.format({
        'Amount to Disburse (₹ Lakhs)': '₹{:.1f} L',
        'Amount to Spend (₹ Lakhs)': '₹{:.2f} L',
        'Leads Required': '{:,}',
        'ROI': '{:.2f}x',
        'Cost per Disbursed Lead': '₹{:.2f}'
    }), use_container_width=True)

with tab2:
    st.header("Visual Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget allocation pie chart
        fig_budget = px.pie(
            results_df, 
            values='Amount to Spend (₹ Lakhs)', 
            names='Channel',
            title='Marketing Budget Allocation',
            hole=0.4
        )
        fig_budget.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_budget, use_container_width=True)
    
    with col2:
        # Leads distribution
        fig_leads = px.bar(
            results_df,
            x='Channel',
            y='Leads Required',
            title='Leads Required by Channel',
            color='Conversion %',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_leads, use_container_width=True)
    
    # ROI comparison
    roi_df = results_df.copy()
    roi_df['ROI'] = roi_df['Amount to Disburse (₹ Lakhs)'] / roi_df['Amount to Spend (₹ Lakhs)']
    
    fig_roi = px.bar(
        roi_df.sort_values('ROI', ascending=True),
        x='ROI',
        y='Channel',
        orientation='h',
        title='Return on Investment by Channel',
        color='ROI',
        color_continuous_scale='Greens'
    )
    fig_roi.update_layout(showlegend=False)
    st.plotly_chart(fig_roi, use_container_width=True)

with tab3:
    st.header("Detailed Results")
    
    # Full results table
    detailed_df = results_df.copy()
    
    # Add totals row
    totals = {
        'Channel': 'TOTAL',
        'Amount to Disburse (₹ Lakhs)': detailed_df['Amount to Disburse (₹ Lakhs)'].sum(),
        'Leads to Disburse': detailed_df['Leads to Disburse'].sum(),
        'Leads Required': detailed_df['Leads Required'].sum(),
        'Amount to Spend (₹ Lakhs)': detailed_df['Amount to Spend (₹ Lakhs)'].sum(),
        'CPL (₹)': '-',
        'Conversion %': '-'
    }
    
    detailed_df = pd.concat([detailed_df, pd.DataFrame([totals])], ignore_index=True)
    
    st.dataframe(detailed_df.style.format({
        'Amount to Disburse (₹ Lakhs)': '₹{:.1f} L',
        'Amount to Spend (₹ Lakhs)': '₹{:.2f} L',
        'Leads to Disburse': '{:,.0f}',
        'Leads Required': '{:,.0f}',
        'CPL (₹)': lambda x: f'₹{x}' if x != '-' else '-',
        'Conversion %': lambda x: f'{x}%' if x != '-' else '-'
    }), use_container_width=True)
    
    # Download button
    csv = detailed_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="marketing_budget_results.csv",
        mime="text/csv"
    )

with tab4:
    st.header("Key Insights & Recommendations")
    
    # Calculate insights
    best_roi_channel = roi_df.loc[roi_df['ROI'].idxmax(), 'Channel']
    worst_roi_channel = roi_df.loc[roi_df['ROI'].idxmin(), 'Channel']
    highest_spend_channel = results_df.loc[results_df['Amount to Spend (₹ Lakhs)'].idxmax(), 'Channel']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **🏆 Best Performing Channel**
        
        {best_roi_channel} shows the highest ROI of {roi_df.loc[roi_df['Channel'] == best_roi_channel, 'ROI'].values[0]:.2f}x
        """)
        
        st.warning(f"""
        **⚠️ Channel Requiring Attention**
        
        {worst_roi_channel} has the lowest ROI of {roi_df.loc[roi_df['Channel'] == worst_roi_channel, 'ROI'].values[0]:.2f}x
        """)
    
    with col2:
        st.success(f"""
        **💰 Budget Efficiency**
        
        Total marketing efficiency: {(target_from_marketing / results_df['Amount to Spend (₹ Lakhs)'].sum()):.2f}x return on marketing spend
        """)
        
        st.info(f"""
        **📊 Lead Generation Cost**
        
        Average cost per disbursed lead: ₹{(results_df['Amount to Spend (₹ Lakhs)'].sum() * 100000 / disbursal_leads_required):.2f}
        """)
    
    # Recommendations
    st.subheader("📋 Recommendations")
    
    recommendations = []
    
    # Check conversion rates
    low_conv_channels = channel_df[channel_df['Conversion %'] < 3]['Channel'].tolist()
    if low_conv_channels:
        recommendations.append(f"• Consider improving conversion rates for {', '.join(low_conv_channels)} through better lead qualification")
    
    # Check CPL
    high_cpl_channels = channel_df[channel_df['CPL'] > 100]['Channel'].tolist()
    if high_cpl_channels:
        recommendations.append(f"• Optimize campaigns for {', '.join(high_cpl_channels)} to reduce Cost Per Lead")
    
    # Budget allocation
    if roi_df.loc[roi_df['Channel'] == best_roi_channel, 'ROI'].values[0] > 2 * roi_df.loc[roi_df['Channel'] == worst_roi_channel, 'ROI'].values[0]:
        recommendations.append(f"• Consider reallocating budget from {worst_roi_channel} to {best_roi_channel} for better ROI")
    
    if recommendations:
        for rec in recommendations:
            st.write(rec)
    else:
        st.write("• Current budget allocation appears to be well-balanced")

# Footer
st.markdown("---")
st.markdown("*Marketing Budget Calculator - Optimize your marketing spend across channels*")
