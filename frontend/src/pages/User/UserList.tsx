import AppLayout from "../../components/Layout/AppLayout";
import { api } from "../../lib/axios";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import EditIcon from "@mui/icons-material/Edit";

export default function UserList() {
  const { data, isLoading } = useQuery({
    queryKey: ["users"],
    queryFn: async () => (await api.get("/user/all")).data,
  });

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Users</h1>

      <Link
        to="/users/create"
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Add User
      </Link>

      <div className="mt-6 bg-white rounded shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 text-left">ID</th>
              <th className="p-3 text-left">Email</th>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.map((u: any) => (
              <tr key={u.id} className="border-t">
                <td className="p-3">{u.id}</td>
                <td className="p-3">{u.email}</td>
                <td className="p-3">{u.name}</td>
                <td className="p-3">
                  <Link
                    to={`/users/edit/${u.id}`}
                    className="text-blue-600 hover:underline flex items-center gap-1"
                  >
                    <EditIcon /> Edit
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
