import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = "http://localhost:8000";

export const maxDuration = 300; // Allow up to 5 minutes

export async function POST(request: NextRequest) {
  try {
    const body = await request.text();

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 290_000); // 290s

    const res = await fetch(`${BACKEND_URL}/api/evaluate/ai-analysis`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    const data = await res.text();

    return new NextResponse(data, {
      status: res.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Proxy error";
    return NextResponse.json(
      { detail: `AI analysis proxy error: ${message}` },
      { status: 502 }
    );
  }
}
