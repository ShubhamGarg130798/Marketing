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
    min_value=10.0, 
    max_value=2000.0, 
    value=250.0, 
    step=10.0,
    help="Total target disbursement amount in lakhs"
)

reloan = st.sidebar.number_input(
    "Reloan (₹ Lakhs)", 
    min_value=0.0, 
    max_value=2000.0, 
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

# Password protection for editing
st.sidebar.markdown("### 🔒 Admin Access")
admin_password = st.sidebar.text_input(
    "Enter Password to Edit Channels",
    type="password",
    key="admin_password",
    help="Contact admin for password"
)

# Set your password here (change this to your desired password)
CORRECT_PASSWORD = "admin123"  # Change this to your secure password

is_admin = (admin_password == CORRECT_PASSWORD)

if admin_password and not is_admin:
    st.sidebar.error("❌ Incorrect password")
elif is_admin:
    st.sidebar.success("✅ Admin access granted")

# Initialize session state for channels if not exists
if 'channels' not in st.session_state:
    st.session_state.channels = [
        {'name': 'Google Ads', 'cpl': 27.5, 'conv': 9.25, 'budget': 45.0},
        {'name': 'Meta Ads', 'cpl': 16.07, 'conv': 3.60, 'budget': 40.0},
        {'name': 'RCS & SMS', 'cpl': 200.0, 'conv': 2.00, 'budget': 5.0},
        {'name': 'WhatsApp', 'cpl': 200.0, 'conv': 2.00, 'budget': 5.0},
        {'name': 'Email', 'cpl': 200.0, 'conv': 2.00, 'budget': 5.0}
    ]

# Only show channel editing section if admin is authenticated
if is_admin:
    st.sidebar.markdown("---")
    
    # Add new channel button
    st.sidebar.markdown("### Edit Channel Parameters")
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        if st.button("➕ Add New Channel", use_container_width=True):
            st.session_state.channels.append({
                'name': f'Channel {len(st.session_state.channels) + 1}',
                'cpl': 100.0,
                'conv': 2.0,
                'budget': 0.0
            })
            st.rerun()

    # Display and edit channels
    edited_channels = []
    channels_to_remove = []

    for idx, channel in enumerate(st.session_state.channels):
        st.sidebar.markdown(f"**Channel {idx + 1}**")
        
        col1, col2 = st.sidebar.columns([4, 1])
        
        with col1:
            channel_name = st.text_input(
                "Channel Name",
                value=channel['name'],
                key=f"name_{idx}",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("🗑️", key=f"del_{idx}", help="Delete channel"):
                channels_to_remove.append(idx)
        
        col1, col2, col3 = st.sidebar.columns(3)
        
        with col1:
            cpl = st.number_input(
                "CPL", 
                min_value=1.0, 
                max_value=1000.0, 
                value=float(channel['cpl']), 
                step=0.1,
                key=f"cpl_{idx}"
            )
        
        with col2:
            conv = st.number_input(
                "Conv %", 
                min_value=0.1, 
                max_value=100.0, 
                value=float(channel['conv']), 
                step=0.1,
                key=f"conv_{idx}"
            )
        
        with col3:
            budget = st.number_input(
                "Budget %", 
                min_value=0.0, 
                max_value=100.0, 
                value=float(channel['budget']), 
                step=1.0,
                key=f"budget_{idx}"
            )
        
        edited_channels.append({
            'name': channel_name,
            'cpl': cpl,
            'conv': conv,
            'budget': budget
        })
        
        st.sidebar.markdown("---")

    # Remove channels marked for deletion
    if channels_to_remove:
        for idx in sorted(channels_to_remove, reverse=True):
            st.session_state.channels.pop(idx)
        st.rerun()

    # Update session state with edited values
    st.session_state.channels = edited_channels
else:
    # Show current channels as read-only information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Current Channels")
    st.sidebar.info("🔒 Enter admin password above to edit channels")
    
    for idx, channel in enumerate(st.session_state.channels):
        st.sidebar.markdown(f"**{channel['name']}**")
        st.sidebar.text(f"CPL: ₹{channel['cpl']} | Conv: {channel['conv']}% | Budget: {channel['budget']}%")

# Create dataframe from current channels
channel_df = pd.DataFrame([
    {
        'Channel': ch['name'],
        'CPL': ch['cpl'],
        'Conversion %': ch['conv'],
        'Budget Split %': ch['budget']
    }
    for ch in st.session_state.channels
])

# Validate budget split
total_budget_split = channel_df['Budget Split %'].sum()
if total_budget_split != 100:
    st.sidebar.error(f"⚠️ Budget split must equal 100%. Current: {total_budget_split:.1f}%")

# Calculate derived values using target_from_marketing
disbursal_leads_required = int(target_from_marketing / avg_ticket_size) if target_from_marketing > 0 else 0

# Main calculations
results = []
for idx, row in channel_df.iterrows():
    channel_target = target_from_marketing * (row['Budget Split %'] / 100)
    leads_to_disburse = int(channel_target / avg_ticket_size) if avg_ticket_size > 0 else 0
    leads_required = int(leads_to_disburse / (row['Conversion %'] / 100)) if row['Conversion %'] > 0 else 0
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
tab1, tab2, tab3 = st.tabs(["📊 Detailed Results", "📈 Charts", "💡 Insights"])

with tab1:
    st.header("Channel Performance Summary")
    
    if len(results_df) > 0:
        # Create comprehensive results table
        detailed_df = results_df.copy()
        
        # Add ROI and Cost per Disbursed Lead columns
        detailed_df['ROI'] = (detailed_df['Amount to Disburse (₹ Lakhs)'] / detailed_df['Amount to Spend (₹ Lakhs)']).replace([float('inf'), -float('inf')], 0).round(2)
        detailed_df['Cost per Disbursed Lead'] = ((detailed_df['Amount to Spend (₹ Lakhs)'] * 100000) / (detailed_df['Amount to Disburse (₹ Lakhs)'] / avg_ticket_size)).replace([float('inf'), -float('inf')], 0).round(2)
        
        # Reorder columns for better readability
        detailed_df = detailed_df[[
            'Channel',
            'CPL (₹)',
            'Conversion %',
            'Leads Required',
            'Leads to Disburse',
            'Amount to Spend (₹ Lakhs)',
            'Amount to Disburse (₹ Lakhs)',
            'ROI',
            'Cost per Disbursed Lead'
        ]]
        
        # Add totals row
        totals = {
            'Channel': 'TOTAL',
            'CPL (₹)': '-',
            'Conversion %': '-',
            'Leads Required': detailed_df['Leads Required'].sum(),
            'Leads to Disburse': detailed_df['Leads to Disburse'].sum(),
            'Amount to Spend (₹ Lakhs)': detailed_df['Amount to Spend (₹ Lakhs)'].sum(),
            'Amount to Disburse (₹ Lakhs)': detailed_df['Amount to Disburse (₹ Lakhs)'].sum(),
            'ROI': '-',
            'Cost per Disbursed Lead': '-'
        }
        
        detailed_df = pd.concat([detailed_df, pd.DataFrame([totals])], ignore_index=True)
        
        # Display the table with formatting
        st.dataframe(detailed_df.style.format({
            'CPL (₹)': lambda x: f'₹{x}' if x != '-' else '-',
            'Conversion %': lambda x: f'{x}%' if x != '-' else '-',
            'Leads Required': '{:,.0f}',
            'Leads to Disburse': '{:,.0f}',
            'Amount to Spend (₹ Lakhs)': '₹{:.2f} L',
            'Amount to Disburse (₹ Lakhs)': '₹{:.1f} L',
            'ROI': lambda x: f'{x}x' if x != '-' else '-',
            'Cost per Disbursed Lead': lambda x: f'₹{x}' if x != '-' else '-'
        }), use_container_width=True)
        
        # Download button
        csv = detailed_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="marketing_budget_results.csv",
            mime="text/csv"
        )
    else:
        st.info("Add channels to see detailed results.")

with tab2:
    st.header("Visual Analytics")
    
    if len(results_df) > 0:
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
        roi_df['ROI'] = (roi_df['Amount to Disburse (₹ Lakhs)'] / roi_df['Amount to Spend (₹ Lakhs)']).replace([float('inf'), -float('inf')], 0)
        
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
    else:
        st.info("Add channels to see the charts.")

with tab3:
    st.header("Key Insights & Recommendations")
    
    if len(results_df) > 0:
        # Calculate insights
        roi_df = results_df.copy()
        roi_df['ROI'] = (roi_df['Amount to Disburse (₹ Lakhs)'] / roi_df['Amount to Spend (₹ Lakhs)']).replace([float('inf'), -float('inf')], 0)
        
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
            total_spend = results_df['Amount to Spend (₹ Lakhs)'].sum()
            if total_spend > 0:
                st.success(f"""
                **💰 Budget Efficiency**
                
                Total marketing efficiency: {(target_from_marketing / total_spend):.2f}x return on marketing spend
                """)
            
            if disbursal_leads_required > 0:
                st.info(f"""
                **📊 Lead Generation Cost**
                
                Average cost per disbursed lead: ₹{(total_spend * 100000 / disbursal_leads_required):.2f}
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
    else:
        st.info("Add channels to see insights and recommendations.")

# Footer
st.markdown("---")
st.markdown("*Marketing Budget Calculator - Optimize your marketing spend across channels*")
