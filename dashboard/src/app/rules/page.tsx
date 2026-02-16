"use client";

import { useEffect, useState } from "react";
import {
  Scale,
  Search,
  Loader2,
  AlertCircle,
  Code2,
  ChevronDown,
  ChevronUp,
  Filter,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { PageTransition } from "@/components/motion/PageTransition";
import { FadeIn } from "@/components/motion/FadeIn";
import { StaggerChildren, StaggerItem } from "@/components/motion/StaggerChildren";
import { fetchRules, type Rule } from "@/lib/api";

function typeBadgeVariant(type: string) {
  switch (type) {
    case "automated":
      return "info" as const;
    case "semi_automated":
      return "warning" as const;
    case "manual":
      return "secondary" as const;
    default:
      return "outline" as const;
  }
}

function typeLabel(type: string) {
  switch (type) {
    case "automated":
      return "Automated";
    case "semi_automated":
      return "Semi-Automated";
    case "manual":
      return "Manual";
    default:
      return type;
  }
}

function severityColor(severity: string) {
  switch (severity) {
    case "critical":
      return "bg-red-500";
    case "high":
      return "bg-orange-500";
    case "medium":
      return "bg-amber-500";
    case "low":
      return "bg-emerald-500";
    default:
      return "bg-gray-500";
  }
}

function severityBadgeVariant(severity: string) {
  switch (severity) {
    case "critical":
      return "danger" as const;
    case "high":
      return "warning" as const;
    case "medium":
      return "secondary" as const;
    case "low":
      return "success" as const;
    default:
      return "outline" as const;
  }
}

function testResultBadge(result?: string) {
  switch (result) {
    case "pass":
      return "success" as const;
    case "fail":
      return "danger" as const;
    case "error":
      return "warning" as const;
    case "skip":
      return "secondary" as const;
    default:
      return "outline" as const;
  }
}

export default function RulesPage() {
  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedCode, setExpandedCode] = useState<Set<string>>(new Set());
  const [filterType, setFilterType] = useState<string>("all");
  const [filterSeverity, setFilterSeverity] = useState<string>("all");

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchRules();
        setRules(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const toggleCode = (id: string) => {
    setExpandedCode((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const filtered = rules.filter((r) => {
    const ruleAny = r as any;
    if (filterType !== "all" && ruleAny.type !== filterType) return false;
    if (filterSeverity !== "all" && ruleAny.severity !== filterSeverity) return false;
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      ruleAny.description?.toLowerCase().includes(q) ||
      ruleAny.rule_id?.toLowerCase().includes(q) ||
      ruleAny.article_number?.toLowerCase().includes(q)
    );
  });

  return (
    <PageTransition>
      <div className="container py-8">
        <FadeIn>
          <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="font-display text-3xl font-bold tracking-tight md:text-4xl">
                Compliance Rules
              </h1>
              <p className="mt-1 text-muted-foreground">
                Generated executable compliance checks with severity levels
              </p>
            </div>
            <Badge variant="outline" className="self-start">
              {filtered.length} rule{filtered.length !== 1 ? "s" : ""}
            </Badge>
          </div>
        </FadeIn>

        {/* Filters */}
        <FadeIn delay={0.05}>
          <div className="mb-6 flex flex-col gap-4 sm:flex-row">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search rules by description, ID, or article..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-xl border bg-background pl-10 pr-4 py-2.5 text-sm placeholder:text-muted-foreground transition-colors"
              />
            </div>
            <div className="flex gap-2">
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-muted-foreground" />
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="rounded-xl border bg-background px-3 py-2.5 text-sm"
                >
                  <option value="all">All Types</option>
                  <option value="automated">Automated</option>
                  <option value="semi_automated">Semi-Automated</option>
                  <option value="manual">Manual</option>
                </select>
              </div>
              <select
                value={filterSeverity}
                onChange={(e) => setFilterSeverity(e.target.value)}
                className="rounded-xl border bg-background px-3 py-2.5 text-sm"
              >
                <option value="all">All Severities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
          </div>
        </FadeIn>

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        )}

        {/* Error */}
        {error && (
          <Card className="border-red-500/30 bg-red-500/5">
            <CardContent className="flex items-center gap-3 pt-6">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <span className="text-sm text-red-500">{error}</span>
            </CardContent>
          </Card>
        )}

        {/* Rules Grid */}
        {!loading && !error && (
          <div>
            {filtered.length === 0 ? (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-12">
                  <Scale className="h-12 w-12 text-muted-foreground/50" />
                  <p className="mt-4 text-sm text-muted-foreground">
                    No rules found.{" "}
                    {searchQuery
                      ? "Try different search criteria."
                      : "Upload and process a regulation first."}
                  </p>
                </CardContent>
              </Card>
            ) : (
              <StaggerChildren className="space-y-4" staggerDelay={0.04}>
                {filtered.map((rule) => {
                  const ruleAny = rule as any;
                  return (
                    <StaggerItem key={rule.id}>
                      <Card className="card-hover-glow">
                        <CardHeader className="pb-3">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 flex-wrap mb-2">
                                <code className="rounded-lg bg-muted px-2 py-0.5 font-mono text-xs">
                                  {ruleAny.rule_id}
                                </code>
                                <Badge variant={typeBadgeVariant(ruleAny.type)}>
                                  {typeLabel(ruleAny.type)}
                                </Badge>
                                <Badge
                                  variant={severityBadgeVariant(ruleAny.severity)}
                                >
                                  <div
                                    className={`mr-1 h-2 w-2 rounded-full ${severityColor(
                                      ruleAny.severity
                                    )}`}
                                  />
                                  {ruleAny.severity?.charAt(0).toUpperCase() +
                                    ruleAny.severity?.slice(1)}
                                </Badge>
                                {ruleAny.test_result && (
                                  <Badge
                                    variant={testResultBadge(ruleAny.test_result)}
                                  >
                                    Test: {ruleAny.test_result.toUpperCase()}
                                  </Badge>
                                )}
                              </div>
                              <CardTitle className="text-base">
                                {ruleAny.description}
                              </CardTitle>
                            </div>
                            <Badge variant="outline" className="shrink-0 text-xs">
                              Art. {ruleAny.article_number}
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="flex items-center justify-between text-xs text-muted-foreground">
                            <span>
                              Requirement:{" "}
                              <code className="rounded-lg bg-muted px-1.5 py-0.5 font-mono">
                                {rule.requirement_id}
                              </code>
                            </span>
                            {ruleAny.check_code && (
                              <Button
                                variant="ghost"
                                size="sm"
                                className="gap-1 text-xs"
                                onClick={() => toggleCode(rule.id)}
                              >
                                <Code2 className="h-3.5 w-3.5" />
                                {expandedCode.has(rule.id) ? "Hide" : "Show"} Code
                                {expandedCode.has(rule.id) ? (
                                  <ChevronUp className="h-3 w-3" />
                                ) : (
                                  <ChevronDown className="h-3 w-3" />
                                )}
                              </Button>
                            )}
                          </div>
                          {expandedCode.has(rule.id) && ruleAny.check_code && (
                            <div className="mt-3 rounded-xl bg-muted p-4 overflow-x-auto">
                              <pre className="text-xs font-mono text-foreground whitespace-pre-wrap">
                                {ruleAny.check_code}
                              </pre>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    </StaggerItem>
                  );
                })}
              </StaggerChildren>
            )}
          </div>
        )}
      </div>
    </PageTransition>
  );
}
