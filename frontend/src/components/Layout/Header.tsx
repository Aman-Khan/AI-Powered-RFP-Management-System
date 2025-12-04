import LogoutIcon from "@mui/icons-material/Logout";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("userId");
    navigate("/");
  };

  return (
    <header className="h-16 bg-white shadow flex items-center justify-between px-6">
      <h2 className="text-lg font-semibold">Dashboard</h2>

      <button
        onClick={logout}
        className="flex items-center gap-2 text-red-600 hover:text-red-800"
      >
        <LogoutIcon />
        Logout
      </button>
    </header>
  );
}
