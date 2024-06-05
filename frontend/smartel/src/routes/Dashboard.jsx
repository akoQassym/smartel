import { useEffect, useState } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";
import { useNavigate } from "react-router-dom";
import { Button } from "../components";

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [appointments, setAppointments] = useState([]);
  const navigate = useNavigate(); // To redirect to patient registration page if not registered
  const { user } = useUser();
  const { isLoaded, session } = useSession();
  const userRole = checkUserRole(session);
  //console.log(userRole);

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

  const getBookedAppointments = async (patient_id) => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/get_patient_appointments/${patient_id}`, {
        method: "GET",
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to fetch appointments: ${error.message}`);
    }
  }

  const updateBookingAppointment = async (appointment_id) => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/cancel_appointment/${appointment_id}`, {
        method: "POST"
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to cancel the appointment: ${error.message}`);
    }
  }

  const cancelAppointment = async (appointment_id) => {
    try {
      await updateBookingAppointment(appointment_id);
      setAppointments(appointments.filter(appointment => appointment.appointment_id !== appointment_id));
    } catch (error) {
      console.log(error);
    }
  }

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

      if (!isPatientReg) {
        console.log("navigating");
        navigate("/patientProfileCompletion");
      } else {
        console.log("patient already already registered");
      }

      try {
        const data = await getBookedAppointments(user.id);
        console.log("DATA", data);
        setAppointments(data);
      } catch (error) {
        console.log(error);
        setAppointments([]);
      }
      setLoading(false); // Set loading to false after the check is complete
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
            
            <div className={appointments.length > 0 ? "py-8 px-10" : "flex justify-center items-center h-screen"}>
              <div>
                <div className="block text-center px-12 py-5">
                  <h1 className={`font-montserrat ${appointments.length > 0 ? "text-4xl" : "text-7xl"} mb-6 text-blue-950`}>
                    Welcome to your dashboard {user?.firstName}
                  </h1>
                  <h1 className="font-montserrat text-blue-950 text-sm mb-6">
                    Book appointments, upload medical documents, and view
                    consultation reports.
                  </h1>
                </div>
                <div className="w-fit ml-auto mr-auto font-montserrat">
                  <p className="font-bold">Upcoming appointments: {appointments.length}</p>
                  {appointments?.length > 0 && appointments.map((appointment, key) => (
                    <div key={key} className="w-[500px] p-6 my-3 py-3 px-3 bg-gray-100 rounded-md cursor-pointer hover:shadow-md">
                      <p><strong>{new Date(appointment.start_date_time).toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' })} {new Date(appointment.start_date_time).toLocaleTimeString('en-GB')}</strong></p>
                      <p>{appointment.physician_name} {appointment.physician_surname}</p>
                      <p>{appointment.phone_number}</p>
                      <Button bgColor="#DC2626" className="mt-6" onClick={cancelAppointment.bind(this, appointment.appointment_id)}>Cancel</Button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default Dashboard;
