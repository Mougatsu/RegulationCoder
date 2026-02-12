"use client";

import { useState, useCallback, useRef } from "react";
import Link from "next/link";
import {
  Upload,
  FileUp,
  FileText,
  CheckCircle2,
  XCircle,
  Loader2,
  ArrowLeft,
  Gavel,
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
    // Simulate pipeline progress (in production, this would poll the backend)
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

      // Simulate remaining pipeline steps
      await simulatePipeline();

      setResultId(result.id);
      setStatus("success");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Upload failed";
      setErrorMsg(msg);
      setStatus("error");
      // Mark current running step as error
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
          <span className="text-sm font-medium">Upload</span>
        </div>
      </header>

      <main className="container flex-1 py-8">
        <div className="mx-auto max-w-2xl space-y-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Upload Regulation
            </h1>
            <p className="mt-2 text-muted-foreground">
              Upload a regulation document (PDF or HTML) to begin the compliance
              analysis pipeline.
            </p>
          </div>

          {/* Drop Zone */}
          <Card>
            <CardContent className="pt-6">
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => inputRef.current?.click()}
                className={`
                  flex cursor-pointer flex-col items-center justify-center
                  rounded-lg border-2 border-dashed p-12 transition-colors
                  ${
                    dragOver
                      ? "border-primary bg-primary/5"
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
                <FileUp className="mb-4 h-12 w-12 text-muted-foreground" />
                <p className="text-sm font-medium">
                  Drag and drop your regulation file here
                </p>
                <p className="mt-1 text-xs text-muted-foreground">
                  or click to browse -- PDF, HTML supported
                </p>
              </div>

              {/* Selected File */}
              {file && (
                <div className="mt-4 flex items-center justify-between rounded-lg border bg-muted/30 p-4">
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
                </div>
              )}

              {/* Upload Button */}
              <div className="mt-6 flex justify-center">
                <Button
                  size="lg"
                  className="gap-2"
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

          {/* Pipeline Progress */}
          {status !== "idle" && (
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
                    <div key={i} className="flex items-center gap-3">
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
                    </div>
                  ))}
                </div>

                {/* Result */}
                {status === "success" && (
                  <div className="mt-6 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-4">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                      <span className="font-medium text-emerald-500">
                        Processing Complete
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Regulation ID:{" "}
                      <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-xs">
                        {resultId}
                      </code>
                    </p>
                    <div className="mt-3 flex gap-2">
                      <Link href="/requirements">
                        <Button size="sm" variant="outline">
                          View Requirements
                        </Button>
                      </Link>
                      <Link href="/rules">
                        <Button size="sm" variant="outline">
                          View Rules
                        </Button>
                      </Link>
                    </div>
                  </div>
                )}

                {/* Error */}
                {status === "error" && (
                  <div className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 p-4">
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
                      className="mt-3"
                      onClick={handleUpload}
                    >
                      Retry
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
