import React, { useState } from "react";
import { useUser, useSession, useOrganization } from "@clerk/clerk-react";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router-dom";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";

function CompletePatientProfile() {
  const { user } = useUser();
  const [loading, setLoading] = useState(false);
  const [registrationError, setRegistrationError] = useState(" "); // To display error message
  const [formData, setFormData] = useState({
    phoneNumber: "",
    weight: "",
    height: "",
    dateOfBirth: "",
    sex: "male",
    bloodType: "",
  });
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
    const dataForPatient = {
      "birth_date": formData.dateOfBirth,
      "blood_type": formData.bloodType,
      "height": formData.height,
      "phone_number": formData.phoneNumber,
      "sex": formData.sex,
      "weight": formData.weight,
    };

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/register/patient/${user.id}`,
        {
          method: "POST", // Specify the HTTP method
          headers: {
            "Content-Type": "application/json", // Specify content type as JSON
          },
          body: JSON.stringify(dataForPatient), // Convert data to JSON string
        }
      );

      if (!res.ok) {
        console.log(res);
        throw new Error("Failed to register user");
      }
      const responseData = await res.json(); // Parse response JSON
      console.log("Patient registered successfully:", responseData);
      navigate("/dashboard");
    } catch (error) {
      console.log("Error registering patient.", error);
      setRegistrationError("There was an error. Please try again.");
    }
    setLoading(false);
  };

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
                        <label className="block mx-4 my-4">Weight (kg):</label>
                        <input
                          className="h-fit p-1 my-auto rounded-md"
                          type="number"
                          name="weight"
                          value={formData.weight}
                          onChange={handleChange}
                          required={true}
                        />
                      </div>

                      <div className="flex justify-evenly">
                        <label className="block mx-4 my-4">Height (cm):</label>
                        <input
                          className="h-fit p-1 my-auto rounded-md"
                          type="number"
                          name="height"
                          value={formData.height}
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
                        <label className="block mx-4 my-4">Blood Type:</label>
                        <input
                          className="h-fit p-1 my-auto rounded-md"
                          type="text"
                          name="bloodType"
                          value={formData.bloodType}
                          onChange={handleChange}
                          required={true}
                        />
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

export default CompletePatientProfile;
