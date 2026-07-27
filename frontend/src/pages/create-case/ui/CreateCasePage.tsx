import { Form, Input, Typography } from 'antd';

export function CreateCasePage() {
  // TODO: В отдельной ветке допилить форму:
  // добавить валидацию, кнопку отправки, обработчик onFinish
  // и отправку данных на backend

  return (
    <Form layout="vertical">
      <Typography.Title level={2}>Форма создания кейса</Typography.Title>

      <Form.Item label="Название кейса" name="title">
        <Input />
      </Form.Item>

      <Form.Item label="Описание идеи" name="description">
        <Input.TextArea rows={6} />
      </Form.Item>

      <Form.Item label="Целевая аудитория" name="audience">
        <Input.TextArea rows={6} />
      </Form.Item>
    </Form>
  );
}
