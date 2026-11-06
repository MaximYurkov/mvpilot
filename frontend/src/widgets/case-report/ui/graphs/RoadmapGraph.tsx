import type { CaseReport } from '@/entities/report/model/types';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import styles from '@/widgets/case-report/ui/Roadmap.module.scss';

export function RoadmapGraph({ data }: { data: CaseReport['roadmap']['stages'] }) {
  const chartData = [...data].reverse();

  return (
    <div className={styles.chart}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 8, right: 20, bottom: 8, left: 20 }}
        >
          <CartesianGrid horizontal={false} />
          <XAxis
            type="number"
            domain={[0, 'dataMax']}
            label={{ value: 'Месяц', position: 'insideBottomRight', offset: -4 }}
          />
          <YAxis type="category" dataKey="name" width={130} />
          <Tooltip
            formatter={(value, name) =>
              name === 'startMonth' ? null : [`${value} мес.`, 'Длительность']
            }
          />
          <Bar
            dataKey="startMonth"
            stackId="roadmap"
            fill="transparent"
            isAnimationActive={false}
            legendType="none"
            tooltipType="none"
          />
          <Bar
            dataKey="duration"
            stackId="roadmap"
            fill="#888"
            radius={[0, 4, 4, 0]}
            isAnimationActive={false}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
