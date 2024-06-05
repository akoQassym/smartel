import { useState, useEffect } from "react";
import { useUser, useSession, useOrganization } from "@clerk/clerk-react";
import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";

function Profile() {
  const { user } = useUser();
  const [loading, setLoading] = useState(false);
  const [userData, setUserData] = useState({});
  const [patientData, setPatientData] = useState({});

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

  const getPatientData = async () => {
    try {
      const res = await fetch(
        `${process.env.SMARTEL_BACKEND_API_URL}/user/patient/${user.id}`,
        {
          method: "GET",
        }
      );
      const data = await res.json();
      setPatientData(data);
      console.log("Patient data set");
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    setLoading(true);
    const getData = async () => {
      const data1 = await getUserData();
      const data2 = await getPatientData();
      setLoading(false);
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
        <div>
          <NavBar linksArray={patientNavLinks} />
          <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
            Your Profile
          </div>
          <div className="w-screen flex justify-center mt-12">
            <div className="w-fit h-fit p-8 bg-slate-100 rounded-lg font-montserrat">
              {userData && patientData ? (
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
                      <div className="font-bold my-1 mr-8">Email Address: </div>{" "}
                      <div>{userData?.email}</div>
                    </div>
                    <div className="flex justify-between">
                      <div className="font-bold  my-1 mr-8">
                        Date of birth:{" "}
                      </div>{" "}
                      <div>{patientData?.birth_date?.substring(0, 10)}</div>
                    </div>
                    <div className="flex justify-between">
                      <div className="font-bold my-1 mr-8">Phone number: </div>{" "}
                      <div>{patientData?.phone_number}</div>
                    </div>
                    <div className="flex justify-between">
                      <div className="font-bold my-1 mr-8">Height: </div>{" "}
                      <div>{patientData?.height} cm</div>
                    </div>
                    <div className="flex justify-between">
                      <div className="font-bold my-1 mr-8">Weight: </div>{" "}
                      <div>{patientData?.weight} kg</div>
                    </div>
                    <div className="flex justify-between">
                      <div className="font-bold my-1 mr-8">Blood Type: </div>{" "}
                      <div>{patientData?.blood_type}</div>
                    </div>
                  </div>
                </>
              ) : (
                <></>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Profile;
