import type { CaseReport } from '@/entities/report/model/types';
import { Card } from 'antd';
import styles from './Market.module.scss';
import { MarketGraph } from './graphs/MarketGraph';
import { MarketTamSamSom } from './graphs/MarketTamSamSom';

export function Market({ data }: { data: CaseReport['market'] }) {
  return (
    <div className={styles.market}>
      <Card title="TAM / SAM / SOM" size="small">
        <MarketTamSamSom data={data} />
      </Card>

      <Card title="Динамика рынка" size="small">
        <div className={styles.lineChart}>
          <MarketGraph data={data} />
        </div>
        <p className={styles.source}>Источник: {data.dynamicsSource}</p>
      </Card>
    </div>
  );
}
