import type { CaseReport } from '@/entities/report/model/types';
import { Card, Tag } from 'antd';
import styles from './Overview.module.scss';
import { RadarOverview } from './graphs/RadarOverview';

export function Overview({ data }: { data: CaseReport['overview'] }) {
  return (
    <div className={styles.GapForAll}>
      <Card title="Идея" size="small" type="inner" variant="borderless">
        {data.idea}
      </Card>
      <div className={styles.StatsCards}>
        {data.tiles.map((item) => (
          <Card size="small">
            {item.label}
            <br />
            <div className={styles.CardText}>
              {item.value} {item.unit}
            </div>
          </Card>
        ))}
      </div>
      <div className={styles.GraphRow}>
        <Card className={styles.Graph} title="Готовность идеи" size="small" type="inner">
          <RadarOverview data={data} />
        </Card>
        {
          <Card className={styles.StatsColumn} title="Оценки по осям" size="small" type="inner">
            {data.readiness.map((item) => (
              <Card
                className={styles.GraphCards}
                variant="borderless"
                title={item.axis}
                size="small"
                extra={<Tag>{item.score}/10</Tag>}
              >
                <span>{item.comment}</span>
              </Card>
            ))}
          </Card>
        }
      </div>
    </div>
  );
}
