import type { CaseReport } from '@/entities/report/model/types';
import { Card, Flex, Table } from 'antd';
import styles from './Competitors.module.scss';
import { CompMap } from './graphs/CompMap';

export function Competitors({ data }: { data: CaseReport['competitors'] }) {
  const swotSections = [
    { title: 'Сильные стороны', items: data.swot.strengths },
    { title: 'Слабые стороны', items: data.swot.weaknesses },
    { title: 'Возможности', items: data.swot.opportunities },
    { title: 'Угрозы', items: data.swot.threats },
  ];

  return (
    <Flex vertical gap={24}>
      <Card title="Карта позиционирования" size="small" type="inner">
        <CompMap data={data} />
      </Card>

      <Card title="Сравнение функций" size="small" type="inner">
        <Table
          size="small"
          rowKey="feature"
          pagination={false}
          dataSource={data.comparison}
          columns={[
            {
              title: 'Функция',
              dataIndex: 'feature',
            },
            {
              title: 'MVPilot',
              dataIndex: 'product',
              align: 'center',
              render: (value: boolean) => (value ? '✓' : '—'),
            },
            {
              title: 'Маркетплейсы',
              dataIndex: 'competitor1',
              align: 'center',
              render: (value: boolean) => (value ? '✓' : '—'),
            },
            {
              title: 'Статьи',
              dataIndex: 'competitor2',
              align: 'center',
              render: (value: boolean) => (value ? '✓' : '—'),
            },
            {
              title: 'Боты',
              dataIndex: 'competitor3',
              align: 'center',
              render: (value: boolean) => (value ? '✓' : '—'),
            },
          ]}
        />
      </Card>

      <Card title="SWOT" type="inner" variant="borderless" size="small">
        <div className={styles.swotGrid}>
          {swotSections.map((item) => (
            <Card title={item.title} size="small" type="inner">
              {item.items.map((item2) => (
                <p>{item2}</p>
              ))}
            </Card>
          ))}
        </div>
      </Card>
    </Flex>
  );
}
