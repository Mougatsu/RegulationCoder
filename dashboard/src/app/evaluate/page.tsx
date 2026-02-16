"use client";

import { useState, useRef } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Brain,
  Play,
  Upload,
  Loader2,
  AlertCircle,
  CheckCircle2,
  XCircle,
  FileJson,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ScoreCard } from "@/components/ScoreCard";
import { ComplianceChart } from "@/components/ComplianceChart";
import { RuleResultRow } from "@/components/RuleResultRow";
import { PageTransition } from "@/components/motion/PageTransition";
import { FadeIn } from "@/components/motion/FadeIn";
import {
  evaluateProfile,
  requestAIAnalysis,
  type SystemProfile,
  type ComplianceReport,
  type AIAnalysisResponse,
} from "@/lib/api";

// ---------- Demo profile (TalentScreen AI) ----------

const DEMO_PROFILE: SystemProfile = {
  system_name: "TalentScreen AI",
  provider_name: "TalentTech GmbH",
  provider_jurisdiction: "Germany",
  system_version: "2.1.0",
  intended_purpose: "Automated screening and ranking of job applicants",
  is_high_risk: true,
  high_risk_category: "Employment, workers management and access to self-employment",
  annex_iii_section: "4(a)",
  uses_training_data: true,
  dataset_names: ["applicant_training_v3", "applicant_validation_v3", "applicant_test_v3"],
  bias_examination_report: {
    covers_health_safety: true,
    covers_fundamental_rights: true,
    covers_prohibited_discrimination: true,
    datasets_examined: ["applicant_training_v3", "applicant_validation_v3", "applicant_test_v3"],
  },
  data_governance_practices_documented: true,
  training_data_relevance_documented: true,
  data_collection_process_documented: true,
  technical_documentation_exists: true,
  automatic_logging_enabled: true,
  logging_capabilities: ["input_logging", "output_logging", "event_logging"],
  instructions_for_use_provided: true,
  intended_purpose_documented: true,
  limitations_documented: true,
  human_oversight_measures: ["human_review_of_decisions", "appeal_mechanism"],
  human_can_override: true,
  human_can_interrupt: true,
  automation_bias_safeguards: [],
  accuracy_metrics_documented: true,
  accuracy_levels_declared: "Precision: 0.82, Recall: 0.78, F1: 0.80",
  disaggregated_performance_metrics: false,
  robustness_measures: ["input_validation", "adversarial_testing"],
  cybersecurity_measures: ["encryption_at_rest", "encryption_in_transit", "access_control"],
  adversarial_testing_performed: true,
  risk_management_system_established: true,
  risk_management_continuous: true,
  residual_risks_documented: true,
  risk_mitigation_measures: ["bias_mitigation", "human_oversight", "monitoring"],
  testing_procedures_documented: true,
};

const EMPTY_PROFILE: SystemProfile = {
  system_name: "",
  provider_name: "",
  intended_purpose: "",
  is_high_risk: true,
  uses_training_data: false,
  dataset_names: [],
  data_governance_practices_documented: false,
  training_data_relevance_documented: false,
  data_collection_process_documented: false,
  technical_documentation_exists: false,
  automatic_logging_enabled: false,
  logging_capabilities: [],
  instructions_for_use_provided: false,
  intended_purpose_documented: false,
  limitations_documented: false,
  human_oversight_measures: [],
  human_can_override: false,
  human_can_interrupt: false,
  automation_bias_safeguards: [],
  accuracy_metrics_documented: false,
  disaggregated_performance_metrics: false,
  robustness_measures: [],
  cybersecurity_measures: [],
  adversarial_testing_performed: false,
  risk_management_system_established: false,
  risk_management_continuous: false,
  residual_risks_documented: false,
  risk_mitigation_measures: [],
  testing_procedures_documented: false,
};

// ---------- Form field definitions ----------

interface BooleanField {
  key: keyof SystemProfile;
  label: string;
}

interface FormSection {
  article: string;
  description: string;
  fields: BooleanField[];
}

