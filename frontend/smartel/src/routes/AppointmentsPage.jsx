import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import { patientNavLinks } from "../utils/patientNavLinks";
import LoadingPage from "../components/LoadingPage";
import Select from 'react-select';
import { Button, CalendarView, Modal } from "../components";
import convertToDateObject from "../utils/convertToDate";
import { useUser } from "@clerk/clerk-react";

function AppointmentsPage() {
  const { user } = useUser();
  const [loading, setLoading] = useState(false);
  const [appointmentsLoading, setAppointmentsLoading] = useState(false);
  const [specializations, setSpecializations] = useState([]);
  const [selectedSpecialization, setSelectedSpecialization] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const postAppointment = async (appointment_id, user_id) => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/book_appointment/${appointment_id}/${user_id}`, {
        method: "POST",
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to book the appointment: ${error.message}`);
    }
  }

  const getAvailableAppointments = async (specialization_id) => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/get_available_appointments/${specialization_id}`, {
        method: "GET",
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to fetch specializations: ${error.message}`);
    }
  }

  const getSpecializations = async () => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/get_specializations`, {
        method: "GET",
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to fetch specializations: ${error.message}`);
    }
  };

  const mapAppointmentsToEvents = (data) => (
    data?.flatMap(physician => (
      physician.appointments?.map(appointment => {
        const startDate = convertToDateObject(appointment.start_date_time);
        if (!startDate) {
          return null;
        }
  
        return {
          title: `${physician.first_name} ${physician.last_name}`,
          start: startDate,
          end: new Date(startDate.getTime() + 60 * 60 * 1000),
          appointment_id: appointment.appointment_id,
        };
      }) || []
    )).filter(event => event !== null)
  );

  const bookAppointment = async () => {
    try {
      await postAppointment(selectedAppointment.appointment_id, user.id);
    } catch (error) {
      console.log(error);
    } finally {
      closeModal();
      setSelectedAppointment(null);
      searchAppointments();
    }
  }

  const searchAppointments = async () => {
    try {
      setAppointmentsLoading(true);
      const data = await getAvailableAppointments(selectedSpecialization.value);
      console.log(data);
      setAppointments(data);
      setCalendarEvents(mapAppointmentsToEvents(data));
    } catch (error) {
      console.log(error);
      setCalendarEvents([]);
      setAppointments([]);
    } finally {
      setAppointmentsLoading(false);
    }
  }

  const selectSpecialization = (value) => {
    setSelectedSpecialization(value);
  }

  const selectAppointment = (event) => {
    setSelectedAppointment(event);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await getSpecializations();
        setSpecializations(data);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [])


  return (
    <>
      <div>
        <NavBar linksArray={patientNavLinks} />
        <div className="px-10 py-3">
          <div className="text-center font-montserrat text-4xl my-6 text-blue-950">
            Book an appointment
          </div>
          {loading ? 
            <LoadingPage />
          :
            <div className="py-5 flex">
              <div className="w-1/4">
                <div className="mb-4">
                  <p className="font-montserrat text-md mb-2 font-bold">Choose a specialization</p>
                  <Select 
                    isClearable 
                    isLoading={appointmentsLoading}
                    value={selectedSpecialization} 
                    onChange={selectSpecialization} 
                    options={
                      [...specializations.map(spec => (
                        {value: spec.specialization_id, label: spec.name}
                      ))]
                    }
                    className="font-montserrat"
                  />
                  <Button className="mt-2" onClick={searchAppointments}>Search for appointments</Button>
                </div>
                <div className="mt-5 max-h-full">
                  <p className="font-montserrat text-md mb-2 font-bold">Available physicians</p>
                  {appointments && appointments.map((physician, key) => (
                    <div key={key} className={`my-3 py-3 px-3 bg-gray-100 rounded-md ${physician.appointments.length === 0 ? 'opacity-20' : 'cursor-pointer hover:shadow-md'}`}>
                      <p>{physician.first_name} {physician.last_name} ({physician.sex})</p>
                    </div>
                  ))}
                </div>
              </div> 
              <div className="flex-1 pl-10">
                {calendarEvents.length <= 0 ? (
                  <div className="calendar-placeholder bg-gray-200 backdrop-filter backdrop-blur-lg p-4 rounded-md py-7 my-2">
                    No events scheduled
                  </div>
                ) : (
                  <CalendarView events={calendarEvents} onSelectEvent={selectAppointment}/>
                )}
              </div>
            </div>  
          }
        </div>
      </div>
      {selectedAppointment && (
        <Modal isOpen={isModalOpen} onClose={closeModal}>
          <div className="p-6">
            <h2 className="text-lg font-semibold mt-4 mb-1">{selectedAppointment.title}</h2>
            <p className="mt-1 mb-4">{selectedSpecialization.label}</p>
            <p><strong>Start Time:</strong> {selectedAppointment.start.toLocaleString()}</p>
            <p><strong>End Time:</strong> {selectedAppointment.end.toLocaleString()}</p>
            <p><strong>Duration:</strong> 1 hour</p>
            <Button className="mt-6" onClick={() => bookAppointment(selectedAppointment.appointment_id)}>Sign Up</Button>
          </div>
      </Modal>
      )}
    </>
  );  
}

export default AppointmentsPage;
