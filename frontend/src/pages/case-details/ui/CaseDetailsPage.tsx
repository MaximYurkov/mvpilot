import { Tabs, Spin, Alert, Typography, Empty } from 'antd';
import { useState, useEffect } from 'react';

import { getCaseReport } from '@/shared/api/fetch';

import type { CaseReport } from '@/shared/api/types';
import { useParams } from 'react-router-dom';

const { Title, Paragraph } = Typography;

export function CaseDetailsPage() {
  const { caseId } = useParams();

  const [data, setData] = useState<CaseReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!caseId) return;

    getCaseReport(caseId)
      .then((data) => setData(data))
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <Spin />;
  }

  if (error) {
    return <Alert type="error" message={`Ошибка: ${error}`} showIcon />;
  }

  if (!data) {
    return <Empty description="Анализ ещё не запускали" />;
  }

  return (
    <Tabs
      tabPlacement="start"
      items={[
        {
          key: 'overview',
          label: 'Обзор',
          children: (
            <div>
              <Title>Обзор</Title>
              <Paragraph>{data.overview.summary}</Paragraph>
              <Paragraph>{data.overview.problem}</Paragraph>
              <Paragraph>{data.overview.audience}</Paragraph>
              <Paragraph>{data.overview.value}</Paragraph>
            </div>
          ),
        },
        {
          key: 'market',
          label: 'Рынок и аудитория',
          children: (
            <div>
              <Title>Рынок и аудитория</Title>
              <Paragraph>{data.overview.summary}</Paragraph>
              <Paragraph>{data.overview.problem}</Paragraph>
              <Paragraph>{data.overview.audience}</Paragraph>
              <Paragraph>{data.overview.value}</Paragraph>
            </div>
          ),
        },
      ]}
    />
  );
}
