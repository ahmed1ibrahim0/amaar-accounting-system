import streamlit as st
import pandas as pd
import os
import io

# ======================================================
# 1️⃣ إعداد الصفحة
# ======================================================
logo_path = r"C:\Users\Lapcell\OneDrive\Desktop\Amaar Company\logo.png"

st.set_page_config(
    page_title="التقرير النهائي",
    page_icon=logo_path if os.path.exists(logo_path) else None,
    layout="wide"
)

# ======================================================
# 2️⃣ الهيدر
# ======================================================
col1, col2 = st.columns([1,5])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)

with col2:
    st.markdown("""
    <div class='header'>
        📊 التقرير النهائي للتحليل النقدي
        <br>
        <span style='font-size:18px;'>ملخص شامل للأداء المالي</span>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# اسم الشركة
# ======================================================
company_name = st.session_state.get("company_name", "")

if company_name:
    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:36px;
        font-weight:bold;
        color:#b34700;
        margin-bottom:30px;
    ">
        {company_name}
    </div>
    """, unsafe_allow_html=True)


# ======================================================
# 3️⃣ CSS (نفس الاستايل)
# ======================================================
st.markdown("""
<style>
.stApp { direction: rtl; font-family: 'Cairo', sans-serif; background:#fff8f0; }

.header {
    background: linear-gradient(90deg, #ff9966, #ff5e62);
    padding: 18px;
    border-radius: 15px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    margin-bottom:25px;
}

.card {
    background: linear-gradient(120deg,#fff2e6,#ffe6cc);
    border:2px solid #ffa64d;
    border-radius:14px;
    padding:20px;
    text-align:center;
    font-weight:bold;
    box-shadow:2px 2px 12px rgba(0,0,0,0.15);
    margin-bottom:20px;
}

.big-number {
    font-size:28px;
    margin-top:10px;
    color:#994d00;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# 4️⃣ التأكد من البيانات
# ======================================================
if "detailed_ledger" not in st.session_state:
    st.error("⚠️ لا توجد بيانات ميزان مراجعة")
    st.stop()

ledger = st.session_state.detailed_ledger

# ======================================================
# 5️⃣ حساب المتحصل والمنصرف
# ======================================================
collected_cash = sum(a.get("mv_dr",0) for a in ledger.get("المجموعة الأولى: النقدية", []))
disbursed_cash = sum(a.get("mv_cr",0) for a in ledger.get("المجموعة الأولى: النقدية", []))

net_cash_flow = collected_cash - disbursed_cash

# ======================================================
# 6️⃣ عرض الكروت
# ======================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        💰 النقدية المتحصلة
        <div class="big-number">{collected_cash:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        💸 النقدية المنصرفة
        <div class="big-number">{disbursed_cash:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        📈 صافي التدفق النقدي
        <div class="big-number">{net_cash_flow:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 7️⃣ مستوى الأداء
# ======================================================
st.divider()

if net_cash_flow > 0:
    st.success("✅ الشركة تحقق تدفق نقدي موجب")
elif net_cash_flow < 0:
    st.error("⚠️ الشركة لديها عجز نقدي")
else:
    st.info("➖ لا يوجد صافي تغير نقدي")

# ======================================================
