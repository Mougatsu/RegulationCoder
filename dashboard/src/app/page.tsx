"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Upload,
  FileText,
  Scale,
  ClipboardCheck,
  ShieldCheck,
  BookOpen,
  ArrowRight,
  Activity,
  Database,
  Layers,
  Gavel,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchRegulations, fetchRequirements, fetchRules } from "@/lib/api";

interface Stats {
  regulations: number;
  requirements: number;
  rules: number;
  loading: boolean;
}

const navLinks = [
  {
    href: "/upload",
    label: "Upload",
    icon: Upload,
    description: "Upload regulation documents (PDF/HTML)",
  },
  {
    href: "/requirements",
    label: "Requirements",
    icon: FileText,
    description: "Browse extracted requirements by article",
  },
  {
    href: "/rules",
    label: "Rules",
    icon: Scale,
    description: "View generated compliance rules",
  },
  {
    href: "/evaluate",
    label: "Evaluate",
    icon: ClipboardCheck,
    description: "Run compliance evaluation against a profile",
  },
  {
    href: "/audit",
    label: "Audit",
    icon: ShieldCheck,
    description: "Inspect the tamper-evident audit trail",
  },
];

export default function HomePage() {
  const [stats, setStats] = useState<Stats>({
    regulations: 0,
    requirements: 0,
    rules: 0,
    loading: true,
  });

  useEffect(() => {
    async function loadStats() {
      try {
        const [regs, reqs, rules] = await Promise.allSettled([
          fetchRegulations(),
          fetchRequirements(),
          fetchRules(),
        ]);
        setStats({
          regulations:
            regs.status === "fulfilled" ? regs.value.length : 0,
          requirements:
            reqs.status === "fulfilled" ? reqs.value.length : 0,
          rules: rules.status === "fulfilled" ? rules.value.length : 0,
          loading: false,
        });
      } catch {
        setStats((s) => ({ ...s, loading: false }));
      }
    }
    loadStats();
  }, []);

  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-3">
            <Gavel className="h-7 w-7 text-primary" />
            <span className="text-xl font-bold tracking-tight">
              RegulationCoder
            </span>
          </div>
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href}>
                <Button variant="ghost" size="sm" className="gap-2">
                  <link.icon className="h-4 w-4" />
                  {link.label}
                </Button>
              </Link>
            ))}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container py-16 md:py-24">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex items-center rounded-full border bg-muted px-4 py-1.5 text-sm">
            <BookOpen className="mr-2 h-4 w-4 text-primary" />
            EU AI Act Compliance Pipeline
          </div>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            From Regulation Text to{" "}
            <span className="text-primary">Executable Audit Rules</span>
          </h1>
          <p className="mt-6 text-lg text-muted-foreground leading-relaxed">
            RegulationCoder automatically parses EU AI Act articles, extracts
            machine-readable requirements, generates compliance rules, and
            evaluates your AI system against them -- with a tamper-evident audit
            trail at every step.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/upload">
              <Button size="lg" className="gap-2">
                <Upload className="h-5 w-5" />
                Upload Regulation
              </Button>
            </Link>
            <Link href="/evaluate">
              <Button size="lg" variant="outline" className="gap-2">
                <ClipboardCheck className="h-5 w-5" />
                Run Evaluation
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Cards */}
      <section className="container pb-16">
        <div className="grid gap-6 sm:grid-cols-3">
          <Card className="animate-fade-in">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Regulations Loaded
              </CardTitle>
              <Database className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {stats.loading ? (
                  <span className="animate-pulse text-muted-foreground">--</span>
                ) : (
                  stats.regulations
                )}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                Parsed regulation documents
              </p>
            </CardContent>
          </Card>

          <Card className="animate-fade-in" style={{ animationDelay: "0.1s" }}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Requirements Extracted
              </CardTitle>
              <Layers className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {stats.loading ? (
                  <span className="animate-pulse text-muted-foreground">--</span>
                ) : (
                  stats.requirements
                )}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                Machine-readable obligations
              </p>
            </CardContent>
          </Card>

          <Card className="animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Compliance Rules
              </CardTitle>
              <Activity className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {stats.loading ? (
                  <span className="animate-pulse text-muted-foreground">--</span>
                ) : (
                  stats.rules
                )}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                Executable audit checks
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Pipeline Steps */}
      <section className="container pb-16">
        <h2 className="mb-8 text-center text-2xl font-bold tracking-tight">
          Five-Stage Compliance Pipeline
        </h2>
        <div className="grid gap-4 md:grid-cols-5">
          {[
            {
              step: "1",
              title: "Ingest",
              desc: "Parse PDF/HTML regulation text into structured clauses",
            },
            {
              step: "2",
              title: "Decompose",
              desc: "Extract atomic requirements with modality and confidence",
            },
            {
              step: "3",
              title: "Generate",
              desc: "Produce executable compliance rules with severity levels",
            },
            {
              step: "4",
              title: "Evaluate",
              desc: "Run rules against your AI system profile and score",
            },
            {
              step: "5",
              title: "Audit",
              desc: "Maintain a tamper-evident hash-chain of every decision",
            },
          ].map((item, i) => (
            <Card key={item.step} className="relative">
              <CardContent className="pt-6">
                <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground font-bold">
                  {item.step}
                </div>
                <h3 className="font-semibold">{item.title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {item.desc}
                </p>
              </CardContent>
              {i < 4 && (
                <ArrowRight className="absolute right-[-20px] top-1/2 hidden h-5 w-5 -translate-y-1/2 text-muted-foreground md:block" />
              )}
            </Card>
          ))}
        </div>
      </section>

      {/* Navigation Cards */}
      <section className="container pb-16">
        <h2 className="mb-8 text-center text-2xl font-bold tracking-tight">
          Explore
        </h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} className="group">
              <Card className="h-full transition-colors hover:border-primary/50">
                <CardContent className="flex items-start gap-4 pt-6">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                    <link.icon className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold">{link.label}</h3>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {link.description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t py-6">
        <div className="container text-center text-sm text-muted-foreground">
          RegulationCoder -- AI-powered compliance analysis for the EU AI Act
        </div>
      </footer>
    </div>
  );
}
