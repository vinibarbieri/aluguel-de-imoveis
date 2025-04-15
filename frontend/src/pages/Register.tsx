import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", user_type: "locador" });

  const handleRegister = async () => {
    try {
      await axios.post("http://localhost:5000/api/auth/register", form);
      alert("Usuário cadastrado com sucesso!");
    } catch (err: any) {
      alert(err.response?.data?.error || "Erro no cadastro");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Cadastro</h2>
      <input
        className="form-control mb-2"
        placeholder="Nome"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />
      <input
        className="form-control mb-2"
        placeholder="Email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />
      <select
        className="form-control mb-2"
        value={form.user_type}
        onChange={(e) => setForm({ ...form, user_type: e.target.value })}
      >
        <option value="locador">Locador</option>
        <option value="locatario">Locatário</option>
      </select>
      <button className="btn btn-success mb-3" onClick={handleRegister}>
        Cadastrar
      </button>
      <p>
        Já tem conta? <Link to="/login">Fazer login</Link>
      </p>
    </div>
  );
}
