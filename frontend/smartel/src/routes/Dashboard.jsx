import React, { useEffect } from "react";
import { useUser, useSession, useOrganization } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";

function Dashboard() {
  const { user } = useUser();
  const { isLoaded, session } = useSession();
  const userRole = checkUserRole(session);
  console.log(userRole);

  const showPhysicianLink = () => {
    return userRole === "org:admin" || userRole === "org:physician";
  };

  return (
    <>
      <div>
        <NavBar
          userRole={userRole}
          linksArray={patientNavLinks}
          showPhysicianLink={showPhysicianLink()}
        />
        <div className="flex justify-center items-center h-screen">
          <div className="block text-center">
            <h1 className="font-montserrat text-7xl mb-6 text-blue-950">
              Welcome to your dashboard {user?.firstName}
            </h1>
            <h1 className="font-montserrat text-blue-950 text-sm mb-6">
              Book appointments, upload medical documents, and view consultation
              reports.
            </h1>
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;