const FORM_SECTIONS: FormSection[] = [
  {
    article: "Article 9 - Risk Management",
    description: "Risk management system throughout lifecycle",
    fields: [
      { key: "risk_management_system_established", label: "Risk management system established" },
      { key: "risk_management_continuous", label: "Risk management is continuous & iterative" },
      { key: "residual_risks_documented", label: "Residual risks documented" },
      { key: "testing_procedures_documented", label: "Testing procedures documented" },
    ],
  },
  {
    article: "Article 10 - Data & Data Governance",
    description: "Training data quality, governance, and bias examination",
    fields: [
      { key: "uses_training_data", label: "System uses training data" },
      { key: "data_governance_practices_documented", label: "Data governance practices documented" },
      { key: "data_collection_process_documented", label: "Data collection process documented" },
      { key: "training_data_relevance_documented", label: "Training data relevance documented" },
    ],
  },
  {
    article: "Article 11 - Technical Documentation",
    description: "Documentation before market placement",
    fields: [
      { key: "technical_documentation_exists", label: "Technical documentation exists" },
    ],
  },
  {
    article: "Article 12 - Record-Keeping",
    description: "Automatic logging of events",
    fields: [
      { key: "automatic_logging_enabled", label: "Automatic logging enabled" },
    ],
  },
  {
    article: "Article 13 - Transparency",
    description: "Instructions for use and system information",
    fields: [
      { key: "instructions_for_use_provided", label: "Instructions for use provided" },
      { key: "intended_purpose_documented", label: "Intended purpose documented" },
      { key: "limitations_documented", label: "Limitations documented" },
      { key: "accuracy_metrics_documented", label: "Accuracy metrics documented" },
    ],
  },
  {
    article: "Article 14 - Human Oversight",
    description: "Human oversight measures and override capabilities",
    fields: [
      { key: "human_can_override", label: "Human can override system" },
      { key: "human_can_interrupt", label: "Human can interrupt system" },
    ],
  },
  {
    article: "Article 15 - Accuracy, Robustness & Cybersecurity",
    description: "Performance metrics, robustness, and security measures",
    fields: [
      { key: "disaggregated_performance_metrics", label: "Disaggregated performance metrics provided" },
      { key: "adversarial_testing_performed", label: "Adversarial testing performed" },
    ],
  },
];

// ---------- Component ----------

