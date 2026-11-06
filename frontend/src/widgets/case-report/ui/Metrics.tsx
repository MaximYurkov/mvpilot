import { Card, Statistic, Table } from 'antd';

import type { CaseReport } from '@/entities/report/model/types';

import { MetricsFunnel } from './graphs/MetricsFunnel';
import { MetricsTree } from './graphs/MetricsTree';
import styles from './Metrics.module.scss';

type FunnelRow = CaseReport['metrics']['funnel'][number] & {
  conversion: string;
};

export function Metrics({ data }: { data: CaseReport['metrics'] }) {
  const rows: FunnelRow[] = data.funnel.map((item, index) => {
    const previousValue = index === 0 ? item.value : data.funnel[index - 1].value;
    const conversion =
      index === 0 || previousValue === 0
        ? '—'
        : `${Math.round((item.value / previousValue) * 100)} %`;

    return { ...item, conversion };
  });

  return (
    <div className={styles.metrics}>
      <Card size="small">
        <Statistic
          title={data.northStar.name}
          value={data.northStar.value === null ? '—' : data.northStar.value.toLocaleString('ru-RU')}
          suffix={data.northStar.unit}
        />
      </Card>

      <Card title="Дерево метрик" size="small">
        <MetricsTree data={data.tree} />
      </Card>

      <Card title="Воронка AARRR" size="small">
        <MetricsFunnel data={data.funnel} />

        <Table
          rowKey="stage"
          size="small"
          pagination={false}
          dataSource={rows}
          columns={[
            {
              title: 'Этап',
              dataIndex: 'stage',
            },
            {
              title: 'Факт',
              dataIndex: 'value',
              render: (value: number) => value.toLocaleString('ru-RU'),
            },
            {
              title: 'Цель',
              dataIndex: 'target',
              render: (value: number) => value.toLocaleString('ru-RU'),
            },
            {
              title: 'Конверсия с прошлого шага',
              dataIndex: 'conversion',
            },
          ]}
        />
      </Card>
    </div>
  );
}
