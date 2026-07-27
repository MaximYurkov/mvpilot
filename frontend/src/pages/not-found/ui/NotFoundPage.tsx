import { Button } from 'antd';
import { useNavigate } from 'react-router-dom';

import styles from './NotFoundPage.module.scss';

export function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className={styles.page}>
      <h1 className={styles.code}>404</h1>
      <p className={styles.message}>Страница не обнаружена</p>

      <Button type="primary" onClick={() => navigate(-1)}>
        Вернуться назад
      </Button>
    </div>
  );
}
