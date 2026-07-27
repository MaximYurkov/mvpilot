import { Tabs } from 'antd';

export function CaseDetailsPage() {
  return (
    <Tabs
      tabPlacement="start"
      items={Array.from({ length: 3 }).map((_, i) => {
        const id = String(i + 1);
        return {
          label: `Вкладка ${id}`,
          key: id,
          children: `Пример текста. ID: ${id}`,
        };
      })}
    />
  );
}
