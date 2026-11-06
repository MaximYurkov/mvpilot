import type { CaseReport } from '@/entities/report/model/types';
import { Card, Steps, Tag } from 'antd';
import styles from './MVP.module.scss';
import { useEffect, useState } from 'react';

export function MVP({ data }: { data: CaseReport['mvp'] }) {
  const ifMust = data.features.filter((item) => item.priority === 'must');
  const ifShould = data.features.filter((item) => item.priority === 'should');
  const ifCould = data.features.filter((item) => item.priority === 'could');
  const ifWont = data.features.filter((item) => item.priority === 'wont');

  const [step, setStep] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setStep(step + 1), 600);

    return () => clearTimeout(timer);
  }, [step]);

  return (
    <div>
      <div className={styles.moscow}>
        <div>
          <h3>MUST</h3>
          {ifMust.map((item) => (
            <Card
              title={item.name}
              size="small"
              type="inner"
              className={styles.must}
              variant="borderless"
            >
              {item.description}
              <br />
              <Tag>{item.priority}</Tag>
            </Card>
          ))}
        </div>

        <div>
          <h3>SHOULD</h3>
          {ifShould.map((item) => (
            <Card
              title={item.name}
              size="small"
              type="inner"
              className={styles.should}
              variant="borderless"
            >
              {item.description}
              <br />
              <Tag>{item.priority}</Tag>
            </Card>
          ))}
        </div>

        <div>
          <h3>COULD</h3>
          {ifCould.map((item) => (
            <Card
              title={item.name}
              size="small"
              type="inner"
              className={styles.could}
              variant="borderless"
            >
              {item.description}
              <br />
              <Tag>{item.priority}</Tag>
            </Card>
          ))}
        </div>

        <div>
          <h3>WONT</h3>
          {ifWont.map((item) => (
            <Card
              title={item.name}
              size="small"
              type="inner"
              className={styles.wont}
              variant="borderless"
            >
              {item.description}
              <br />
              <Tag>{item.priority}</Tag>
            </Card>
          ))}
        </div>
      </div>

      <Card size="small" type="inner" title="Пользовательский путь">
        <Steps
          size="small"
          type="panel"
          variant="outlined"
          current={data.userFlow.length}
          items={data.userFlow.map((step) => ({
            title: <strong>{step.step}</strong>,
            content: step.description,
          }))}
        />
      </Card>
    </div>
  );
}
