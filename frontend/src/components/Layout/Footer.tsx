export default function Footer() {
  return (
    <footer className="h-12 bg-white shadow flex items-center justify-center text-gray-500 text-sm">
      © {new Date().getFullYear()} RFP AI System. All rights reserved.
    </footer>
  );
}
