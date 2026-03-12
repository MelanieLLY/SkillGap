import React, { useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function ProtectedRoute() {
  const { token, user, fetchUser } = useAuthStore((state) => ({
    token: state.token,
    user: state.user,
    fetchUser: state.fetchUser,
  }));

  useEffect(() => {
    if (token && !user) {
      fetchUser();
    }
  }, [token, user, fetchUser]);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Wait until user is fully loaded, otherwise downstream components that
  // rely on 'user' existing might flicker or error.
  if (token && !user) {
    return (
      <div className="min-h-screen bg-[#0f1117] flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-[#38e5b1]/20 border-t-[#38e5b1] rounded-full animate-spin" />
      </div>
    );
  }

  return <Outlet />;
}
