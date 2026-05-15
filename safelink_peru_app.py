"""
SafeLink Perú - Digital Shield Demo App
Desarrollado como demo interactiva de ciberseguridad para PYMEs peruanas.
Ejecutar con: streamlit run safelink_peru_app.py
"""

import streamlit as st
import re
import time
import random
from PIL import Image
import io
import hashlib
from datetime import datetime

# ─── CONFIG ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SafeLink Perú · Digital Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS STYLING ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #0A0E1A;
    color: #E8EDF5;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0A0E1A 0%, #0D1F3C 50%, #0A1628 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0,212,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,59,48,0.06) 0%, transparent 70%);
    pointer-events: none;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #00D4FF, #FFFFFF 60%, #FF9A3C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
}

.hero-sub {
    color: rgba(232,237,245,0.55);
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #00D4FF;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 0.4rem;
    border: 1px solid rgba(255,255,255,0.07);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.6rem 1.4rem;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    color: rgba(232,237,245,0.5);
    border: none;
    background: transparent;
    transition: all 0.2s;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,212,255,0.15) !important;
    color: #00D4FF !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.3s;
}

.card:hover {
    border-color: rgba(0,212,255,0.25);
}

.card-danger {
    background: rgba(255,59,48,0.06);
    border-color: rgba(255,59,48,0.3);
}

.card-success {
    background: rgba(52,199,89,0.06);
    border-color: rgba(52,199,89,0.3);
}

.card-warning {
    background: rgba(255,149,0,0.06);
    border-color: rgba(255,149,0,0.3);
}

/* ── Result Badges ── */
.badge-danger {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,59,48,0.15);
    border: 1px solid rgba(255,59,48,0.4);
    color: #FF3B30;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

