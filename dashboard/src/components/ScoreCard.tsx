"use client";

import { cn } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";

interface ScoreCardProps {
  score: number;
  label: string;
  description?: string;
  className?: string;
}

function getScoreColor(score: number): string {
  if (score >= 80) return "text-emerald-500";
  if (score >= 60) return "text-amber-500";
  if (score >= 40) return "text-orange-500";
  return "text-red-500";
}

function getScoreRing(score: number): string {
  if (score >= 80) return "ring-emerald-500/30";
  if (score >= 60) return "ring-amber-500/30";
  if (score >= 40) return "ring-orange-500/30";
  return "ring-red-500/30";
}

function getScoreGradient(score: number): string {
  if (score >= 80) return "from-emerald-500/10 to-transparent";
  if (score >= 60) return "from-amber-500/10 to-transparent";
  if (score >= 40) return "from-orange-500/10 to-transparent";
  return "from-red-500/10 to-transparent";
}

export function ScoreCard({ score, label, description, className }: ScoreCardProps) {
  const roundedScore = Math.round(score);

  return (
    <Card
      className={cn(
        "relative overflow-hidden ring-2",
        getScoreRing(score),
        className
      )}
    >
      <div
        className={cn(
          "absolute inset-0 bg-gradient-to-br",
          getScoreGradient(score)
        )}
      />
      <CardContent className="relative flex flex-col items-center justify-center p-6">
        <div
          className={cn(
            "text-5xl font-bold tabular-nums tracking-tight",
            getScoreColor(score)
          )}
        >
          {roundedScore}
          <span className="text-2xl text-muted-foreground">%</span>
        </div>
        <div className="mt-2 text-sm font-medium text-foreground">{label}</div>
        {description && (
          <div className="mt-1 text-xs text-muted-foreground text-center">
            {description}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
