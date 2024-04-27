import React from "react";
import { useUser } from "@clerk/clerk-react";
import NavBar from "../components/NavBar";

function Dashboard() {
  const { user } = useUser();

  return (
    <>
      <div>
        <NavBar />
        <div className="flex justify-center items-center h-screen">
          <div className="block text-center">
            <h1 className="font-montserrat text-7xl mb-6 text-blue-950">
              Welcome to your dashboard {user?.firstName}
            </h1>
            <h1 className="font-montserrat text-blue-950 text-sm mb-6">
              Schedule appointments, upload medical documents, and view
              consultation reports.
            </h1>
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;
