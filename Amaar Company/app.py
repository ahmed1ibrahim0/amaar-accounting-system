import streamlit as st
import pandas as pd
import os

# ================== 1. إعداد الصفحة واللوجو ==================
logo_path = r"C:\Users\Lapcell\OneDrive\Desktop\Amaar Company\logo.png"
st.set_page_config(
    page_title="شركة عمار حميد سعد المالكي",
    page_icon=logo_path if os.path.exists(logo_path) else None,
    layout="wide"
)

# ================== الهيدر ==================
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=100)
with col2:
    st.markdown("""
    <div class='header'>شركة عمار حميد سعد المالكي<br><span style='font-size:18px;'>نظام ميزان المراجعة التحليلي والتدقيق الآلي</span></div>
    """, unsafe_allow_html=True)

# ================== اسم الشركة ==================
if "company_name" not in st.session_state:
    st.session_state.company_name = ""

st.markdown("### 🏢 اسم الشركة")
company_name = st.text_input(
    "اسم الشركة المتعامل معها",
    value=st.session_state.company_name,
    placeholder="اكتب اسم الشركة هنا..."
)
if company_name:
    st.session_state.company_name = company_name

# ================== 2. Session State ==================
if "detailed_ledger" not in st.session_state:
    groups = [
    "المجموعة الأولى: النقدية",
    "المجموعة الثانية: الذمم المدينة",
    "المجموعة الثالثة: المخزون",
    "المجموعة الرابعة: الأصول المتداولة",
    "المجموعة الخامسة: الإيرادات المستحقة",
    "المجموعة السادسة: المصاريف المقدمة",
    "المجموعة السابعة: الأصول الثابتة",
    "المجموعة الثامنة: الأصول غير الملموسة",
    "المجموعة التاسعة: عقارات استثمارية",  
    "المجموعة العاشرة: الذمم الدائنة",
    "المجموعة الحادية عشر: مجمعات الاستهلاك",
    "المجموعة الثانية عشر: المخصصات",
    "المجموعة الثالثة عشر: القروض قصيرة الأجل",
    "المجموعة الرابعة عشر: القروض طويلة الأجل",
    "المجموعة الخامسة عشر: الإيرادات المقدمة",
    "المجموعة السادسة عشر: المصاريف المستحقة",
    "المجموعة السابعة عشر: أطراف ذات علاقة",
    "المجموعة الثامنة عشر: حقوق الملكية",
    "المجموعة التاسعة عشر: حسابات الأرباح المبقاة",
    "المجموعة العشرون: المبيعات",
    "المجموعة الواحد وعشرون: المشتريات",
    "المجموعة الاثنين وعشرون: المصروفات الإدارية والعمومية",
    "المجموعة الثالثة وعشرون: المصروفات البيعية والتسويقية",
    "المجموعة الرابعة وعشرون: مصروفات المخصصات والاستهلاكات",
    "المجموعة الخامسة وعشرون: العملاء",
    "المجموعة السادسة وعشرون: الموردين",
    "المجموعة السابعة وعشرون: تكلفة المبيعات",
    "المجموعة الثامنة وعشرون: ضريبة القيمة المضافة",
    "المجموعة التاسعة وعشرون: إجمالي الربح",
    "المجموعة الثلاثون: أخرى",  
    "المجموعة الحادية والثلاثون: التوريدات الضريبية",
    "المجموعة الثانية والثلاثون: المدخلات الضريبية"
]

    st.session_state.detailed_ledger = {g: [] for g in groups}

