import React from "react";
import { useUser } from "@clerk/clerk-react";
import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = () => {
  const { isSignedIn } = useUser();

  if (!isSignedIn) {
    // Redirect to the sign-in page if not signed in
    return (
      <>
        <div className="flex justify-center">
          <Navigate to="/sign-in" replace />
        </div>
      </>
    );
  }

  // If signed in, render the child routes
  return <Outlet />;
};

export default ProtectedRoute;
