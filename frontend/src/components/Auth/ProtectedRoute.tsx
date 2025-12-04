import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute() {
  const userId = localStorage.getItem("userId");

  // If no user, redirect to login immediately
  if (!userId) {
    return <Navigate to="/login" replace />;
  }

  // Otherwise render nested routes
  return <Outlet />;
}
