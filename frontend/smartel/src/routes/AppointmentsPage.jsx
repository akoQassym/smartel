import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";

function AppointmentsPage() {
  return (
    <>
      <div>
        <NavBar linksArray={patientNavLinks} />
        <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
          Book an appointment
        </div>
      </div>
    </>
  );
}

export default AppointmentsPage;
