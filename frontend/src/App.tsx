// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import LocadorDashboard from "./pages/LocadorDashboard";
import LocatarioDashboard from "./pages/LocatarioDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import { getLoggedUser } from "./utils/auth";

export default function App() {
  const user = getLoggedUser();

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rota protegida para dashboard */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            {user?.user_type === "locador" ? <LocadorDashboard /> : <LocatarioDashboard />}
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}
