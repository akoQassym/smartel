import { useEffect, useState } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { physicianNavLinks } from "../utils/physicianNavLinks";
import LoadingPage from "../components/LoadingPage";

function PhysicianDashboard() {
  const [loading, setLoading] = useState(false);
  const { user } = useUser();
  const { isLoaded, session } = useSession(); // You get role information from session
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState("");

  const checkIfPhysicianRegistered = async () => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/user/physician/${user.id}`,
        {
          method: "GET",
        }
      );
      const data = await res.json();
      console.log("checking if physician is registered", data);
      return data !== null;
    } catch (error) {
      console.log(error);
    }
  };

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

  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      const isReg = await checkIfPhysicianRegistered();
      if (!isReg) {
        navigate("/physicianProfileCompletion"); // go to physician registration page
      } else {
        console.log("Physician already registered");
      }

      setLoading(false); // Set loading to false after the check is complete
    };
    fetchData();
  }, []);

  return (
    <>
      {loading ? (
        <LoadingPage />
      ) : (
        <div>
          <NavBar
            showPhysicianLink={false}
            showPatientLink={true}
            linksArray={physicianNavLinks}
          />
          <div className="flex justify-center items-center h-screen">
            <div className="block text-center px-10">
              <h1 className="font-montserrat text-7xl mb-6 text-blue-950">
                Welcome to your Physician Portal Dr. {user?.firstName}
              </h1>
              <h1 className="font-montserrat text-blue-950 text-sm mb-6">
                Schedule appointments and generate consultation reports
              </h1>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default PhysicianDashboard;
