"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

interface ComplianceChartProps {
  passed: number;
  failed: number;
  notApplicable: number;
  errors?: number;
}

const COLORS = {
  passed: "#10b981",
  failed: "#ef4444",
  notApplicable: "#6b7280",
  errors: "#f59e0b",
};

interface CustomLabelProps {
  cx: number;
  cy: number;
  midAngle: number;
  innerRadius: number;
  outerRadius: number;
  percent: number;
}

function renderCustomLabel({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}: CustomLabelProps) {
  if (percent < 0.05) return null;
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor="middle"
      dominantBaseline="central"
      className="text-xs font-semibold"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
}

export function ComplianceChart({
  passed,
  failed,
  notApplicable,
  errors = 0,
}: ComplianceChartProps) {
  const data = [
    { name: "Passed", value: passed, color: COLORS.passed },
    { name: "Failed", value: failed, color: COLORS.failed },
    { name: "N/A", value: notApplicable, color: COLORS.notApplicable },
    ...(errors > 0
      ? [{ name: "Errors", value: errors, color: COLORS.errors }]
      : []),
  ].filter((d) => d.value > 0);

  const total = passed + failed + notApplicable + errors;

  if (total === 0) {
    return (
      <div className="flex h-[300px] items-center justify-center text-muted-foreground">
        No data available
      </div>
    );
  }

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            dataKey="value"
            labelLine={false}
            label={renderCustomLabel}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "0.5rem",
              color: "hsl(var(--foreground))",
            }}
            formatter={(value: number, name: string) => [
              `${value} (${((value / total) * 100).toFixed(1)}%)`,
              name,
            ]}
          />
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value: string) => (
              <span className="text-sm text-foreground">{value}</span>
            )}
          />
          {/* Center text */}
          <text
            x="50%"
            y="45%"
            textAnchor="middle"
            dominantBaseline="central"
            className="fill-foreground text-3xl font-bold"
          >
            {total}
          </text>
          <text
            x="50%"
            y="55%"
            textAnchor="middle"
            dominantBaseline="central"
            className="fill-muted-foreground text-xs"
          >
            Total Rules
          </text>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
