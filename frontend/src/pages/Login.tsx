import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", { email });
      const user = res.data.user;
      localStorage.setItem("user", JSON.stringify(user));
      alert(`Bem-vindo, ${user.name}!`);
      navigate("/dashboard"); // redireciona para rota protegida
    } catch (err: any) {
      alert(err.response?.data?.error || "Erro no login");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Login</h2>
      <input
        type="email"
        className="form-control mb-2"
        placeholder="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button className="btn btn-primary mb-3" onClick={handleLogin}>
        Entrar
      </button>
      <p>
        Não tem conta? <Link to="/register">Cadastrar-se</Link>
      </p>
    </div>
  );
}
