import { Button, Card, Col, InputNumber, Progress, Row, Statistic } from 'antd';
import { useState } from 'react';

import type { CaseReport } from '@/entities/report/model/types';

import styles from './Finance.module.scss';

export function Finance({ data }: { data: CaseReport['finance'] }) {
  const [sections, setSections] = useState(() =>
    data.budgetSections.map((section) => ({
      ...section,
      amount: section.recommended,
    })),
  );

  const budgetLimit = data.recommendedTotal ?? 0;
  const total = sections.reduce((sum, section) => sum + section.amount, 0);
  const remaining = budgetLimit - total;
  const isOverBudget = remaining < 0;
  const progress = Math.min(Math.round((total / budgetLimit) * 100), 100);

  function changeAmount(name: string, value: number | null) {
    if (value === null) return;

    setSections((current) =>
      current.map((section) =>
        section.name === name ? { ...section, amount: Math.max(value, section.minimum) } : section,
      ),
    );
  }

  function setRecommended() {
    setSections(
      data.budgetSections.map((section) => ({
        ...section,
        amount: section.recommended,
      })),
    );
  }

  function setMinimum() {
    setSections(
      data.budgetSections.map((section) => ({
        ...section,
        amount: section.minimum,
      })),
    );
  }

  return (
    <div className={styles.finance}>
      <Row gutter={[12, 12]}>
        <Col xs={24} md={8}>
          <Card size="small" className={styles.figureCard}>
            <Statistic
              title="Рекомендуемый бюджет"
              value={budgetLimit}
              suffix="₽"
              groupSeparator=" "
            />
          </Card>
        </Col>

        <Col xs={24} md={8}>
          <Card size="small" className={styles.figureCard}>
            <Statistic title="Распределено" value={total} suffix="₽" groupSeparator=" " />
          </Card>
        </Col>

        <Col xs={24} md={8}>
          <Card size="small" className={styles.figureCard}>
            <Statistic
              title={isOverBudget ? 'Превышение бюджета' : 'Остаток'}
              value={Math.abs(remaining)}
              suffix="₽"
              groupSeparator=" "
              valueStyle={{ color: isOverBudget ? '#cf1322' : undefined }}
            />
          </Card>
        </Col>
      </Row>

      <Card
        title="Распределение бюджета MVP"
        size="small"
        extra={
          <div className={styles.budgetButtons}>
            <Button onClick={setMinimum}>Минимальный</Button>
            <Button onClick={setRecommended}>Рекомендуемый</Button>
          </div>
        }
      >
        <Progress percent={progress} status={isOverBudget ? 'exception' : 'normal'} />

        {sections.map((section) => (
          <div className={styles.budgetItem} key={section.name}>
            <div className={styles.budgetHeader}>
              <strong>{section.name}</strong>

              <InputNumber
                min={section.minimum}
                step={10000}
                value={section.amount}
                formatter={(value) =>
                  value == null ? '' : `${Number(value).toLocaleString('ru-RU')} ₽`
                }
                parser={(value) => Number(value?.replace(/[^\d]/g, '') ?? 0)}
                onChange={(value) => changeAmount(section.name, value)}
              />
            </div>

            <span>
              Рекомендуется {section.recommended.toLocaleString('ru-RU')} ₽ · минимум{' '}
              {section.minimum.toLocaleString('ru-RU')} ₽
            </span>
          </div>
        ))}

        <div className={styles.total}>
          <strong>Всего распределено</strong>
          <strong>{total.toLocaleString('ru-RU')} ₽</strong>
        </div>
      </Card>
    </div>
  );
}
