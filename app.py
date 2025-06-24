import streamlit as st
import pandas as pd
import re
import fitz
from io import BytesIO
from collections import defaultdict
import time

# === Streamlit Config ===
st.set_page_config(
    page_title="Reliance GRN Parser Pro", 
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📦"
)

# === Enhanced CSS for Modern UI ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.main {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.stApp {
    background: transparent;
}

/* Header Styling */
.main-header {
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    text-align: center;
}

.main-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-subtitle {
    font-size: 1.2rem;
    color: #64748b;
    font-weight: 400;
    margin-bottom: 0;
}

/* Card Styling */
.glass-card {
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin-bottom: 2rem;
}

.upload-zone {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border: 2px dashed #667eea;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.upload-zone:hover {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
}

/* Metrics Cards */
.metrics-container {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
}

.metric-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(15px);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    flex: 1;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    background: rgba(255, 255, 255, 0.98);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    display: block;
}

.metric-label {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a67d8 0%, #6b5b95 100%);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Secondary Button */
.secondary-btn {
    background: rgba(148, 163, 184, 0.1) !important;
    color: #64748b !important;
    border: 2px solid rgba(148, 163, 184, 0.3) !important;
}

.secondary-btn:hover {
    background: rgba(148, 163, 184, 0.2) !important;
    color: #475569 !important;
}

/* Download Button Special Styling */
.download-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
}

.download-btn:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
}

/* Progress Bar */
.stProgress .st-bo {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

/* Data Table */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(102, 126, 234, 0.1);
    border-radius: 12px;
    font-weight: 600;
    color: #4338ca;
}

/* Success/Warning Messages */
.stSuccess {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 12px;
    color: #059669;
}

.stWarning {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    color: #d97706;
}

/* File Uploader Styling */
.stFileUploader label {
    font-weight: 600;
    color: #374151;
    margin-bottom: 1rem;
}

/* Animation Classes */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeInUp 0.6s ease-out;
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-title {
        font-size: 2rem;
    }
    
    .metrics-container {
        flex-direction: column;
    }
    
    .metric-card {
        margin-bottom: 1rem;
    }
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# === Session State Initialization ===
if 'df_result' not in st.session_state:
    st.session_state.df_result = None
if 'file_count' not in st.session_state:
    st.session_state.file_count = 0
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# === Utility Functions ===
def clean_text(text):
    return text.strip().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')

