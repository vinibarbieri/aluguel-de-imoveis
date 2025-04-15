// src/utils/auth.ts
export function getLoggedUser() {
    const data = localStorage.getItem("user");
    return data ? JSON.parse(data) : null;
  }
  
  export function logout() {
    localStorage.removeItem("user");
    window.location.href = "/login";
  }
  