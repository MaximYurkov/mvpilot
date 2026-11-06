import type { CaseReport } from '@/entities/report/model/types';
import styles from '@/widgets/case-report/ui/Overview.module.scss';
import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';

export function RadarOverview({ data }: { data: CaseReport['overview'] }) {
  return (
    <div className={styles.ChartContainer}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data.readiness}>
          <PolarGrid />
          <PolarAngleAxis dataKey="axis" />
          <Radar
            name="Готовность идеи"
            dataKey="score"
            stroke="#000"
            fill="#000"
            fillOpacity={0.15}
          />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
