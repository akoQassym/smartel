import { useEffect, useState } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { physicianNavLinks } from "../utils/physicianNavLinks";

function PhysicianProfile() {
  const { user } = useUser();
  const { isLoaded, session } = useSession(); // You get role information from session
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState("");

  useEffect(() => {
    if (isLoaded) {
      const role = checkUserRole(session); // Get role info
      setUserRole(role);
      console.log(userRole);
      if (role != "org:admin" && role != "org:physician") {
        navigate("/dashboard"); // If user is not admin or physician then restrict access to this page
      }
    }
  }, [isLoaded]);

  return (
    <>
      <div>
        <NavBar
          showPhysicianLink={false}
          showPatientLink={true}
          linksArray={physicianNavLinks}
        />
        <div className="flex justify-center items-center h-screen">
          <div className="block text-center px-10">
            <h1 className="font-montserrat text-7xl mb-6 text-blue-950">
              Physician Profile
            </h1>
          </div>
        </div>
      </div>
    </>
  );
}

export default PhysicianProfile;
