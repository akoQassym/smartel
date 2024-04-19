import React from "react";
import { Link } from "react-router-dom";
import NavBar from "../components/NavBar";

function Dashboard() {
  return (
    <>
      <div>
        <NavBar />
        <div className="flex justify-center items-center h-screen">
          <div className="block text-center">
            <h1 className="font-montserrat text-7xl mb-6 text-blue-950">
              Welcome to your dashboard
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