def extract_text_from_pdf(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except:
        return ""

def extract_grn_data(text):
    metadata = {
        "GRN No": None, "GRN Date": None, "Vendor Invoice No": None, "PO No": None,
        "PO Date": None, "Consignee Location": None, "Truck No": None, "Challan No": None
    }

    patterns = {
        "GRN No": r'GOODS RECEIPT NOTE No\.\s*:\s*(\S+)',
        "GRN Date": r'Date:\s*(\d{2}\.\d{2}\.\d{4})',
        "Vendor Invoice No": r'Vendor invoice no\s*:\s*(\S+)',
        "Consignee Location": r'Consignee\s*:\s*([^\n]+)\n',
        "PO No": r'PO Number\s*:\s*(\S+)',
        "PO Date": r'PO Number.*?Date\s*:\s*(\d{2}\.\d{2}\.\d{4})|(?<!\S)Date\s*:\s*(\d{2}\.\d{2}\.\d{4})',
        "Truck No": r'Truck/ Lorry/ Carrier No:\s*(\S+)',
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata[key] = match.group(1) or match.group(2)

    if metadata["Vendor Invoice No"]:
        metadata["Challan No"] = metadata["Vendor Invoice No"]

    items = []
    table_start = re.search(r'S No\s+Article', text, re.IGNORECASE)
    if table_start:
        table_text = text[table_start.start():]
        # Updated pattern to handle multi-line descriptions
        item_pattern = re.compile(
            r'(\d+)\s+(\d+)\s+([\w\s\.\-%#]+?)\s+(\d{13})\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d\.]+)\b'
        )
        for match in item_pattern.finditer(table_text):
            # Clean description by collapsing extra spaces
            description = re.sub(r'\s+', ' ', match.group(3).strip())
            items.append({
                "S No": match.group(1), 
                "Article": match.group(2), 
                "Item Description": description,
                "EAN Number": match.group(4), 
                "UoM": match.group(5), 
                "Challan Qty": match.group(6),
                "Received Qty": match.group(7), 
                "Accepted Qty": match.group(8), 
                "MRP": match.group(9)
            })

    return metadata, items

# === Header Section ===
st.markdown("""
<div class="main-header animate-fade-in">
    <h1 class="main-title">📦 GRN Parser Pro</h1>
    <p class="main-subtitle">Transform your Goods Receipt Note PDFs into organized Excel data with advanced parsing technology</p>
</div>
""", unsafe_allow_html=True)

# === Upload Section ===
st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="upload-zone">
        <h3 style="color: #667eea; margin-bottom: 1rem;">📁 Upload Your GRN PDFs</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">Select multiple PDF files to process them all at once</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)

# === File Metrics ===
if uploaded_files:
    st.session_state.file_count = len(uploaded_files)
    
    st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
    st.markdown("### 📊 Upload Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{len(uploaded_files)}</span>
            <div class="metric-label">Files Uploaded</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_size = sum(file.size for file in uploaded_files) / (1024 * 1024)
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{total_size:.2f}</span>
            <div class="metric-label">Total Size (MB)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_size = total_size / len(uploaded_files)
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{avg_size:.2f}</span>
            <div class="metric-label">Avg Size (MB)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === Processing Section ===
    st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Process All PDFs", key="process_btn"):
            with st.spinner("🔄 Processing your files..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                all_data = []
                
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"Processing: {file.name}")
                    
                    text = extract_text_from_pdf(file.read())
                    metadata, items = extract_grn_data(text)
                    
                    if not items:
                        row = defaultdict(lambda: "")
                        row.update(metadata)
                        row["file_name"] = file.name
                        all_data.append(row)
                    else:
                        for item in items:
                            row = {**metadata, **item, "file_name": file.name}
                            all_data.append(row)
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    time.sleep(0.1)  # Small delay for better UX
                
                status_text.text("✅ Processing complete!")
                
                if all_data:
                    st.session_state.df_result = pd.DataFrame(all_data)
                    st.session_state.processing_complete = True
                    st.success("🎉 All files processed successfully!")
                else:
                    st.session_state.df_result = pd.DataFrame()
                    st.warning("⚠️ No data could be extracted from the uploaded files.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# === Results Section ===
if st.session_state.df_result is not None and st.session_state.processing_complete:
    df = st.session_state.df_result
    
    st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
    st.markdown("### 📈 Processing Results")
    
    if not df.empty:
        # Results metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{len(df)}</span>
                <div class="metric-label">Total Records</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            unique_grns = df['GRN No'].nunique() if 'GRN No' in df.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{unique_grns}</span>
                <div class="metric-label">Unique GRNs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unique_pos = df['PO No'].nunique() if 'PO No' in df.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{unique_pos}</span>
                <div class="metric-label">Purchase Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            success_rate = (len(df[df['GRN No'].notna()]) / len(df) * 100) if len(df) > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{success_rate:.1f}%</span>
                <div class="metric-label">Success Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data Preview
        st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
        with st.expander("🔍 Preview Extracted Data", expanded=True):
            st.dataframe(df, use_container_width=True, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Section
        st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
        st.markdown("### 📥 Download Your Data")
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="GRN_Data")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                "📊 Download Excel File",
                data=output.getvalue(),
                file_name=f"grn_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_btn"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
        st.warning("⚠️ No valid data could be extracted from the uploaded files. Please check your PDF format and try again.")
        st.markdown('</div>', unsafe_allow_html=True)

# === Reset Section ===
if st.session_state.df_result is not None or uploaded_files:
    st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start Over", key="reset_btn"):
            st.session_state.df_result = None
            st.session_state.file_count = 0
            st.session_state.processing_complete = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# === Footer ===
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">
    <p>Made with ❤️ using Streamlit | GRN Parser Pro v2.0</p>
</div>
""", unsafe_allow_html=True)