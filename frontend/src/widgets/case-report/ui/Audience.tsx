import type { CaseReport } from '@/entities/report/model/types';
import { Card, Tag } from 'antd';
import styles from './Audience.module.scss';
import { AudiencePie } from './graphs/AudiencePie';

export function Audience({ data }: { data: CaseReport['audience'] }) {
  return (
    <div>
      <div className={styles.CardRow}>
        <Card title="Доли сегментов" className={styles.Graph} size="small" type="inner">
          <AudiencePie segments={data.segments} />
        </Card>
        <Card title="Сегменты" className={styles.StatsColumn} size="small" type="inner">
          {data.segments.map((item) => (
            <Card
              className={styles.CardGap}
              size="small"
              type="inner"
              title={item.name}
              variant="borderless"
              extra={<Tag>{item.estimatedShare} %</Tag>}
            >
              {item.description}
              <br />
              <br />
              {item.needs.map((item2) => (
                <Tag className={styles.TagGap}>{item2}</Tag>
              ))}
            </Card>
          ))}
        </Card>
      </div>
      <Card title="JTBD" variant="borderless" size="small">
        <div className={styles.CardRow}>
          {data.jtbd.map((item) => (
            <Card title="Работа" extra={<Tag>{item.priority}</Tag>} size="small" type="inner">
              <Tag>Когда</Tag>
              {item.situation}
              <br />
              <br />
              <Tag>Я хочу</Tag>
              {item.motivation}
              <br />
              <br />
              <Tag>Чтобы</Tag>
              {item.outcome}
            </Card>
          ))}
        </div>
      </Card>
    </div>
  );
}