# ================== 3. تحسين الشكل ==================
st.markdown("""
<style>
/* اتجاه الصفحة وخط */
.stApp { direction: rtl; font-family: 'Cairo', sans-serif; background:#fff8f0; }

/* الهيدر */
.header {
    background: linear-gradient(90deg, #ff9966, #ff5e62);
    padding: 15px;
    border-radius: 15px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    margin-bottom:20px;
}

/* عناوين المجموعات */
.group-header { 
    background:#ffe6cc; 
    font-weight:bold; 
    padding:8px; 
    border-radius:10px;
    border:1px solid #e6b89c; 
    text-align:center; 
    color:#663300;
    box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    margin-bottom:5px;
}

/* بطاقات الحسابات */
.account-row {
    padding:6px 12px; 
    margin:4px 0; 
    border-left:5px solid #ffb84d; 
    background:#fff2e6; 
    border-radius:10px;
    box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
    transition: all 0.2s;
}
.account-row:hover { 
    background:#ffd9b3; 
    transform: scale(1.02);
}

/* بطاقة التحليلات */
.ratio-card {
    border: 2px solid #ffa64d;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    background: linear-gradient(120deg, #fff2e6, #ffe6cc);
    box-shadow: 2px 2px 12px rgba(0,0,0,0.15);
}
.ratio-title { font-size: 22px; font-weight: bold; color:#994d00; }
.ratio-value { font-size: 18px; margin-top: 6px; color:#663300; }
.ratio-percent { font-size: 28px; font-weight: bold; color: #b45f06; }

/* الأعمدة */
.stColumns [data-testid="stColumn"] { padding: 0 6px; }

/* الإجمالي */
.total-header { 
    background:#ffd699; 
    font-weight:bold; 
    padding:15px; 
    border-radius:12px;
    border:2px solid #cc7a00; 
    text-align:center; 
    color:#663300;
    font-size:18px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ================== 4. إدخال البيانات ==================
with st.sidebar:
    st.header("📥 إدخال الحساب")
    g = st.selectbox("المجموعة", list(st.session_state.detailed_ledger.keys()))
    name = st.text_input("اسم الحساب")
    c1, c2 = st.columns(2)
    op_dr = c1.number_input("أول المدة مدين", 0.0)
    op_cr = c2.number_input("أول المدة دائن", 0.0)
    c3, c4 = st.columns(2)
    mv_dr = c3.number_input("حركة مدين", 0.0)
    mv_cr = c4.number_input("حركة دائن", 0.0)
    c5, c6 = st.columns(2)
    ad_dr = c5.number_input("تسوية مدين", 0.0)
    ad_cr = c6.number_input("تسوية دائن", 0.0)

    if st.button("➕ إضافة"):
        if name:
            st.session_state.detailed_ledger[g].append({
                "name": name,
                "op_dr": op_dr, "op_cr": op_cr,
                "mv_dr": mv_dr, "mv_cr": mv_cr,
                "ad_dr": ad_dr, "ad_cr": ad_cr
            })
            st.rerun()
        else:
            st.error("اكتب اسم الحساب")

# ================== 5. ledger → DataFrame ==================
def ledger_to_df(ledger):
    rows = []
    for g, accs in ledger.items():
        for a in accs:
            rows.append({
                "المجموعة": g,
                "الحساب": a["name"],
                "أول المدة مدين": a["op_dr"],
                "أول المدة دائن": a["op_cr"],
                "حركة مدين": a["mv_dr"],
                "حركة دائن": a["mv_cr"],
                "تسوية مدين": a["ad_dr"],
                "تسوية دائن": a["ad_cr"]
            })
    return pd.DataFrame(rows)

# ================== 6. تعديل الحسابات ==================
st.subheader("✏️ تعديل الحسابات")
ledger_df = ledger_to_df(st.session_state.detailed_ledger)
edited_df = st.data_editor(ledger_df, num_rows="dynamic", use_container_width=True)

if st.button("💾 حفظ التعديلات"):
    new_ledger = {g: [] for g in st.session_state.detailed_ledger}
    for _, r in edited_df.iterrows():
        new_ledger[r["المجموعة"]].append({
            "name": r["الحساب"],
            "op_dr": r["أول المدة مدين"],
            "op_cr": r["أول المدة دائن"],
            "mv_dr": r["حركة مدين"],
            "mv_cr": r["حركة دائن"],
            "ad_dr": r["تسوية مدين"],
            "ad_cr": r["تسوية دائن"]
        })
    st.session_state.detailed_ledger = new_ledger
    st.success("تم حفظ التعديلات بنجاح ✅")

# ================== 7 & 8. العرض (تعديل لفصل المجموعتين 31 و30) ==================
# أولاً، نفصل المجموعات العادية عن المجموعتين 29 و30
main_groups = {g: accs for g, accs in st.session_state.detailed_ledger.items()
               if g not in ["المجموعة الحادية والثلاثون: التوريدات الضريبية",
                            "المجموعة الثانية والثلاثون: المدخلات الضريبية"]}
tax_groups = {g: accs for g, accs in st.session_state.detailed_ledger.items()
              if g in ["المجموعة الحادية والثلاثون: التوريدات الضريبية",
                       "المجموعة الثانية والثلاثون: المدخلات الضريبية"]}

# ===== العرض الأساسي (بدون المجموعتين 29 و30) =====
headers = ["الحساب","أول المدة مدين","أول المدة دائن",
           "حركة مدين","حركة دائن","تسوية مدين","تسوية دائن",
           "آخر المدة مدين","آخر المدة دائن"]
cols = st.columns([2,1,1,1,1,1,1,1,1])
for c,h in zip(cols, headers):
    c.markdown(f"**{h}**")

g_op_dr=g_op_cr=g_mv_dr=g_mv_cr=g_ad_dr=g_ad_cr=0

for gname, accs in main_groups.items():
    t_op_dr = sum(a["op_dr"] for a in accs)
    t_op_cr = sum(a["op_cr"] for a in accs)
    t_mv_dr = sum(a["mv_dr"] for a in accs)
    t_mv_cr = sum(a["mv_cr"] for a in accs)
    t_ad_dr = sum(a["ad_dr"] for a in accs)
    t_ad_cr = sum(a["ad_cr"] for a in accs)
    net = (t_op_dr+t_mv_dr+t_ad_dr)-(t_op_cr+t_mv_cr+t_ad_cr)
    t_end_dr=max(net,0)
    t_end_cr=max(-net,0)

    g_op_dr+=t_op_dr; g_op_cr+=t_op_cr
    g_mv_dr+=t_mv_dr; g_mv_cr+=t_mv_cr
    g_ad_dr+=t_ad_dr; g_ad_cr+=t_ad_cr

    cols = st.columns([2,1,1,1,1,1,1,1,1])
    values = [gname,t_op_dr,t_op_cr,t_mv_dr,t_mv_cr,t_ad_dr,t_ad_cr,t_end_dr,t_end_cr]
    for c,v in zip(cols, values):
        c.markdown(f"<div class='group-header'>{v:,.0f}</div>" if isinstance(v,(int,float)) else f"<div class='group-header'>{v}</div>", unsafe_allow_html=True)

    for a in accs:
        net=(a["op_dr"]+a["mv_dr"]+a["ad_dr"])-(a["op_cr"]+a["mv_cr"]+a["ad_cr"])
        end_dr=max(net,0)
        end_cr=max(-net,0)
        cols=st.columns([2,1,1,1,1,1,1,1,1])
        vals=["• "+a["name"],a["op_dr"],a["op_cr"],a["mv_dr"],a["mv_cr"],a["ad_dr"],a["ad_cr"],end_dr,end_cr]
        for c,v in zip(cols,vals):
            c.markdown(f"<div class='account-row'>{v:,.0f}</div>" if isinstance(v,(int,float)) else f"<div class='account-row'>{v}</div>", unsafe_allow_html=True)

# ===== الإجمالي العام (بدون المجموعتين 29 و30) =====
g_end_dr=g_op_dr+g_mv_dr+g_ad_dr
g_end_cr=g_op_cr+g_mv_cr+g_ad_cr

cols=st.columns([2,1,1,1,1,1,1,1,1])
totals=["الإجمالي العام",g_op_dr,g_op_cr,g_mv_dr,g_mv_cr,g_ad_dr,g_ad_cr,g_end_dr,g_end_cr]
for c,v in zip(cols,totals):
    c.markdown(f"<div class='total-header'>{v:,.0f}</div>" if isinstance(v,(int,float)) else f"<div class='total-header'>{v}</div>", unsafe_allow_html=True)

difference=abs(g_end_dr-g_end_cr)
if difference!=0:
    st.error("⚠️ ميزان المراجعة غير متزن")
    st.metric("فرق الميزان", f"{difference:,.0f}")
else:
    st.success("✅ ميزان المراجعة متزن")

# ===== عرض المجموعتين 29 و30 بشكل مستقل =====
if tax_groups:
    st.divider()
    st.subheader("📌 المجموعتين الضريبية ")

    cols = st.columns([2,1,1,1,1,1,1,1,1])
    for c,h in zip(cols, headers):
        c.markdown(f"**{h}**")

    for gname, accs in tax_groups.items():
        t_op_dr = sum(a["op_dr"] for a in accs)
        t_op_cr = sum(a["op_cr"] for a in accs)
        t_mv_dr = sum(a["mv_dr"] for a in accs)
        t_mv_cr = sum(a["mv_cr"] for a in accs)
        t_ad_dr = sum(a["ad_dr"] for a in accs)
        t_ad_cr = sum(a["ad_cr"] for a in accs)
        net = (t_op_dr+t_mv_dr+t_ad_dr)-(t_op_cr+t_mv_cr+t_ad_cr)
        t_end_dr=max(net,0)
        t_end_cr=max(-net,0)

        cols = st.columns([2,1,1,1,1,1,1,1,1])
        values = [gname,t_op_dr,t_op_cr,t_mv_dr,t_mv_cr,t_ad_dr,t_ad_cr,t_end_dr,t_end_cr]
        for c,v in zip(cols, values):
            c.markdown(f"<div class='group-header'>{v:,.0f}</div>" if isinstance(v,(int,float)) else f"<div class='group-header'>{v}</div>", unsafe_allow_html=True)

        for a in accs:
            net=(a["op_dr"]+a["mv_dr"]+a["ad_dr"])-(a["op_cr"]+a["mv_cr"]+a["ad_cr"])
            end_dr=max(net,0)
            end_cr=max(-net,0)
            cols=st.columns([2,1,1,1,1,1,1,1,1])
            vals=["• "+a["name"],a["op_dr"],a["op_cr"],a["mv_dr"],a["mv_cr"],a["ad_dr"],a["ad_cr"],end_dr,end_cr]
            for c,v in zip(cols,vals):
                c.markdown(f"<div class='account-row'>{v:,.0f}</div>" if isinstance(v,(int,float)) else f"<div class='account-row'>{v}</div>", unsafe_allow_html=True)



st.divider()
st.subheader("➡️ التحليلات")
if st.button("💰 الانتقال إلى تحليل النقدية"):
    st.switch_page("pages/cash_analysis.py")
