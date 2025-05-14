export function ScrollArea({ children, className = '' }) {
  return (
    <div className={`overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 ${className}`}>
      {children}
    </div>
  );
}
