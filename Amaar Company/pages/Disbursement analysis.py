import streamlit as st
import pandas as pd
import os

# ======================================================
# 1️⃣ إعداد الصفحة واللوجو
# ======================================================
logo_path = "logo.png"

st.set_page_config(
    page_title="تحليل منصرف  النقدية",
    page_icon=logo_path if os.path.exists(logo_path) else None,
    layout="wide"
)

# ======================================================
# 2️⃣ الهيدر
# ======================================================
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)

with col2:
    st.markdown("""
    <div class='header'>
        تحليل منصرف النقدية<br>
        <span style='font-size:18px;'>مستخرج مباشرة من ميزان المراجعة</span>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 3️⃣ CSS
# ======================================================
st.markdown("""
<style>
.stApp {
    direction: rtl;
    font-family: 'Cairo', sans-serif;
    background:#fff8f0;
}

/* الهيدر */
.header {
    background: linear-gradient(90deg, #ff9966, #ff5e62);
    padding: 18px;
    border-radius: 15px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    margin-bottom:20px;
}

/* بطاقة رقم */
.metric-card {
    background: linear-gradient(120deg,#fff2e6,#ffe6cc);
    border:2px solid #ffa64d;
    border-radius:14px;
    padding:15px;
    text-align:center;
    font-weight:bold;
    box-shadow:2px 2px 12px rgba(0,0,0,0.15);
    margin-bottom:20px;
}

/* جدول */
.cash-row {
    display:grid;
    grid-template-columns: 2.5fr 1fr 1fr 1fr;
    background:#fff2e6;
    border-left:6px solid #ffb84d;
    border-radius:12px;
    padding:10px;
    margin-bottom:6px;
    box-shadow:1px 1px 6px rgba(0,0,0,0.08);
    transition:0.2s;
}
.cash-row:hover { transform:scale(1.01); background:#ffd9b3; }

.cash-header {
    background:#ffe0b3;
    font-weight:bold;
    border:2px solid #cc7a00;
}

.total-row {
    background:linear-gradient(120deg,#ffd699,#ffcc80);
    font-weight:bold;
    border:2px solid #cc7a00;
}

/* CSS للـ NumberInput */
div[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
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
# 5️⃣ النقدية المتحصلة
# ======================================================
collected_cash = sum(a.get("mv_cr", 0) for a in ledger.get("المجموعة الأولى: النقدية", []))

st.markdown(f"""
<div class="metric-card">
    💵 منصرف النقدية<br>
    <span style="font-size:26px;">{collected_cash:,.2f}</span>
</div>
""", unsafe_allow_html=True)

# ======================================================
# 6️⃣ مصادر النقدية
# ======================================================
sources_map = [
    {"code":201,"name":"الموردين", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الخامسة وعشرون: الموردين", []))},
    {"code":202,"name":"مشتريات ", "compute": lambda l: max(sum(a.get("mv_dr",0) for a in l.get("المجموعة العشرون: المشتريات", [])) - sum(a.get("mv_dr",0) for a in l.get("المجموعة الخامسة وعشرون: الموردين", [])),0)},
    {"code":203,"name":"أصول متداولة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الرابعة: الأصول المتداولة", []))},
    {"code":204,"name":"ذمم مدينة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الثانية: الذمم المدينة", []))},
    {"code":205,"name":"أصول ثابتة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة السابعة: الأصول الثابتة", []))},
    {"code":206,"name":"أصول غير ملموسة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الثامنة: الأصول غير الملموسة", []))},
    {"code":207,"name":"عقارات استثمارية", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة التاسعة: عقارات استثمارية", []))},
    {"code":208,"name":"مصروف مدفوع مقدم", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة السادسة: المصاريف المقدمة", []))},
    {"code":209,"name":"قروض قصيرة الأجل", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الثانية عشر: القروض قصيرة الأجل", []))},
    {"code":210,"name":"قروض طويلة الأجل", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الثالثة عشر: القروض طويلة الأجل", []))},
    {"code":211,"name":"مصروفات مستحقة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الخامسة عشر: المصاريف المستحقة", []))},
    {"code":212,"name":"إيراد مقدم", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الرابعة عشر: الإيرادات المقدمة", []))},
    {"code":213,"name":"إيراد مستحق", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الخامسة: الإيرادات المستحقة", []))},
    {"code":214,"name":"حقوق الملكية", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة السابعة عشر: حقوق الملكية", []))},
    {"code":215,"name":"مصروفات إدارية وعمومية", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الواحد وعشرون: المصروفات الإدارية والعمومية", []))},
    {"code":216,"name":"مصروفات بيع وتسويقية", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الاثنين وعشرون: المصروفات البيعية والتسويقية", []))},
    {"code":217,"name":"ضريبة القيمة المضافة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة السابعة وعشرون: ضريبة القيمة المضافة", []))},
    {"code":218,"name":"تكلفة المبيعات", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة السادسة وعشرون: تكلفة المبيعات", []))},
    {"code":219,"name":"الأرباح المبقاة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة الثامنة عشر: حسابات الأرباح المبقاة", []))},
    {"code":220,"name":"أطراف ذات علاقة", "compute": lambda l: sum(a.get("mv_dr",0) for a in l.get("المجموعة السادسة عشر: أطراف ذات علاقة", []))}
]

# ======================================================
# 7️⃣ تجهيز DataFrame
# ======================================================
rows=[]
for s in sources_map:
    amt = float(s["compute"](ledger))
    pct = (amt / collected_cash * 100) if collected_cash else 0
    rows.append({"name": s["name"], "amount": amt, "percent": pct})

df = pd.DataFrame(rows)
total_amount = df["amount"].sum()
deviation_value = collected_cash - total_amount

# ======================================================
# 8️⃣ معامل الانحراف
# ======================================================
if "multible_deviation" not in st.session_state:
    st.session_state.multible_deviation = 1.0

multiplier = st.number_input(
    label="معامل الانحراف",
    min_value=1.0,
    max_value=5.0,
    step=0.1,
    value=st.session_state.multible_deviation,
    key="multible_deviation",
    label_visibility="collapsed"
)

adjusted_deviation_value = deviation_value * multiplier
df["deviation_value"] = df["percent"] / df["percent"].sum() * adjusted_deviation_value if df["percent"].sum() else 0

# ======================================================
# 9️⃣ عرض الجدول
# ======================================================
st.subheader("📊 تحليل مصادر النقدية")

st.markdown("""
<div class="cash-row cash-header">
    <div>البند</div>
    <div>المبلغ</div>
    <div>النسبة</div>
    <div>الانحراف</div>
</div>
""", unsafe_allow_html=True)

for _, r in df.iterrows():
    st.markdown(f"""
    <div class="cash-row">
        <div>{r['name']}</div>
        <div>{r['amount']:,.2f}</div>
        <div>{r['percent']:.2f}%</div>
        <div>{r['deviation_value']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 10️⃣ صف الإجمالي
# ======================================================
total_percent = df["percent"].sum()
st.markdown(f"""
<div class="cash-row total-row">
    <div>الإجمالي</div>
    <div>{total_amount:,.2f}</div>
    <div>{total_percent:.2f}%</div>
    <div>{adjusted_deviation_value:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# 11️⃣ بطاقة مستوى الانحراف
# ======================================================
deviation_percent = 100 - total_percent
st.markdown(f"""
<div class="cash-row total-row">
    <div> مستوى الانحراف</div>
    <div>{deviation_value:,.2f}</div>
    <div>{deviation_percent:.2f}%</div>
    <div></div>
</div>
""", unsafe_allow_html=True)


st.divider()
st.subheader("➡️ التقرير")
if st.button(" الانتقال إلى  التقرير"):
    st.switch_page("pages/report.py")