export default function EvaluatePage() {
  const [profile, setProfile] = useState<SystemProfile>(EMPTY_PROFILE);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ComplianceReport | null>(null);
  const [aiAnalysis, setAiAnalysis] = useState<AIAnalysisResponse | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const updateField = (key: keyof SystemProfile, value: unknown) => {
    setProfile((prev) => ({ ...prev, [key]: value }));
  };

  const loadDemoProfile = () => {
    setProfile(DEMO_PROFILE);
    setResult(null);
    setError("");
  };

  const handleImportJSON = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const data = JSON.parse(ev.target?.result as string);
        setProfile(data as SystemProfile);
        setResult(null);
        setError("");
      } catch {
        setError("Invalid JSON file");
      }
    };
    reader.readAsText(file);
  };

  const handleEvaluate = async () => {
    if (!profile.system_name || !profile.provider_name || !profile.intended_purpose) {
      setError("Please fill in System Name, Provider Name, and Intended Purpose");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await evaluateProfile(profile);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Evaluation failed");
    } finally {
      setLoading(false);
    }
  };

  const handleAIAnalysis = async () => {
    if (!profile.system_name) return;
    setAiLoading(true);
    setAiError("");
    setAiAnalysis(null);
    try {
      const res = await requestAIAnalysis(profile);
      setAiAnalysis(res);
    } catch (err) {
      setAiError(err instanceof Error ? err.message : "AI analysis failed");
    } finally {
      setAiLoading(false);
    }
  };

  const exportJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `compliance-report-${result.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const allGaps = [
    ...(result?.critical_gaps ?? []),
    ...(result?.high_gaps ?? []),
    ...(result?.medium_gaps ?? []),
  ];

  return (
    <PageTransition>
      <div className="container py-8">
        <FadeIn>
          <div className="mb-8">
            <h1 className="font-display text-3xl font-bold tracking-tight md:text-4xl">
              Compliance Evaluation
            </h1>
            <p className="mt-2 text-muted-foreground">
              Describe your AI system and evaluate it against EU AI Act requirements
            </p>
          </div>
        </FadeIn>

        <div className="grid gap-8 lg:grid-cols-[1fr_380px]">
          {/* Left: Profile Form */}
          <div className="space-y-6">
            {/* System Info Card */}
            <FadeIn delay={0.05}>
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between flex-wrap gap-4">
                    <div>
                      <CardTitle>System Information</CardTitle>
                      <CardDescription>Basic details about the AI system being evaluated</CardDescription>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm" className="gap-2" onClick={loadDemoProfile}>
                        <Sparkles className="h-4 w-4" />
                        Load Demo
                      </Button>
                      <input ref={fileInputRef} type="file" accept=".json" className="hidden" onChange={handleImportJSON} />
                      <Button variant="outline" size="sm" className="gap-2" onClick={() => fileInputRef.current?.click()}>
                        <Upload className="h-4 w-4" />
                        Import JSON
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div>
                      <label className="text-sm font-medium text-muted-foreground">System Name *</label>
                      <input
                        type="text"
                        value={profile.system_name}
                        onChange={(e) => updateField("system_name", e.target.value)}
                        className="mt-1 w-full rounded-lg border bg-background px-3 py-2 text-sm transition-colors"
                        placeholder="e.g. TalentScreen AI"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-muted-foreground">Provider Name *</label>
                      <input
                        type="text"
                        value={profile.provider_name}
                        onChange={(e) => updateField("provider_name", e.target.value)}
                        className="mt-1 w-full rounded-lg border bg-background px-3 py-2 text-sm transition-colors"
                        placeholder="e.g. TalentTech GmbH"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">Intended Purpose *</label>
                    <input
                      type="text"
                      value={profile.intended_purpose}
                      onChange={(e) => updateField("intended_purpose", e.target.value)}
                      className="mt-1 w-full rounded-lg border bg-background px-3 py-2 text-sm transition-colors"
                      placeholder="e.g. Automated screening and ranking of job applicants"
                    />
                  </div>
                  <div className="grid gap-4 sm:grid-cols-3">
                    <div>
                      <label className="text-sm font-medium text-muted-foreground">Jurisdiction</label>
                      <input
                        type="text"
                        value={profile.provider_jurisdiction ?? ""}
                        onChange={(e) => updateField("provider_jurisdiction", e.target.value)}
                        className="mt-1 w-full rounded-lg border bg-background px-3 py-2 text-sm transition-colors"
                        placeholder="e.g. Germany"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-muted-foreground">High-Risk Category</label>
                      <input
                        type="text"
                        value={profile.high_risk_category ?? ""}
                        onChange={(e) => updateField("high_risk_category", e.target.value)}
                        className="mt-1 w-full rounded-lg border bg-background px-3 py-2 text-sm transition-colors"
                        placeholder="e.g. Employment"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-muted-foreground">System Version</label>
                      <input
                        type="text"
                        value={profile.system_version ?? ""}
                        onChange={(e) => updateField("system_version", e.target.value)}
                        className="mt-1 w-full rounded-lg border bg-background px-3 py-2 text-sm transition-colors"
                        placeholder="e.g. 2.1.0"
                      />
                    </div>
                  </div>
                  <div className="flex items-center justify-between rounded-xl border bg-muted/20 p-3">
                    <label className="text-sm font-medium">High-Risk AI System</label>
                    <button
                      type="button"
                      onClick={() => updateField("is_high_risk", !profile.is_high_risk)}
                      className={`relative h-6 w-11 rounded-full transition-colors ${profile.is_high_risk ? "bg-red-500" : "bg-muted-foreground/30"}`}
                    >
                      <span className={`absolute left-0.5 top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${profile.is_high_risk ? "translate-x-5" : "translate-x-0"}`} />
                    </button>
                  </div>
                </CardContent>
              </Card>
            </FadeIn>

            {/* Article Sections */}
            <FadeIn delay={0.1}>
              <Card>
                <CardHeader>
                  <CardTitle>Compliance Profile</CardTitle>
                  <CardDescription>Toggle the compliance controls that apply to your system</CardDescription>
                </CardHeader>
                <CardContent className="space-y-8">
                  {FORM_SECTIONS.map((section) => (
                    <div key={section.article}>
                      <h3 className="mb-1 text-sm font-semibold text-primary">{section.article}</h3>
                      <p className="mb-3 text-xs text-muted-foreground">{section.description}</p>
                      <div className="space-y-2">
                        {section.fields.map((field) => (
                          <div
                            key={field.key}
                            className="flex items-center justify-between rounded-xl border bg-muted/20 p-3 transition-colors hover:bg-muted/30"
                          >
                            <label className="text-sm cursor-pointer">{field.label}</label>
                            <button
                              type="button"
                              onClick={() => updateField(field.key, !(profile[field.key] as boolean))}
                              className={`relative h-6 w-11 rounded-full transition-colors ${
                                (profile[field.key] as boolean) ? "bg-emerald-500" : "bg-muted-foreground/30"
                              }`}
                            >
                              <span
                                className={`absolute left-0.5 top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
                                  (profile[field.key] as boolean) ? "translate-x-5" : "translate-x-0"
                                }`}
                              />
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </FadeIn>
          </div>

          {/* Right: Action Panel */}
          <div className="space-y-6">
            <FadeIn delay={0.15} direction="right">
              <Card className="sticky top-24">
                <CardHeader>
                  <CardTitle className="text-lg">Run Evaluation</CardTitle>
                  <CardDescription>
                    Evaluate against all 53 EU AI Act compliance rules
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {profile.system_name && (
                    <div className="rounded-xl bg-muted/50 p-3">
                      <div className="text-xs text-muted-foreground mb-1">System</div>
                      <div className="font-semibold">{profile.system_name}</div>
                      <div className="text-xs text-muted-foreground">{profile.provider_name}</div>
                    </div>
                  )}

                  <div className="rounded-xl bg-muted/50 p-3">
                    <div className="text-xs text-muted-foreground mb-1">Profile Status</div>
                    <div className="text-2xl font-bold font-display">
                      {Object.values(profile).filter((v) => v === true).length}
                      <span className="text-sm font-normal font-body text-muted-foreground"> boolean fields enabled</span>
                    </div>
                  </div>

                  <Button className="w-full gap-2 rounded-xl" size="lg" disabled={loading} onClick={handleEvaluate}>
                    {loading ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        Evaluating...
                      </>
                    ) : (
                      <>
                        <Play className="h-5 w-5" />
                        Run Evaluation
                      </>
                    )}
                  </Button>

                  <Button
                    className="w-full gap-2 rounded-xl"
                    size="lg"
                    variant="outline"
                    disabled={aiLoading || loading}
                    onClick={handleAIAnalysis}
                  >
                    {aiLoading ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        Analyzing with Claude 4.6...
                      </>
                    ) : (
                      <>
                        <Brain className="h-5 w-5" />
                        Deep AI Analysis (Claude Opus 4.6)
                      </>
                    )}
                  </Button>
                  <p className="text-[10px] text-muted-foreground text-center">
                    Powered by Anthropic Claude Opus 4.6
                  </p>

                  {aiError && (
                    <div className="flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 p-3">
                      <AlertCircle className="h-4 w-4 text-red-500 shrink-0" />
                      <span className="text-xs text-red-500">{aiError}</span>
                    </div>
                  )}

                  {error && (
                    <div className="flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 p-3">
                      <AlertCircle className="h-4 w-4 text-red-500 shrink-0" />
                      <span className="text-xs text-red-500">{error}</span>
                    </div>
                  )}

                  {result && (
                    <div className="space-y-3 pt-2">
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="flex-1 gap-2 rounded-xl" onClick={exportJSON}>
                          <FileJson className="h-4 w-4" />
                          Export JSON
                        </Button>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </FadeIn>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.21, 0.47, 0.32, 0.98] }}
            className="mt-12 space-y-8"
          >
            <h2 className="font-display text-2xl font-bold tracking-tight">Evaluation Results</h2>

            {/* Scorecard + Stats */}
            <div className="grid gap-6 md:grid-cols-[1fr_1fr_400px]">
              <ScoreCard
                score={result.summary.compliance_score}
                label="Overall Compliance"
                description={`${result.summary.passed} of ${result.summary.total_rules} rules passed`}
              />
              <Card>
                <CardContent className="grid grid-cols-2 gap-4 pt-6">
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-1">
                      <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                      <span className="text-2xl font-bold font-display text-emerald-500">{result.summary.passed}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">Passed</span>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-1">
                      <XCircle className="h-4 w-4 text-red-500" />
                      <span className="text-2xl font-bold font-display text-red-500">{result.summary.failed}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">Failed</span>
                  </div>
                  <div className="text-center">
                    <span className="text-2xl font-bold font-display text-muted-foreground">{result.summary.not_applicable}</span>
                    <br />
                    <span className="text-xs text-muted-foreground">N/A</span>
                  </div>
                  <div className="text-center">
                    <span className="text-2xl font-bold font-display text-amber-500">{result.summary.manual_review}</span>
                    <br />
                    <span className="text-xs text-muted-foreground">Manual</span>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-muted-foreground">Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  <ComplianceChart
                    passed={result.summary.passed}
                    failed={result.summary.failed}
                    notApplicable={result.summary.not_applicable}
                    errors={result.summary.manual_review}
                  />
                </CardContent>
              </Card>
            </div>

            {/* Verdict Banner */}
            <div
              className={`rounded-xl border p-4 text-center ${
                result.overall_verdict === "compliant"
                  ? "border-emerald-500/30 bg-emerald-500/10"
                  : result.overall_verdict === "partial_compliance"
                  ? "border-amber-500/30 bg-amber-500/10"
                  : "border-red-500/30 bg-red-500/10"
              }`}
            >
              <div className="text-lg font-bold font-display">
                {result.overall_verdict.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              </div>
              <div className="text-sm text-muted-foreground">{result.system_name} by {result.provider_name}</div>
            </div>

            {/* Gaps Section */}
            {allGaps.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Compliance Gaps ({allGaps.length})</CardTitle>
                  <CardDescription>Areas where your system does not meet regulatory requirements</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {result.critical_gaps.map((gap, i) => (
                    <div key={`c${i}`} className="rounded-xl border-l-4 border-l-red-500 bg-red-500/5 p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="danger">CRITICAL</Badge>
                        <span className="text-sm font-semibold">{gap.article_ref}</span>
                        <span className="text-xs text-muted-foreground">{gap.rule_id}</span>
                      </div>
                      <p className="text-sm">{gap.description}</p>
                      <p className="mt-2 text-xs text-muted-foreground">{gap.remediation}</p>
                    </div>
                  ))}
                  {result.high_gaps.map((gap, i) => (
                    <div key={`h${i}`} className="rounded-xl border-l-4 border-l-orange-500 bg-orange-500/5 p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="warning">HIGH</Badge>
                        <span className="text-sm font-semibold">{gap.article_ref}</span>
                        <span className="text-xs text-muted-foreground">{gap.rule_id}</span>
                      </div>
                      <p className="text-sm">{gap.description}</p>
                      <p className="mt-2 text-xs text-muted-foreground">{gap.remediation}</p>
                    </div>
                  ))}
                  {result.medium_gaps.map((gap, i) => (
                    <div key={`m${i}`} className="rounded-xl border-l-4 border-l-amber-500 bg-amber-500/5 p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="secondary">MEDIUM</Badge>
                        <span className="text-sm font-semibold">{gap.article_ref}</span>
                        <span className="text-xs text-muted-foreground">{gap.rule_id}</span>
                      </div>
                      <p className="text-sm">{gap.description}</p>
                      <p className="mt-2 text-xs text-muted-foreground">{gap.remediation}</p>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Rule Results Table */}
            <Card>
              <CardHeader>
                <CardTitle>Rule Results ({result.rule_results.length})</CardTitle>
                <CardDescription>Detailed per-rule verdicts. Click a row to expand.</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-8" />
                      <TableHead>Rule</TableHead>
                      <TableHead>Title</TableHead>
                      <TableHead>Verdict</TableHead>
                      <TableHead>Severity</TableHead>
                      <TableHead>Article</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {result.rule_results.map((rr) => (
                      <RuleResultRow key={rr.rule_id} result={rr} />
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>

            {/* Disclaimer */}
            <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 p-4">
              <p className="text-xs text-muted-foreground">{result.disclaimer}</p>
            </div>
          </motion.div>
        )}

        {aiAnalysis && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.21, 0.47, 0.32, 0.98] }}
            className="mt-12 space-y-8"
          >
            <div className="flex items-center gap-3">
              <Brain className="h-7 w-7 text-primary" />
              <div>
                <h2 className="font-display text-2xl font-bold tracking-tight">AI Analysis</h2>
                <p className="text-sm text-muted-foreground">
                  Deep compliance analysis by Claude Opus 4.6
                </p>
              </div>
              <Badge variant="outline" className="ml-auto">
                {aiAnalysis.analysis.model_used}
              </Badge>
            </div>

            {/* Executive Summary */}
            <Card className="border-primary/30 bg-primary/5">
              <CardHeader>
                <CardTitle className="text-lg">Executive Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed">{aiAnalysis.analysis.executive_summary}</p>
              </CardContent>
            </Card>

            {/* Risk Assessment */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Risk Assessment</CardTitle>
                  <Badge
                    variant={
                      aiAnalysis.analysis.overall_risk_level === "critical"
                        ? "danger"
                        : aiAnalysis.analysis.overall_risk_level === "high"
                        ? "warning"
                        : aiAnalysis.analysis.overall_risk_level === "medium"
                        ? "secondary"
                        : "success"
                    }
                  >
                    {aiAnalysis.analysis.overall_risk_level.toUpperCase()} RISK
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed">{aiAnalysis.analysis.risk_narrative}</p>
              </CardContent>
            </Card>

            {/* Strengths */}
            {aiAnalysis.analysis.key_strengths.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Key Strengths</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {aiAnalysis.analysis.key_strengths.map((s, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <CheckCircle2 className="h-4 w-4 text-emerald-500 mt-0.5 shrink-0" />
                        <span>{s}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Detailed Insights */}
            {aiAnalysis.analysis.insights.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Detailed Insights ({aiAnalysis.analysis.insights.length})</CardTitle>
                  <CardDescription>Per-area compliance analysis</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {aiAnalysis.analysis.insights.map((insight, i) => (
                    <div
                      key={i}
                      className={`rounded-xl border-l-4 p-4 ${
                        insight.severity === "critical"
                          ? "border-l-red-500 bg-red-500/5"
                          : insight.severity === "high"
                          ? "border-l-orange-500 bg-orange-500/5"
                          : insight.severity === "medium"
                          ? "border-l-amber-500 bg-amber-500/5"
                          : insight.severity === "low"
                          ? "border-l-emerald-500 bg-emerald-500/5"
                          : "border-l-blue-500 bg-blue-500/5"
                      }`}
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="outline" className="text-[10px]">
                          {insight.category.replace(/_/g, " ")}
                        </Badge>
                        <span className="text-sm font-semibold">{insight.title}</span>
                        {insight.relevant_articles.length > 0 && (
                          <span className="text-[10px] text-muted-foreground ml-auto">
                            {insight.relevant_articles.join(", ")}
                          </span>
                        )}
                      </div>
                      <p className="text-sm mb-3">{insight.analysis}</p>
                      {insight.recommendations.length > 0 && (
                        <div>
                          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                            Recommendations
                          </span>
                          <ul className="mt-1 space-y-1">
                            {insight.recommendations.map((rec, j) => (
                              <li key={j} className="text-xs text-muted-foreground flex items-start gap-1.5">
                                <span className="text-primary mt-0.5">&rarr;</span>
                                <span>{rec}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Prioritized Actions */}
            {aiAnalysis.analysis.prioritized_actions.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Prioritized Action Plan</CardTitle>
                  <CardDescription>Recommended actions in order of priority</CardDescription>
                </CardHeader>
                <CardContent>
                  <ol className="space-y-3">
                    {aiAnalysis.analysis.prioritized_actions.map((action, i) => (
                      <li key={i} className="flex items-start gap-3 text-sm">
                        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-bold shrink-0">
                          {i + 1}
                        </span>
                        <span className="pt-0.5">{action}</span>
                      </li>
                    ))}
                  </ol>
                </CardContent>
              </Card>
            )}

            {/* Regulatory Context */}
            {aiAnalysis.analysis.regulatory_context && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Regulatory Context</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {aiAnalysis.analysis.regulatory_context}
                  </p>
                </CardContent>
              </Card>
            )}
          </motion.div>
        )}
      </div>
    </PageTransition>
  );
}
