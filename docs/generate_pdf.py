"""
CasePilot V2 - Professional PDF Generator
Clean design inspired by Google/Meta material design guidelines.
"""
import re
from fpdf import FPDF

# ── Colour Palette (Material Design inspired) ──
WHITE       = (255, 255, 255)
BG_LIGHT    = (250, 250, 250)
TEXT_PRIMARY = (33, 33, 33)      # #212121
TEXT_SECOND  = (97, 97, 97)      # #616161
TEXT_LIGHT   = (158, 158, 158)   # #9E9E9E
ACCENT       = (25, 118, 210)    # #1976D2  Material Blue 700
ACCENT_DARK  = (13, 71, 161)     # #0D47A1  Material Blue 900
ACCENT_LIGHT = (227, 242, 253)   # #E3F2FD  Material Blue 50
CODE_BG      = (245, 245, 245)   # #F5F5F5
CODE_BORDER  = (224, 224, 224)   # #E0E0E0
TABLE_HEADER = (33, 150, 243)    # #2196F3
TABLE_ALT    = (245, 248, 255)
DIVIDER      = (224, 224, 224)
GREEN        = (46, 125, 50)
ORANGE       = (230, 126, 34)
RED          = (198, 40, 40)

class CasePilotPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(True, margin=25)
        self.set_margins(25, 25, 25)
        
        # Register fonts - use built-in Helvetica (clean sans-serif)
        self.section_number = 0
    
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*TEXT_LIGHT)
            self.cell(0, 8, 'CasePilot V2  |  High Level Design', align='L')
            self.cell(0, 8, f'Page {self.page_no()}', align='R', new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(*DIVIDER)
            self.line(25, 15, 185, 15)
            self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*TEXT_LIGHT)
        self.cell(0, 10, 'Confidential  |  Bhupender Sharma  |  June 2026', align='C')

    # ── Cover Page ──
    def cover_page(self):
        self.add_page()
        
        # Top accent bar
        self.set_fill_color(*ACCENT_DARK)
        self.rect(0, 0, 210, 6, 'F')
        
        # Title block
        self.ln(60)
        self.set_font('Helvetica', 'B', 36)
        self.set_text_color(*TEXT_PRIMARY)
        self.cell(0, 18, 'CasePilot V2', align='C', new_x="LMARGIN", new_y="NEXT")
        
        self.ln(3)
        self.set_font('Helvetica', '', 16)
        self.set_text_color(*ACCENT)
        self.cell(0, 10, 'AI-Powered Security Investigation Assistant', align='C', new_x="LMARGIN", new_y="NEXT")
        
        self.ln(2)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.8)
        self.line(60, self.get_y(), 150, self.get_y())
        
        self.ln(8)
        self.set_font('Helvetica', '', 14)
        self.set_text_color(*TEXT_SECOND)
        self.cell(0, 8, 'High Level Design (HLD)', align='C', new_x="LMARGIN", new_y="NEXT")
        
        # Metadata
        self.ln(30)
        meta = [
            ('Document Type', 'Technical Proposal'),
            ('Version', '2.1'),
            ('Author', 'Bhupender Sharma'),
            ('Date', 'June 2026'),
            ('Status', 'Final'),
            ('Audience', 'Architects, Engineering Leads, Security Teams'),
        ]
        self.set_font('Helvetica', '', 11)
        for label, value in meta:
            self.set_text_color(*TEXT_LIGHT)
            self.cell(45, 8, label, align='R')
            self.set_text_color(*TEXT_PRIMARY)
            self.set_font('Helvetica', 'B', 11)
            self.cell(5, 8, '')
            self.cell(0, 8, value, new_x="LMARGIN", new_y="NEXT")
            self.set_font('Helvetica', '', 11)
        
        # Bottom accent bar
        self.set_fill_color(*ACCENT_DARK)
        self.rect(0, 291, 210, 6, 'F')

    # ── Table of Contents ──
    def toc_page(self, sections):
        self.add_page()
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(*TEXT_PRIMARY)
        self.cell(0, 14, 'Table of Contents', new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.6)
        self.line(25, self.get_y(), 80, self.get_y())
        self.ln(8)
        
        for num, title in sections:
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(*ACCENT_DARK)
            self.cell(12, 8, str(num))
            self.set_font('Helvetica', '', 11)
            self.set_text_color(*TEXT_PRIMARY)
            self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")

    # ── Heading helpers ──
    def h1(self, text):
        self.section_number += 1
        self.add_page()
        
        # Section number + accent bar
        self.set_fill_color(*ACCENT)
        self.rect(25, self.get_y(), 4, 14, 'F')
        
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(*TEXT_PRIMARY)
        x = self.get_x()
        self.cell(10, 14, '')
        self.cell(0, 14, f'{self.section_number}. {text}', new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
    
    def h2(self, text):
        self.ln(4)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*ACCENT_DARK)
        self.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
    
    def h3(self, text):
        self.ln(2)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*TEXT_PRIMARY)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    # ── Body text ──
    def body(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*TEXT_PRIMARY)
        self.multi_cell(0, 5.5, text)
        self.ln(2)
    
    def body_bold(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*TEXT_PRIMARY)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    # ── Bullet list ──
    def bullet_list(self, items):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*TEXT_PRIMARY)
        left = self.l_margin
        for item in items:
            self.set_x(left)
            self.set_text_color(*ACCENT)
            self.cell(6, 5.5, '-')  # bullet
            self.set_text_color(*TEXT_PRIMARY)
            w = self.w - self.r_margin - self.get_x()
            if w < 10:
                self.ln()
                self.set_x(left + 6)
                w = self.w - self.r_margin - self.get_x()
            self.multi_cell(w, 5.5, item)
        self.ln(2)

    # ── Table ──
    def data_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = 160 / len(headers)
            col_widths = [w] * len(headers)
        
        # Header
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(*TABLE_HEADER)
        self.set_text_color(*WHITE)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=0, fill=True, align='L')
        self.ln()
        
        # Rows
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*TEXT_PRIMARY)
        for r_idx, row in enumerate(rows):
            if r_idx % 2 == 1:
                self.set_fill_color(*TABLE_ALT)
                fill = True
            else:
                fill = False
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6.5, str(cell), border=0, fill=fill, align='L')
            self.ln()
        self.ln(3)

    # ── Code block ──
    def code_block(self, code, language=''):
        self.set_fill_color(*CODE_BG)
        self.set_draw_color(*CODE_BORDER)
        
        lines = code.strip().split('\n')
        block_height = len(lines) * 4.5 + 6
        
        # Check if we need a new page
        if self.get_y() + block_height > 270:
            self.add_page()
        
        y_start = self.get_y()
        self.rect(25, y_start, 160, block_height, 'DF')
        
        self.set_font('Courier', '', 8)
        self.set_text_color(*TEXT_PRIMARY)
        self.ln(3)
        for line in lines:
            self.cell(5, 4.5, '')
            self.cell(0, 4.5, line[:100], new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    # ── Callout box ──
    def callout(self, title, text, color=ACCENT):
        self.set_fill_color(color[0], color[1], color[2])
        y = self.get_y()
        self.rect(25, y, 3, 20, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*color)
        self.cell(8, 6, '')
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*TEXT_SECOND)
        self.cell(8, 5, '')
        self.multi_cell(150, 5, text)
        self.ln(4)

    # ── Divider ──
    def divider(self):
        self.ln(2)
        self.set_draw_color(*DIVIDER)
        self.set_line_width(0.3)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(4)


