import { useEffect, useState } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { physicianNavLinks } from "../utils/physicianNavLinks";
import LoadingPage from "../components/LoadingPage";

function PhysicianProfile() {
  const { user } = useUser();
  const { isLoaded, session } = useSession(); // You get role information from session
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState("");
  const [userData, setUserData] = useState({});
  const [physicianData, setPhysicianData] = useState({});
  const [loading, setLoading] = useState(false);

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

  const getUserData = async () => {
    try {
      const res = await fetch(
        `${process.env.SMARTEL_BACKEND_API_URL}/user/${user.id}`,
        {
          method: "GET",
        }
      );
      const data = await res.json();
      setUserData(data);
      console.log("User data set successfully");
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  };

  const getPhysicianData = async () => {
    try {
      const res = await fetch(
        `${process.env.SMARTEL_BACKEND_API_URL}/user/physician/${user.id}`,
        {
          method: "GET",
        }
      );
      const data = await res.json();
      setPhysicianData(data);
      console.log("Physician data set");
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    setLoading(true);
    const getData = async () => {
      try {
        const data1 = await getUserData();
        const data2 = await getPhysicianData();
        setLoading(false);
      } catch (error) {
        console.log("Error getting user and physician data", error);
        setLoading(false);
      }
    };
    getData();
  }, []);

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
              showPhysicianLink={false}
              showPatientLink={true}
              linksArray={physicianNavLinks}
            />
            <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
              Your Profile
            </div>
            <div className="w-screen flex justify-center mt-12">
              <div className="w-fit h-fit p-8 bg-slate-100 rounded-lg font-montserrat">
                {userData && physicianData ? (
                  <>
                    <div className="block">
                      <div className="flex justify-between">
                        <div className="font-bold  my-1 mr-8">First Name: </div>{" "}
                        <div>{userData?.first_name}</div>
                      </div>
                      <div className="flex justify-between">
                        <div className="font-bold my-1  mr-8">Last Name: </div>{" "}
                        <div>{userData?.last_name}</div>
                      </div>
                      <div className="flex justify-between">
                        <div className="font-bold my-1 mr-8">
                          Email Address:{" "}
                        </div>{" "}
                        <div>{userData?.email}</div>
                      </div>
                      <div className="flex justify-between">
                        <div className="font-bold  my-1 mr-8">
                          Date of birth:{" "}
                        </div>{" "}
                        <div>{physicianData?.birth_date?.substring(0, 10)}</div>
                      </div>
                      <div className="flex justify-between">
                        <div className="font-bold my-1 mr-8">
                          Phone number:{" "}
                        </div>{" "}
                        <div>{physicianData?.phone_number}</div>
                      </div>
                      <div className="flex justify-between">
                        <div className="font-bold my-1 mr-8">Sex: </div>{" "}
                        <div>{physicianData?.sex}</div>
                      </div>
                    </div>
                  </>
                ) : (
                  <></>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default PhysicianProfile;
