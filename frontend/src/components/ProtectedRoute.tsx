// src/components/ProtectedRoute.tsx
import { Navigate } from "react-router-dom";
import { ReactNode } from "react";
import { getLoggedUser } from "../utils/auth";

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const user = getLoggedUser();
  return user ? <>{children}</> : <Navigate to="/login" />;
}
