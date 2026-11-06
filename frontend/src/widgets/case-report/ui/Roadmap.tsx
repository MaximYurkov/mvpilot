import { Card, Col, Row } from 'antd';
import type { CaseReport } from '@/entities/report/model/types';

import styles from './Roadmap.module.scss';
import { RoadmapGraph } from './graphs/RoadmapGraph';

export function Roadmap({ data }: { data: CaseReport['roadmap']['stages'] }) {
  return (
    <div className={styles.roadmap}>
      <Card title="Этапы по месяцам" size="small">
        <RoadmapGraph data={data} />
      </Card>

      <Row gutter={[12, 12]} className={styles.stages}>
        {data.map((stage) => (
          <Col xs={24} sm={12} lg={6} key={stage.name}>
            <Card
              size="small"
              title={stage.name}
              extra={<span className={styles.duration}>{stage.duration} мес.</span>}
              className={styles.stageCard}
            >
              <span className={styles.goal}>{stage.goal}</span>

              <ul className={styles.results}>
                {stage.results.map((result) => (
                  <li key={result}>{result}</li>
                ))}
              </ul>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}
