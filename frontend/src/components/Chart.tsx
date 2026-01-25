import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from "recharts";
import type { Debtor } from "../api";

interface DebtorChartProps {
  data: Debtor[];
}

export function DebtorChart({ data }: DebtorChartProps) {
  // Transform data for the chart (make balance positive for display)
  const chartData = data.map((d) => ({
    name: d.username,
    amount: Math.abs(d.balance),
    originalBalance: d.balance,
  }));

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={Math.max(300, data.length * 50)}>
        <BarChart
          layout="vertical"
          data={chartData}
          margin={{ top: 20, right: 80, left: 80, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
          <XAxis
            type="number"
            domain={[0, "auto"]}
            tickFormatter={(value) => `€${value.toFixed(0)}`}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={70}
            tick={{ fontSize: 14 }}
          />
          <Tooltip
            formatter={(value) => [`€${Number(value).toFixed(2)}`, "Amount Owed"]}
            labelStyle={{ fontWeight: "bold" }}
          />
          <Bar dataKey="amount" radius={[0, 4, 4, 0]}>
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill="#e74c3c" />
            ))}
            <LabelList
              dataKey="amount"
              position="right"
              formatter={(value) => `€${Number(value).toFixed(2)}`}
              style={{ fontSize: 12, fill: "#333" }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
