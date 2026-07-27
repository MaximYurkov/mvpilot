import { Button, Card, Empty, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

export function CasesPage() {
  const navigate = useNavigate();

  return (
    <Card>
      <Title level={1}>Список кейсов</Title>

      <Paragraph>Здесь будут отображаться продуктовые кейсы, созданные пользователем.</Paragraph>

      <Empty description="Кейсов пока нет">
        <Button type="primary" onClick={() => navigate('/cases/new')}>
          Создать первый кейс
        </Button>
      </Empty>
    </Card>
  );
}
