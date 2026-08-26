import { BrowserRouter } from 'react-router-dom';

import { AppRouter } from './router/router';
import { ConfigProvider } from 'antd';

export function App() {
  return (
    <ConfigProvider
      theme={{
        components: {
          Menu: {
            fontSize: 20,
            itemColor: '#000000',
            itemHoverColor: '#000000',
            itemSelectedColor: '#000000',
            itemHoverBg: '#f0f0f0',
            horizontalItemSelectedColor: '#000000',
          },
        },
      }}
    >
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </ConfigProvider>
  );
}
