import { useEffect, useState } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { physicianNavLinks } from "../utils/physicianNavLinks";
import { AudioRecorder } from "react-audio-voice-recorder";

function PhysicianConsultationGen() {
  const { user } = useUser();
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

  // For audio recorder
  const addAudioElement = async (blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement("audio");
    audio.src = URL.createObjectURL(blob);
    audio.controls = true;
    setAudioElement(audio);
    const formData = new FormData(); // To send to backend
    formData.append("audio_file", blob, "recording.webm");
    try {
      const res = await fetch("http://127.0.0.1:8000/transcribe_audio/", {
        // Get transcription of audio
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setTranscribedText(data.transcription);
      console.log(data.transcription);
    } catch (error) {
      console.log("Error making fetch request", error);
    }
  };

  return (
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
          <div className="flex justify-center mt-12">
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
                <h1 className="font-montserrat text-[#0c1454] text-lg mt-2 mr-4">
                  Recorded Audio:
                </h1>
                <audio controls src={audioElement.src}></audio>
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default PhysicianConsultationGen;