.badge-ok {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(52,199,89,0.15);
    border: 1px solid rgba(52,199,89,0.4);
    color: #34C759;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

.badge-warning {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,149,0,0.15);
    border: 1px solid rgba(255,149,0,0.4);
    color: #FF9500;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

/* ── Threat Meter ── */
.meter-container {
    background: rgba(255,255,255,0.05);
    border-radius: 50px;
    height: 12px;
    overflow: hidden;
    margin: 0.8rem 0;
}

.meter-fill-danger {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #FF9500, #FF3B30);
    transition: width 1s ease;
}

.meter-fill-ok {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #34C759, #30D158);
    transition: width 1s ease;
}

/* ── Keyword Tags ── */
.kw-tag-danger {
    display: inline-block;
    background: rgba(255,59,48,0.2);
    border: 1px solid rgba(255,59,48,0.5);
    color: #FF6B6B;
    border-radius: 6px;
    padding: 0.2rem 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    margin: 0.2rem;
    font-weight: 500;
}

.kw-tag-ok {
    display: inline-block;
    background: rgba(52,199,89,0.15);
    border: 1px solid rgba(52,199,89,0.4);
    color: #34C759;
    border-radius: 6px;
    padding: 0.2rem 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    margin: 0.2rem;
}

/* ── Learn Cards ── */
.learn-card {
    background: rgba(255,255,255,0.03);
    border-left: 4px solid #00D4FF;
    border-radius: 0 12px 12px 0;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1rem;
}

.learn-card-red { border-left-color: #FF3B30; }
.learn-card-yellow { border-left-color: #FF9500; }
.learn-card-green { border-left-color: #34C759; }

.learn-title {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.5rem;
}

.learn-body {
    color: rgba(232,237,245,0.7);
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Stat Grid ── */
.stat-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: #00D4FF;
    display: block;
    line-height: 1;
}

.stat-label {
    font-size: 0.78rem;
    color: rgba(232,237,245,0.5);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.4rem;
    display: block;
}

/* ── Input Overrides ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 12px !important;
    color: #E8EDF5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}

.stTextArea textarea:focus {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00D4FF, #0095B6) !important;
    color: #0A0E1A !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: rgba(232,237,245,0.9);
    letter-spacing: -0.01em;
    margin-bottom: 0.4rem;
}

.section-sub {
    font-size: 0.83rem;
    color: rgba(232,237,245,0.4);
    margin-bottom: 1.5rem;
}

/* ── Analysis Log ── */
.log-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: rgba(0,212,255,0.7);
    padding: 0.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.log-line-red { color: rgba(255,59,48,0.8); }
.log-line-green { color: rgba(52,199,89,0.8); }
.log-line-yellow { color: rgba(255,149,0,0.8); }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Tooltip ── */
.tip-box {
    background: rgba(255,149,0,0.08);
    border: 1px solid rgba(255,149,0,0.25);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    font-size: 0.86rem;
    color: rgba(232,237,245,0.75);
    margin-top: 1.2rem;
}

.tip-box strong { color: #FF9500; }

/* ── Image Upload Area ── */
.stFileUploader > div {
    background: rgba(255,255,255,0.03) !important;
    border: 2px dashed rgba(0,212,255,0.25) !important;
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── ANALYSIS ENGINE ─────────────────────────────────────────────────────────

BANKS_PE = {
    "BCP": ["bcp", "banco de crédito", "credito", "crédito del perú"],
    "Interbank": ["interbank", "inter bank", "interbanc"],
    "BBVA": ["bbva", "continental", "banco continental"],
    "Scotiabank": ["scotiabank", "scotia"],
    "Yape": ["yape"],
    "Plin": ["plin"],
    "BANBIF": ["banbif"],
}

URGENCY_WORDS = [
    "urgente", "inmediato", "inmediatamente", "ya", "ahora",
    "suspendido", "bloqueado", "bloqueará", "suspenderá", "vencido",
    "última oportunidad", "48 horas", "24 horas", "horas",
    "restringen", "deshabilitar", "verificar ahora", "confirmar",
    "account suspended", "limited", "verify now",
]

SUSPICIOUS_URLS = [
    r"bit\.ly", r"tinyurl", r"t\.co", r"goo\.gl",
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # IP raw
    r"\.xyz", r"\.top", r"\.click", r"\.info",
    r"secure.*login", r"login.*secure", r"update.*account",
    r"verify.*bank", r"bank.*verify",
]

PERSONAL_DATA_HOOKS = [
    "dni", "clave", "contraseña", "password", "pin", "cvc",
    "número de tarjeta", "cuenta", "código de seguridad",
]

def analyze_sms(text: str) -> dict:
    lower = text.lower()
    found_banks = []
    for bank, keywords in BANKS_PE.items():
        for kw in keywords:
            if kw in lower:
                found_banks.append(bank)
                break

    found_urgency = [w for w in URGENCY_WORDS if w in lower]
    found_urls = []
    for pattern in SUSPICIOUS_URLS:
        matches = re.findall(pattern, lower)
        if matches:
            found_urls.extend(matches)

    found_personal = [w for w in PERSONAL_DATA_HOOKS if w in lower]

    # Scoring
    score = 0
    score += min(len(found_banks) * 20, 30)
    score += min(len(found_urgency) * 15, 35)
    score += min(len(found_urls) * 25, 40)
    score += min(len(found_personal) * 20, 30)

    risk = "ALTO" if score >= 60 else ("MEDIO" if score >= 30 else "BAJO")

    return {
        "score": min(score, 100),
        "risk": risk,
        "banks": list(set(found_banks)),
        "urgency": found_urgency,
        "urls": found_urls,
        "personal": found_personal,
    }

def analyze_voucher(img: Image.Image, filename: str) -> dict:
    """Simulated metadata and visual analysis for vouchers."""
    # Deterministic-ish result based on image hash for demo consistency
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_hash = hashlib.md5(buf.getvalue()).hexdigest()
    seed = int(img_hash[:8], 16) % 100

    width, height = img.size
    mode = img.mode
    file_ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "?"

    # Simulate checks
    checks = {
        "metadata_fecha": {
            "label": "Metadatos de fecha consistentes",
            "pass": seed > 40,
            "detail": f"EXIF DateTimeOriginal {'encontrado y válido' if seed > 40 else 'ausente o manipulado'}",
        },
        "dpi_normal": {
            "label": "Resolución DPI estándar",
            "pass": 72 <= (seed * 3) % 300 <= 200,
            "detail": f"DPI detectado: {(seed * 3) % 300 + 50}",
        },
        "aspect_ratio": {
            "label": "Proporción de imagen normal",
            "pass": 0.4 <= (width / max(height, 1)) <= 2.5,
            "detail": f"Ratio {width}x{height} = {width/max(height,1):.2f}",
        },
        "color_profile": {
            "label": "Perfil de color original",
            "pass": seed > 55,
            "detail": f"Modo: {mode} — {'sRGB estándar' if seed > 55 else 'perfil de color alterado'}",
        },
        "compression": {
            "label": "Compresión sin re-edición",
            "pass": seed > 35,
            "detail": f"Nivel de compresión {'normal' if seed > 35 else 'inusualmente alto (posible edición)'}",
        },
        "timestamp_match": {
            "label": "Timestamp coincide con fecha visible",
            "pass": seed > 50,
            "detail": f"Fecha visible {'consistente' if seed > 50 else 'NO coincide'} con metadatos del archivo",
        },
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    total = len(checks)
    pct = int((passed / total) * 100)
    risk = "SOSPECHOSO" if pct < 60 else ("PRECAUCIÓN" if pct < 80 else "VÁLIDO")

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "pct": pct,
        "risk": risk,
        "filename": filename,
        "dimensions": f"{width}×{height}px",
        "mode": mode,
    }

# ─── EXAMPLES ────────────────────────────────────────────────────────────────

SMS_EXAMPLES = {
    "⚠️ Phishing BCP clásico": (
        "BCP ALERTA: Su cuenta ha sido SUSPENDIDA por actividad sospechosa. "
        "Verifique su DNI y clave ahora en: http://bcp-seguro-pe.xyz/verificar "
        "antes de 24 horas o será bloqueado definitivamente."
    ),
    "⚠️ Phishing Interbank urgente": (
        "INTERBANK: Su tarjeta está bloqueada. Ingrese su número de tarjeta y PIN "
        "en bit.ly/inter-verify para evitar suspensión inmediata. URGENTE."
    ),
    "✅ SMS legítimo (Yape)": (
        "Yape: Recibiste S/50.00 de Juan Pérez. "
        "Tu saldo actual es S/150.00. ¡Gracias por usar Yape!"
    ),
    "✅ SMS legítimo (banco)": (
        "BBVA: Realizaste un consumo de S/35.00 en METRO CHORRILLOS el 14/05/2026. "
        "Si no reconoces este cargo llama al 595-0000."
    ),
}

# ─── HEADER ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🛡️ &nbsp; SafeLink Perú · Digital Shield</div>
    <div class="hero-title">Protégete del fraude digital</div>
    <p class="hero-sub">Detector de Phishing · Verificador de Vouchers · Educación Digital</p>
</div>
""", unsafe_allow_html=True)

# ─── STATS ROW ───────────────────────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class="stat-box">
        <span class="stat-number">73%</span>
        <span class="stat-label">fraudes por SMS en PE</span>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="stat-box">
        <span class="stat-number">S/480M</span>
        <span class="stat-label">pérdidas anuales estimadas</span>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="stat-box">
        <span class="stat-number">3 seg</span>
        <span class="stat-label">análisis en tiempo real</span>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="stat-box">
        <span class="stat-number">BCP · IB · BBVA</span>
        <span class="stat-label">bancos monitoreados</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs([
    "📡  Scanner de Enlaces",
    "🖼️  Verificador de Vouchers",
    "📚  Aprende Digital",
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: SMS SCANNER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div class="section-header">📨 Pega tu mensaje SMS o WhatsApp</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Analiza mensajes sospechosos de bancos, Yape o Plin antes de hacer clic en cualquier enlace.</div>', unsafe_allow_html=True)

        # Example selector
        example_choice = st.selectbox(
            "Cargar ejemplo:",
            ["— Escribe tu propio mensaje —"] + list(SMS_EXAMPLES.keys()),
            key="sms_example"
        )

        default_text = SMS_EXAMPLES.get(example_choice, "") if example_choice != "— Escribe tu propio mensaje —" else ""

        sms_text = st.text_area(
            "Mensaje a analizar:",
            value=default_text,
            height=140,
            placeholder="Pega aquí el SMS, WhatsApp o correo que recibiste...",
            label_visibility="collapsed",
            key="sms_input"
        )

        analyze_btn = st.button("🔍 Analizar ahora", key="btn_scan", use_container_width=True)

    with right:
        st.markdown('<div class="section-header">🎯 ¿Qué detectamos?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="margin-top:0">
            <div style="font-size:0.88rem; color:rgba(232,237,245,0.65); line-height:1.8;">
                🏦 &nbsp;<b style="color:#E8EDF5">Menciones de bancos peruanos</b><br>
                BCP, Interbank, BBVA, Scotiabank, Yape, Plin<br><br>
                ⏰ &nbsp;<b style="color:#E8EDF5">Urgencia psicológica</b><br>
                "suspendido", "bloqueado", "24 horas", "inmediato"<br><br>
                🔗 &nbsp;<b style="color:#E8EDF5">URLs sospechosas</b><br>
                acortadores, IPs desnudas, dominios raros (.xyz, .top)<br><br>
                🔑 &nbsp;<b style="color:#E8EDF5">Solicitud de datos personales</b><br>
                DNI, clave, PIN, número de tarjeta, CVC
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RESULTS ──
    if analyze_btn:
        if not sms_text.strip():
            st.warning("Por favor escribe o pega un mensaje para analizar.")
        else:
            with st.spinner("Analizando patrones de amenaza..."):
                time.sleep(1.2)
                result = analyze_sms(sms_text)

            st.markdown("---")
            st.markdown('<div class="section-header">📊 Resultado del análisis</div>', unsafe_allow_html=True)

            r1, r2, r3 = st.columns([2, 2, 3], gap="medium")

            with r1:
                # Risk level
                risk = result["risk"]
                if risk == "ALTO":
                    badge_class = "badge-danger"
                    icon = "🚨"
                    msg = "RIESGO ALTO"
                elif risk == "MEDIO":
                    badge_class = "badge-warning"
                    icon = "⚠️"
                    msg = "RIESGO MEDIO"
                else:
                    badge_class = "badge-ok"
                    icon = "✅"
                    msg = "PARECE SEGURO"

                st.markdown(f'<div class="{badge_class}">{icon} &nbsp; {msg}</div>', unsafe_allow_html=True)

                score = result["score"]
                fill_class = "meter-fill-danger" if risk == "ALTO" else ("meter-fill-danger" if risk == "MEDIO" else "meter-fill-ok")
                st.markdown(f"""
                <div style="margin-bottom:0.5rem">
                    <span style="font-size:0.78rem;color:rgba(232,237,245,0.45);text-transform:uppercase;letter-spacing:0.06em">Índice de amenaza</span>
                </div>
                <div class="meter-container">
                    <div class="{fill_class}" style="width:{score}%"></div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:rgba(232,237,245,0.4);margin-top:0.3rem">
                    <span>0</span><span style="color:#E8EDF5;font-weight:700">{score}/100</span><span>100</span>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                # Detection log
                st.markdown('<div style="font-size:0.78rem;color:rgba(232,237,245,0.45);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.5rem">Log de detección</div>', unsafe_allow_html=True)

                log_items = []
                log_items.append(f'<div class="log-line">[INIT] Texto cargado: {len(sms_text)} chars</div>')

                if result["banks"]:
                    for b in result["banks"]:
                        log_items.append(f'<div class="log-line log-line-yellow">[BANK] Detectado: {b}</div>')
                else:
                    log_items.append('<div class="log-line log-line-green">[BANK] Sin menciones bancarias</div>')

                if result["urgency"]:
                    for u in result["urgency"][:3]:
                        log_items.append(f'<div class="log-line log-line-red">[URGENCY] "{u}"</div>')
                else:
                    log_items.append('<div class="log-line log-line-green">[URGENCY] Sin urgencia detectada</div>')

                if result["urls"]:
                    log_items.append(f'<div class="log-line log-line-red">[URL] {len(result["urls"])} enlace(s) sospechoso(s)</div>')
                else:
                    log_items.append('<div class="log-line log-line-green">[URL] Sin URLs sospechosas</div>')

                if result["personal"]:
                    personal_str = ", ".join(result["personal"][:3])
                    log_items.append(f'<div class="log-line log-line-red">[DATA] Solicita: {personal_str}</div>')

                log_items.append(f'<div class="log-line">[SCORE] Resultado final: {score}/100 → {risk}</div>')

                st.markdown(
                    f'<div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:0.8rem;border:1px solid rgba(255,255,255,0.06)">{"".join(log_items)}</div>',
                    unsafe_allow_html=True
                )

            with r3:
                # Findings detail
                st.markdown('<div style="font-size:0.78rem;color:rgba(232,237,245,0.45);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.8rem">Señales detectadas</div>', unsafe_allow_html=True)

                if result["banks"]:
                    st.markdown("**🏦 Bancos mencionados**")
                    tags = "".join(f'<span class="kw-tag-danger">{b}</span>' for b in result["banks"])
                    st.markdown(tags, unsafe_allow_html=True)
                    st.markdown("")

                if result["urgency"]:
                    st.markdown("**⏰ Palabras de urgencia**")
                    tags = "".join(f'<span class="kw-tag-danger">{w}</span>' for w in result["urgency"][:5])
                    st.markdown(tags, unsafe_allow_html=True)
                    st.markdown("")

                if result["personal"]:
                    st.markdown("**🔑 Datos personales solicitados**")
                    tags = "".join(f'<span class="kw-tag-danger">{w}</span>' for w in result["personal"])
                    st.markdown(tags, unsafe_allow_html=True)
                    st.markdown("")

                if not result["banks"] and not result["urgency"] and not result["personal"] and not result["urls"]:
                    st.markdown('<span class="kw-tag-ok">✅ Sin señales de phishing</span>', unsafe_allow_html=True)

            # Advice
            st.markdown("<br>", unsafe_allow_html=True)
            if risk == "ALTO":
                st.markdown("""
                <div class="card card-danger">
                    <b style="color:#FF3B30">🚨 ¡No hagas clic en ningún enlace!</b><br>
                    <span style="font-size:0.88rem;color:rgba(232,237,245,0.7)">Este mensaje tiene múltiples señales de phishing. Los bancos peruanos <b>NUNCA</b> te pedirán tu clave, PIN o número de tarjeta por SMS. 
                    Bloquea el número, reporta al banco oficial y avisa a tu familia.</span>
                </div>
                """, unsafe_allow_html=True)
            elif risk == "MEDIO":
                st.markdown("""
                <div class="card card-warning">
                    <b style="color:#FF9500">⚠️ Procede con cuidado</b><br>
                    <span style="font-size:0.88rem;color:rgba(232,237,245,0.7)">Algunas señales sospechosas encontradas. Antes de actuar, llama directamente a tu banco 
                    al número oficial del reverso de tu tarjeta, no al número del mensaje.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="card card-success">
                    <b style="color:#34C759">✅ Sin señales de alarma</b><br>
                    <span style="font-size:0.88rem;color:rgba(232,237,245,0.7)">Este mensaje parece legítimo, pero mantén siempre la guardia. Si tienes dudas, 
                    contacta a tu banco directamente por sus canales oficiales.</span>
                </div>
                """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: VOUCHER VERIFIER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    lv, rv = st.columns([3, 2], gap="large")

    with lv:
        st.markdown('<div class="section-header">📎 Sube el comprobante a verificar</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Vouchers de Yape, Plin, transferencias bancarias. Formatos: JPG, PNG, WEBP.</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Arrastra aquí tu voucher",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

    with rv:
        st.markdown('<div class="section-header">🔬 ¿Qué analizamos?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="margin-top:0">
            <div style="font-size:0.88rem; color:rgba(232,237,245,0.65); line-height:1.9;">
                📅 &nbsp;<b style="color:#E8EDF5">Metadatos EXIF</b> — fecha y hora<br>
                📐 &nbsp;<b style="color:#E8EDF5">Resolución DPI</b> — estándar vs editado<br>
                🎨 &nbsp;<b style="color:#E8EDF5">Perfil de color</b> — original vs alterado<br>
                🗜️ &nbsp;<b style="color:#E8EDF5">Nivel de compresión</b> — re-guardados<br>
                🕐 &nbsp;<b style="color:#E8EDF5">Timestamp del archivo</b> — consistencia<br>
                📏 &nbsp;<b style="color:#E8EDF5">Proporciones</b> — ratio imagen normal
            </div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:
        st.markdown("---")
        try:
            img = Image.open(uploaded_file)
            uploaded_file.seek(0)

            col_img, col_result = st.columns([1, 2], gap="large")

            with col_img:
                st.image(img, caption=uploaded_file.name, use_container_width=True)
                st.markdown(f"""
                <div style="font-size:0.78rem;color:rgba(232,237,245,0.4);text-align:center;margin-top:0.5rem">
                    {uploaded_file.name} · {img.size[0]}×{img.size[1]}px · {img.mode}
                </div>
                """, unsafe_allow_html=True)

            with col_result:
                with st.spinner("Ejecutando análisis forense..."):
                    time.sleep(1.5)
                    vr = analyze_voucher(img, uploaded_file.name)

                risk = vr["risk"]
                if risk == "SOSPECHOSO":
                    badge_class = "badge-danger"
                    icon = "🚨"
                elif risk == "PRECAUCIÓN":
                    badge_class = "badge-warning"
                    icon = "⚠️"
                else:
                    badge_class = "badge-ok"
                    icon = "✅"

                st.markdown(f'<div class="{badge_class}">{icon} &nbsp; Voucher {risk}</div>', unsafe_allow_html=True)

                pct = vr["pct"]
                fill_cls = "meter-fill-ok" if pct >= 80 else "meter-fill-danger"
                st.markdown(f"""
                <div style="margin-bottom:0.4rem">
                    <span style="font-size:0.78rem;color:rgba(232,237,245,0.45);text-transform:uppercase;letter-spacing:0.06em">
                    Integridad del archivo
                    </span>
                </div>
                <div class="meter-container">
                    <div class="{fill_cls}" style="width:{pct}%"></div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:rgba(232,237,245,0.4);margin-top:0.3rem;margin-bottom:1rem">
                    <span>0%</span><span style="color:#E8EDF5;font-weight:700">{pct}% ({vr['passed']}/{vr['total']} checks)</span><span>100%</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div style="font-size:0.78rem;color:rgba(232,237,245,0.45);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.8rem">Checklist forense</div>', unsafe_allow_html=True)

                for key, check in vr["checks"].items():
                    passed = check["pass"]
                    dot = "🟢" if passed else "🔴"
                    label_color = "rgba(52,199,89,0.9)" if passed else "rgba(255,59,48,0.9)"
                    status = "OK" if passed else "ALERTA"
                    st.markdown(f"""
                    <div style="display:flex;align-items:flex-start;gap:0.8rem;padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                        <span style="font-size:0.9rem;flex-shrink:0">{dot}</span>
                        <div>
                            <div style="font-size:0.85rem;font-weight:600;color:#E8EDF5">{check['label']}</div>
                            <div style="font-size:0.78rem;color:rgba(232,237,245,0.45);font-family:'JetBrains Mono',monospace">{check['detail']} — <span style="color:{label_color}">{status}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Advice
            st.markdown("<br>", unsafe_allow_html=True)
            if risk == "SOSPECHOSO":
                st.markdown("""
                <div class="card card-danger">
                    <b style="color:#FF3B30">🚨 Este voucher presenta señales de manipulación</b><br>
                    <span style="font-size:0.88rem;color:rgba(232,237,245,0.7)">No entregues productos ni servicios basándote en este comprobante. 
                    Verifica directamente en tu app de Yape/Plin o contacta al banco para confirmar la transferencia. 
                    Los estafadores editan screenshots con apps como PicsArt o Photoshop.</span>
                </div>
                """, unsafe_allow_html=True)
            elif risk == "PRECAUCIÓN":
                st.markdown("""
                <div class="card card-warning">
                    <b style="color:#FF9500">⚠️ Algunas irregularidades detectadas</b><br>
                    <span style="font-size:0.88rem;color:rgba(232,237,245,0.7)">Confirma la operación directamente desde tu app antes de proceder. 
                    Una demora de 30 segundos puede ahorrarte una pérdida.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="card card-success">
                    <b style="color:#34C759">✅ El voucher parece auténtico</b><br>
                    <span style="font-size:0.88rem;color:rgba(232,237,245,0.7)">Los metadatos son consistentes. De todas formas, siempre confirma desde tu app que 
                    el monto aparece acreditado antes de cerrar cualquier transacción.</span>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al procesar la imagen: {e}")

    else:
        st.markdown("""
        <div class="tip-box" style="margin-top:1.5rem">
            <strong>💡 ¿Cómo funciona la estafa del voucher falso?</strong><br>
            El estafador te envía un screenshot editado de Yape o Plin que <em>parece</em> mostrar una transferencia realizada. 
            Tú entregas el producto o servicio… pero el dinero nunca llegó. Siempre verifica en tu propia app.
        </div>
        """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: LEARN DIGITAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📚 Aprende a protegerte — en peruano, sin tecnicismos</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Guías rápidas para que tú, tu familia y tu negocio no caigan en estafas digitales.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Module 1: What is phishing
    st.markdown("### 🎣 ¿Qué es el Phishing?")
    st.markdown("""
    <div class="learn-card learn-card-red">
        <div class="learn-title">El "phishing" es pescar... pero a ti</div>
        <div class="learn-body">
        Imagínate que alguien te manda un mensaje haciéndose pasar por tu banco o por Yape. 
        Te dice que tu cuenta está en peligro y que tienes que entrar <em>ya mismo</em> a un enlace. 
        Tú entras, pones tu clave... y listo, te pescaron. Eso es phishing: engañarte para que tú mismo 
        les des tus datos.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        st.markdown("""
        <div class="learn-card learn-card-red">
            <div class="learn-title">🚩 Las 5 señales de alarma</div>
            <div class="learn-body">
            1. <b>Te meten prisa</b> — "actúa en 24 horas"<br>
            2. <b>Te piden tu clave o PIN</b> — ningún banco lo hace<br>
            3. <b>El enlace es raro</b> — bcp-seguro.xyz ≠ bcp.com.pe<br>
            4. <b>Hay faltas de ortografía</b> — señal clásica de fraude<br>
            5. <b>Te amenazan</b> — "tu cuenta será bloqueada"
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="learn-card learn-card-green">
            <div class="learn-title">✅ Regla de oro peruana</div>
            <div class="learn-body">
            <b>Si te llega un mensaje de tu banco, no hagas clic.</b><br><br>
            Cierra el mensaje, busca el número oficial en tu tarjeta física o en la app oficial, 
            y llama directamente. Nunca uses el número o enlace del mensaje sospechoso. 
            30 segundos de pausa pueden salvarte cientos de soles.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💸 Estafas más comunes en el Perú")

    scams = [
        ("🟡", "learn-card-yellow", "Voucher de Yape/Plin falso",
         "Te mandan un screenshot editado que dice que ya te pagaron. Nunca confirmes la venta sin revisar TÚ MISMO en tu app que el dinero llegó a tu cuenta."),
        ("🔴", "learn-card-red", "Falso soporte técnico bancario",
         "Alguien llama diciendo ser del BCP o Interbank para 'ayudarte con un problema'. Te piden instalar apps o darte acceso remoto. Ningún banco hace esto. Cuelga."),
        ("🔴", "learn-card-red", "SMS de bloqueo de cuenta",
         "Mensaje urgente que dice que tu cuenta fue bloqueada. El enlace lleva a una web falsa idéntica a la de tu banco. Siempre entra directo desde la app oficial."),
        ("🟡", "learn-card-yellow", "Premio falso de Tottus, Wong o Metro",
         "\"¡Ganaste un vale de S/500! Haz clic aquí\". Es mentira. Las cadenas reales no rifan premios por WhatsApp. Ignora y bloquea."),
        ("🔴", "learn-card-red", "Estafa del mototaxi/taxi con QR",
         "Te cobran un servicio con un QR que en realidad es para que TÚ pagues a ellos, o es un enlace de phishing. Siempre verifica el monto antes de confirmar cualquier pago."),
    ]

    for i, (dot, card_class, title, body) in enumerate(scams):
        st.markdown(f"""
        <div class="learn-card {card_class}">
            <div class="learn-title">{dot} {title}</div>
            <div class="learn-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛡️ Checklist de protección personal")

    checks_learn = [
        ("Activa el doble factor de autenticación (2FA) en tu app del banco", True),
        ("Nunca compartas tu clave de 6 dígitos de Yape, ni con 'empleados del banco'", True),
        ("Revisa siempre la URL antes de ingresar datos: bcp.com.pe ≠ bcp-login.xyz", True),
        ("Instala solo apps oficiales desde Play Store o App Store", True),
        ("Avisa a tu familia mayor sobre estas estafas — ellos son el blanco principal", True),
        ("Reporta mensajes sospechosos a tu banco y al Indecopi", True),
    ]

    for text, _ in checks_learn:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.8rem;padding:0.7rem 1rem;background:rgba(52,199,89,0.05);border:1px solid rgba(52,199,89,0.15);border-radius:10px;margin-bottom:0.5rem">
            <span style="color:#34C759;font-size:1rem;flex-shrink:0">☑</span>
            <span style="font-size:0.88rem;color:rgba(232,237,245,0.8)">{text}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Emergency contacts
    st.markdown("### 📞 ¿Fuiste víctima? Actúa ya")
    ec1, ec2, ec3 = st.columns(3, gap="medium")
    contacts = [
        ("🏦", "Tu banco", "Bloquea tu tarjeta de inmediato.\nBCP: 311-9898\nInterbank: 311-9000\nBBVA: 595-0000"),
        ("🚔", "PNP — Ciberdelincuencia", "Denuncia en la comisaría más cercana o en:\nwww.pnp.gob.pe\nTeléfono: 105"),
        ("⚖️", "Indecopi", "Para denunciar empresas o servicios fraudulentos:\n0800-4-4040 (gratuito)\nwww.indecopi.gob.pe"),
    ]
    for col, (icon, title, body) in zip([ec1, ec2, ec3], contacts):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center">
                <div style="font-size:2rem;margin-bottom:0.5rem">{icon}</div>
                <div style="font-weight:700;margin-bottom:0.5rem;font-size:0.95rem">{title}</div>
                <div style="font-size:0.8rem;color:rgba(232,237,245,0.55);white-space:pre-line;line-height:1.7">{body}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid rgba(255,255,255,0.07)">
    <div style="font-size:1.1rem;font-weight:700;background:linear-gradient(90deg,#00D4FF,#FFFFFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.4rem">
        🛡️ SafeLink Perú · Digital Shield
    </div>
    <div style="font-size:0.78rem;color:rgba(232,237,245,0.3);letter-spacing:0.06em;text-transform:uppercase">
        Demo educativa · No reemplaza asesoría legal o bancaria oficial
    </div>
</div>
""", unsafe_allow_html=True)
