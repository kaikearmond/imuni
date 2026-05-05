import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Saúde & Vacinação Brasil",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(99,102,241,0.3);
    }

    header[data-testid="stHeader"] { background: transparent; }
    .stDeployButton { display: none; }

    /* ── Hero ── */
    .hero-banner {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        border-radius: 20px;
        padding: 40px 50px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(99,102,241,0.4);
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    .hero-title {
        color: white;
        font-size: 2.4em;
        font-weight: 700;
        margin: 0 0 8px 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 1.1em;
        font-weight: 300;
        margin: 0;
    }

    /* ── Section Title ── */
    .section-title {
        color: #e2e8f0;
        font-size: 1.5em;
        font-weight: 600;
        margin: 30px 0 15px 0;
        padding-left: 14px;
        border-left: 4px solid #6366f1;
    }

    /* ── Stat Cards ── */
    .stat-card {
        background: linear-gradient(135deg, #1e293b, #2d3748);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .stat-number { font-size: 2em; font-weight: 700; color: #818cf8; }
    .stat-label  { color: #94a3b8; font-size: 0.82em; margin-top: 4px; }

    /* ── Disease Cards ── */
    .disease-card {
        border-radius: 16px;
        padding: 22px 22px 16px;
        margin: 10px 0;
        position: relative;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .card-lethal {
        background: linear-gradient(135deg, #1e0a0a 0%, #2d1515 100%);
        border: 1px solid rgba(239,68,68,0.4);
    }
    .card-notlethal {
        background: linear-gradient(135deg, #0a1e0a 0%, #152d15 100%);
        border: 1px solid rgba(34,197,94,0.4);
    }
    .card-disease-name {
        font-size: 1.15em;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .card-lethal   .card-disease-name { color: #fca5a5; }
    .card-notlethal .card-disease-name { color: #86efac; }

    .badge-lethal {
        display: inline-block;
        background: rgba(239,68,68,0.2);
        color: #f87171;
        border: 1px solid rgba(239,68,68,0.5);
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75em;
        font-weight: 600;
        margin-bottom: 14px;
    }
    .badge-notlethal {
        display: inline-block;
        background: rgba(34,197,94,0.15);
        color: #4ade80;
        border: 1px solid rgba(34,197,94,0.4);
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75em;
        font-weight: 600;
        margin-bottom: 14px;
    }

    /* symptom tags */
    .symptom-tag {
        display: inline-block;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 0.78em;
        margin: 2px 3px 2px 0;
        border: 1px solid;
    }
    .tag-lethal    { background: rgba(239,68,68,0.1);  color: #fca5a5; border-color: rgba(239,68,68,0.25); }
    .tag-notlethal { background: rgba(34,197,94,0.1);  color: #86efac; border-color: rgba(34,197,94,0.22); }

    .card-description {
        color: #94a3b8;
        font-size: 0.82em;
        line-height: 1.6;
        padding-top: 6px;
        min-height: 80px;
    }
    .symptom-area { min-height: 80px; padding-top: 4px; }

    .card-footer {
        margin-top: 14px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 0.78em;
        color: #64748b;
    }
    .card-footer span { color: #a5b4fc; font-weight: 500; }

    /* ── Vaccine Banner ── */
    .vaccine-banner {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 20px;
        padding: 32px 40px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(5,150,105,0.25);
    }
    .vaccine-title { color: #6ee7b7; font-size: 1.6em; font-weight: 700; margin-bottom: 12px; }
    .vaccine-text  { color: #a7f3d0; font-size: 0.95em; line-height: 1.7; }
    .vaccine-points {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 16px;
    }
    .vaccine-point {
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(52,211,153,0.2);
        border-radius: 10px;
        padding: 10px 14px;
        color: #d1fae5;
        font-size: 0.85em;
    }

    /* ── CTA ── */
    .cta-container { text-align: center; margin: 28px 0 10px; }
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        text-decoration: none !important;
        padding: 16px 40px;
        border-radius: 50px;
        font-size: 1em;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(5,150,105,0.5);
        letter-spacing: 0.02em;
    }

    /* Streamlit button overrides for mini tabs */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        border-radius: 8px !important;
        font-size: 0.78em !important;
        padding: 5px 4px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Região": ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"],
        "Doses_aplicadas": [9528028, 24498632, 33744336, 13670421, 7805724]
    })

diseases = [
    {
        "name": "Sarampo",
        "lethal": True,
        "symptoms": ["Febre alta", "Tosse seca", "Conjuntivite", "Manchas avermelhadas", "Coriza"],
        "description": "Doença viral altamente contagiosa. Pode causar complicações graves como pneumonia e encefalite, especialmente em crianças não vacinadas.",
        "vaccine": "Tríplice Viral (SCR)"
    },
    {
        "name": "Poliomielite",
        "lethal": True,
        "symptoms": ["Febre", "Dor muscular", "Paralisia flácida", "Fadiga", "Rigidez na nuca"],
        "description": "Infecção viral que pode causar paralisia permanente. Praticamente erradicada graças à vacinação em massa no Brasil.",
        "vaccine": "VIP / VOP (Polio)"
    },
    {
        "name": "Tétano",
        "lethal": True,
        "symptoms": ["Rigidez muscular", "Espasmos", "Travamento do maxilar", "Dificuldade de engolir", "Convulsões"],
        "description": "Infecção bacteriana grave causada por toxinas que afetam o sistema nervoso. Pode causar morte por parada respiratória.",
        "vaccine": "Tríplice Bacteriana (DTPa)"
    },
    {
        "name": "Hepatite B",
        "lethal": True,
        "symptoms": ["Icterícia", "Fadiga intensa", "Dor abdominal", "Náuseas", "Urina escura"],
        "description": "Infecção viral crônica que ataca o fígado. Pode evoluir para cirrose e câncer hepático se não tratada adequadamente.",
        "vaccine": "Hepatite B (3 doses)"
    },
    {
        "name": "Febre Amarela",
        "lethal": True,
        "symptoms": ["Febre", "Icterícia", "Sangramento", "Vômito intenso", "Insuf. hepática"],
        "description": "Doença viral transmitida por mosquitos. Na forma grave pode causar falência múltipla de órgãos com alta mortalidade.",
        "vaccine": "Febre Amarela (dose única)"
    },
    {
        "name": "Influenza",
        "lethal": False,
        "symptoms": ["Febre", "Dor no corpo", "Tosse", "Dor de garganta", "Calafrios"],
        "description": "Infecção viral respiratória comum. Geralmente autolimitada, mas pode ser grave em idosos, crianças e imunossuprimidos.",
        "vaccine": "Influenza (anual)"
    },
    {
        "name": "Catapora",
        "lethal": False,
        "symptoms": ["Bolhas pelo corpo", "Coceira intensa", "Febre baixa", "Mal-estar", "Perda de apetite"],
        "description": "Infecção viral causada pelo vírus Varicela-Zoster. Geralmente benigna em crianças, mas pode ser grave em adultos.",
        "vaccine": "Varicela (Catapora)"
    },
    {
        "name": "Caxumba",
        "lethal": False,
        "symptoms": ["Inchaço nas parótidas", "Dif. de mastigar", "Febre", "Dor de cabeça", "Fadiga"],
        "description": "Infecção viral que afeta as glândulas salivares. Pode causar surdez ou infertilidade masculina em casos complicados.",
        "vaccine": "Tríplice Viral (SCR)"
    },
    {
        "name": "Rubéola",
        "lethal": False,
        "symptoms": ["Erupção cutânea", "Febre baixa", "Linfonodos aumentados", "Dor nas articulações", "Olhos vermelhos"],
        "description": "Infecção viral geralmente leve. Extremamente perigosa durante a gravidez, podendo causar síndrome da rubéola congênita.",
        "vaccine": "Tríplice Viral (SCR)"
    },
]

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<p style='color:#94a3b8; font-size:0.85em; margin-bottom:6px;'>Filtrar Doenças</p>", unsafe_allow_html=True)
    show_lethal    = st.checkbox("Mostrar Doenças Letais", value=True)
    show_notlethal = st.checkbox("Mostrar Doenças Não-Letais", value=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div class='hero-title'>Saúde Pública & Vacinação no Brasil</div>
    <div class='hero-subtitle'>
        Conheça as principais doenças preveníveis, seus sintomas e a importância de se vacinar.<br>
        Proteja-se e proteja quem você ama.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Stats ────────────────────────────────────────────────────────────────
df = load_data()
col1, col2, col3, col4 = st.columns(4)
kpis = [
    ("89,2M", "Doses Aplicadas (Total)"),
    ("9",     "Doenças Cobertas"),
    ("5",     "Regiões do Brasil"),
    ("95%",   "Meta de Cobertura SUS"),
]
for col, (num, label) in zip([col1, col2, col3, col4], kpis):
    with col:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{num}</div>
            <div class='stat-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts ───────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Doses Aplicadas por Região</div>", unsafe_allow_html=True)

colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b']
col_c1, col_c2 = st.columns([3, 2])

with col_c1:
    fig_bar = go.Figure(go.Bar(
        x=df["Região"], y=df["Doses_aplicadas"],
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        text=[f'{v/1e6:.1f}M' for v in df["Doses_aplicadas"]],
        textposition='outside',
        textfont=dict(color='#e2e8f0', size=12),
        hovertemplate='<b>%{x}</b><br>Doses: %{y:,.0f}<extra></extra>'
    ))
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', family='Inter'),
        xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8', size=11)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#64748b')),
        margin=dict(l=10, r=10, t=20, b=10), height=300, showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

with col_c2:
    fig_pie = go.Figure(go.Pie(
        labels=df["Região"], values=df["Doses_aplicadas"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color='#0f172a', width=2)),
        textinfo='percent', textfont=dict(color='white', size=11),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} doses<br>%{percent}<extra></extra>'
    ))
    fig_pie.add_annotation(text="<b>89.2M</b><br>Total", x=0.5, y=0.5,
                           font=dict(color='#e2e8f0', size=14), showarrow=False)
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', family='Inter'),
        margin=dict(l=0, r=0, t=0, b=0), height=300,
        legend=dict(font=dict(color='#94a3b8', size=10), bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

# ─── Disease Flash Cards ───────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Doenças Preveníveis por Vacina</div>", unsafe_allow_html=True)

filtered = [d for d in diseases if (d["lethal"] and show_lethal) or (not d["lethal"] and show_notlethal)]

if not filtered:
    st.info("Selecione pelo menos um tipo de doença no menu lateral.")
else:
    # Initialize session state for all cards
    for disease in diseases:
        key = f"tab_{disease['name']}"
        if key not in st.session_state:
            st.session_state[key] = "sintomas"

    cols = st.columns(3)
    for i, disease in enumerate(filtered):
        col       = cols[i % 3]
        lethal    = disease["lethal"]
        c_class   = "card-lethal" if lethal else "card-notlethal"
        b_class   = "badge-lethal" if lethal else "badge-notlethal"
        b_text    = "Potencialmente Letal" if lethal else "Geralmente Não Letal"
        tag_class = "tag-lethal" if lethal else "tag-notlethal"
        tab_key   = f"tab_{disease['name']}"

        with col:
            # Card header
            st.markdown(f"""
            <div class='disease-card {c_class}'>
                <div class='card-disease-name'>{disease['name']}</div>
                <div><span class='{b_class}'>{b_text}</span></div>
            </div>
            """, unsafe_allow_html=True)

            # Mini tab buttons
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Sintomas", key=f"btn_s_{disease['name']}", use_container_width=True):
                    st.session_state[tab_key] = "sintomas"
                    st.rerun()
            with b2:
                if st.button("Descrição", key=f"btn_d_{disease['name']}", use_container_width=True):
                    st.session_state[tab_key] = "descricao"
                    st.rerun()

            # Tab content
            active_tab = st.session_state[tab_key]
            if active_tab == "sintomas":
                tags_html = "".join([
                    f"<span class='symptom-tag {tag_class}'>{s}</span>"
                    for s in disease["symptoms"]
                ])
                st.markdown(f"<div class='symptom-area'>{tags_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card-description'>{disease['description']}</div>", unsafe_allow_html=True)

            # Footer
            st.markdown(f"""
            <div class='card-footer'>
                Vacina: <span>{disease['vaccine']}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

# ─── Vaccine Importance ────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Por Que se Vacinar?</div>", unsafe_allow_html=True)

st.markdown("""
<div class='vaccine-banner'>
    <div class='vaccine-title'>A Vacinação Salva Vidas</div>
    <div class='vaccine-text'>
        A vacinação é uma das intervenções de saúde pública mais eficazes já desenvolvidas pela humanidade.
        Ao vacinar-se, você não apenas se protege individualmente, mas contribui para a <strong>imunidade coletiva</strong>,
        protegendo também aqueles que não podem ser vacinados — como recém-nascidos, idosos e imunossuprimidos.
    </div>
    <div class='vaccine-points'>
        <div class='vaccine-point'><strong>Imunidade Coletiva</strong><br>Com 95% de cobertura, surtos são evitados e comunidades ficam protegidas.</div>
        <div class='vaccine-point'><strong>Custo-Benefício</strong><br>Vacinas são muito mais baratas do que tratar doenças graves. O SUS oferece gratuitamente.</div>
        <div class='vaccine-point'><strong>Erradicação de Doenças</strong><br>A poliomielite e a varíola foram erradicadas no Brasil graças à vacinação em massa.</div>
        <div class='vaccine-point'><strong>Proteção dos Vulneráveis</strong><br>Crianças, idosos e gestantes dependem da vacinação de toda a população.</div>
        <div class='vaccine-point'><strong>Segurança Comprovada</strong><br>Todas as vacinas do SUS passam por rigorosos testes de segurança e eficácia da ANVISA.</div>
        <div class='vaccine-point'><strong>Calendário Atualizado</strong><br>Mantenha sua caderneta de vacinação em dia. Há vacinas para todas as faixas etárias.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CTA ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='cta-container'>
    <a class='cta-button' href='https://meususdigital.saude.gov.br' target='_blank'>
        Encontrar Posto de Saúde Mais Próximo
    </a>
    <div style='color:#475569; font-size:0.82em; margin-top:12px;'>
        Acesse o <strong style='color:#6ee7b7;'>Meu SUS Digital</strong>
        e localize o posto de vacinação mais próximo de você
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Cobertura por Região ──────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Cobertura Vacinal por Região (%)</div>", unsafe_allow_html=True)

coverage   = {"Sudeste": 88, "Sul": 84, "Centro-Oeste": 76, "Nordeste": 72, "Norte": 65}
colors_cov = ["#10b981", "#6366f1", "#f59e0b", "#8b5cf6", "#ef4444"]
regions    = list(coverage.keys())
cov_vals   = list(coverage.values())

fig_cov = go.Figure(go.Bar(
    y=regions, x=cov_vals, orientation='h',
    marker=dict(color=colors_cov, line=dict(color='rgba(255,255,255,0.05)', width=1)),
    text=[f'{v}%' for v in cov_vals], textposition='outside',
    textfont=dict(color='#e2e8f0', size=12),
    hovertemplate='<b>%{y}</b>: %{x}%<extra></extra>'
))
fig_cov.add_vline(x=95, line_dash="dash", line_color="rgba(239,68,68,0.6)",
                  annotation_text="Meta: 95%", annotation_font_color="#f87171",
                  annotation_font_size=11)
fig_cov.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#94a3b8', family='Inter'),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
               range=[0, 105], ticksuffix='%', tickfont=dict(color='#64748b')),
    yaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8', size=12)),
    margin=dict(l=10, r=60, t=20, b=10), height=260, showlegend=False
)
st.plotly_chart(fig_cov, use_container_width=True, config={'displayModeBar': False})

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding:24px; border-top:1px solid rgba(99,102,241,0.15); margin-top:20px;'>
    <div style='color:#475569; font-size:0.82em;'>
        Dashboard de Saúde Pública · Dados: Ministério da Saúde do Brasil ·
        <a href='https://meususdigital.saude.gov.br' target='_blank' style='color:#6366f1;'>Meu SUS Digital</a>
    </div>
</div>
""", unsafe_allow_html=True)
