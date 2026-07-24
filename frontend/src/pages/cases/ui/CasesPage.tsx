import { Button, Card, Empty, Typography } from 'antd';
import { Link } from 'react-router-dom';

const { Title, Paragraph } = Typography;

export function CasesPage() {
  return (
    <Card>
      <Title level={1}>Список кейсов</Title>

      <Paragraph>Здесь будут отображаться продуктовые кейсы, созданные пользователем.</Paragraph>

      <Empty description="Кейсов пока нет">
        <Button type="primary">
          <Link to="/cases/new">Создать первый кейс</Link>
        </Button>
      </Empty>
    </Card>
  );
}
