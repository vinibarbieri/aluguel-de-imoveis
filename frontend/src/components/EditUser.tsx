import { useState } from "react";
import axios from "axios";

interface EditUserProps {
  userId: string;
  currentName: string;
  currentEmail: string;
  onUserUpdated?: (user: any) => void; // chamada para atualizar o estado do dashboard
}

export default function EditUser({ userId, currentName, currentEmail, onUserUpdated }: EditUserProps) {
  const [name, setName] = useState(currentName);
  const [email, setEmail] = useState(currentEmail);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.put("http://localhost:5000/api/auth/edit", {
        id: userId,
        name,
        email,
      });

      // Atualiza o localStorage
      const updatedUser = { ...JSON.parse(localStorage.getItem("user") || "{}"), name, email };
      localStorage.setItem("user", JSON.stringify(updatedUser));

      // Atualiza o estado no componente pai (LocadorDashboard)
      if (onUserUpdated) {
        onUserUpdated(updatedUser);
      }

      setMessage(res.data.message);
    } catch (err: any) {
      setMessage(err.response?.data?.error || "Erro ao atualizar.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Editar Cadastro</h2>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Nome"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Salvar</button>
      <p>{message}</p>
    </form>
  );
}
