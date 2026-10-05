import { Alert, Button, List, Spin } from 'antd';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { fetchCasesCard } from '@/shared/api/fetch';

import type { Case } from '@/shared/api/types';

export function CasesPage() {
  const navigate = useNavigate();

  const [data, setData] = useState<Case[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCasesCard()
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

  return (
    <List
      itemLayout="horizontal"
      dataSource={data ?? []}
      renderItem={(item) => (
        <List.Item>
          <List.Item.Meta title={<p>{item.title}</p>} description={<p>{item.description}</p>} />
          <Button onClick={() => navigate(`/cases/${item.id}`)}>Перейти</Button>
        </List.Item>
      )}
    />
  );
}
