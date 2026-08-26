import { Layout, Menu } from 'antd';
import { NavLink, Outlet, useLocation } from 'react-router-dom';

import styles from './AppLayout.module.scss';
import { Separator } from '@/entites/separator/separator';

const { Header, Content } = Layout;

export function AppLayout() {
  const { pathname } = useLocation();

  return (
    <Layout className={styles.layout}>
      <Header className={styles.header}>
        <div className={styles.logo}>MVPilot</div>

        <Menu
          className={styles.menu}
          mode="horizontal"
          selectedKeys={[pathname]}
          items={[
            {
              key: '/cases',
              label: <NavLink to="/cases">Список кейсов</NavLink>,
            },
            {
              key: '/cases/new',
              label: <NavLink to="/cases/new">Создать кейс</NavLink>,
            },
          ]}
        />
      </Header>

      <Separator />

      <Content className={styles.content}>
        <Outlet />
      </Content>
    </Layout>
  );
}
