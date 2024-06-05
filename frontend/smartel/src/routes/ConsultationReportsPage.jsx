import { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import { useUser, useSession } from "@clerk/clerk-react";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";
import Markdown from "react-markdown";

function ConsultationReportsPage() {
  const [loading, setLoading] = useState(false);
  const { user } = useUser();
  const [summaryDocs, setSummaryDocs] = useState([]);
  const [isViewingDoc, setIsViewingDoc] = useState(false);
  const [docComponent, setDocComponent] = useState(null);

  useEffect(() => {
    setLoading(true);
    const getDocs = async () => {
      try {
        const res = await fetch(
          `${process.env.SMARTEL_BACKEND_API_URL}/get_summary_documents/${user.id}`
        );
        if (res.ok) {
          const data = await res.json();
          console.log("Received summary docs", data);
          setSummaryDocs(data);
        }
        setLoading(false);
      } catch (error) {
        console.log("Error fetching docs", error);
        setLoading(false);
      }
    };

    getDocs();
  }, []);

  const formatDateTime = (dateTimeString) => {
    const dateTime = new Date(dateTimeString);
    // Options for formatting the date and time
    const options = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    };
    // Convert datetime to the desired format
    return dateTime.toLocaleString("en-US", options);
  };

  const viewDocButton = (summary) => {
    setIsViewingDoc(true);
    const comp = (
      <SummaryDocumentView
        summary_details={summary}
        setIsViewingDoc={setIsViewingDoc}
        setDocComponent={setDocComponent}
      />
    );
    setDocComponent(comp);
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
            <NavBar linksArray={patientNavLinks} />
            <div>
              <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
                Consultation Reports
              </div>
              {isViewingDoc ? (
                <>{docComponent}</>
              ) : (
                <>
                  <div className="flex justify-center  mt-16">
                    <div className="w-3/5 block">
                      <h1 className="font-montserrat font-bold text-blue-950 mb-4">
                        Previous Reports:
                      </h1>
                      {summaryDocs?.map((s) => {
                        return (
                          <div
                            className="flex justify-between font-montserrat my-8 items-center"
                            key={s.appointment_details.appointment_id}
                          >
                            <div className="text-sm w-2/5 text-wrap">
                              {formatDateTime(
                                s.appointment_details.start_date_time
                              )}
                            </div>
                            <button
                              onClick={() => viewDocButton(s.summary_details)}
                              className="rounded-md bg-blue-500 text-white font-montserrat py-2 px-4 max-w-fit text-center text-sm mt-2 mx-3 hover:bg-blue-300"
                            >
                              View Report
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
}

function SummaryDocumentView({
  summary_details,
  setIsViewingDoc,
  setDocComponent,
}) {
  console.log("Printing here", summary_details);
  const backButtonHandler = () => {
    setIsViewingDoc(false);
    setDocComponent(null);
  };
  console.log(summary_details.markdown_summary);
  return (
    <>
      <div>
        <div className="flex justify-center mt-12">
          <div className="w-2/3 h-fit rounded-md font-montserrat block">
            <button
              className="w-fit h-fit px-4 py-2 bg-blue-500 hover:bg-blue-300 text-white rounded-md"
              onClick={backButtonHandler}
            >
              Back
            </button>
            <div className="w-full h-fit p-4 mt-4 rounded-md bg-slate-100 font-montserrat">
              <Markdown>{summary_details.markdown_summary}</Markdown>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ConsultationReportsPage;
