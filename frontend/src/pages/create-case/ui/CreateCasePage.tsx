import type { CaseFormValues } from '@/shared/api/types';
import { Button, Form, Input, Modal, Spin, Steps, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { LoadingOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import styles from './CreateCasePage.module.scss';

const STAGES = [
  'Планирование анализа',
  'Анализ рынка и аудитории',
  'Формирование JTBD, Lean Canvas и MVP',
  'Проверка результата',
  'Сборка финального отчёта',
];

export function CreateCasePage() {
  const navigate = useNavigate();

  const [isRunning, setIsRunning] = useState(false);
  const [step, setStep] = useState(0);

  const handleSubmit = async (values: CaseFormValues) => {
    setIsRunning(true);
    console.log(values);
    // fetch('UrlToBackend', {
    //   method: 'POST',
    //   body: values
    // });
    // console.log(values);
  };

  useEffect(() => {
    if (!isRunning) return;

    if (step >= STAGES.length) {
      // todo: пока моковое значение кейса - доделать когда будет апи с бека
      navigate('/cases/1');
      return;
    }

    const timer = setTimeout(() => setStep(step + 1), 600);

    return () => clearTimeout(timer);
  }, [isRunning, step, navigate]);

  return (
    <div className={styles.page}>
      <Form layout="vertical" onFinish={handleSubmit}>
        <Typography.Title level={2}>Форма создания кейса</Typography.Title>

        <Form.Item
          label="Название кейса"
          name="title"
          rules={[
            { required: true, whitespace: true, message: 'Введите как будет называться кейс' },
            { max: 50, message: 'Максимум 50 символов' },
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
          ]}
        >
          <Input.TextArea rows={6} />
        </Form.Item>

        <Button type="primary" htmlType="submit">
          Создать кейс
        </Button>
      </Form>
      <Modal open={isRunning} title="Создание кейса" footer={null} closable={false}>
        <Steps direction="vertical" current={step} items={STAGES.map((title) => ({ title }))} />
        <Spin indicator={<LoadingOutlined spin />} />
      </Modal>
    </div>
  );
}
