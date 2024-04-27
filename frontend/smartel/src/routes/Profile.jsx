import React, { useState } from "react";
import { useUser, useSession, useOrganization } from "@clerk/clerk-react";
import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";

function Profile() {
  const { user } = useUser();

  const [formData, setFormData] = useState({
    phoneNumber: "",
    weight: "",
    height: "",
    dateOfBirth: "",
    sex: "",
    bloodType: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
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

    // const dataForPatient = {

    // }
  };

  return (
    <>
      <div>
        <NavBar linksArray={patientNavLinks} />
        <div className="w-screen flex justify-center mt-12">
          <div>
            <h1 className="my-4 font-montserrat text-lg font-bold text-blue-950">
              Complete Registration:
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
                    />
                  </div>

                  <div className="flex justify-evenly">
                    <label className="block mx-4 my-4">Date of Birth:</label>
                    <input
                      className="h-fit p-1 my-auto rounded-md"
                      type="date"
                      name="dateOfBirth"
                      value={formData.dateOfBirth}
                      onChange={handleChange}
                    />
                  </div>

                  <div className="flex justify-evenly">
                    <label className="block mx-4 my-4">Sex:</label>
                    <select
                      className="h-fit p-1 my-auto rounded-md"
                      name="sex"
                      value={formData.sex}
                      onChange={handleChange}
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
  );
}

export default Profile;
