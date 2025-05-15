export function Button({ children, ...props }) {
  return (
    <button
      {...props}
      className="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-white text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
    >
      {children}
    </button>
  );
}
