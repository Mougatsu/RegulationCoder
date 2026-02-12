"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { TableRow, TableCell } from "@/components/ui/table";
import type { RuleResult } from "@/lib/api";

interface RuleResultRowProps {
  result: RuleResult;
}

function verdictBadgeVariant(verdict: string) {
  switch (verdict) {
    case "pass":
      return "success" as const;
    case "fail":
      return "danger" as const;
    case "not_applicable":
      return "secondary" as const;
    case "manual_review":
      return "warning" as const;
    default:
      return "outline" as const;
  }
}

function verdictLabel(verdict: string) {
  switch (verdict) {
    case "pass":
      return "Pass";
    case "fail":
      return "Fail";
    case "not_applicable":
      return "N/A";
    case "manual_review":
      return "Manual";
    default:
      return verdict;
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

export function RuleResultRow({ result }: RuleResultRowProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <>
      <TableRow
        className="cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <TableCell className="w-8">
          {expanded ? (
            <ChevronDown className="h-4 w-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="h-4 w-4 text-muted-foreground" />
          )}
        </TableCell>
        <TableCell className="font-mono text-xs">{result.rule_id}</TableCell>
        <TableCell className="max-w-[300px] truncate">
          {result.title}
        </TableCell>
        <TableCell>
          <Badge variant={verdictBadgeVariant(result.verdict)}>
            {verdictLabel(result.verdict)}
          </Badge>
        </TableCell>
        <TableCell>
          <div className="flex items-center gap-2">
            <div
              className={`h-2.5 w-2.5 rounded-full ${severityColor(
                result.severity
              )}`}
            />
            <span className="text-xs capitalize">{result.severity}</span>
          </div>
        </TableCell>
        <TableCell className="text-xs text-muted-foreground">
          {result.article_ref}
        </TableCell>
      </TableRow>
      {expanded && (
        <TableRow className="bg-muted/30">
          <TableCell colSpan={6} className="p-4">
            <div className="space-y-3">
              {result.details && (
                <div>
                  <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Details
                  </span>
                  <p className="mt-1 text-sm">{result.details}</p>
                </div>
              )}
              {result.remediation && (
                <div>
                  <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Remediation
                  </span>
                  <p className="mt-1 text-sm">{result.remediation}</p>
                </div>
              )}
              {!result.details && !result.remediation && (
                <p className="text-sm text-muted-foreground">
                  No additional details available for this rule.
                </p>
              )}
            </div>
          </TableCell>
        </TableRow>
      )}
    </>
  );
}
