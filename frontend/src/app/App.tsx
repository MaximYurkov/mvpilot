import { BrowserRouter } from 'react-router-dom';

import { AppRouter } from './router/router';
import { ConfigProvider } from 'antd';

export function App() {
  return (
    <ConfigProvider
      theme={{
        components: {
          List: { itemPadding: '24px 32px' },
          Menu: {
            fontSize: 20,
            activeBarHeight: 3,
          },
        },

        token: {
          colorPrimary: '#000000',
          colorBgLayout: '#ffff',
          lineWidth: 2,
          colorSplit: '#000000',
          colorBorderSecondary: '#00000067',
        },
      }}
    >
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </ConfigProvider>
  );
}
