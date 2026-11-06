import type { CaseReport } from '@/entities/report/model/types';
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

export function AudiencePie({ segments }: { segments: CaseReport['audience']['segments'] }) {
  const colors = ['#000', '#777', '#bbb'];

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={segments}
            dataKey="estimatedShare"
            nameKey="name"
            innerRadius="45%"
            outerRadius="70%"
            paddingAngle={2}
          >
            {segments.map((item, index) => (
              <Cell key={item.name} fill={colors[index % colors.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ backgroundColor: '#fff' }}
            itemStyle={{ color: '#000' }}
            labelStyle={{ color: '#000' }}
          />
          <Legend formatter={(value) => <span style={{ color: '#000' }}>{value}</span>} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
