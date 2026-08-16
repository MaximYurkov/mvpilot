import { Button, Form, Input, Typography } from 'antd';

export function CreateCasePage() {
  const handleSubmit = (values) => {
    // TODO: В отдельной ветке допилить форму:
    // отправку данных на backend
    console.log(values);
  };

  return (
    <Form layout="vertical" onFinish={handleSubmit}>
      <Typography.Title level={2}>Форма создания кейса</Typography.Title>

      <Form.Item
        label="Название кейса"
        name="title"
        rules={[
          { required: true, whitespace: true, message: 'Введите как будет называться кейс' },
          { max: 50, message: 'Максимум 50 символов' },
          { min: 5, message: 'Минимум 5 символов' },
        ]}
      >
        <Input.TextArea rows={3} />
      </Form.Item>

      <Form.Item
        label="Описание идеи"
        name="description"
        rules={[
          { required: true, whitespace: true, message: 'Введите описание идеи' },
          { max: 200, message: 'Максимум 200 символов' },
          { min: 20, message: 'Минимум 20 символов' },
        ]}
      >
        <Input.TextArea rows={6} />
      </Form.Item>

      <Form.Item
        label="Целевая аудитория"
        name="audience"
        rules={[
          { required: true, whitespace: true, message: 'Введите целевую аудиторию' },
          { max: 200, message: 'Максимум 200 символов' },
          { min: 20, message: 'Минимум 20 символов' },
        ]}
      >
        <Input.TextArea rows={6} />
      </Form.Item>

      <Button type="primary" htmlType="submit">
        Отправить
      </Button>
    </Form>
  );
}
