import streamlit as st
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

CITIES = {
    "Bangalore": {
        "areas": {
            "Koramangala":  {"avg_rent": 25000, "safety": 4, "commute": 3, "social": 5, "gym": True,  "temple": True,  "desc": "Startup hub · cafes · nightlife",         "landmark": "Forum Mall"},
            "HSR Layout":   {"avg_rent": 22000, "safety": 5, "commute": 4, "social": 4, "gym": True,  "temple": True,  "desc": "Planned, family-friendly, parks",          "landmark": "HSR BDA Complex"},
            "Whitefield":   {"avg_rent": 18000, "safety": 4, "commute": 2, "social": 3, "gym": True,  "temple": True,  "desc": "IT hub · malls · expat community",         "landmark": "Phoenix Marketcity"},
        }
    },
    "Mumbai": {
        "areas": {
            "Andheri West": {"avg_rent": 35000, "safety": 3, "commute": 4, "social": 5, "gym": True,  "temple": True,  "desc": "Entertainment hub · metro connectivity",   "landmark": "Infiniti Mall"},
            "Powai":        {"avg_rent": 40000, "safety": 5, "commute": 3, "social": 4, "gym": True,  "temple": False, "desc": "Lakeside premium living · IT crowd",       "landmark": "Hiranandani Gardens"},
            "Thane":        {"avg_rent": 22000, "safety": 4, "commute": 3, "social": 3, "gym": True,  "temple": True,  "desc": "Affordable suburb · growing infra",        "landmark": "Viviana Mall"},
        }
    },
    "Hyderabad": {
        "areas": {
            "Gachibowli":   {"avg_rent": 20000, "safety": 4, "commute": 3, "social": 4, "gym": True,  "temple": True,  "desc": "IT corridor · upscale amenities",         "landmark": "Inorbit Mall"},
            "Banjara Hills":{"avg_rent": 30000, "safety": 5, "commute": 3, "social": 5, "gym": True,  "temple": True,  "desc": "Premium · top restaurants · boutiques",   "landmark": "Road No. 12"},
            "Kondapur":     {"avg_rent": 18000, "safety": 4, "commute": 4, "social": 3, "gym": True,  "temple": True,  "desc": "Near HITEC · value for money",            "landmark": "Sarath City Mall"},
        }
    },
    "Delhi": {
        "areas": {
            "Hauz Khas":    {"avg_rent": 32000, "safety": 3, "commute": 4, "social": 5, "gym": True,  "temple": True,  "desc": "Bohemian · art galleries · nightlife",    "landmark": "Hauz Khas Village"},
            "Dwarka":       {"avg_rent": 18000, "safety": 5, "commute": 4, "social": 3, "gym": True,  "temple": True,  "desc": "Very safe · excellent metro",             "landmark": "Ambience Mall"},
            "Lajpat Nagar": {"avg_rent": 25000, "safety": 3, "commute": 5, "social": 4, "gym": False, "temple": True,  "desc": "Central · vibrant market · metro",        "landmark": "Central Market"},
        }
    },
    "Pune": {
        "areas": {
            "Koregaon Park":{"avg_rent": 28000, "safety": 4, "commute": 3, "social": 5, "gym": True,  "temple": False, "desc": "Cosmopolitan · Osho Ashram · cafes",      "landmark": "KP Annexe"},
            "Baner":        {"avg_rent": 22000, "safety": 4, "commute": 3, "social": 4, "gym": True,  "temple": True,  "desc": "IT hub · modern apartments",              "landmark": "Balewadi High St."},
            "Viman Nagar":  {"avg_rent": 20000, "safety": 5, "commute": 4, "social": 4, "gym": True,  "temple": True,  "desc": "Near airport · upscale residential",      "landmark": "Ezone Mall"},
        }
    },
}

