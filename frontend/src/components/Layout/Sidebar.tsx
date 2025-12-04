import { Home, People, Description } from "@mui/icons-material";
import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();

  const navItems = [
    { label: "Users", icon: <People />, path: "/users" },
    { label: "Create RFP", icon: <Description />, path: "/rfp/create" }
  ];

  return (
    <aside className="w-56 bg-white shadow-md flex flex-col py-6">
      <h1 className="text-xl font-bold text-center mb-8">RFP Manager</h1>

      {navItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          className={`flex items-center gap-3 px-6 py-3
            ${location.pathname === item.path ? "bg-blue-100 text-blue-600" : "text-gray-700"}
          `}
        >
          {item.icon}
          {item.label}
        </Link>
      ))}
    </aside>
  );
}
