import { useEffect, useState } from "react";
import { api } from "../../lib/axios";
import { useNavigate, useParams } from "react-router-dom";

export default function EditUser() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");

  useEffect(() => {
    api.get(`/user/${id}`).then(res => {
      setEmail(res.data.email);
      setName(res.data.name);
    });
  }, []);

  const updateUser = async () => {
    await api.put(`/user/${id}`, { email, name });
    navigate("/users");
  };

  const deleteUser = async () => {
    await api.delete(`/user/${id}`);
    navigate("/users");
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">Edit User</h1>

      <input
        className="border p-2 w-full mb-3"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        className="border p-2 w-full mb-3"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <button
        onClick={updateUser}
        className="bg-blue-600 text-white px-4 py-2 rounded mr-3"
      >
        Update
      </button>

      <button
        onClick={deleteUser}
        className="bg-red-600 text-white px-4 py-2 rounded"
      >
        Delete
      </button>
    </div>
  );
}
