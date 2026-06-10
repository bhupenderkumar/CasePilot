"""
CasePilot V2 — Final Architecture Diagram
Comprehensive horizontal layout with all 10 architectural layers.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

fig, ax = plt.subplots(figsize=(36, 44))
ax.set_xlim(-1, 37)
ax.set_ylim(-1, 44)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# ── Colour palette ──
IDENTITY = '#1A5276'
SUMMARY  = '#E67E22'
CHAT     = '#2980B9'
ORCH     = '#8E44AD'
PROMPT   = '#16A085'
LLM      = '#2C3E50'
CACHE    = '#1ABC9C'
DATA     = '#2C3E80'
SECURITY = '#C0392B'
AUDIT    = '#7D3C98'
COST     = '#D4AC0D'
RELIABLE = '#943126'
OBSERVE  = '#117A65'
FUTURE   = '#5D6D7E'
EXTERN   = '#34495E'
ARROW_C  = '#555555'

W, H = 3.0, 1.2       # standard box
SW, SH = 2.4, 0.9     # small box
MW, MH = 3.6, 1.2     # medium-wide box

def box(x, y, c, t1, t2=None, w=W, h=H, fs=10, alpha=0.93):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                 boxstyle="round,pad=0.12", fc=c, ec='white', lw=2.5, alpha=alpha))
    if t2:
        ax.text(x, y + 0.18, t1, ha='center', va='center',
                fontsize=fs, fontweight='bold', color='white')
        ax.text(x, y - 0.18, t2, ha='center', va='center',
                fontsize=fs - 1.5, color='#DDD', style='italic')
    else:
        ax.text(x, y, t1, ha='center', va='center',
                fontsize=fs, fontweight='bold', color='white')

def sbox(x, y, c, t1, t2=None):
    box(x, y, c, t1, t2, SW, SH, 9)

def ar(x1, y1, x2, y2, c=ARROW_C, lw=1.8, lab=None, lo=0.25):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=c, lw=lw))
    if lab:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + lo, lab, ha='center', va='bottom',
                fontsize=7.5, color='#888', style='italic')

def section_bg(y_top, height, color, alpha=0.08):
    ax.add_patch(Rectangle((-0.5, y_top - height), 37, height,
                 fc=color, ec='none', alpha=alpha, zorder=0))

def section_label(y, label, color):
    ax.text(-0.2, y, label, ha='left', va='center',
            fontsize=11, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, lw=1.5, alpha=0.95))

def divider(y, style='--'):
    ax.plot([-0.5, 36.5], [y, y], color='#CCC', ls=style, lw=1, zorder=0)

# ═══════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════
ax.text(18, 43.2, 'CasePilot V2', ha='center', fontsize=26, fontweight='bold', color='#1A1A2E')
ax.text(18, 42.5, 'Enterprise AI Copilot for Case Investigation & Resolution',
        ha='center', fontsize=13, color='#666')
ax.text(18, 42.0, 'End-to-End Architecture', ha='center', fontsize=11, color='#999')

# ═══════════════════════════════════════════════════════════
# LAYER 1 — IDENTITY & ACCESS (y ~ 40)
# ═══════════════════════════════════════════════════════════
Y = 40.5
section_bg(Y + 0.8, 2.6, IDENTITY)
section_label(Y, '1. Identity & Access', IDENTITY)

box(6, Y, IDENTITY, 'Analyst Browser', 'Angular UI')
box(12, Y, IDENTITY, 'Microsoft Entra ID', 'SSO / Auth')
box(18, Y, IDENTITY, 'API Gateway', 'Routing / Rate Limit')
sbox(24, Y + 0.5, IDENTITY, 'RBAC')
sbox(24, Y - 0.5, IDENTITY, 'Rate Limiting')

ar(6 + W/2, Y, 12 - W/2, Y, IDENTITY, lab='authenticate')
ar(12 + W/2, Y, 18 - W/2, Y, IDENTITY, lab='token')
ar(18 + W/2, Y + 0.1, 24 - SW/2, Y + 0.5, IDENTITY)
ar(18 + W/2, Y - 0.1, 24 - SW/2, Y - 0.5, IDENTITY)

divider(Y - 1.5)

# ═══════════════════════════════════════════════════════════
# LAYER 2 — SUMMARY GENERATION (y ~ 36.5)
# ═══════════════════════════════════════════════════════════
Y = 36.5
section_bg(Y + 1.5, 4.5, SUMMARY)
section_label(Y + 1.2, '2. Summary Generation (Async)', SUMMARY)

# Row 1: Event pipeline
box(4, Y + 0.8, SUMMARY, 'Case Event', 'Backend Publish')
box(8.5, Y + 0.8, '#C0392B', 'Kafka Topic', 'case.events')
box(13, Y + 0.8, SUMMARY, 'Request Queue', '')
box(17.5, Y + 0.8, SUMMARY, 'Worker Pool', 'Summary Workers')
box(22, Y + 0.8, SUMMARY, 'Data Aggregator', 'Multi-Source')

ar(4 + W/2, Y + 0.8, 8.5 - W/2, Y + 0.8)
ar(8.5 + W/2, Y + 0.8, 13 - W/2, Y + 0.8)
ar(13 + W/2, Y + 0.8, 17.5 - W/2, Y + 0.8)
ar(17.5 + W/2, Y + 0.8, 22 - W/2, Y + 0.8)

# Data sources (below aggregator)
sbox(26.5, Y + 1.5, EXTERN, 'Case Mgmt')
sbox(26.5, Y + 0.5, EXTERN, 'Customer Svc')
sbox(30.5, Y + 1.5, EXTERN, 'Payment Svc')
sbox(30.5, Y + 0.5, EXTERN, 'Session Svc')
ar(22 + W/2, Y + 1.0, 26.5 - SW/2, Y + 1.5, EXTERN)
ar(22 + W/2, Y + 0.6, 26.5 - SW/2, Y + 0.5, EXTERN)
ar(22 + W/2, Y + 1.0, 30.5 - SW/2, Y + 1.5, EXTERN)
ar(22 + W/2, Y + 0.6, 30.5 - SW/2, Y + 0.5, EXTERN)

# Row 2: Security pipeline + AI
box(4, Y - 0.8, SECURITY, 'PII Redaction', 'Presidio')
box(8.5, Y - 0.8, SECURITY, 'Injection Detect', 'Prompt Safety')
box(13, Y - 0.8, SECURITY, 'Prompt Guardrails', 'Policy')
box(17.5, Y - 0.8, PROMPT, 'Context Builder', '')
box(22, Y - 0.8, ORCH, 'AI Orchestrator', '')

ar(22, Y + 0.8 - H/2, 22, Y - 0.8 + H/2, ORCH, lab='aggregate')
ar(17.5, Y + 0.8 - H/2, 4, Y - 0.8 + H/2, SECURITY, lw=1.2)
ar(4 + W/2, Y - 0.8, 8.5 - W/2, Y - 0.8)
ar(8.5 + W/2, Y - 0.8, 13 - W/2, Y - 0.8)
ar(13 + W/2, Y - 0.8, 17.5 - W/2, Y - 0.8)
ar(17.5 + W/2, Y - 0.8, 22 - W/2, Y - 0.8)

# Result queue + persistence
box(26.5, Y - 0.8, SUMMARY, 'Result Queue', '')
box(30.5, Y - 0.8, DATA, 'Summary DB', 'PostgreSQL')
ar(22 + W/2, Y - 0.8, 26.5 - W/2, Y - 0.8)
ar(26.5 + W/2, Y - 0.8, 30.5 - W/2, Y - 0.8, lab='persist')

# Retry + DLQ
sbox(34.5, Y + 0.2, RELIABLE, 'Retry Queue')
sbox(34.5, Y - 0.8, RELIABLE, 'DLQ')
ar(30.5 + W/2 - 0.5, Y - 0.3, 34.5 - SW/2, Y + 0.2, RELIABLE, lw=1.2)
ar(34.5, Y + 0.2 - SH/2, 34.5, Y - 0.8 + SH/2, RELIABLE, lw=1.2)

divider(Y - 2.2)

# ═══════════════════════════════════════════════════════════
# LAYER 3 — CHAT & Q&A (y ~ 31.5)
# ═══════════════════════════════════════════════════════════
Y = 31.5
section_bg(Y + 1.5, 4.5, CHAT)
section_label(Y + 1.2, '3. Chat & Q&A (Real-Time)', CHAT)

# Row 1: Chat pipeline
box(4, Y + 0.8, CHAT, 'Chat Service', 'Session Mgmt')
box(8.5, Y + 0.8, CACHE, 'Redis Session', 'Cache')
box(13, Y + 0.8, SECURITY, 'PII Redaction', '')
box(17.5, Y + 0.8, SECURITY, 'Injection Detect', '')
box(22, Y + 0.8, SECURITY, 'Prompt Guardrails', '')

ar(18, 40.5 - H/2 - 0.3, 4, Y + 0.8 + H/2, CHAT, lab='POST /chat')
ar(4 + W/2, Y + 0.8, 8.5 - W/2, Y + 0.8)
ar(8.5 + W/2, Y + 0.8, 13 - W/2, Y + 0.8)
ar(13 + W/2, Y + 0.8, 17.5 - W/2, Y + 0.8)
ar(17.5 + W/2, Y + 0.8, 22 - W/2, Y + 0.8)

# Row 2: Context -> Orchestrator -> Validation -> Stream
box(4, Y - 0.8, PROMPT, 'Context Builder', '')
box(8.5, Y - 0.8, ORCH, 'AI Orchestrator', '')
box(13, Y - 0.8, SECURITY, 'Response Valid.', 'Safety Check')
box(17.5, Y - 0.8, CHAT, 'SSE Streaming', 'Real-Time')
box(22, Y - 0.8, DATA, 'Chat DB', 'PostgreSQL')

ar(22, Y + 0.8 - H/2, 4, Y - 0.8 + H/2, PROMPT, lw=1.2)
ar(4 + W/2, Y - 0.8, 8.5 - W/2, Y - 0.8)
ar(8.5 + W/2, Y - 0.8, 13 - W/2, Y - 0.8)
ar(13 + W/2, Y - 0.8, 17.5 - W/2, Y - 0.8)
ar(17.5 + W/2, Y - 0.8, 22 - W/2, Y - 0.8, lab='store')

# Chat retry path
sbox(26.5, Y - 0.8, RELIABLE, 'Chat Retry Q')
sbox(30.5, Y - 0.8, RELIABLE, 'Chat DLQ')
ar(8.5 + W/2 + 0.2, Y - 0.8 - H/2 + 0.2, 26.5 - SW/2, Y - 0.8, RELIABLE, lw=1.2, lab='on failure')
ar(26.5 + SW/2, Y - 0.8, 30.5 - SW/2, Y - 0.8, RELIABLE, lw=1.2)

divider(Y - 2.2)

# ═══════════════════════════════════════════════════════════
# LAYER 4 — AI ORCHESTRATOR (y ~ 26.5)
# ═══════════════════════════════════════════════════════════
Y = 26.5
section_bg(Y + 0.8, 2.6, ORCH)
section_label(Y, '4. AI Orchestrator', ORCH)

caps = ['Model\nSelection', 'Retry\nPolicy', 'Provider\nFailover', 'Token\nTracking',
        'Cost\nTracking', 'Prompt\nVersioning', 'Response\nValidation', 'Routing\nDecisions']
for i, cap in enumerate(caps):
    cx = 4 + i * 4
    sbox(cx, Y, ORCH, cap)

divider(Y - 1.2)

# ═══════════════════════════════════════════════════════════
# LAYER 5 — PROMPT MANAGEMENT (y ~ 24)
# ═══════════════════════════════════════════════════════════
Y = 24
section_bg(Y + 0.8, 2.4, PROMPT)
section_label(Y, '5. Prompt Management', PROMPT)

box(6, Y, PROMPT, 'Prompt Service', '')
box(12, Y, PROMPT, 'Prompt Repository', 'Versioned')
sbox(18, Y, PROMPT, 'Version Control')
sbox(22, Y, PROMPT, 'Rollback')
sbox(26, Y, PROMPT, 'A/B Testing')
sbox(30, Y, PROMPT, 'Governance')

ar(6 + W/2, Y, 12 - W/2, Y)
ar(12 + W/2, Y, 18 - SW/2, Y)
ar(18 + SW/2, Y, 22 - SW/2, Y)
ar(22 + SW/2, Y, 26 - SW/2, Y)
ar(26 + SW/2, Y, 30 - SW/2, Y)

divider(Y - 1.2)

# ═══════════════════════════════════════════════════════════
# LAYER 6 — LLM PROVIDER LAYER (y ~ 21.5)
# ═══════════════════════════════════════════════════════════
Y = 21.5
section_bg(Y + 1, 3, LLM)
section_label(Y + 0.5, '6. LLM Provider Layer', LLM)

box(8, Y + 0.5, LLM, 'LLM Provider Layer', 'Abstraction')

box(4, Y - 0.8, '#0078D4', 'Azure OpenAI', 'Primary')
box(12, Y - 0.8, '#D4A76A', 'Anthropic Claude', 'Long Context')
box(20, Y - 0.8, '#4285F4', 'Google Gemini', 'Multimodal')
box(28, Y - 0.8, FUTURE, 'Future Providers', 'Pluggable')

ar(8 - 0.5, Y + 0.5 - H/2, 4, Y - 0.8 + H/2, LLM)
ar(8 + 0.5, Y + 0.5 - H/2, 12, Y - 0.8 + H/2, LLM)
ar(8 + W/2 + 1, Y + 0.5 - H/2, 20, Y - 0.8 + H/2, LLM)
ar(8 + W/2 + 3, Y + 0.5 - 0.3, 28 - W/2, Y - 0.8 + H/2, LLM)

# Failover chain
ax.text(16, Y + 0.5, 'Failover:  Azure  -->  Claude  -->  Gemini',
        ha='center', fontsize=9, color='#C0392B', style='italic',
        bbox=dict(boxstyle='round,pad=0.2', fc='#FFEBEE', ec='#C0392B', lw=1, alpha=0.8))

divider(Y - 2)

# ═══════════════════════════════════════════════════════════
# LAYER 7 — CACHING (y ~ 18)
# ═══════════════════════════════════════════════════════════
Y = 18
section_bg(Y + 0.8, 2.4, CACHE)
section_label(Y, '7. Caching Layer (Redis)', CACHE)

caches = ['Session\nCache', 'Summary\nCache', 'Context\nCache', 'Response\nCache', 'Rate Limit\nCache']
for i, c in enumerate(caches):
    cx = 5 + i * 5.5
    sbox(cx, Y, CACHE, c)

divider(Y - 1.2)

# ═══════════════════════════════════════════════════════════
# LAYER 8 — SERVICE-OWNED DATABASES (y ~ 15.5)
# ═══════════════════════════════════════════════════════════
Y = 15.5
section_bg(Y + 0.8, 2.4, DATA)
section_label(Y, '8. Data Layer (Service-Owned DBs)', DATA)

dbs = ['Chat DB', 'Summary DB', 'Audit DB', 'Cost DB', 'Prompt DB']
for i, d in enumerate(dbs):
    cx = 5 + i * 5.5
    sbox(cx, Y, DATA, d, 'PostgreSQL')

divider(Y - 1.2)

# ═══════════════════════════════════════════════════════════
# LAYER 9 — SECURITY & GOVERNANCE (y ~ 13)
# ═══════════════════════════════════════════════════════════
Y = 13
section_bg(Y + 0.8, 2.6, SECURITY)
section_label(Y, '9. Security & Governance', SECURITY)

sec_items = ['Entra ID\nAuth', 'RBAC\nAuthZ', 'PII\nRedaction', 'Injection\nDetection',
             'Prompt\nGuardrails', 'Content\nFiltering', 'Audit\nLogging', 'Key Vault\nSecrets']
for i, s in enumerate(sec_items):
    cx = 4 + i * 4
    sbox(cx, Y, SECURITY, s)

divider(Y - 1.2)

# ═══════════════════════════════════════════════════════════
# LAYER 10 — COST & AUDIT & RELIABILITY (y ~ 10)
# ═══════════════════════════════════════════════════════════
Y = 10
section_bg(Y + 1, 3.2, AUDIT)
section_label(Y + 0.6, '10. Cost, Audit & Reliability', AUDIT)

# Audit
box(4, Y + 0.5, AUDIT, 'Audit Service', 'Traceability')
ax.text(4, Y - 0.5, 'UserId | CaseId | Model\nTokens | Cost | Timestamp',
        ha='center', fontsize=7.5, color='#666', style='italic')

# Cost
box(12, Y + 0.5, COST, 'Cost Service', 'Token Tracking')
ax.text(12, Y - 0.5, 'Dashboards | Alerts\nBudgets | Trends',
        ha='center', fontsize=7.5, color='#666', style='italic')

# Reliability
box(20, Y + 0.5, RELIABLE, 'Reliability Layer', '')
ax.text(20, Y - 0.5, 'Retry | DLQ | Circuit Breaker\nFailover | Idempotency',
        ha='center', fontsize=7.5, color='#666', style='italic')

# Observability
box(28, Y + 0.5, OBSERVE, 'Observability', 'Monitoring')
ax.text(28, Y - 0.5, 'OpenTelemetry | Prometheus\nGrafana | Alerting',
        ha='center', fontsize=7.5, color='#666', style='italic')

divider(Y - 1.5)

# ═══════════════════════════════════════════════════════════
# FUTURE ROADMAP (y ~ 7)
# ═══════════════════════════════════════════════════════════
Y = 7
section_bg(Y + 0.8, 2.4, FUTURE)
section_label(Y, 'Future Roadmap (V3)', FUTURE)

futures = ['Vector DB\nEmbeddings', 'RAG\nPipeline', 'Semantic\nSearch',
           'Multi-Agent\nWorkflows', 'Feedback\nLoop', 'AI Eval\nFramework']
for i, f in enumerate(futures):
    cx = 4 + i * 5
    sbox(cx, Y, FUTURE, f)

# ═══════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════
LY = 4.5
ax.text(18, LY + 0.8, 'Legend', ha='center', fontsize=10, fontweight='bold', color='#333')
items = [
    (IDENTITY, 'Identity & Access'),  (SUMMARY, 'Summary Flow'),
    (CHAT, 'Chat Flow'),             (ORCH, 'AI Orchestrator'),
    (PROMPT, 'Prompt Mgmt'),         (LLM, 'LLM Providers'),
    (CACHE, 'Caching'),              (DATA, 'Databases'),
    (SECURITY, 'Security'),          (RELIABLE, 'Reliability'),
    (AUDIT, 'Audit'),                (COST, 'Cost'),
    (OBSERVE, 'Observability'),      (FUTURE, 'Future'),
]
for i, (c, label) in enumerate(items):
    col = i % 7
    row = i // 7
    lx = 2.5 + col * 4.8
    ly = LY - row * 0.7
    ax.add_patch(FancyBboxPatch((lx - 0.5, ly - 0.2), 1.0, 0.4,
                 boxstyle="round,pad=0.05", fc=c, ec='white', lw=1, alpha=0.9))
    ax.text(lx + 0.7, ly, label, ha='left', va='center', fontsize=8, color='#555')

# ── Save ──
plt.tight_layout()
os.makedirs('docs/images', exist_ok=True)
out = 'docs/images/final_architecture_v2.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print(f'Generated: {out}')
