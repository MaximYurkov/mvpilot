import { Tooltip } from 'antd';
import styles from '@/widgets/case-report/ui/Market.module.scss';
import type { CaseReport } from '@/entities/report/model/types';

export function MarketTamSamSom({ data }: { data: CaseReport['market'] }) {
  const circles = [
    { ...data.tam, shortLabel: 'TAM', className: styles.tam },
    { ...data.sam, shortLabel: 'SAM', className: styles.sam },
    { ...data.som, shortLabel: 'SOM', className: styles.som },
  ];

  return (
    <>
      <div className={styles.circleChart}>
        {circles.map((circle) => (
          <Tooltip key={circle.label} title={`${circle.label}: ${circle.value} ${circle.unit}`}>
            <div className={`${styles.circle} ${circle.className}`}>
              <strong>{circle.shortLabel}</strong>
            </div>
          </Tooltip>
        ))}
      </div>

      <p className={styles.method}>
        Метод расчёта: {data.method}
        <br />
        {data.methodComment}
      </p>
    </>
  );
}
