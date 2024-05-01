import React, { useEffect, useState } from "react";
import { useUser, useSession, useOrganization } from "@clerk/clerk-react";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router-dom";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";

function CompletePhysicianProfile() {
  const { user } = useUser();
  const [loading, setLoading] = useState(false);
  const [registrationError, setRegistrationError] = useState(" "); // To display error message
  const [formData, setFormData] = useState({
    phoneNumber: "",
    dateOfBirth: "",
    sex: "male",
    specialization_id: "0",
  });
  const [specializationIDs, setSpecializationIDs] = useState([]);
  const navigate = useNavigate(""); // To redirect to dashboard after registration

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    console.log("Submitting");
    const dataForPhysician = {
      "birth_date": formData.dateOfBirth,
      "phone_number": formData.phoneNumber,
      "sex": formData.sex,
      "specialization_id": formData.specialization_id,
    };

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/register/physician/${user.id}`,
        {
          method: "POST", // Specify the HTTP method
          headers: {
            "Content-Type": "application/json", // Specify content type as JSON
          },
          body: JSON.stringify(dataForPhysician), // Convert data to JSON string
        }
      );

      if (!res.ok) {
        console.log(res);
        throw new Error("Failed to register user");
      }
      const responseData = await res.json(); // Parse response JSON
      console.log("Patient registered successfully:", responseData);
      navigate("/physicianDashboard");
    } catch (error) {
      console.log("Error registering patient.", error);
      setRegistrationError("There was an error. Please try again.");
    }
    setLoading(false);
  };

  // To get specialization IDs
  useEffect(() => {
    const getData = async () => {
      const res = await fetch(`http://127.0.0.1:8000/get_specializations`, {
        method: "GET",
      });
      const data = await res.json();
      setSpecializationIDs(data);
      console.log("Specialization IDs set", data);
      console.log(data[0].specialization_id);
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
          <div className="h-screen items-center w-screen flex justify-center">
            <div className="w-screen flex justify-center">
              <div>
                <h1 className="mb-4 font-montserrat text-lg text-red-600 text-center">
                  {registrationError}
                </h1>
                <h1 className="my-8 font-montserrat text-lg font-bold text-blue-950 text-center">
                  Complete Registration to continue
                </h1>
                <div className="w-fit h-fit p-8 bg-slate-100 rounded-lg">
                  <form onSubmit={handleSubmit}>
                    <div className="block font-montserrat">
                      <div className="flex justify-evenly">
                        <label className="block mx-4 my-4">Phone Number:</label>
                        <input
                          className="h-fit p-1 my-auto rounded-md"
                          type="text"
                          name="phoneNumber"
                          value={formData.phoneNumber}
                          onChange={handleChange}
                          required={true}
                        />
                      </div>
                      <div className="flex justify-evenly">
                        <label className="block mx-4 my-4">
                          Date of Birth:
                        </label>
                        <input
                          className="h-fit p-1 my-auto rounded-md"
                          type="date"
                          name="dateOfBirth"
                          value={formData.dateOfBirth}
                          onChange={handleChange}
                          required={true}
                        />
                      </div>
                      <div className="flex justify-evenly">
                        <label className="block mx-4 my-4">Sex:</label>
                        <select
                          className="h-fit p-1 my-auto rounded-md"
                          name="sex"
                          value={formData.sex}
                          onChange={handleChange}
                          required={true}
                        >
                          <option value="male">Male</option>
                          <option value="female">Female</option>
                          <option value="other">Other</option>
                        </select>
                      </div>
                      <div className="flex justify-evenly">
                        <label className="block mx-4 my-4">Sex:</label>
                        <select
                          className="h-fit p-1 my-auto rounded-md"
                          name="specialization_id"
                          value={formData.specialization_id}
                          onChange={handleChange}
                          required={true}
                        >
                          <option value="0">Select</option>
                          <option
                            value={String(
                              specializationIDs[0]?.specialization_id
                            )}
                          >
                            Pediatrician
                          </option>
                        </select>
                      </div>
                      <div className="flex justify-center mt-5">
                        <button
                          type="submit"
                          className=" px-4 py-2 w-fit h-fit bg-green-500 rounded-md text-white hover:bg-green-300"
                        >
                          Submit
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default CompletePhysicianProfile;
