import { Card } from 'antd';
import styles from './LeanCanvas.module.scss';
import type { CaseReport } from '@/entities/report/model/types';
import { TextList } from '@/widgets/case-report/ui/lean-canvas/TextList';

export function LeanCanvas({ data }: { data: CaseReport['leanCanvas'] }) {
  return (
    <div className={styles.canvas}>
      <Card className={styles.problems} title="Проблема" size="small" type="inner">
        <TextList items={data.problems} />
      </Card>

      <Card className={styles.solutions} title="Решение" size="small" type="inner">
        <TextList items={data.solutions} />
      </Card>

      <Card className={styles.value} title="Уникальность" size="small" type="inner">
        {data.value}
      </Card>

      <Card className={styles.advantage} title="Преимущество" size="small" type="inner">
        {data.advantage}
      </Card>

      <Card className={styles.segments} title="Сегменты" size="small" type="inner">
        <TextList items={data.segments} />
      </Card>

      <Card className={styles.metrics} title="Метрики" size="small" type="inner">
        <TextList items={data.metrics} />
      </Card>

      <Card className={styles.channels} title="Каналы" size="small" type="inner">
        <TextList items={data.channels} />
      </Card>

      <Card className={styles.costs} title="Издержки" size="small" type="inner">
        <TextList items={data.costs} />
      </Card>

      <Card className={styles.revenue} title="Прибыль" size="small" type="inner">
        <TextList items={data.revenue} />
      </Card>
    </div>
  );
}
