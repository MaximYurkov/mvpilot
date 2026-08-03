import { Layout, Menu } from 'antd';
import { NavLink, Outlet, useLocation } from 'react-router-dom';

import styles from './AppLayout.module.scss';

const { Header, Content } = Layout;

export function AppLayout() {
  const { pathname } = useLocation();

  return (
    <Layout className={styles.layout}>
      <Header className={styles.header}>
        <div className={styles.logo}>MVPilot</div>

        <Menu
          className={styles.menu}
          theme="dark"
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

      <Content className={styles.content}>
        <Outlet />
      </Content>
    </Layout>
  );
}
