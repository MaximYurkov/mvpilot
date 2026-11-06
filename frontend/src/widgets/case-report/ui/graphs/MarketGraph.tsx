import type { CaseReport } from '@/entities/report/model/types';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from 'recharts';

export function MarketGraph({ data }: { data: CaseReport['market'] }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data.dynamics} margin={{ top: 16, right: 16, bottom: 8, left: 8 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="year" label={{ value: 'Год', position: 'insideBottom', offset: -5 }} />
        <YAxis label={{ value: 'млрд', position: 'insideLeft', offset: -5 }} />
        <Line
          type="monotone"
          dataKey="value"
          name={data.tam?.unit ?? 'млрд ₽'}
          stroke="#000"
          strokeWidth={2}
          dot={{ fill: '#000' }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
