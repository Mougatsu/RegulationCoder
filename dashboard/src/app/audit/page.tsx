"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Gavel,
  ShieldCheck,
  Search,
  Loader2,
  AlertCircle,
  CheckCircle2,
  XCircle,
  Filter,
  Hash,
  Calendar,
  RefreshCw,
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
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  fetchAuditLogs,
  verifyAuditChain,
  type AuditLog,
  type AuditChainVerification,
} from "@/lib/api";

const STAGES = [
  "all",
  "ingest",
  "decompose",
  "generate",
  "evaluate",
  "audit",
];

const VERDICTS = ["all", "pass", "fail", "error", "info"];

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStage, setFilterStage] = useState("all");
  const [filterVerdict, setFilterVerdict] = useState("all");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [verification, setVerification] =
    useState<AuditChainVerification | null>(null);
  const [verifying, setVerifying] = useState(false);

  const loadLogs = async () => {
    setLoading(true);
    setError("");
    try {
      const filters: Record<string, string> = {};
      if (filterStage !== "all") filters.stage = filterStage;
      if (filterVerdict !== "all") filters.verdict = filterVerdict;
      if (fromDate) filters.from_date = fromDate;
      if (toDate) filters.to_date = toDate;
      const data = await fetchAuditLogs(
        Object.keys(filters).length > 0 ? filters : undefined
      );
      setLogs(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load audit logs");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterStage, filterVerdict, fromDate, toDate]);

  const handleVerifyChain = async () => {
    setVerifying(true);
    setVerification(null);
    try {
      const result = await verifyAuditChain();
      setVerification(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Chain verification failed"
      );
    } finally {
      setVerifying(false);
    }
  };

  const filtered = logs.filter((log) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      log.action.toLowerCase().includes(q) ||
      log.stage.toLowerCase().includes(q) ||
      JSON.stringify(log.details).toLowerCase().includes(q) ||
      log.input_hash.toLowerCase().includes(q) ||
      log.output_hash.toLowerCase().includes(q)
    );
  });

  function verdictBadgeVariant(verdict?: string) {
    switch (verdict) {
      case "pass":
        return "success" as const;
      case "fail":
        return "danger" as const;
      case "error":
        return "warning" as const;
      case "info":
        return "info" as const;
      default:
        return "secondary" as const;
    }
  }

  function stageBadgeVariant(stage: string) {
    switch (stage) {
      case "ingest":
        return "info" as const;
      case "decompose":
        return "warning" as const;
      case "generate":
        return "secondary" as const;
      case "evaluate":
        return "success" as const;
      case "audit":
        return "outline" as const;
      default:
        return "secondary" as const;
    }
  }

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
          <span className="text-sm font-medium">Audit Trail</span>
        </div>
      </header>

      <main className="container flex-1 py-8">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Audit Trail</h1>
            <p className="mt-1 text-muted-foreground">
              Tamper-evident log of every pipeline decision with hash-chain
              integrity verification
            </p>
          </div>
          <Button
            variant="outline"
            className="gap-2 self-start"
            disabled={verifying}
            onClick={handleVerifyChain}
          >
            {verifying ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Hash className="h-4 w-4" />
            )}
            Verify Hash Chain
          </Button>
        </div>

        {/* Verification Result */}
        {verification && (
          <div className="mb-6">
            <Card
              className={
                verification.is_valid
                  ? "border-emerald-500/30 bg-emerald-500/5"
                  : "border-red-500/30 bg-red-500/5"
              }
            >
              <CardContent className="flex items-center gap-4 pt-6">
                {verification.is_valid ? (
                  <CheckCircle2 className="h-8 w-8 text-emerald-500 shrink-0" />
                ) : (
                  <XCircle className="h-8 w-8 text-red-500 shrink-0" />
                )}
                <div>
                  <div className="font-semibold">
                    {verification.is_valid
                      ? "Hash Chain Verified"
                      : "Hash Chain Broken"}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {verification.total_entries} entries verified
                    {verification.errors.length > 0 &&
                      ` -- ${verification.errors.length} error(s) found`}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-col gap-4 md:flex-row">
              {/* Search */}
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search logs by action, stage, or hash..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full rounded-md border bg-background pl-10 pr-4 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>

              {/* Stage Filter */}
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-muted-foreground shrink-0" />
                <select
                  value={filterStage}
                  onChange={(e) => setFilterStage(e.target.value)}
                  className="rounded-md border bg-background px-3 py-2 text-sm"
                >
                  {STAGES.map((s) => (
                    <option key={s} value={s}>
                      {s === "all"
                        ? "All Stages"
                        : s.charAt(0).toUpperCase() + s.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              {/* Verdict Filter */}
              <select
                value={filterVerdict}
                onChange={(e) => setFilterVerdict(e.target.value)}
                className="rounded-md border bg-background px-3 py-2 text-sm"
              >
                {VERDICTS.map((v) => (
                  <option key={v} value={v}>
                    {v === "all"
                      ? "All Verdicts"
                      : v.charAt(0).toUpperCase() + v.slice(1)}
                  </option>
                ))}
              </select>

              {/* Date Filters */}
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-muted-foreground shrink-0" />
                <input
                  type="date"
                  value={fromDate}
                  onChange={(e) => setFromDate(e.target.value)}
                  className="rounded-md border bg-background px-2 py-2 text-sm"
                  placeholder="From"
                />
                <span className="text-muted-foreground text-xs">to</span>
                <input
                  type="date"
                  value={toDate}
                  onChange={(e) => setToDate(e.target.value)}
                  className="rounded-md border bg-background px-2 py-2 text-sm"
                  placeholder="To"
                />
              </div>

              {/* Refresh */}
              <Button
                variant="ghost"
                size="icon"
                onClick={loadLogs}
                disabled={loading}
              >
                <RefreshCw
                  className={`h-4 w-4 ${loading ? "animate-spin" : ""}`}
                />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Error */}
        {error && (
          <Card className="mb-6 border-red-500/30 bg-red-500/5">
            <CardContent className="flex items-center gap-3 pt-6">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <span className="text-sm text-red-500">{error}</span>
            </CardContent>
          </Card>
        )}

        {/* Log Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Log Entries</CardTitle>
                <CardDescription>
                  {filtered.length} entr{filtered.length !== 1 ? "ies" : "y"}{" "}
                  found
                </CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : filtered.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12">
                <ShieldCheck className="h-12 w-12 text-muted-foreground/50" />
                <p className="mt-4 text-sm text-muted-foreground">
                  No audit log entries found.
                </p>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Timestamp</TableHead>
                    <TableHead>Stage</TableHead>
                    <TableHead>Action</TableHead>
                    <TableHead>Verdict</TableHead>
                    <TableHead>Input Hash</TableHead>
                    <TableHead>Output Hash</TableHead>
                    <TableHead>Details</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filtered.map((log) => (
                    <TableRow key={log.id}>
                      <TableCell className="text-xs text-muted-foreground whitespace-nowrap">
                        {new Date(log.timestamp).toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <Badge variant={stageBadgeVariant(log.stage)}>
                          {log.stage}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm max-w-[200px] truncate">
                        {log.action}
                      </TableCell>
                      <TableCell>
                        {log.verdict ? (
                          <Badge variant={verdictBadgeVariant(log.verdict)}>
                            {log.verdict}
                          </Badge>
                        ) : (
                          <span className="text-xs text-muted-foreground">
                            --
                          </span>
                        )}
                      </TableCell>
                      <TableCell>
                        <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
                          {log.input_hash.substring(0, 12)}...
                        </code>
                      </TableCell>
                      <TableCell>
                        <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
                          {log.output_hash.substring(0, 12)}...
                        </code>
                      </TableCell>
                      <TableCell className="text-xs text-muted-foreground max-w-[200px] truncate">
                        {log.details ? JSON.stringify(log.details) : "--"}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
