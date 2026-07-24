import { Form, Input } from 'antd';

export function CreateCasePage() {
  return (
    <Form layout="vertical">
      <h2
        style={{
          textAlign: 'left',
          color: '#1677ff',
          marginBottom: 24,
        }}
      >
        Форма создания кейса
      </h2>

      <Form.Item label="Название кейса" name="title">
        <Input />
      </Form.Item>

      <Form.Item label="Название кейса" name="title">
        <Input />
      </Form.Item>

      <Form.Item label="Название кейса" name="title">
        <Input />
      </Form.Item>
    </Form>
  );
}
