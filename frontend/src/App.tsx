// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import LocadorDashboard from "./pages/LocadorDashboard";
import LocatarioDashboard from "./pages/LocatarioDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import { getLoggedUser } from "./utils/auth";
import { useEffect, useState } from "react";

export default function App() {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = getLoggedUser();
    setUser(storedUser);
    setLoading(false);
  }, []);


  if (loading) {
    return <div>Carregando...</div>;
  }


  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rota protegida para dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              {user
                ? user.user_type === "locador"
                  ? <LocadorDashboard />
                  : <LocatarioDashboard />
                : <Navigate to="/login" />}
            </ProtectedRoute>
          }
        />


      </Routes>
    </Router>
  );
}
