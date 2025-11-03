import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Indian number formatting function
def format_indian_number(number):
    """Format number according to Indian numbering system with commas"""
    if pd.isna(number) or number == 0:
        return "0"
    
    s = str(int(number))
    if len(s) <= 3:
        return s
    
    # Split into last 3 digits and remaining
    last_three = s[-3:]
    remaining = s[:-3]
    
    # Add commas every 2 digits for remaining part
    result = ''
    for i, digit in enumerate(reversed(remaining)):
        if i > 0 and i % 2 == 0:
            result = ',' + result
        result = digit + result
    
    return result + ',' + last_three

# Set page configuration
st.set_page_config(
    page_title="Marketing Budget Calculator",
    page_icon="💰",
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
    /* Custom metric cards */
    .metric-card {
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        text-align: center;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-card h3 {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        opacity: 0.8;
    }
    .metric-card p {
        font-size: 1.6rem;
        font-weight: bold;
        margin: 0;
    }
    .card-blue {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #1565c0;
    }
    .card-green {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        color: #6a1b9a;
    }
    .card-orange {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
        color: #00695c;
    }
    .card-purple {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        color: #e65100;
    }
    .card-teal {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        color: #c2185b;
    }
    /* Chart card styling */
    .chart-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>💰 Marketing Budget Calculator</h1>", unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("Input Parameters")
st.sidebar.markdown("*All amounts are in Lakhs (₹)*")

# New Input parameters
target = st.sidebar.number_input(
    "Target (₹ Lakhs)", 
    min_value=0.0, 
    max_value=10000000.0, 
    value=250.0, 
    step=10.0,
    help="Total target disbursement amount in lakhs"
)

reloan = st.sidebar.number_input(
    "Reloan (₹ Lakhs)", 
    min_value=0.0, 
    max_value=10000000.0, 
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
    min_value=0.0, 
    max_value=10000000.0, 
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
CORRECT_PASSWORD = "Fintech@24680"  # Change this to your secure password

is_admin = (admin_password == CORRECT_PASSWORD)

if admin_password and not is_admin:
    st.sidebar.error("❌ Incorrect password")
elif is_admin:
    st.sidebar.success("✅ Admin access granted")

# Initialize session state for channels if not exists
if 'channels' not in st.session_state:
    st.session_state.channels = [
        {'name': 'Google Ads', 'cpl': 50.0, 'conv': 9.60, 'budget': 45.0},
        {'name': 'Meta Ads', 'cpl': 50.0, 'conv': 4.80, 'budget': 40.0},
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
                min_value=0.0, 
                max_value=10000000.0, 
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
        'Marketing Spend (₹ Lakhs)': amount_to_spend,
        'CPL (₹)': row['CPL'],
        'Conversion %': row['Conversion %']
    })

results_df = pd.DataFrame(results)

# Main content area - Updated metrics with colorful cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card card-blue">
        <h3>Total Target</h3>
        <p>₹{target:.0f} L</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card card-green">
        <h3>Reloan</h3>
        <p>₹{reloan:.0f} L</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card card-orange">
        <h3>Target from Marketing</h3>
        <p>₹{target_from_marketing:.0f} L</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card card-purple">
        <h3>Total Leads Required</h3>
        <p>{format_indian_number(results_df['Leads Required'].sum())}</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card card-teal">
        <h3>Total Marketing Spend</h3>
        <p>₹{results_df['Marketing Spend (₹ Lakhs)'].sum():.1f} L</p>
    </div>
    """, unsafe_allow_html=True)

# Main content sections - all on one page

# Section 1: Detailed Results Table
st.header("📊 Channel Performance Summary")

if len(results_df) > 0:
    # Create comprehensive results table
    detailed_df = results_df.copy()
    
    # Add ROI and Cost per Disbursed Lead columns
    detailed_df['ROI'] = (detailed_df['Amount to Disburse (₹ Lakhs)'] / detailed_df['Marketing Spend (₹ Lakhs)']).replace([float('inf'), -float('inf')], 0).round(2)
    detailed_df['Cost per Disbursed Lead'] = ((detailed_df['Marketing Spend (₹ Lakhs)'] * 100000) / (detailed_df['Amount to Disburse (₹ Lakhs)'] / avg_ticket_size)).replace([float('inf'), -float('inf')], 0).round(0)  # Round to whole number
    
    # Add serial number column starting from 1
    detailed_df.insert(0, 'S.No', range(1, len(detailed_df) + 1))
    
    # Reorder columns for better readability
    detailed_df = detailed_df[[
        'S.No',
        'Channel',
        'CPL (₹)',
        'Conversion %',
        'Leads Required',
        'Leads to Disburse',
        'Marketing Spend (₹ Lakhs)',
        'Amount to Disburse (₹ Lakhs)',
        'ROI',
        'Cost per Disbursed Lead'
    ]]
    
    # Add totals row
    totals = {
        'S.No': '-',
        'Channel': 'TOTAL',
        'CPL (₹)': '-',
        'Conversion %': '-',
        'Leads Required': detailed_df['Leads Required'].sum(),
        'Leads to Disburse': detailed_df['Leads to Disburse'].sum(),
        'Marketing Spend (₹ Lakhs)': detailed_df['Marketing Spend (₹ Lakhs)'].sum(),
        'Amount to Disburse (₹ Lakhs)': detailed_df['Amount to Disburse (₹ Lakhs)'].sum(),
        'ROI': '-',
        'Cost per Disbursed Lead': '-'
    }
    
    detailed_df = pd.concat([detailed_df, pd.DataFrame([totals])], ignore_index=True)
    
    # Display the table with formatting
    styled_df = detailed_df.style.format({
        'S.No': lambda x: x if x != '-' else '-',
        'CPL (₹)': lambda x: f'₹{x}' if x != '-' else '-',
        'Conversion %': lambda x: f'{x}%' if x != '-' else '-',
        'Leads Required': lambda x: format_indian_number(x) if x != '-' else '-',
        'Leads to Disburse': lambda x: format_indian_number(x) if x != '-' else '-',
        'Marketing Spend (₹ Lakhs)': '₹{:.2f} L',
        'Amount to Disburse (₹ Lakhs)': '₹{:.1f} L',
        'ROI': lambda x: f'{x}x' if isinstance(x, (int, float)) and x != '-' else '-',
        'Cost per Disbursed Lead': lambda x: f'₹{int(x)}' if isinstance(x, (int, float)) and x != '-' else '-'
    })
    
    # Apply bold styling and background to TOTAL row
    def highlight_total(row):
        if row['Channel'] == 'TOTAL':
            return ['font-weight: bold; background-color: #e3f2fd; color: #1565c0;'] * len(row)
        return [''] * len(row)
    
    # Apply alternating row colors
    def alternating_rows(row):
        if row.name % 2 == 0 and row['Channel'] != 'TOTAL':
            return ['background-color: #f8f9fa;'] * len(row)
        elif row['Channel'] != 'TOTAL':
            return ['background-color: white;'] * len(row)
        return [''] * len(row)
    
    styled_df = styled_df.apply(highlight_total, axis=1)
    styled_df = styled_df.apply(alternating_rows, axis=1)
    
    # Set table properties
    styled_df = styled_df.set_properties(**{
        'text-align': 'center',
        'vertical-align': 'middle',
        'padding': '12px',
        'border': '1px solid #dee2e6'
    })
    
    # Style the header
    styled_df = styled_df.set_table_styles([
        {'selector': 'thead th', 
         'props': [
             ('background-color', '#1565c0'),
             ('color', 'white'),
             ('font-weight', 'bold'),
             ('text-align', 'center'),
             ('vertical-align', 'middle'),
             ('padding', '12px'),
             ('border', '1px solid #1565c0')
         ]},
        {'selector': 'tbody td', 
         'props': [
             ('border', '1px solid #dee2e6'),
             ('text-align', 'center'),
             ('vertical-align', 'middle')
         ]}
    ])
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
else:
    st.info("Add channels to see detailed results.")

st.markdown("---")

# Section 2: Visual Analytics
st.header("📈 Visual Analytics")

if len(results_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget allocation pie chart
        fig_budget = px.pie(
            results_df, 
            values='Marketing Spend (₹ Lakhs)', 
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
            color_continuous_scale='Blues',
            text='Leads Required'
        )
        # Format text labels with Indian numbering
        fig_leads.update_traces(
            texttemplate=[format_indian_number(val) for val in results_df['Leads Required']],
            textposition='outside'
        )
        # Add padding to top for labels
        max_val = results_df['Leads Required'].max()
        fig_leads.update_layout(
            yaxis=dict(range=[0, max_val * 1.15])  # Add 15% padding at top
        )
        st.plotly_chart(fig_leads, use_container_width=True)
    
    # Comparison bar chart: Amount to Spend vs Amount to Disburse
    col1, col2 = st.columns(2)
    
    with col1:
        # Create comparison dataframe
        comparison_df = results_df[['Channel', 'Marketing Spend (₹ Lakhs)', 'Amount to Disburse (₹ Lakhs)']].copy()
        comparison_df_melted = comparison_df.melt(
            id_vars='Channel',
            value_vars=['Marketing Spend (₹ Lakhs)', 'Amount to Disburse (₹ Lakhs)'],
            var_name='Type',
            value_name='Amount (₹ Lakhs)'
        )
        
        fig_comparison = px.bar(
            comparison_df_melted,
            x='Channel',
            y='Amount (₹ Lakhs)',
            color='Type',
            title='Spend vs Disburse Comparison by Channel',
            barmode='group',
            color_discrete_map={
                'Marketing Spend (₹ Lakhs)': '#EF553B',
                'Amount to Disburse (₹ Lakhs)': '#00CC96'
            },
            text='Amount (₹ Lakhs)'
        )
        fig_comparison.update_traces(texttemplate='₹%{text:.2f}L', textposition='outside')
        # Add padding to top for labels
        max_val = comparison_df_melted['Amount (₹ Lakhs)'].max()
        fig_comparison.update_layout(
            xaxis_title="Channel",
            yaxis_title="Amount (₹ Lakhs)",
            yaxis=dict(range=[0, max_val * 1.15]),  # Add 15% padding at top
            legend_title="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col2:
        # ROI comparison
        roi_df = results_df.copy()
        roi_df['ROI'] = (roi_df['Amount to Disburse (₹ Lakhs)'] / roi_df['Marketing Spend (₹ Lakhs)']).replace([float('inf'), -float('inf')], 0)
        
        fig_roi = px.bar(
            roi_df.sort_values('ROI', ascending=True),
            x='ROI',
            y='Channel',
            orientation='h',
            title='Return on Investment by Channel',
            color='ROI',
            color_continuous_scale='Greens',
            text='ROI'
        )
        fig_roi.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
        # Add padding to right for labels
        max_val = roi_df['ROI'].max()
        fig_roi.update_layout(
            showlegend=False,
            xaxis=dict(range=[0, max_val * 1.15])  # Add 15% padding on right
        )
        st.plotly_chart(fig_roi, use_container_width=True)
else:
    st.info("Add channels to see the charts.")

st.markdown("---")

# Section 3: Key Insights & Recommendations
st.header("💡 Key Insights")

if len(results_df) > 0:
    # Calculate insights
    roi_df = results_df.copy()
    roi_df['ROI'] = (roi_df['Amount to Disburse (₹ Lakhs)'] / roi_df['Marketing Spend (₹ Lakhs)']).replace([float('inf'), -float('inf')], 0)
    
    # Find best and worst performing channels
    max_roi = roi_df['ROI'].max()
    min_roi = roi_df['ROI'].min()
    
    best_roi_channels = roi_df[roi_df['ROI'] == max_roi]['Channel'].tolist()
    worst_roi_channels = roi_df[roi_df['ROI'] == min_roi]['Channel'].tolist()
    
    highest_spend_channel = results_df.loc[results_df['Marketing Spend (₹ Lakhs)'].idxmax(), 'Channel']
    
    col1, col2 = st.columns(2)
    
    with col1:
        best_channels_text = ', '.join(best_roi_channels) if len(best_roi_channels) > 1 else best_roi_channels[0]
        st.info(f"""
        **🏆 Best Performing Channel{'s' if len(best_roi_channels) > 1 else ''}**
        
        {best_channels_text} show{'s' if len(best_roi_channels) == 1 else ''} the highest ROI of {max_roi:.2f}x
        """)
        
        worst_channels_text = ', '.join(worst_roi_channels) if len(worst_roi_channels) > 1 else worst_roi_channels[0]
        st.warning(f"""
        **⚠️ Channel{'s' if len(worst_roi_channels) > 1 else ''} Requiring Attention**
        
        {worst_channels_text} ha{'s' if len(worst_roi_channels) == 1 else 've'} the lowest ROI of {min_roi:.2f}x
        """)
    
    with col2:
        total_spend = results_df['Marketing Spend (₹ Lakhs)'].sum()
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
else:
    st.info("Add channels to see insights and recommendations.")

# Footer
st.markdown("---")
st.markdown("")
