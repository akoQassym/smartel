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

  const checkIfRegistered = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/user/${user.id}`, {
        method: "GET",
      });
      const data = await res.json();

      return data !== null;
    } catch (error) {
      console.log(error);
    }
  };

  // Register user if record doesn't exist on backend (first time login)
  const register = async () => {
    const dataToRegister = {
      "user_id": user.id,
      "first_name": user.firstName,
      "last_name": user.lastName,
      "email": user.primaryEmailAddress.emailAddress,
    };
    console.log(dataToRegister);
    try {
      const res = await fetch("http://127.0.0.1:8000/register", {
        method: "POST", // Specify the HTTP method
        headers: {
          "Content-Type": "application/json", // Specify content type as JSON
        },
        body: JSON.stringify(dataToRegister), // Convert data to JSON string
      });
      if (!res.ok) {
        console.log(res);
        throw new Error("Failed to register user");
      }

      const responseData = await res.json(); // Parse response JSON
      console.log("User registered successfully:", responseData);
    } catch (error) {
      console.error("Error registering user:", error);
    }
  };

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
      const isReg = await checkIfRegistered();
      if (!isReg) {
        await register();
      } else {
        console.log("User already registered");
      }
      const isPhysicianReg = await checkIfPhysicianRegistered();
      if (!isPhysicianReg) {
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
