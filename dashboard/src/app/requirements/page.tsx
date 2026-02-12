"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Gavel,
  FileText,
  Search,
  ChevronRight,
  Loader2,
  AlertCircle,
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
import { fetchRequirements, type Requirement } from "@/lib/api";

const ARTICLES = [
  { number: "9", title: "Risk Management System" },
  { number: "10", title: "Data and Data Governance" },
  { number: "11", title: "Technical Documentation" },
  { number: "12", title: "Record-Keeping" },
  { number: "13", title: "Transparency and Provision of Information" },
  { number: "14", title: "Human Oversight" },
  { number: "15", title: "Accuracy, Robustness and Cybersecurity" },
];

function modalityBadgeVariant(modality: string) {
  switch (modality) {
    case "must":
      return "danger" as const;
    case "should":
      return "warning" as const;
    case "may":
      return "success" as const;
    default:
      return "secondary" as const;
  }
}

function confidenceColor(confidence: number) {
  if (confidence >= 0.8) return "text-emerald-500";
  if (confidence >= 0.6) return "text-amber-500";
  return "text-red-500";
}

export default function RequirementsPage() {
  const [requirements, setRequirements] = useState<Requirement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedArticle, setSelectedArticle] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchRequirements(selectedArticle || undefined);
        setRequirements(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    }
    setLoading(true);
    load();
  }, [selectedArticle]);

  const filtered = requirements.filter((r) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      r.subject.toLowerCase().includes(q) ||
      r.action.toLowerCase().includes(q) ||
      r.citation.toLowerCase().includes(q) ||
      r.id.toLowerCase().includes(q)
    );
  });

  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center gap-4">
          <Link href="/">
            <Button variant="ghost" size="sm" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
          </Link>
          <div className="flex items-center gap-2">
            <Gavel className="h-5 w-5 text-primary" />
            <span className="font-semibold">RegulationCoder</span>
          </div>
          <span className="text-muted-foreground">/</span>
          <span className="text-sm font-medium">Requirements</span>
        </div>
      </header>

      <div className="container flex-1 py-8">
        <div className="flex gap-8">
          {/* Sidebar - Article Tree */}
          <aside className="hidden w-64 shrink-0 lg:block">
            <div className="sticky top-24">
              <h3 className="mb-4 text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                Articles
              </h3>
              <nav className="space-y-1">
                <button
                  onClick={() => setSelectedArticle(null)}
                  className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                    selectedArticle === null
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`}
                >
                  <FileText className="h-4 w-4" />
                  All Articles
                </button>
                {ARTICLES.map((article) => (
                  <button
                    key={article.number}
                    onClick={() => setSelectedArticle(article.number)}
                    className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                      selectedArticle === article.number
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                    }`}
                  >
                    <ChevronRight className="h-3 w-3" />
                    <span>
                      Art. {article.number}{" "}
                      <span className="text-xs opacity-70">
                        - {article.title}
                      </span>
                    </span>
                  </button>
                ))}
              </nav>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 min-w-0">
            <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">
                  Requirements
                </h1>
                <p className="mt-1 text-muted-foreground">
                  {selectedArticle
                    ? `Article ${selectedArticle} -- ${
                        ARTICLES.find((a) => a.number === selectedArticle)
                          ?.title || ""
                      }`
                    : "All extracted requirements across articles 9-15"}
                </p>
              </div>
              <Badge variant="outline" className="self-start">
                {filtered.length} requirement{filtered.length !== 1 ? "s" : ""}
              </Badge>
            </div>

            {/* Mobile Article Select */}
            <div className="mb-4 lg:hidden">
              <select
                value={selectedArticle || ""}
                onChange={(e) =>
                  setSelectedArticle(e.target.value || null)
                }
                className="w-full rounded-md border bg-background px-3 py-2 text-sm"
              >
                <option value="">All Articles</option>
                {ARTICLES.map((a) => (
                  <option key={a.number} value={a.number}>
                    Art. {a.number} - {a.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Search */}
            <div className="relative mb-6">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search requirements by subject, action, or citation..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-md border bg-background pl-10 pr-4 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

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

            {/* Requirement Cards */}
            {!loading && !error && (
              <div className="space-y-4">
                {filtered.length === 0 ? (
                  <Card>
                    <CardContent className="flex flex-col items-center justify-center py-12">
                      <FileText className="h-12 w-12 text-muted-foreground/50" />
                      <p className="mt-4 text-sm text-muted-foreground">
                        No requirements found.{" "}
                        {searchQuery
                          ? "Try a different search."
                          : "Upload a regulation to get started."}
                      </p>
                    </CardContent>
                  </Card>
                ) : (
                  filtered.map((req) => (
                    <Card
                      key={req.id}
                      className="transition-colors hover:border-primary/30"
                    >
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex items-center gap-2 flex-wrap">
                            <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-xs">
                              {req.id}
                            </code>
                            <Badge
                              variant={modalityBadgeVariant(req.modality)}
                            >
                              {req.modality.toUpperCase()}
                            </Badge>
                            <Badge variant="outline" className="text-xs">
                              Art. {req.article_number}
                              {req.paragraph ? `(${req.paragraph})` : ""}
                            </Badge>
                          </div>
                          <div
                            className={`text-sm font-mono font-semibold ${confidenceColor(
                              req.confidence
                            )}`}
                          >
                            {(req.confidence * 100).toFixed(0)}%
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="grid gap-2 sm:grid-cols-2">
                          <div>
                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                              Subject
                            </span>
                            <p className="mt-0.5 text-sm">{req.subject}</p>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                              Action
                            </span>
                            <p className="mt-0.5 text-sm">{req.action}</p>
                          </div>
                        </div>
                        {req.condition && (
                          <div>
                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                              Condition
                            </span>
                            <p className="mt-0.5 text-sm text-muted-foreground">
                              {req.condition}
                            </p>
                          </div>
                        )}
                        {req.object && (
                          <div>
                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                              Object
                            </span>
                            <p className="mt-0.5 text-sm text-muted-foreground">
                              {req.object}
                            </p>
                          </div>
                        )}
                        <div className="rounded-md bg-muted/50 p-3">
                          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            Citation
                          </span>
                          <p className="mt-1 text-xs text-muted-foreground italic leading-relaxed">
                            &quot;{req.citation}&quot;
                          </p>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
