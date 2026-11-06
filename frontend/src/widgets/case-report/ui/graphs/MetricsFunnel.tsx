import { Funnel, FunnelChart, LabelList, ResponsiveContainer, Tooltip } from 'recharts';

import type { CaseReport } from '@/entities/report/model/types';
import styles from './MetricsFunnel.module.scss';

const COLORS = ['#333333', '#4a4a4a', '#606060', '#777777', '#909090'];

const SHORT_NAMES = ['Визиты', 'Начали опрос', 'Завершили опрос', 'Подборка', 'В магазин'];

export function MetricsFunnel({ data }: { data: CaseReport['metrics']['funnel'] }) {
  const chartData = data.map((item, index) => ({
    ...item,
    shortName: SHORT_NAMES[index] ?? item.stage,
    fill: COLORS[index % COLORS.length],
  }));

  return (
    <div className={styles.chart}>
      <ResponsiveContainer width="100%" height="100%">
        <FunnelChart margin={{ top: 12, right: 130, bottom: 12, left: 20 }}>
          <Tooltip
            formatter={(value) => Number(value).toLocaleString('ru-RU')}
            labelFormatter={(_, payload) => payload?.[0]?.payload?.stage ?? ''}
          />

          <Funnel data={chartData} dataKey="value" nameKey="stage">
            <LabelList dataKey="shortName" position="right" fill="#000" fontSize={12} />
          </Funnel>
        </FunnelChart>
      </ResponsiveContainer>
    </div>
  );
}