VENDORS = {
    "Bangalore": {
        "accommodation": "NoBroker / MagicBricks",
        "bike":    "Royal Brothers · ₹3,000/mo",
        "tiffin":  "Homely Meals · ₹2,500/mo",
        "maid":    "UrbanCompany · ₹2,500/mo",
        "gym":     "Cult.fit · ₹1,999/mo",
        "mall":    "Phoenix Marketcity",
        "temple":  "ISKCON / Bull Temple",
    },
    "Mumbai": {
        "accommodation": "NoBroker / Housing.com",
        "bike":    "Bounce · ₹4,000/mo",
        "tiffin":  "Mumbai Dabba · ₹3,500/mo",
        "maid":    "UrbanCompany · ₹3,000/mo",
        "gym":     "Cult.fit · ₹1,999/mo",
        "mall":    "Phoenix Palladium",
        "temple":  "Siddhivinayak Temple",
    },
    "Hyderabad": {
        "accommodation": "NoBroker / 99acres",
        "bike":    "Vogo · ₹1,500/mo",
        "tiffin":  "HydTiffin · ₹2,000/mo",
        "maid":    "UrbanCompany · ₹2,200/mo",
        "gym":     "Cult.fit · ₹1,999/mo",
        "mall":    "Inorbit Mall",
        "temple":  "Birla Mandir",
    },
    "Delhi": {
        "accommodation": "NoBroker / CommonFloor",
        "bike":    "Royal Brothers · ₹3,500/mo",
        "tiffin":  "Delhi Dabba · ₹2,800/mo",
        "maid":    "UrbanCompany · ₹2,500/mo",
        "gym":     "Cult.fit · ₹1,999/mo",
        "mall":    "Select City Walk",
        "temple":  "Akshardham Temple",
    },
    "Pune": {
        "accommodation": "NoBroker / MagicBricks",
        "bike":    "Royal Brothers · ₹2,800/mo",
        "tiffin":  "Pune Tiffin · ₹2,200/mo",
        "maid":    "UrbanCompany · ₹2,000/mo",
        "gym":     "Cult.fit · ₹1,999/mo",
        "mall":    "Phoenix Marketcity Pune",
        "temple":  "Dagdusheth Temple",
    },
}

ADDON_COSTS = {"bike": 3000, "tiffin": 2500, "maid": 2500, "gym": 1999}

# ─────────────────────────────────────────────
# CONFIG — update these for production
# ─────────────────────────────────────────────
WA_NUMBER  = "919999999999"          # WhatsApp number with country code, no +
WA_DEFAULT = "Hi! I saw ReloPlan and I'd like help planning my relocation."

# ─────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────

