"use client";

import { useState, useCallback, useRef } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Upload,
  FileUp,
  FileText,
  CheckCircle2,
  XCircle,
  Loader2,
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
import { PageTransition } from "@/components/motion/PageTransition";
import { FadeIn } from "@/components/motion/FadeIn";
import { uploadRegulation } from "@/lib/api";

type UploadStatus = "idle" | "uploading" | "processing" | "success" | "error";

interface PipelineStep {
  label: string;
  status: "pending" | "running" | "done" | "error";
}

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [errorMsg, setErrorMsg] = useState("");
  const [resultId, setResultId] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const [pipelineSteps, setPipelineSteps] = useState<PipelineStep[]>([
    { label: "Upload file", status: "pending" },
    { label: "Parse document", status: "pending" },
    { label: "Extract clauses", status: "pending" },
    { label: "Decompose requirements", status: "pending" },
    { label: "Generate rules", status: "pending" },
  ]);

  const updateStep = (index: number, stepStatus: PipelineStep["status"]) => {
    setPipelineSteps((prev) =>
      prev.map((s, i) => (i === index ? { ...s, status: stepStatus } : s))
    );
  };

  const simulatePipeline = useCallback(async () => {
    for (let i = 1; i < 5; i++) {
      await new Promise((r) => setTimeout(r, 800 + Math.random() * 600));
      updateStep(i, "running");
      await new Promise((r) => setTimeout(r, 600 + Math.random() * 400));
      updateStep(i, "done");
    }
  }, []);

  const handleUpload = async () => {
    if (!file) return;

    setStatus("uploading");
    setErrorMsg("");
    setPipelineSteps((prev) => prev.map((s) => ({ ...s, status: "pending" })));
    updateStep(0, "running");

    try {
      const result = await uploadRegulation(file);
      updateStep(0, "done");
      setStatus("processing");

      await simulatePipeline();

      setResultId(result.id);
      setStatus("success");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Upload failed";
      setErrorMsg(msg);
      setStatus("error");
      setPipelineSteps((prev) =>
        prev.map((s) =>
          s.status === "running" ? { ...s, status: "error" } : s
        )
      );
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setStatus("idle");
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDragOver(false);
  }, []);

  const fileExtension = file?.name.split(".").pop()?.toUpperCase() || "";
  const isValidType = ["PDF", "HTML", "HTM"].includes(fileExtension);

  return (
    <PageTransition>
      <div className="container py-8">
        <div className="mx-auto max-w-2xl space-y-8">
          <FadeIn>
            <div>
              <h1 className="font-display text-3xl font-bold tracking-tight md:text-4xl">
                Upload Regulation
              </h1>
              <p className="mt-2 text-muted-foreground">
                Upload a regulation document (PDF or HTML) to begin the compliance
                analysis pipeline.
              </p>
            </div>
          </FadeIn>

          {/* Drop Zone */}
          <FadeIn delay={0.1}>
            <Card>
              <CardContent className="pt-6">
                <div
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onClick={() => inputRef.current?.click()}
                  className={`
                    flex cursor-pointer flex-col items-center justify-center
                    rounded-xl border-2 border-dashed p-12 transition-all duration-300
                    ${
                      dragOver
                        ? "border-primary bg-primary/5 scale-[1.01]"
                        : "border-muted-foreground/25 hover:border-primary/50 hover:bg-muted/50"
                    }
                  `}
                >
                  <input
                    ref={inputRef}
                    type="file"
                    accept=".pdf,.html,.htm"
                    className="hidden"
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) {
                        setFile(f);
                        setStatus("idle");
                      }
                    }}
                  />
                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 mb-4">
                    <FileUp className="h-8 w-8 text-primary" />
                  </div>
                  <p className="text-sm font-medium">
                    Drag and drop your regulation file here
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    or click to browse &mdash; PDF, HTML supported
                  </p>
                </div>

                {/* Selected File */}
                {file && (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 flex items-center justify-between rounded-xl border bg-muted/30 p-4"
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="h-8 w-8 text-primary" />
                      <div>
                        <p className="text-sm font-medium">{file.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {(file.size / 1024).toFixed(1)} KB
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={isValidType ? "info" : "danger"}
                      >
                        {fileExtension}
                      </Badge>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setFile(null);
                          setStatus("idle");
                        }}
                      >
                        <XCircle className="h-4 w-4" />
                      </Button>
                    </div>
                  </motion.div>
                )}

                {/* Upload Button */}
                <div className="mt-6 flex justify-center">
                  <Button
                    size="lg"
                    className="gap-2 rounded-xl px-8 shadow-lg shadow-primary/20 transition-all duration-300 hover:shadow-xl hover:shadow-primary/30"
                    disabled={
                      !file ||
                      !isValidType ||
                      status === "uploading" ||
                      status === "processing"
                    }
                    onClick={handleUpload}
                  >
                    {status === "uploading" || status === "processing" ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        {status === "uploading"
                          ? "Uploading..."
                          : "Processing..."}
                      </>
                    ) : (
                      <>
                        <Upload className="h-5 w-5" />
                        Upload &amp; Process
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </FadeIn>

          {/* Pipeline Progress */}
          {status !== "idle" && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Pipeline Progress</CardTitle>
                  <CardDescription>
                    Processing your regulation document through the analysis
                    pipeline
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {pipelineSteps.map((step, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className="flex items-center gap-3"
                      >
                        <div className="flex h-8 w-8 shrink-0 items-center justify-center">
                          {step.status === "done" && (
                            <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                          )}
                          {step.status === "running" && (
                            <Loader2 className="h-5 w-5 animate-spin text-primary" />
                          )}
                          {step.status === "error" && (
                            <XCircle className="h-5 w-5 text-red-500" />
                          )}
                          {step.status === "pending" && (
                            <div className="h-3 w-3 rounded-full border-2 border-muted-foreground/30" />
                          )}
                        </div>
                        <span
                          className={`text-sm ${
                            step.status === "done"
                              ? "text-foreground"
                              : step.status === "running"
                              ? "text-primary font-medium"
                              : step.status === "error"
                              ? "text-red-500"
                              : "text-muted-foreground"
                          }`}
                        >
                          {step.label}
                        </span>
                      </motion.div>
                    ))}
                  </div>

                  {/* Result */}
                  {status === "success" && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-6 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4"
                    >
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                        <span className="font-medium text-emerald-500">
                          Processing Complete
                        </span>
                      </div>
                      <p className="mt-2 text-sm text-muted-foreground">
                        Regulation ID:{" "}
                        <code className="rounded-lg bg-muted px-1.5 py-0.5 font-mono text-xs">
                          {resultId}
                        </code>
                      </p>
                      <div className="mt-3 flex gap-2">
                        <Link href="/requirements">
                          <Button size="sm" variant="outline" className="rounded-xl">
                            View Requirements
                          </Button>
                        </Link>
                        <Link href="/rules">
                          <Button size="sm" variant="outline" className="rounded-xl">
                            View Rules
                          </Button>
                        </Link>
                      </div>
                    </motion.div>
                  )}

                  {/* Error */}
                  {status === "error" && (
                    <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                      <div className="flex items-center gap-2">
                        <XCircle className="h-5 w-5 text-red-500" />
                        <span className="font-medium text-red-500">
                          Processing Failed
                        </span>
                      </div>
                      <p className="mt-2 text-sm text-muted-foreground">
                        {errorMsg}
                      </p>
                      <Button
                        size="sm"
                        variant="outline"
                        className="mt-3 rounded-xl"
                        onClick={handleUpload}
                      >
                        Retry
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </PageTransition>
  );
}
