import React, { useEffect, useState } from "react";
import { useUser, useSession, useOrganization } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // To redirect to patient registration page if not registered
  const { user } = useUser();
  const { isLoaded, session } = useSession();
  const userRole = checkUserRole(session);
  console.log(userRole);

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

  const checkIfPatientRegistered = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/user/patient/${user.id}`, {
        method: "GET",
      });
      const data = await res.json();
      console.log("checking if patient registered", data);
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

  // To check if user is registered
  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      const isReg = await checkIfRegistered();
      if (!isReg) {
        await register();
      } else {
        console.log("User already registered");
      }
      const isPatientReg = await checkIfPatientRegistered();
      console.log(isPatientReg, "is patient reg");

      setLoading(false); // Set loading to false after the check is complete
      if (!isPatientReg) {
        console.log("navigating");
        navigate("/patientProfileCompletion");
      } else {
        console.log("patient already already registered");
      }
    };
    fetchData();
  }, []);

  // Check if you should show link to physician portal, by checking if user is an admin/physician
  const showPhysicianLink = () => {
    return userRole === "org:admin" || userRole === "org:physician";
  };

  return (
    <>
      {loading ? (
        <>
          <LoadingPage />
        </>
      ) : (
        <>
          <div>
            <NavBar
              userRole={userRole}
              linksArray={patientNavLinks}
              showPhysicianLink={showPhysicianLink()}
            />
            <div className="flex justify-center items-center h-screen">
              <div className="block text-center px-12">
                <h1 className="font-montserrat text-7xl mb-6 text-blue-950">
                  Welcome to your dashboard {user?.firstName}
                </h1>
                <h1 className="font-montserrat text-blue-950 text-sm mb-6">
                  Book appointments, upload medical documents, and view
                  consultation reports.
                </h1>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default Dashboard;
