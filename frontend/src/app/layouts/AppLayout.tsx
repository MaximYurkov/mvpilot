import { Layout, Menu } from 'antd';
import { NavLink, Outlet } from 'react-router-dom';

const { Header, Content } = Layout;

export function AppLayout() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 32,
        }}
      >
        <div style={{ color: '#fff', fontWeight: 700, fontSize: 20 }}>MVPilot</div>

        <Menu
          theme="dark"
          mode="horizontal"
          style={{
            flex: 1,
            minWidth: 0,
          }}
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

      <Content
        style={{
          maxWidth: 1100,
          width: '100%',
          margin: '0 auto',
          padding: 32,
        }}
      >
        <Outlet />
      </Content>
    </Layout>
  );
}
