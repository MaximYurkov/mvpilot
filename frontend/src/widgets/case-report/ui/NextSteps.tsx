import type { CaseReport } from '@/entities/report/model/types';
import { Card } from 'antd';
import styles from './NextSteps.module.scss';
// const HeartIcon: React.FC = () => (
//   <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true">
//     <path d="M12 20.7l-1.4-1.3C5.4 14.8 2 11.7 2 8a5 5 0 0 1 10-1.7A5 5 0 0 1 22 8c0 3.7-3.4 6.8-8.6 11.4L12 20.7z" />
//   </svg>
// );

export function NextSteps({ data }: { data: CaseReport['nextSteps']['items'] }) {
  return (
    <div>
      {data.map((step) => (
        <Card
          className={styles.cardstep}
          title={step.title}
          size="small"
          type="inner"
          variant="borderless"
        >
          {step.description}
          {/* <br/>
                    <Tag icon={<HeartIcon />} color="#eb2f96"> Наш партнер</Tag> */}
          {/* todo: Реалезовать партнерские программы(например т-бизнес для регистрации бизнеса) */}
        </Card>
      ))}
    </div>
  );
}