def score_area(area, budget, lifestyle):
    # Budget (40%)
    diff = area["avg_rent"] - budget
    b = 1.0 if diff <= 0 else max(0.0, 1 - diff / budget)

    # Commute (30%)
    c = area["commute"] / 5.0

    # Lifestyle (30%)
    lc = [area["safety"] / 5.0]
    if "Nightlife & Social" in lifestyle: lc.append(area["social"] / 5.0)
    if "Fitness"            in lifestyle: lc.append(1.0 if area["gym"]    else 0.0)
    if "Spiritual / Temple" in lifestyle: lc.append(1.0 if area["temple"] else 0.0)
    if "Safety"             in lifestyle: lc.append(area["safety"] / 5.0)
    l = sum(lc) / len(lc)

    return round((b * 0.40 + c * 0.30 + l * 0.30) * 100, 1)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(page_title="ReloPlan", page_icon="🏙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.main>div{padding-top:0.5rem}
footer,header,#MainMenu{display:none}
.card{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.hero{background:linear-gradient(135deg,#1e1b4b,#4c1d95);border-radius:18px;padding:2.5rem 2rem;color:#fff;text-align:center;margin-bottom:1.5rem}
.badge{display:inline-block;background:rgba(255,255,255,.15);color:#fff;border-radius:999px;padding:.2rem .8rem;font-size:.78rem;font-weight:600;margin-bottom:.75rem}
.chip{display:inline-block;background:#ede9fe;color:#6d28d9;border-radius:6px;padding:.15rem .55rem;font-size:.72rem;font-weight:700;margin:2px}
.metric{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:.75rem;text-align:center}
.cost-row{display:flex;justify-content:space-between;padding:.45rem 0;border-bottom:1px solid #f1f5f9}
.stButton>button{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border:none;border-radius:8px;font-weight:600;width:100%}
.stButton>button:hover{background:linear-gradient(135deg,#4f46e5,#7c3aed);box-shadow:0 4px 14px rgba(99,102,241,.4)}
/* WhatsApp float */
.wa-float{position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;
  background:#25d366;color:#fff;border-radius:999px;padding:.7rem 1.1rem;
  font-weight:700;font-size:.88rem;text-decoration:none;display:flex;align-items:center;gap:.4rem;
  box-shadow:0 4px 18px rgba(37,211,102,.45);transition:transform .2s}
.wa-float:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(37,211,102,.55);color:#fff;text-decoration:none}
/* Instagram form */
.ig-card{background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);
  border-radius:18px;padding:2px;margin-bottom:1.5rem}
.ig-inner{background:#fff;border-radius:16px;padding:1.5rem}
.ig-header{display:flex;align-items:center;gap:.6rem;margin-bottom:1rem}
.ig-logo{width:32px;height:32px;background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);
  border-radius:8px;display:flex;align-items:center;justify-content:center;
  font-size:1.1rem;flex-shrink:0}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────

for k, v in [("page","landing"),("fd",{}),("res",{}),("subs",[]),("admin_ok",False),("ig_leads",[])]:
    if k not in st.session_state: st.session_state[k] = v

def go(page): st.session_state.page = page; st.rerun()

# ─────────────────────────────────────────────
# NAV
# ─────────────────────────────────────────────

c = st.columns([2.5,1,1,1,1])
c[0].markdown("### 🏙️ **ReloPlan**")
with c[1]:
    if st.button("Home"):    go("landing")
with c[2]:
    if st.button("Plan Move"): go("form")
with c[3]:
    if st.button("Results"):  go("results")
with c[4]:
    if st.button("Admin"):    go("admin")
st.markdown("---")

# ── WhatsApp floating button (all pages) ──
import urllib.parse
st.markdown(
    f'<a class="wa-float" href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(WA_DEFAULT)}" '
    f'target="_blank">💬 WhatsApp Us</a>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────

if st.session_state.page == "landing":

    st.markdown("""
    <div class="hero">
      <div class="badge">✨ Smart Relocation for Modern India</div>
      <h1 style="font-size:2.6rem;margin:.4rem 0;color:#fff">Find Your Perfect City & Area</h1>
      <p style="opacity:.85;max-width:560px;margin:0 auto 1.8rem;font-size:1.05rem">
        Tell us your budget and lifestyle. We rank areas, build your starter bundle,
        and show your total monthly cost — in seconds.
      </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for col, icon, title, desc in zip(cols, ["🎯","📦","💰","⚡"],
        ["Smart Matching","Starter Bundle","Cost Breakdown","Instant Plan"],
        ["Scored on budget, commute & lifestyle","Housing, tiffin, maid, gym & more",
         "See total spend before you move","Ready in under 2 minutes"]):
        col.markdown(f"""
        <div class="card" style="text-align:center">
          <div style="font-size:1.8rem;margin-bottom:.4rem">{icon}</div>
          <div style="font-weight:700;margin-bottom:.25rem">{title}</div>
          <div style="color:#6b7280;font-size:.82rem">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,1.2,1])
    with mid:
        if st.button("🚀 Plan My Relocation →"): go("form")

    # ── Instagram Lead Form ──
    st.markdown("<br>", unsafe_allow_html=True)
    _, ig_col, _ = st.columns([1, 1.6, 1])
    with ig_col:
        st.markdown("""
        <div class="ig-card">
          <div class="ig-inner">
            <div class="ig-header">
              <div class="ig-logo">📸</div>
              <div>
                <div style="font-weight:700;font-size:.9rem">ReloPlan</div>
                <div style="color:#6b7280;font-size:.72rem">Sponsored · Get a free relocation plan</div>
              </div>
            </div>
            <p style="font-size:.88rem;color:#374151;margin-bottom:1rem">
              Moving to a new city? Drop your details and we'll send your personalised area plan instantly.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("ig_lead_form"):
            ig_name  = st.text_input("Full Name",     placeholder="Priya Mehta",    label_visibility="collapsed")
            ig_phone = st.text_input("Phone Number",  placeholder="📞 Phone Number", label_visibility="collapsed")
            ig_city  = st.selectbox("City of Interest", list(CITIES.keys()),         label_visibility="collapsed")
            ig_sub   = st.form_submit_button("📲 Send Me My Free Plan", use_container_width=True)

        if ig_sub:
            if ig_name and ig_phone:
                st.session_state.ig_leads.append({
                    "name": ig_name, "phone": ig_phone, "city": ig_city,
                    "source": "Instagram Lead Form",
                    "ts": datetime.now().strftime("%d %b %Y %H:%M"),
                })
                st.success(f"✅ Got it, {ig_name}! We'll WhatsApp your plan to {ig_phone} shortly.")
            else:
                st.warning("Please fill in your name and phone number.")

    st.markdown("### Cities Covered")
    city_cols = st.columns(5)
    icons = {"Bangalore":"🌿","Mumbai":"🌊","Hyderabad":"🍖","Delhi":"🏛️","Pune":"🎓"}
    for col,(city,icon) in zip(city_cols, icons.items()):
        col.markdown(f"""
        <div class="metric" style="margin-bottom:.5rem">
          <div style="font-size:1.6rem">{icon}</div>
          <div style="font-weight:700;font-size:.9rem">{city}</div>
          <div style="color:#6b7280;font-size:.75rem">3 areas</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: FORM
# ─────────────────────────────────────────────

elif st.session_state.page == "form":

    st.markdown("## 📋 Plan Your Relocation")
    with st.form("relo"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Basic Info**")
            name   = st.text_input("Your Name", placeholder="Rahul Sharma")
            city   = st.selectbox("Target City", list(CITIES.keys()))
            budget = st.slider("Monthly Rent Budget (₹)", 10000, 60000, 22000, 1000, format="₹%d")
        with c2:
            st.markdown("**Priorities**")
            lifestyle = st.multiselect("Lifestyle Preferences",
                ["Safety","Nightlife & Social","Fitness","Spiritual / Temple","Family-Friendly"],
                default=["Safety","Fitness"])
            work_loc  = st.text_input("Work Location / Area", placeholder="e.g. Electronic City")

        st.markdown("**Add-on Services**")
        ac1,ac2,ac3,ac4 = st.columns(4)
        bike   = ac1.checkbox("🛵 Bike Rental", value=True)
        tiffin = ac2.checkbox("🍱 Tiffin",      value=True)
        maid   = ac3.checkbox("🧹 Maid",         value=False)
        gym    = ac4.checkbox("🏋 Gym",           value=True)

        submitted = st.form_submit_button("🔍 Find My Best Areas →")

    if submitted:
        if not name:
            st.error("Please enter your name.")
        else:
            areas  = CITIES[city]["areas"]
            scored = {n: {"score": score_area(d, budget, lifestyle), "data": d}
                      for n, d in areas.items()}
            top2   = sorted(scored.items(), key=lambda x: x[1]["score"], reverse=True)[:2]

            # cost breakdown for #1 area
            top_data = top2[0][1]["data"]
            costs = {"🏠 Rent": top_data["avg_rent"], "⚡ Utilities": 1500, "📱 Internet + Mobile": 800}
            if tiffin: costs["🍱 Tiffin"]       = ADDON_COSTS["tiffin"]
            else:      costs["🍽 Self Cooking"]  = 5500
            if bike:   costs["🛵 Bike Rental"]   = ADDON_COSTS["bike"]
            if maid:   costs["🧹 Maid Service"]  = ADDON_COSTS["maid"]
            if gym:    costs["🏋 Gym"]            = ADDON_COSTS["gym"]

            st.session_state.fd  = {"name":name,"city":city,"budget":budget,
                                    "lifestyle":lifestyle,"work_loc":work_loc,
                                    "bike":bike,"tiffin":tiffin,"maid":maid,"gym":gym,
                                    "ts":datetime.now().strftime("%d %b %Y %H:%M")}
            st.session_state.res = {"top2":top2,"all":scored,"costs":costs,
                                    "total":sum(costs.values()),"vendors":VENDORS[city]}
            st.session_state.subs.append(st.session_state.fd)
            go("results")

# ─────────────────────────────────────────────
# PAGE: RESULTS
# ─────────────────────────────────────────────

elif st.session_state.page == "results":

    if not st.session_state.res:
        st.info("No results yet — fill the form first.")
        if st.button("← Go to Form"): go("form")
        st.stop()

    fd   = st.session_state.fd
    res  = st.session_state.res
    top2 = res["top2"];  costs = res["costs"];  total = res["total"]
    vnd  = res["vendors"];  city = fd["city"]

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b,#4c1d95);border-radius:14px;
         padding:1.25rem 1.75rem;color:#fff;margin-bottom:1.25rem">
      <h2 style="margin:0;color:#fff">👋 Hi {fd['name']}!</h2>
      <p style="margin:.2rem 0 0;opacity:.85">Top 2 areas in <b>{city}</b> ranked for your preferences.</p>
    </div>""", unsafe_allow_html=True)

    # ── Top 2 cards ──
    st.markdown("### 🏆 Recommended Areas")
    ac = st.columns(2)
    for i,(aname,ainfo) in enumerate(top2):
        d = ainfo["data"]; s = ainfo["score"]
        badge = ('🥇 Best Match' if i==0 else '🥈 Runner-Up')
        border = "2px solid #6366f1" if i==0 else "1px solid #e5e7eb"
        bc = "#ede9fe" if i==0 else "#f0fdf4"; tc = "#6d28d9" if i==0 else "#16a34a"
        stars = lambda n: "★"*n + "☆"*(5-n)
        with ac[i]:
            st.markdown(f"""
            <div class="card" style="border:{border}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.4rem">
                <h3 style="margin:0">{aname}</h3>
                <span style="background:{bc};color:{tc};border-radius:999px;
                             padding:.15rem .7rem;font-size:.72rem;font-weight:700">{badge}</span>
              </div>
              <p style="color:#6b7280;font-size:.83rem;margin-bottom:.8rem">{d['desc']}</p>
              <div style="display:flex;gap:.75rem;margin-bottom:.8rem">
                <div class="metric" style="flex:1">
                  <div style="font-size:.7rem;color:#6b7280">Avg Rent</div>
                  <div style="font-weight:700;color:#6366f1">₹{d['avg_rent']:,}</div>
                </div>
                <div class="metric" style="flex:1">
                  <div style="font-size:.7rem;color:#6b7280">Match Score</div>
                  <div style="font-weight:700;color:#10b981">{s}%</div>
                </div>
              </div>
              <div style="font-size:.83rem;line-height:1.8">
                🛡 Safety&nbsp; {stars(d['safety'])}<br>
                🚇 Commute {stars(d['commute'])}<br>
                🎉 Social&nbsp;&nbsp; {stars(d['social'])}<br>
                🏋 Gym: {"✅" if d['gym'] else "❌"} &nbsp;|&nbsp; 🛕 Temple: {"✅" if d['temple'] else "❌"}
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bundle + Cost ──
    bc_col, cost_col = st.columns(2)
    top_name = top2[0][0]

    with bc_col:
        st.markdown(f"### 📦 Starter Bundle — *{top_name}*")
        bundle = [
            ("🏠","Accommodation", vnd["accommodation"]),
            ("🛍","Nearest Mall",   vnd["mall"]),
            ("🛕","Temple / Meditation", vnd["temple"]),
        ]
        if fd["tiffin"]: bundle.insert(1,("🍱","Tiffin Plan",    vnd["tiffin"]))
        if fd["bike"]:   bundle.insert(2,("🛵","Bike Rental",    vnd["bike"]))
        if fd["maid"]:   bundle.insert(3,("🧹","Maid Service",   vnd["maid"]))
        if fd["gym"]:    bundle.insert(4,("🏋","Gym",             vnd["gym"]))

        for icon, label, vendor in bundle:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.6rem;padding:.5rem 0;border-bottom:1px solid #f1f5f9">
              <span style="font-size:1.1rem">{icon}</span>
              <span style="flex:1;font-weight:600;font-size:.88rem">{label}</span>
              <span style="color:#6366f1;font-size:.78rem;font-weight:600">{vendor}</span>
            </div>""", unsafe_allow_html=True)

    with cost_col:
        st.markdown(f"### 💰 Monthly Breakdown — *{top_name}*")
        for item, amt in costs.items():
            st.markdown(f"""
            <div class="cost-row">
              <span style="color:#374151">{item}</span>
              <span style="font-weight:600">₹{amt:,}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b,#4c1d95);border-radius:10px;
             padding:.9rem 1.1rem;margin-top:.8rem;display:flex;justify-content:space-between">
          <span style="color:#fff;font-weight:600">Total / Month</span>
          <span style="color:#fff;font-weight:800;font-size:1.25rem">₹{total:,}</span>
        </div>""", unsafe_allow_html=True)

    # ── Activate + WhatsApp buttons ──
    st.markdown("<br>", unsafe_allow_html=True)
    btn_l, btn_r = st.columns(2)
    with btn_l:
        if st.button(f"⚡ Activate My Move to {top_name} →"):
            st.balloons()
            st.success(f"🎉 Plan activated for **{top_name}, {city}**! We'll reach out to **{fd['name']}** shortly.")
    with btn_r:
        wa_text = (f"Hi! I just used ReloPlan and got matched to {top_name}, {city}. "
                   f"My budget is ₹{fd['budget']:,}/mo. Can you help me activate my move?")
        st.markdown(
            f'<a href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_text)}" target="_blank" '
            f'style="display:block;background:#25d366;color:#fff;text-align:center;border-radius:8px;'
            f'padding:.55rem 1rem;font-weight:700;font-size:.9rem;text-decoration:none;'
            f'box-shadow:0 4px 14px rgba(37,211,102,.35)">💬 WhatsApp My Plan</a>',
            unsafe_allow_html=True,
        )

    # ── All scores ──
    with st.expander("📊 All Area Scores"):
        rows = [{"Area":k,"Score":f"{v['score']}%","Rent":f"₹{v['data']['avg_rent']:,}",
                 "Safety":"★"*v['data']['safety'],"Commute":"★"*v['data']['commute'],
                 "Social":"★"*v['data']['social']}
                for k,v in sorted(res["all"].items(), key=lambda x:x[1]["score"], reverse=True)]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Scale-up roadmap ──
    with st.expander("🚀 How This Scales — Product Roadmap"):
        r1, r2 = st.columns(2)
        r1.markdown("""
**Phase 1 — MVP (Now)**
- ✅ Smart area matching
- ✅ Starter bundle generator
- ✅ Monthly cost calculator
- ✅ Admin panel

**Phase 2 — Monetization**
- 💳 Razorpay / Stripe payments
- 🤝 Real vendor partnerships (rev-share)
- 📦 Premium bundles & subscriptions
- 🏢 Corporate relocation packages
        """)
        r2.markdown("""
**Phase 3 — Intelligence**
- 🗺 Google Maps (real commute times)
- 🤖 AI recommendations (Claude API)
- 📊 Live rental data (API integrations)
- 📱 WhatsApp bot delivery

**Phase 4 — Enterprise**
- 🏢 B2B corporate relocation dashboard
- 📈 HR analytics & reporting
- 🌍 Pan-India + international expansion
- 🔗 White-label API for real-estate platforms
        """)

# ─────────────────────────────────────────────
# PAGE: ADMIN
# ─────────────────────────────────────────────

elif st.session_state.page == "admin":

    st.markdown("## 🔐 Admin Panel")

    if not st.session_state.admin_ok:
        with st.form("login"):
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if pwd == "admin123": st.session_state.admin_ok = True; st.rerun()
                else: st.error("Incorrect password.")
        st.stop()

    if st.button("Logout"): st.session_state.admin_ok = False; st.rerun()

    t1, t2, t3, t4 = st.tabs(["📋 Submissions", "📸 Instagram Leads", "🏘 Areas", "🏪 Vendors"])

    with t1:
        subs = st.session_state.subs
        if subs: st.dataframe(pd.DataFrame(subs), use_container_width=True, hide_index=True)
        else: st.info("No submissions yet.")

    with t2:
        ig_leads = st.session_state.ig_leads
        if ig_leads:
            st.markdown(f"**{len(ig_leads)} lead(s) captured via Instagram Lead Form**")
            st.dataframe(pd.DataFrame(ig_leads), use_container_width=True, hide_index=True)
        else:
            st.info("No Instagram leads yet.")

    with t2:
        city = st.selectbox("City", list(CITIES.keys()), key="adm_city")
        for aname, ad in CITIES[city]["areas"].items():
            with st.expander(f"📍 {aname}"):
                c1,c2 = st.columns(2)
                c1.write(f"**Rent:** ₹{ad['avg_rent']:,}  |  **Safety:** {ad['safety']}/5  |  **Commute:** {ad['commute']}/5")
                c2.write(f"**Social:** {ad['social']}/5  |  **Gym:** {'✅' if ad['gym'] else '❌'}  |  **Temple:** {'✅' if ad['temple'] else '❌'}")

    with t3:
        city = st.selectbox("City", list(VENDORS.keys()), key="adm_vendor")
        for cat, val in VENDORS[city].items():
            st.markdown(f"**{cat.title()}:** {val}")
