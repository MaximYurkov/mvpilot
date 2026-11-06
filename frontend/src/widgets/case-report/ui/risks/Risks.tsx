import type { CaseReport } from '@/entities/report/model/types';
import { Card, Col, Flex, Row } from 'antd';
import styles from './Risks.module.scss';
import { Cell } from '@/widgets/case-report/ui/risks/Cell';

export function Risks({ data }: { data: CaseReport['risks']['items'] }) {
  return (
    <Flex vertical gap={16}>
      <Card title="Тепловая карта рисков" size="small">
        <Row className={styles.RowTitle}>ВЛИЯНИЕ</Row>
        <Row>
          <Col className={styles.ColumnRisks}>Высокая</Col>
          <Col span={6} className={styles.OrangeSpace}>
            <Cell risks={data} cellNumber={1} />
          </Col>
          <Col span={6} className={styles.RedSpace}>
            <Cell risks={data} cellNumber={2} />
          </Col>
          <Col span={6} className={styles.RedSpace}>
            <Cell risks={data} cellNumber={3} />
          </Col>
        </Row>
        <Row>
          <Col className={styles.ColumnRisks}>Средняя</Col>
          <Col span={6} className={styles.GreenSpace}>
            <Cell risks={data} cellNumber={4} />
          </Col>
          <Col span={6} className={styles.OrangeSpace}>
            <Cell risks={data} cellNumber={5} />
          </Col>
          <Col span={6} className={styles.RedSpace}>
            <Cell risks={data} cellNumber={6} />
          </Col>
          <Col className={styles.ColumnTitle}>ВЕРОЯТНОСТЬ</Col>
        </Row>
        <Row>
          <Col className={styles.ColumnRisks}>Низкая</Col>
          <Col span={6} className={styles.GreenSpace}>
            <Cell risks={data} cellNumber={7} />
          </Col>
          <Col span={6} className={styles.GreenSpace}>
            <Cell risks={data} cellNumber={8} />
          </Col>
          <Col span={6} className={styles.OrangeSpace}>
            <Cell risks={data} cellNumber={9} />
          </Col>
        </Row>
        <Row>
          <Col className={styles.ColumnRisks}></Col>
          <Col span={6} className={styles.RowRisks}>
            Низкая
          </Col>
          <Col span={6} className={styles.RowRisks}>
            Средняя
          </Col>
          <Col span={6} className={styles.RowRisks}>
            Высокая
          </Col>
        </Row>
      </Card>
      <Card title="Список рисков" size="small" variant="borderless" type="inner">
        {data.map((item, index) => (
          <Card
            title={item.description}
            size="small"
            type="inner"
            extra={index + 1}
            className={styles.CardGap}
          >
            {item.mitigation}
            <br />
            {item.cheapCheck}
          </Card>
        ))}
      </Card>
    </Flex>
  );
}
