import { useEffect, useState } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { physicianNavLinks } from "../utils/physicianNavLinks";
import { AudioRecorder } from "react-audio-voice-recorder";
import LoadingPage from "../components/LoadingPage";

function PhysicianConsultationGen() {
  const { user } = useUser();
  const [loading, setLoading] = useState(false);
  const [appointmentID, setAppointmentID] = useState(null);
  const [appointments, setAppointments] = useState(null);
  const [summaryDocID, setSummaryDocID] = useState(null);
  const [summaryText, setSummaryText] = useState(null);
  const [editedSummaryText, setEditedSummaryText] = useState("");
  const { isLoaded, session } = useSession(); // You get role information from session
  const [transcribedText, setTranscribedText] = useState(""); // For displaying transcription
  const [audioElement, setAudioElement] = useState(null); // For audio player
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState("");

  // This useEffect is to check if user is a physician, and allow access
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

  // Get the booked appointments from the backend
  useEffect(() => {
    setLoading(true);
    const getAppointments = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:8000/get_appointments/isbooked/${user.id}`,
          {
            method: "GET",
          }
        );
        if (res.ok) {
          const data = await res.json();
          setAppointments(data);
          console.log(data);
          //console.log(appointments);
        }
      } catch (error) {
        console.log("Couldn't fetch appointments", error);
      }
    };
    getAppointments();
  }, []);

  // Once appointments are loaded, stop loading animation
  useEffect(() => {
    if (appointments) {
      setLoading(false);
    }
  }, [appointments]);

  // For audio recorder
  const addAudioElement = async (blob) => {
    setLoading(true);
    const url = URL.createObjectURL(blob);
    const audio = document.createElement("audio");
    audio.src = URL.createObjectURL(blob);
    audio.controls = true;
    setAudioElement(audio);
    const formData = new FormData(); // To send to backend
    formData.append("audio_file", blob, "recording.webm");
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/transcribe_audio/${appointmentID}`,
        {
          // Get transcription of audio
          method: "POST",
          body: formData,
        }
      );
      const data = await res.json();
      // setTranscribedText(data.transcription);
      setSummaryDocID(data[0]?.summary_doc_id);
      console.log(data[0]?.summary_doc_id);
    } catch (error) {
      console.log("Error making fetch request", error);
    }
    setLoading(false);
  };

  // Format datetime into a readable format
  const formatDateTime = (dateTimeString) => {
    const dateTime = new Date(dateTimeString);
    return dateTime.toLocaleString(); // Format according to user's locale
  };

  const handleGenerateSummary = async () => {
    setLoading(true);
    setSummaryText(null);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/summarize_transcription/${summaryDocID}`,
        {
          method: "POST",
        }
      );
      if (res.ok) {
        console.log("Summary generated");
        const data = await res.json();
        console.log(data);
        setSummaryText(data.summary);
        setEditedSummaryText(data.summary);
      }
    } catch (error) {
      console.log("Error generating summary", error);
    }
    setLoading(false);
  };

  // Handle sending edited summary text to backend
  const handleConfirmEdit = async () => {
    setLoading(true);
    try {
      const payload = {
        "appointment_id": appointmentID,
        "transcription": "",
        "markdown_summary": editedSummaryText,
      };
      const res = await fetch(
        `http://127.0.0.1:8000/review_edit_summary_doc/${summaryDocID}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );
      if (res.ok) {
        console.log("Edited summary sent successfully");
        const data = await res.json();
        console.log(data);
      }
    } catch (error) {
      console.log("Error sending edited summary", error);
    }
    setLoading(false);
  };

  const handleDone = () => {
    setEditedSummaryText(null);
    setAudioElement(null);
    setSummaryDocID(null);
    setSummaryText(null);
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
              showPhysicianLink={false}
              showPatientLink={true}
              linksArray={physicianNavLinks}
            />
            <div className="font-montserrat">
              <div className="text-center mt-8 text-3xl text-blue-950">
                Consultation Generation
              </div>
              <div className="flex justify-center">
                <h1 className="mt-9  mr-4 text-lg text-blue-950">
                  Appointment:
                </h1>
                <select
                  className="w-fit h-fit py-2 px-4 mt-8 rounded-md text-blue-950 bg-slate-100"
                  value={appointmentID}
                  onChange={(e) => setAppointmentID(e.target.value)}
                >
                  <option value="" key={"select"}>
                    Select an appointment
                  </option>
                  {appointments?.map((appointment) => (
                    <option
                      key={appointment.appointment_id}
                      value={appointment.appointment_id}
                    >
                      {formatDateTime(appointment.start_date_time)}
                    </option>
                  ))}
                </select>
              </div>
              {appointmentID && (
                <>
                  <div className="flex justify-center mt-8">
                    <div className="text-center text-lg mt-2 text-blue-950">
                      Record consultation:
                    </div>
                    <div className="mx-8">
                      <AudioRecorder
                        onRecordingComplete={addAudioElement}
                        audioTrackConstraints={{
                          noiseSuppression: true,
                          echoCancellation: true,
                        }}
                        downloadOnSavePress={false}
                        downloadFileExtension="webm"
                      />
                    </div>
                    {audioElement && (
                      <>
                        <h1 className="font-montserrat text-[#0c1454] text-lg mt-2 mr-6">
                          Recorded Audio:
                        </h1>
                        <audio controls src={audioElement.src}></audio>
                      </>
                    )}
                  </div>
                  {summaryDocID && (
                    <div className="flex justify-center mt-8">
                      <button
                        className="w-fit h-fit px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-300"
                        onClick={handleGenerateSummary}
                      >
                        Generate Summary
                      </button>
                    </div>
                  )}
                  {summaryText && (
                    <>
                      <h1 className="text-center mt-8 text-lg text-blue-950">
                        Summary:
                      </h1>
                      {editedSummaryText !== null ? (
                        <>
                          <div className="flex justify-center mt-4">
                            <textarea
                              className="w-2/3 h-48 p-4 bg-slate-100 text-black rounded-md mb-8"
                              value={editedSummaryText}
                              onChange={(e) =>
                                setEditedSummaryText(e.target.value)
                              }
                            />
                          </div>
                          <div className="flex justify-center mt-4">
                            <button
                              className="w-fit h-fit px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-300"
                              onClick={handleConfirmEdit}
                            >
                              Confirm Changes
                            </button>
                            <button
                              className="w-fit h-fit px-4 py-2 mx-4 bg-green-500 text-white rounded-md hover:bg-green-300"
                              onClick={handleDone}
                            >
                              Done
                            </button>
                          </div>
                        </>
                      ) : (
                        <></>
                      )}
                    </>
                  )}
                </>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
}

export default PhysicianConsultationGen;