def build_pdf():
    pdf = CasePilotPDF()
    
    # ═══════════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════════
    pdf.cover_page()
    
    # ═══════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════
    sections = [
        (1, 'Executive Summary'),
        (2, 'Problem Statement'),
        (3, 'Goals'),
        (4, 'High-Level Architecture'),
        (5, 'Architecture Principles'),
        (6, 'Core Services'),
        (7, 'Summary Generation Service - Deep Dive'),
        (8, 'AI Gateway Service - Deep Dive'),
        (9, 'Chat Service'),
        (10, 'Security Design'),
        (11, 'Monitoring & Observability'),
        (12, 'Future Enhancements'),
        (13, 'Conclusion'),
    ]
    pdf.toc_page(sections)
    
    # ═══════════════════════════════════════
    # 1. EXECUTIVE SUMMARY
    # ═══════════════════════════════════════
    pdf.h1('Executive Summary')
    pdf.body('CasePilot V2 is an AI-powered investigation platform designed to assist security analysts in understanding and investigating fraud, risk, and security-related cases.')
    pdf.body('The platform integrates with existing enterprise systems, automatically generates investigation summaries, and provides a conversational interface for analysts to ask questions about a case.')
    pdf.body('The solution follows a service-oriented architecture and centralizes all AI interactions through a dedicated AI Gateway Service, allowing the organization to remain provider-agnostic while maintaining security, observability, and operational control.')
    
    # ═══════════════════════════════════════
    # 2. PROBLEM STATEMENT
    # ═══════════════════════════════════════
    pdf.h1('Problem Statement')
    pdf.body('Security analysts often need to review information spread across multiple systems:')
    pdf.bullet_list([
        'Case Management System',
        'Customer Management System',
        'Payment Platform',
        'Session & Device Intelligence Platform',
        'Risk & Fraud Detection Systems',
    ])
    pdf.body('As a result:')
    pdf.bullet_list([
        'Investigations are slow',
        'Context gathering is manual',
        'Summaries are inconsistent',
        'Knowledge is difficult to transfer',
        'Analysts spend more time collecting information than analyzing it',
    ])
    pdf.body('CasePilot aims to reduce investigation time by automatically aggregating information and presenting it through AI-generated summaries and conversational interfaces.')
    
    # ═══════════════════════════════════════
    # 3. GOALS
    # ═══════════════════════════════════════
    pdf.h1('Goals')
    pdf.h2('Functional Goals')
    pdf.bullet_list([
        'Automatic case summarization',
        'AI-powered chat assistant',
        'Multi-model LLM support',
        'Cost tracking and monitoring',
        'Secure processing of customer data',
    ])
    pdf.h2('Non-Functional Goals')
    pdf.bullet_list([
        'Scalability',
        'Reliability',
        'Security',
        'Auditability',
        'Provider independence',
        'Cost optimization',
    ])
    
    # ═══════════════════════════════════════
    # 4. HIGH-LEVEL ARCHITECTURE
    # ═══════════════════════════════════════
    pdf.h1('High-Level Architecture')
    pdf.body('The system consists of three primary business capabilities:')
    pdf.bullet_list([
        'Summary Generation Flow - Generates AI summaries when case events occur',
        'Chat & Q&A Flow - Allows analysts to interact with case data using natural language',
        'Cost & Usage Tracking - Tracks AI usage, token consumption, and operational costs',
    ])
    pdf.body('A dedicated AI Gateway Service centralizes all communication with LLM providers.')
    
    # ═══════════════════════════════════════
    # 5. ARCHITECTURE PRINCIPLES
    # ═══════════════════════════════════════
    pdf.h1('Architecture Principles')
    
    principles = [
        ('Separation of Responsibilities', 'Each service owns a specific business capability.'),
        ('Event-Driven Processing', 'Case updates are processed asynchronously through Kafka.'),
        ('Provider Agnostic Design', 'Business services never directly call OpenAI, Claude, or Gemini. All AI interactions occur through AI Gateway.'),
        ('Security First', 'PII is removed before information is sent to external AI providers.'),
        ('Observability', 'All requests, failures, and token consumption are tracked.'),
    ]
    for title, desc in principles:
        pdf.h3(title)
        pdf.body(desc)
    
    # ═══════════════════════════════════════
    # 6. CORE SERVICES
    # ═══════════════════════════════════════
    pdf.h1('Core Services')
    pdf.data_table(
        ['Service', 'Responsibility'],
        [
            ['Summary Service', 'Generates case summaries'],
            ['Chat Service', 'Handles analyst conversations'],
            ['AI Gateway Service', 'Manages LLM providers'],
            ['Cost Service', 'Tracks usage and costs'],
            ['Kafka', 'Event transport'],
            ['Redis', 'Session caching'],
            ['Summary Database', 'Stores summaries'],
            ['Chat Database', 'Stores conversations'],
            ['Usage Database', 'Stores AI metrics'],
        ],
        [60, 100]
    )
    
    # ═══════════════════════════════════════
    # 7. SUMMARY GENERATION SERVICE — DEEP DIVE
    # ═══════════════════════════════════════
    pdf.h1('Summary Generation Service - Deep Dive')
    
    pdf.body('The Summary Generation Service is the primary value-delivery component of CasePilot. It consumes case lifecycle events from Kafka, aggregates investigation data from four upstream systems, applies security controls, and produces structured AI-generated investigation summaries.')
    
    # 7.2 Kafka Consumer
    pdf.h2('7.1 Kafka Consumer Design')
    pdf.body('The service uses a Kafka consumer group with configurable concurrency.')
    pdf.data_table(
        ['Parameter', 'Value', 'Rationale'],
        [
            ['Consumer Group', 'casepilot-summary-consumer', 'Dedicated consumer group'],
            ['Topic', 'case-events', 'All case lifecycle events'],
            ['Partition Strategy', 'By caseId', 'Ordered processing per case'],
            ['Auto Commit', 'Disabled', 'Manual commit after persistence'],
            ['Max Poll Records', '10', 'Bounded batch size'],
            ['Concurrency', '3', 'Parallel partition consumers'],
        ],
        [45, 55, 60]
    )
    pdf.callout('Why manual commit?', 'Auto-commit risks marking a message as consumed before processing completes. If the service crashes mid-processing, the message is lost. With manual commit, the offset is committed only after the summary is persisted.')
    
    pdf.body('Input Event Schema:')
    pdf.code_block('''{
  "eventId": "evt-a8f3c912",
  "caseId": "CASE-1001",
  "eventType": "CASE_CREATED",
  "timestamp": "2026-06-10T10:00:00Z",
  "source": "case-management-service",
  "version": "1.0"
}''')
    
    pdf.body('Event Validation: Before processing, each event is validated against schema, checked for duplicates using Redis (TTL 24h), and verified against the event type whitelist. Invalid events are routed to the DLQ.')
    
    # 7.3 Data Aggregation
    pdf.h2('7.2 Data Aggregation Strategy')
    pdf.body('The service makes parallel HTTP calls to four upstream services. Parallel execution is critical because sequential calls would add 2-4 seconds of latency per additional system.')
    
    pdf.data_table(
        ['Service', 'Timeout', 'Retry', 'On Failure'],
        [
            ['Case Management', '3s', '1 retry', 'Abort - case data required'],
            ['Customer System', '2s', '1 retry', 'Proceed with partial data'],
            ['Payment System', '3s', '1 retry', 'Proceed with partial data'],
            ['Session System', '2s', '1 retry', 'Proceed without session data'],
        ],
        [40, 25, 25, 70]
    )
    
    pdf.callout('Why is Case Management mandatory?', 'Without case details (alerts, risk score, case status), a summary would be meaningless. Other data sources enrich the summary but are not strictly required.')
    
    pdf.body('Aggregated Context Model:')
    pdf.code_block('''{
  "caseId": "CASE-1001",
  "caseStatus": "OPEN",
  "riskScore": 82,
  "alerts": [
    {
      "alertId": "ALR-501",
      "type": "VELOCITY_CHECK",
      "severity": "HIGH",
      "description": "15 transactions in 2 hours from 3 countries"
    }
  ],
  "customer": {
    "customerId": "CUST-2200",
    "accountAge": "P2Y3M",
    "kycStatus": "VERIFIED",
    "riskTier": "MEDIUM"
  },
  "transactions": [ ... ],
  "sessions": [ ... ],
  "dataCompleteness": {
    "caseData": true,
    "customerData": true,
    "paymentData": true,
    "sessionData": true
  }
}''')
    
    pdf.body('The dataCompleteness field tells the LLM which data sources were available. If sessionData is false, the summary includes a note: "Session data was unavailable during summary generation."')
    
    # 7.4 PII Redaction
    pdf.h2('7.3 PII Redaction Pipeline')
    pdf.body('PII redaction occurs in two stages before data reaches the AI provider.')
    
    pdf.h3('Stage 1: Pattern-Based Redaction (Regex)')
    pdf.data_table(
        ['Pattern', 'Example', 'Replacement'],
        [
            ['Email', 'john@example.com', '[EMAIL_1]'],
            ['Phone', '+44 7911 123456', '[PHONE_1]'],
            ['IBAN', 'DE89 3704 0044 0532 0130 00', '[IBAN_1]'],
            ['Credit Card', '4111 1111 1111 1111', '[CARD_1]'],
            ['IP Address', '192.168.1.100', '[IP_1]'],
        ],
        [40, 70, 50]
    )
    
    pdf.h3('Stage 2: Named Entity Recognition (NER via Microsoft Presidio)')
    pdf.data_table(
        ['Entity', 'Example', 'Replacement'],
        [
            ['Person Name', 'John Smith', '[PERSON_1]'],
            ['Address', '123 Baker Street, London', '[ADDRESS_1]'],
            ['Organization', 'Acme Corp', '[ORG_1]'],
        ],
        [40, 70, 50]
    )
    
    pdf.callout('What is NOT redacted (and why)', 'Transaction amounts, timestamps, risk scores, alert types, and country codes are preserved. The LLM needs these for risk analysis, temporal pattern detection, and cross-border investigation.')
    
    pdf.body('Re-identification: After the LLM generates the summary, placeholders are replaced back with original values using an in-memory mapping. This mapping is never persisted or logged.')
    
    # 7.5 Context Window
    pdf.h2('7.4 Context Window Management')
    pdf.body('A fraud case can contain 200+ transactions. Sending all of them would exceed the context window and waste tokens.')
    
    pdf.h3('Token Budget Allocation')
    pdf.data_table(
        ['Component', 'Budget', 'Notes'],
        [
            ['System prompt', '1,500 tokens', 'Fixed'],
            ['Case metadata', '1,000 tokens', 'Fixed'],
            ['Customer profile', '500 tokens', 'Fixed'],
            ['Alerts', '1,500 tokens', '~15 alerts max'],
            ['Transactions', '4,000 tokens', '~40 transactions'],
            ['Sessions', '1,500 tokens', '~15 sessions'],
            ['Response buffer', '4,000 tokens', 'For generated summary'],
            ['Total', '14,000 tokens', ''],
        ],
        [50, 45, 65]
    )
    
    pdf.h3('Entity Prioritization')
    pdf.body('When entities exceed their budget, they are ranked by priority score:')
    pdf.code_block('priority = 0.4 * risk_score + 0.25 * recency + 0.2 * amount_normalized + 0.15 * anomaly_count')
    pdf.body('Top-K entities per type are included. Remaining entities are summarized as a count with totals.')
    
    pdf.h3('Large Case Strategy (200+ entities)')
    pdf.body('For exceptionally large cases, a map-reduce approach is used:')
    pdf.bullet_list([
        'Chunk entities into groups of 40',
        'Generate a mini-summary for each chunk',
        'Merge mini-summaries into a final summary',
    ])
    pdf.body('This costs ~3x more tokens but ensures no significant information is lost.')
    
    # 7.6 Prompt Engineering
    pdf.h2('7.5 Prompt Engineering')
    pdf.body('The prompt is structured, versioned, and stored in a Prompt Repository.')
    
    pdf.h3('System Prompt (v2.3)')
    pdf.code_block('''You are a fraud investigation assistant for a financial institution.

Your task: analyze the provided case data and produce a structured
investigation summary.

RULES:
1. Base your analysis ONLY on the provided data
2. Never invent transactions, alerts, or entities not in the input
3. If data is missing, explicitly state what is unavailable
4. Use professional language suitable for compliance documentation
5. Include specific transaction IDs, amounts, and timestamps
6. Provide a risk assessment with supporting evidence

OUTPUT FORMAT: JSON with fields:
  overview, keyFindings, riskAssessment, timelineOfEvents,
  entitiesInvolved, recommendedActions, dataGaps''')
    
    pdf.callout('Why JSON output?', 'Structured JSON allows the frontend to render each section independently (risk assessment as a badge, timeline as a visual). It also enables programmatic validation.')
    
    pdf.h3('Prompt Version History')
    pdf.data_table(
        ['Version', 'Change', 'Date'],
        [
            ['v1.0', 'Initial prompt', '2026-05-01'],
            ['v2.0', 'Added timeline of events', '2026-05-15'],
            ['v2.1', 'Added data gaps section', '2026-05-20'],
            ['v2.3', 'Refined risk assessment format', '2026-06-01'],
        ],
        [30, 90, 40]
    )
    
    # 7.7 Anti-Hallucination
    pdf.h2('7.6 Response Validation (Anti-Hallucination)')
    pdf.body('LLMs can generate plausible but incorrect information. In fraud investigation, a hallucinated transaction could lead to a wrong decision.')
    
    pdf.h3('Validation Rules')
    pdf.bullet_list([
        'Schema validation - response must match expected JSON structure',
        'Entity cross-reference - every transaction ID in the summary must exist in input data',
        'Amount verification - stated amounts are cross-checked against source data',
        'Completeness check - all required sections must be present',
        'Content safety - no prompt leakage (system prompt in output)',
    ])
    
    pdf.h3('On Validation Failure')
    pdf.data_table(
        ['Issue', 'Action'],
        [
            ['Missing optional field', 'Auto-fix and proceed'],
            ['Entity hallucination', 'Remove reference, add warning'],
            ['Invalid JSON / empty', 'Retry (max 2 retries)'],
            ['Persistent failure', 'Store "failed" record, notify analyst'],
        ],
        [60, 100]
    )
    
    # 7.8 Database Schema
    pdf.h2('7.7 Persistence and Versioning')
    pdf.code_block('''CREATE TABLE case_summary (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         VARCHAR(100) NOT NULL,
    version         INTEGER NOT NULL DEFAULT 1,
    summary_json    JSONB NOT NULL,
    model_name      VARCHAR(50) NOT NULL,
    model_provider  VARCHAR(50) NOT NULL,
    prompt_version  VARCHAR(20) NOT NULL,
    input_tokens    INTEGER NOT NULL,
    output_tokens   INTEGER NOT NULL,
    cost_usd        DECIMAL(10,6) NOT NULL,
    processing_ms   INTEGER NOT NULL,
    data_completeness JSONB NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_case_version UNIQUE (case_id, version)
);''')
    pdf.callout('Why JSONB?', 'The summary structure evolves as prompt versions change. JSONB allows schema flexibility without migrations. PostgreSQL JSONB supports indexing and querying individual fields.')
    
    # 7.9 Reliability
    pdf.h2('7.8 Reliability Design')
    pdf.h3('Retry Policy')
    pdf.data_table(
        ['Attempt', 'Wait', 'Action'],
        [
            ['1', 'Immediate', 'Process event'],
            ['2', '2 seconds', 'Retry'],
            ['3', '4 seconds', 'Retry'],
            ['After 3', '-', 'Route to DLQ'],
        ],
        [40, 40, 80]
    )
    
    pdf.h3('Idempotency')
    pdf.body('Key: caseId + eventId. Before processing, the service checks Redis. After success, the key is stored with 24h TTL. This prevents duplicates from Kafka at-least-once delivery.')
    
    # 7.10 Performance
    pdf.h2('7.9 Performance Targets')
    pdf.data_table(
        ['Metric', 'Target'],
        [
            ['End-to-end latency (P50)', '< 8 seconds'],
            ['End-to-end latency (P95)', '< 15 seconds'],
            ['Data aggregation (P95)', '< 3 seconds'],
            ['LLM response (P95)', '< 10 seconds'],
            ['Success rate', '> 99%'],
            ['Throughput', '100 summaries/minute'],
        ],
        [80, 80]
    )
    
    # ═══════════════════════════════════════
    # 8. AI GATEWAY SERVICE — DEEP DIVE
    # ═══════════════════════════════════════
    pdf.h1('AI Gateway Service - Deep Dive')
    
    pdf.body('The AI Gateway is the single point of contact between CasePilot business services and external LLM providers. It encapsulates all AI-specific concerns: provider routing, retry logic, circuit breaking, failover, token tracking, cost calculation, and response validation.')
    pdf.body('No business service communicates directly with an LLM provider.')
    
    # 8.2 API Contract
    pdf.h2('8.1 API Contract')
    
    pdf.h3('Generate Summary')
    pdf.code_block('''POST /api/v1/ai/generate
Content-Type: application/json
Authorization: Bearer <service-token>
X-Correlation-Id: corr-abc123
X-Idempotency-Key: CASE-1001:v2.3:evt-a8f3c912

{
  "requestType": "SUMMARY",
  "caseId": "CASE-1001",
  "context": { ... },
  "promptVersion": "v2.3",
  "maxTokens": 4000,
  "temperature": 0.2,
  "responseFormat": "json",
  "priority": "NORMAL",
  "callerService": "summary-service"
}''')
    
    pdf.h3('Response')
    pdf.code_block('''{
  "requestId": "req-xyz789",
  "status": "SUCCESS",
  "provider": "azure-openai",
  "model": "gpt-4o",
  "response": { ... },
  "usage": {
    "inputTokens": 3200,
    "outputTokens": 1850,
    "totalTokens": 5050,
    "costUsd": 0.065
  },
  "latencyMs": 4200,
  "promptVersion": "v2.3"
}''')
    
    # 8.3 Pipeline
    pdf.h2('8.2 Request Processing Pipeline')
    pdf.body('Every request passes through a 7-stage pipeline:')
    
    stages = [
        ('Stage 1: Request Validation', 'Validates required fields, maxTokens range (100-8000), temperature (0.0-1.0), payload size (< 500KB), and caller service registration.'),
        ('Stage 2: Rate Limit Check', 'Per-service rate limits using Redis. Summary Service: 200 req/min. Chat Service: 500 req/min. Exceeded limits return HTTP 429 with Retry-After header.'),
        ('Stage 3: Provider Selection', 'Routes requests based on type, cost, and availability. Summary requests use GPT-4o-mini (10x cheaper). Chat requests use GPT-4o (stronger reasoning). Long-context requests route to Claude.'),
        ('Stage 4: Prompt Assembly', 'Loads prompt template, injects context data, counts tokens. If prompt exceeds 80% of context window, the Context Builder reduces the context.'),
        ('Stage 5: LLM Execution', 'Executes with retry and failover logic (detailed below).'),
        ('Stage 6: Response Validation', 'Verifies JSON format, completeness, and safety. Alerts on 50%+ token deviation.'),
        ('Stage 7: Usage Recording', 'Fires usage event to Kafka for cost tracking (asynchronous, fire-and-forget).'),
    ]
    for title, desc in stages:
        pdf.h3(title)
        pdf.body(desc)
    
    # Provider Routing
    pdf.h2('8.3 Provider Routing Policy')
    pdf.data_table(
        ['Request Type', 'Model', 'Provider', 'Rationale'],
        [
            ['Summary', 'GPT-4o-mini', 'Azure OpenAI', 'Structured extraction; 10x cheaper'],
            ['Chat', 'GPT-4o', 'Azure OpenAI', 'Complex reasoning needed'],
            ['Chat (>100K tokens)', 'Claude 3.5 Sonnet', 'Anthropic', '200K context window'],
            ['Fallback', 'Gemini 1.5 Pro', 'Google', 'Third-tier fallback'],
        ],
        [40, 40, 35, 45]
    )
    
    # Circuit Breaker
    pdf.h2('8.4 Circuit Breaker Design')
    pdf.body('Each provider has an independent circuit breaker:')
    pdf.data_table(
        ['Parameter', 'Value'],
        [
            ['Failure threshold (to open)', '5 consecutive failures'],
            ['Success threshold (to close)', '3 successes from half-open'],
            ['Open state duration', '30 seconds'],
        ],
        [80, 80]
    )
    
    pdf.h3('Circuit Breaker States')
    pdf.code_block('''CLOSED (normal)
    |
    5 consecutive failures
    |
    v
OPEN (fail fast, skip provider)
    |
    30 seconds
    |
    v
HALF-OPEN (allow 1 test request)
    |
    +-- Success --> CLOSED
    +-- Failure --> OPEN''')
    
    pdf.body('When a circuit is OPEN, the Provider Router automatically skips that provider and routes to the next in the failover chain. The caller is unaware of the failover.')
    
    # Failover
    pdf.h2('8.5 Retry and Failover Strategy')
    pdf.data_table(
        ['Error', 'Action'],
        [
            ['HTTP 429 (Rate Limit)', 'Respect Retry-After, retry same provider'],
            ['HTTP 500/502/503', 'Retry once, then failover'],
            ['Timeout (>30s)', 'Immediate failover to next provider'],
            ['HTTP 401/403', 'Do NOT retry. Alert operations.'],
            ['Network error', 'Failover to next provider'],
            ['Circuit OPEN', 'Skip provider, use next in chain'],
        ],
        [55, 105]
    )
    
    pdf.h3('Failover Chain')
    pdf.code_block('''Azure OpenAI (primary)
      |
      v  (429 / 5xx / timeout)
Anthropic Claude (secondary)
      |
      v  (failure)
Google Gemini (tertiary)
      |
      v  (failure)
Return error to caller''')
    
    # Cost
    pdf.h2('8.6 Cost Calculation Engine')
    pdf.data_table(
        ['Model', 'Input / 1M tokens', 'Output / 1M tokens'],
        [
            ['GPT-4o-mini', '$0.15', '$0.60'],
            ['GPT-4o', '$2.50', '$10.00'],
            ['Claude 3.5 Sonnet', '$3.00', '$15.00'],
            ['Gemini 1.5 Pro', '$1.25', '$5.00'],
        ],
        [55, 50, 55]
    )
    
    pdf.h3('Budget Controls')
    pdf.data_table(
        ['Control', 'Threshold', 'Action'],
        [
            ['Per-case cap', '$0.50', 'Switch to cheapest model'],
            ['Per-analyst daily', '50 questions', 'Soft limit with override'],
            ['Global daily', '$500', 'Alert engineering team'],
        ],
        [50, 45, 65]
    )
    
    pdf.h3('Projected Monthly Cost (1,000 cases/day)')
    pdf.data_table(
        ['Operation', 'Model', 'Volume/Day', 'Monthly Cost'],
        [
            ['Summaries', 'GPT-4o-mini', '1,200', '$21'],
            ['Chat Q&A', 'GPT-4o', '3,000', '$930'],
            ['Total', '', '4,200', '$951'],
        ],
        [40, 40, 35, 45]
    )
    
    # Observability
    pdf.h2('8.7 Observability')
    pdf.h3('Prometheus Metrics')
    pdf.data_table(
        ['Metric', 'Type', 'Labels'],
        [
            ['ai_gateway_requests_total', 'Counter', 'provider, model, status'],
            ['ai_gateway_latency_seconds', 'Histogram', 'provider, model'],
            ['ai_gateway_tokens_total', 'Counter', 'provider, direction'],
            ['ai_gateway_cost_usd_total', 'Counter', 'provider, model'],
            ['ai_gateway_circuit_state', 'Gauge', 'provider'],
            ['ai_gateway_failover_total', 'Counter', 'from, to'],
        ],
        [60, 30, 70]
    )
    
    pdf.h3('Alerts')
    pdf.data_table(
        ['Alert', 'Condition', 'Severity'],
        [
            ['High error rate', '> 5% errors in 5 min', 'P2'],
            ['Circuit open', 'Any provider circuit opens', 'P2'],
            ['Cost spike', 'Daily cost > 2x average', 'P3'],
            ['All providers down', 'All circuits open', 'P1'],
        ],
        [50, 60, 50]
    )
    
    # ═══════════════════════════════════════
    # 9. CHAT SERVICE
    # ═══════════════════════════════════════
    pdf.h1('Chat Service')
    pdf.body('The Chat Service allows analysts to ask questions about a case using natural language. It leverages previously generated summaries and conversation history.')
    
    pdf.h2('Request Flow')
    pdf.bullet_list([
        'Receive analyst request',
        'Load conversation history from Redis (last 10 turns)',
        'Load latest case summary from Summary DB',
        'Build conversational context',
        'Apply PII redaction',
        'Call AI Gateway',
        'Store response in Chat DB',
        'Stream response to analyst via SSE',
    ])
    
    pdf.h2('Redis Session Cache')
    pdf.code_block('Key:   chat:{caseId}:{userId}\nTTL:   24 Hours\nValue: Last 10 conversation turns')
    
    # ═══════════════════════════════════════
    # 10. SECURITY
    # ═══════════════════════════════════════
    pdf.h1('Security Design')
    pdf.data_table(
        ['Control', 'Implementation'],
        [
            ['Authentication', 'Microsoft Entra ID'],
            ['Authorization', 'Role-Based Access Control (RBAC)'],
            ['PII Protection', 'Two-stage redaction (regex + NER)'],
            ['Audit Logging', 'All AI requests logged with correlation ID'],
            ['Secrets', 'Azure Key Vault'],
        ],
        [50, 110]
    )
    
    # ═══════════════════════════════════════
    # 11. MONITORING
    # ═══════════════════════════════════════
    pdf.h1('Monitoring & Observability')
    pdf.data_table(
        ['Service', 'Key Metrics'],
        [
            ['Summary Service', 'Processing latency, success rate, DLQ depth'],
            ['AI Gateway', 'Provider usage, token consumption, cost/request, circuit state'],
            ['Chat Service', 'Active sessions, response times, user activity'],
        ],
        [50, 110]
    )
    
    # ═══════════════════════════════════════
    # 12. FUTURE
    # ═══════════════════════════════════════
    pdf.h1('Future Enhancements')
    pdf.bullet_list([
        'Retrieval Augmented Generation (RAG) with vector search',
        'Prompt versioning UI with A/B testing',
        'Human feedback loop for summary quality',
        'Multi-region deployment',
        'Streaming responses for summary generation',
    ])
    
    # ═══════════════════════════════════════
    # 13. CONCLUSION
    # ═══════════════════════════════════════
    pdf.h1('Conclusion')
    pdf.body('CasePilot V2 provides a scalable and secure AI-assisted investigation platform.')
    pdf.body('The Summary Generation Service automates investigation summaries by aggregating information across enterprise systems, applying PII redaction, managing context windows, and validating LLM outputs against hallucination.')
    pdf.body('The AI Gateway Service centralizes all AI interactions, providing provider independence through a 7-stage request pipeline, circuit breaker failover, cost tracking, and comprehensive observability.')
    pdf.body('Together, these services establish a foundation for enterprise-grade AI adoption within security and fraud investigation workflows.')
    
    # ── Save ──
    output = 'docs/CasePilot_V2_HLD.pdf'
    pdf.output(output)
    print(f'Generated: {output}')
    return output

if __name__ == '__main__':
    build_pdf()
