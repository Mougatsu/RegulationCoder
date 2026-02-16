"use client";

import { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { useInView } from "framer-motion";
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
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FadeIn } from "@/components/motion/FadeIn";
import { StaggerChildren, StaggerItem } from "@/components/motion/StaggerChildren";
import { useCountUp } from "@/hooks/useCountUp";
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

const pipelineSteps = [
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
];

function StatCard({
  value,
  loading,
  label,
  description,
  icon: Icon,
}: {
  value: number;
  loading: boolean;
  label: string;
  description: string;
  icon: React.ElementType;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true });
  const count = useCountUp(value, 1800, isInView && !loading);

  return (
    <Card ref={ref} className="card-hover-glow overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {label}
        </CardTitle>
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
          <Icon className="h-4 w-4 text-primary" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-4xl font-bold font-display tabular-nums tracking-tight">
          {loading ? (
            <span className="animate-pulse text-muted-foreground">--</span>
          ) : (
            count
          )}
        </div>
        <p className="mt-1 text-xs text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  );
}

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
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 md:py-28 lg:py-36 noise-overlay">
        {/* Background gradient orbs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
          <div className="hero-orb-1 absolute -top-[10%] left-[15%] w-[400px] h-[400px] md:w-[600px] md:h-[600px] rounded-full bg-primary/[0.07] blur-[100px] md:blur-[140px]" />
          <div className="hero-orb-2 absolute -bottom-[15%] right-[5%] w-[350px] h-[350px] md:w-[500px] md:h-[500px] rounded-full bg-primary/[0.05] blur-[80px] md:blur-[120px]" />
          <div className="hero-orb-3 absolute top-[30%] left-[55%] w-[250px] h-[250px] md:w-[400px] md:h-[400px] rounded-full bg-primary/[0.04] blur-[80px] md:blur-[100px]" />
        </div>

        {/* Grid pattern */}
        <div className="absolute inset-0 grid-pattern opacity-40 pointer-events-none" aria-hidden="true" />

        <div className="container relative z-10">
          <div className="mx-auto max-w-3xl text-center">
            <FadeIn>
              <div className="mb-8 inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-5 py-2 text-sm text-primary backdrop-blur-sm">
                <BookOpen className="mr-2 h-4 w-4" />
                EU AI Act Compliance Pipeline
              </div>
            </FadeIn>

            <FadeIn delay={0.1}>
              <h1 className="font-display text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl leading-[1.1]">
                From Regulation Text to{" "}
                <span className="text-gradient">Executable Audit Rules</span>
              </h1>
            </FadeIn>

            <FadeIn delay={0.2}>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground leading-relaxed md:text-xl">
                RegulationCoder automatically parses EU AI Act articles, extracts
                machine-readable requirements, generates compliance rules, and
                evaluates your AI system against them &mdash; with a tamper-evident
                audit trail at every step.
              </p>
            </FadeIn>

            <FadeIn delay={0.3}>
              <div className="mt-10 flex flex-wrap justify-center gap-4">
                <Link href="/upload">
                  <Button
                    size="lg"
                    className="gap-2 rounded-xl px-8 shadow-lg shadow-primary/20 transition-all duration-300 hover:shadow-xl hover:shadow-primary/30 hover:scale-[1.02]"
                  >
                    <Upload className="h-5 w-5" />
                    Upload Regulation
                  </Button>
                </Link>
                <Link href="/evaluate">
                  <Button
                    size="lg"
                    variant="outline"
                    className="gap-2 rounded-xl px-8 transition-all duration-300 hover:bg-primary/5 hover:border-primary/30"
                  >
                    <ClipboardCheck className="h-5 w-5" />
                    Run Evaluation
                  </Button>
                </Link>
              </div>
            </FadeIn>
          </div>
        </div>
      </section>

      {/* Stats Cards */}
      <section className="container -mt-4 pb-20 relative z-10">
        <div className="grid gap-6 sm:grid-cols-3">
          {[
            {
              value: stats.regulations,
              label: "Regulations Loaded",
              desc: "Parsed regulation documents",
              icon: Database,
            },
            {
              value: stats.requirements,
              label: "Requirements Extracted",
              desc: "Machine-readable obligations",
              icon: Layers,
            },
            {
              value: stats.rules,
              label: "Compliance Rules",
              desc: "Executable audit checks",
              icon: Activity,
            },
          ].map((stat, i) => (
            <FadeIn key={stat.label} delay={i * 0.1}>
              <StatCard
                value={stat.value}
                loading={stats.loading}
                label={stat.label}
                description={stat.desc}
                icon={stat.icon}
              />
            </FadeIn>
          ))}
        </div>
      </section>

      {/* Pipeline Steps */}
      <section className="container pb-24">
        <FadeIn>
          <h2 className="mb-12 text-center font-display text-3xl font-bold tracking-tight md:text-4xl">
            Five-Stage Compliance Pipeline
          </h2>
        </FadeIn>
        <StaggerChildren className="grid gap-4 md:grid-cols-5" staggerDelay={0.1}>
          {pipelineSteps.map((item, i) => (
            <StaggerItem key={item.step}>
              <Card className="relative card-hover-glow h-full">
                <CardContent className="pt-6">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-primary/10 text-primary font-display text-lg font-bold animate-pulse-glow">
                    {item.step}
                  </div>
                  <h3 className="font-semibold text-base">{item.title}</h3>
                  <p className="mt-1.5 text-sm text-muted-foreground leading-relaxed">
                    {item.desc}
                  </p>
                </CardContent>
                {i < 4 && (
                  <ArrowRight className="absolute right-[-20px] top-1/2 hidden h-5 w-5 -translate-y-1/2 text-primary/30 md:block" />
                )}
              </Card>
            </StaggerItem>
          ))}
        </StaggerChildren>
      </section>

      {/* Navigation Cards */}
      <section className="container pb-24">
        <FadeIn>
          <h2 className="mb-12 text-center font-display text-3xl font-bold tracking-tight md:text-4xl">
            Explore
          </h2>
        </FadeIn>
        <StaggerChildren className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3" staggerDelay={0.08}>
          {navLinks.map((link) => (
            <StaggerItem key={link.href}>
              <Link href={link.href} className="group block h-full">
                <Card className="h-full card-hover-glow">
                  <CardContent className="flex items-start gap-4 pt-6">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300">
                      <link.icon className="h-6 w-6" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-base">{link.label}</h3>
                      <p className="mt-1 text-sm text-muted-foreground leading-relaxed">
                        {link.description}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            </StaggerItem>
          ))}
        </StaggerChildren>
      </section>
    </div>
  );
}
