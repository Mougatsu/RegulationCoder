const API_BASE = "/api";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorBody = await res.text().catch(() => "Unknown error");
    throw new Error(`API Error ${res.status}: ${errorBody}`);
  }

  return res.json();
}

// ---------- Regulations ----------

export interface Regulation {
  id: string;
  title: string;
  short_name: string;
  document_version: string;
  jurisdiction: string;
  language: string;
  source_url?: string;
  total_articles: number;
  total_clauses: number;
}

export async function fetchRegulations(): Promise<Regulation[]> {
  return apiFetch<Regulation[]>("/regulations/");
}

// ---------- Clauses ----------

export interface Clause {
  id: string;
  regulation_id: string;
  article_number: number;
  paragraph_number?: number;
  subsection_letter?: string;
  text: string;
  parent_clause_id?: string;
}

export async function fetchClauses(regulationId: string): Promise<Clause[]> {
  return apiFetch<Clause[]>(`/regulations/${regulationId}/clauses`);
}

// ---------- Requirements ----------

export interface Requirement {
  id: string;
  clause_id: string;
  modality: "must" | "must_not" | "should" | "should_not" | "may";
  subject: string;
  action: string;
  object: string;
  conditions: { description: string; clause_reference?: string }[];
  exceptions: { description: string; clause_reference?: string }[];
  scope: string;
  confidence: number;
  ambiguity_notes: string;
  citations: { clause_id: string; article_ref: string; exact_quote: string }[];
}

export async function fetchRequirements(
  regulationId?: string
): Promise<Requirement[]> {
  const query = regulationId ? `?regulation_id=${regulationId}` : "";
  return apiFetch<Requirement[]>(`/requirements/${query}`);
}

// ---------- Rules ----------

export interface Rule {
  id: string;
  requirement_id: string;
  rule_type: "automated" | "semi_automated" | "manual";
  title: string;
  description: string;
  inputs_needed: string[];
  evaluation_logic: string;
  severity: "critical" | "high" | "medium" | "low" | "info";
  remediation: string;
  test_cases: { id: string; description: string; expected_result: string }[];
  citations: { clause_id: string; article_ref: string; exact_quote: string }[];
}

export async function fetchRules(regulationId?: string): Promise<Rule[]> {
  const query = regulationId ? `?regulation_id=${regulationId}` : "";
  return apiFetch<Rule[]>(`/rules/${query}`);
}

// ---------- System Profile ----------

export interface BiasExaminationReport {
  covers_health_safety: boolean;
  covers_fundamental_rights: boolean;
  covers_prohibited_discrimination: boolean;
  datasets_examined: string[];
  examination_date?: string | null;
  methodology?: string;
  findings_summary?: string;
}

export interface SystemProfile {
  system_name: string;
  provider_name: string;
  provider_jurisdiction?: string;
  system_version?: string;
  intended_purpose: string;
  is_high_risk: boolean;
  high_risk_category?: string;
  annex_iii_section?: string;
  uses_training_data: boolean;
  dataset_names: string[];
  bias_examination_report?: BiasExaminationReport | null;
  data_governance_practices_documented: boolean;
  training_data_relevance_documented: boolean;
  data_collection_process_documented: boolean;
  technical_documentation_exists: boolean;
  technical_documentation_url?: string;
  automatic_logging_enabled: boolean;
  logging_capabilities: string[];
  instructions_for_use_provided: boolean;
  intended_purpose_documented: boolean;
  limitations_documented: boolean;
  human_oversight_measures: string[];
  human_can_override: boolean;
  human_can_interrupt: boolean;
  automation_bias_safeguards: string[];
  accuracy_metrics_documented: boolean;
  accuracy_levels_declared?: string;
  disaggregated_performance_metrics: boolean;
  robustness_measures: string[];
  cybersecurity_measures: string[];
  adversarial_testing_performed: boolean;
  risk_management_system_established: boolean;
  risk_management_continuous: boolean;
  residual_risks_documented: boolean;
  risk_mitigation_measures: string[];
  testing_procedures_documented: boolean;
  extra?: Record<string, unknown>;
}

