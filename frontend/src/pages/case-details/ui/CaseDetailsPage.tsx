import { Tabs, Spin, Alert, Empty } from 'antd';
import { useState, useEffect } from 'react';

import { getCaseReport } from '@/shared/api/fetch';

import type { CaseReport } from '@/entities/report/model/types';
import { useParams } from 'react-router-dom';
import { LeanCanvas } from '@/widgets/case-report/ui/lean-canvas/LeanCanvas';
import { NextSteps } from '@/widgets/case-report/ui/NextSteps';
import { MVP } from '@/widgets/case-report/ui/MVP';
import { Overview } from '@/widgets/case-report/ui/Overview';
import { Audience } from '@/widgets/case-report/ui/Audience';
import { Risks } from '@/widgets/case-report/ui/risks/Risks';
import { Market } from '@/widgets/case-report/ui/Market';
import { Competitors } from '@/widgets/case-report/ui/Competitors';
import { Finance } from '@/widgets/case-report/ui/Finance';
import { Metrics } from '@/widgets/case-report/ui/Metrics';
import { Roadmap } from '@/widgets/case-report/ui/Roadmap';

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
  }, [caseId]);

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
          children: <Overview data={data.overview} />,
        },
        {
          key: 'market',
          label: 'Рынок',
          children: <Market data={data.market} />,
        },
        {
          key: 'audience',
          label: 'Аудитория',
          children: <Audience data={data.audience} />,
        },
        {
          key: 'competitors',
          label: 'Конкуренты',
          children: <Competitors data={data.competitors} />,
        },
        {
          key: 'leancanvas',
          label: 'LeanCanvas',
          children: <LeanCanvas data={data.leanCanvas} />,
        },
        {
          key: 'mvp',
          label: 'MVP',
          children: <MVP data={data.mvp} />,
        },
        {
          key: 'roadmap',
          label: 'Roadmap',
          children: <Roadmap data={data.roadmap.stages} />,
        },
        {
          key: 'finance',
          label: 'Финансы',
          children: <Finance data={data.finance} />,
        },
        {
          key: 'metrics',
          label: 'Метрики',
          children: <Metrics data={data.metrics} />,
        },
        {
          key: 'risks',
          label: 'Риски',
          children: <Risks data={data.risks.items} />,
        },
        {
          key: 'nextsteps',
          label: 'Следующие шаги',
          children: <NextSteps data={data.nextSteps.items} />,
        },
      ]}
    />
  );
}
