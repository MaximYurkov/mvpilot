export function TextList({ items }: { items: string[] }) {
  return (
    <div>
      {items.map((item: string) => (
        <p key={item}>{item}</p>
      ))}
    </div>
  );
}