// ---------- Evaluation ----------

export interface RuleResult {
  rule_id: string;
  requirement_id: string;
  title: string;
  verdict: "pass" | "fail" | "not_applicable" | "manual_review";
  severity: string;
  details: string;
  remediation: string;
  article_ref: string;
}

export interface ComplianceGap {
  rule_id: string;
  requirement_id: string;
  description: string;
  severity: string;
  remediation: string;
  article_ref: string;
}

export interface EvaluationSummary {
  total_rules: number;
  passed: number;
  failed: number;
  not_applicable: number;
  manual_review: number;
  compliance_score: number;
}

export interface ComplianceReport {
  id: string;
  regulation_id: string;
  system_name: string;
  provider_name: string;
  evaluation_date: string;
  summary: EvaluationSummary;
  rule_results: RuleResult[];
  critical_gaps: ComplianceGap[];
  high_gaps: ComplianceGap[];
  medium_gaps: ComplianceGap[];
  overall_verdict: string;
  disclaimer: string;
}

export async function evaluateProfile(
  profile: SystemProfile
): Promise<ComplianceReport> {
  return apiFetch<ComplianceReport>("/evaluate/", {
    method: "POST",
    body: JSON.stringify(profile),
  });
}

// ---------- AI Analysis ----------

export interface AIInsight {
  category: string;
  title: string;
  analysis: string;
  severity: string;
  recommendations: string[];
  relevant_articles: string[];
}

export interface AIAnalysisResult {
  id: string;
  report_id: string;
  model_used: string;
  executive_summary: string;
  overall_risk_level: string;
  risk_narrative: string;
  key_strengths: string[];
  insights: AIInsight[];
  prioritized_actions: string[];
  regulatory_context: string;
  timestamp: string;
}

export interface AIAnalysisResponse {
  report_id: string;
  system_name: string;
  provider_name: string;
  compliance_score: number;
  overall_verdict: string;
  analysis: AIAnalysisResult;
}

export async function requestAIAnalysis(
  profile: SystemProfile
): Promise<AIAnalysisResponse> {
  // Uses Next.js API route at /api/evaluate/ai-analysis/route.ts
  // which proxies to FastAPI with a 5-minute timeout for Claude Opus 4.6
  const res = await fetch(`${API_BASE}/evaluate/ai-analysis`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });

  if (!res.ok) {
    const errorBody = await res.text().catch(() => "Unknown error");
    throw new Error(`AI Analysis Error ${res.status}: ${errorBody}`);
  }

  return res.json();
}

// ---------- Reports ----------

export async function fetchReports(): Promise<ComplianceReport[]> {
  return apiFetch<ComplianceReport[]>("/evaluate/reports");
}

// ---------- Upload ----------

export async function uploadRegulation(
  file: File
): Promise<{ id: string; status: string }> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload/`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorBody = await res.text().catch(() => "Unknown error");
    throw new Error(`Upload Error ${res.status}: ${errorBody}`);
  }

  return res.json();
}

// ---------- Audit ----------

export interface AuditLog {
  id: string;
  timestamp: string;
  action: string;
  stage: string;
  actor: string;
  target_ids: string[];
  input_hash: string;
  output_hash: string;
  previous_hash: string;
  entry_hash: string;
  details: Record<string, unknown>;
  model_used: string;
  verdict: string;
}

export async function fetchAuditLogs(filters?: Record<string, string | number | undefined>): Promise<AuditLog[]> {
  const params = new URLSearchParams();
  if (filters) {
    for (const [key, value] of Object.entries(filters)) {
      if (value !== undefined) params.set(key, String(value));
    }
  }
  const query = params.toString() ? `?${params.toString()}` : "";
  return apiFetch<AuditLog[]>(`/audit/logs${query}`);
}

export interface AuditVerification {
  is_valid: boolean;
  total_entries: number;
  errors: string[];
}

export type AuditChainVerification = AuditVerification;

export async function verifyAuditChain(): Promise<AuditVerification> {
  return apiFetch<AuditVerification>("/audit/verify");
}
