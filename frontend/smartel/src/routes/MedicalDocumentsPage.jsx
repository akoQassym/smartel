import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";

function MedicalDocumentsPage() {
  return (
    <>
      <div>
        <NavBar linksArray={patientNavLinks} />
        <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
          Medical Documents Page
        </div>
      </div>
    </>
  );
}

export default MedicalDocumentsPage;
