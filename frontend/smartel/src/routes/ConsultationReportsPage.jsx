import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import { useUser, useSession } from "@clerk/clerk-react";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";

function ConsultationReportsPage() {
  const [loading, setLoading] = useState(false);
  const { user } = useUser();
  const [summaryDocs, setSummaryDocs] = useState([]);

  useEffect(() => {
    setLoading(true);
    const getDocs = async () => {};
    setLoading(false);
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
            <NavBar linksArray={patientNavLinks} />
            <div>
              <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
                Consultation Reports
              </div>
              <div className="flex justify-center  mt-16">
                <div className="w-3/5 block">
                  <h1 className="font-montserrat font-bold text-blue-950 mb-4">
                    Previous Reports:
                  </h1>
                  <div className="flex justify-between font-montserrat my-8 items-center">
                    <div className="text-sm w-2/5 text-wrap">
                      10th February 2024 with cardiologist
                    </div>
                    <div className="rounded-md bg-[#002CFF] text-white font-montserrat py-2 px-2 max-w-fit text-center text-sm mt-2 mx-3 hover:bg-[#3D5FFF]">
                      Download Report
                    </div>
                  </div>
                  <div className="flex justify-between font-montserrat my-8 items-center">
                    <div className="text-sm w-2/5 text-wrap">
                      5th February 2024 with radiologist
                    </div>
                    <div className="rounded-md bg-[#002CFF] text-white font-montserrat py-2 px-2 max-w-fit text-center text-sm mt-2 mx-3 hover:bg-[#3D5FFF]">
                      Download Report
                    </div>
                  </div>
                  <div className="flex justify-between font-montserrat my-8 items-center">
                    <div className="text-sm w-2/5 text-wrap">
                      28th April 2023 with Dentist
                    </div>
                    <div className="rounded-md bg-[#002CFF] text-white font-montserrat py-2 px-2 max-w-fit text-center text-sm mt-2 mx-3 hover:bg-[#3D5FFF]">
                      Download Report
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default ConsultationReportsPage;
