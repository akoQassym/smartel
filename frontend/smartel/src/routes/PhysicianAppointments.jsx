import { useEffect, useState, useCallback } from "react";
import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { physicianNavLinks } from "../utils/physicianNavLinks";
import { CalendarView, LoadingPage, Modal } from "../components";
import convertToDateObject from "../utils/convertToDate";

function PhysicianAppointments() {
  const { user } = useUser();
  const { isLoaded, session } = useSession();
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState("");

  const [loading, setLoading] = useState(false);
  const [appointments, setAppointments] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [events, setEvents] = useState([]);
  const [slotToBook, setSlotToBook] = useState();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSlotModalOpen, setIsSlotModalOpen] = useState(false);

  const getAppointments = async (physician_id) => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/get_appointments/${physician_id}`, {
        method: "GET",
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to fetch appointments: ${error.message}`);
    }
  }

  const postCreateAppointment = async (physician_id, start_time) => {
    try {
      const res = await fetch(`${process.env.SMARTEL_BACKEND_API_URL}/add_appointment/${physician_id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          start_date_time: start_time.toISOString() // Convert the date to ISO string format
        })
      });
      const data = await res.json();
      return data;
    } catch (error) {
      throw new Error(`Failed to add the appointment: ${error.message}`);
    }
  }

  const selectSlot = useCallback(
    ({ start }) => {
      setSlotToBook(start);
      setIsSlotModalOpen(true);
    },
    [setEvents]
  )

  const cancelSlotBooking = () => {
    setSlotToBook(null);
    setIsSlotModalOpen(false);
  }

  const confirmSlotBooking = async () => {
    setIsSlotModalOpen(false);
    try {
      setLoading(true);
      const data = await postCreateAppointment(user.id, slotToBook);
      setAppointments((prev) => [...prev, data]);
      setEvents(mapToEvents(appointments));
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }

  const openAppointmentDetails = (event) => {
    setSelectedEvent(event);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const closeSlotModal = () => {
    setIsSlotModalOpen(false);
  };

  const mapToEvents = (data) => (
    data.flatMap(appointment => {
      const startDate = convertToDateObject(appointment.start_date_time);
      return {
        title: appointment.isBooked ? "BOOKED" : "",
        start: startDate,
        end: new Date(startDate.getTime() + 60 * 60 * 1000),
        appointment_id: appointment.appointment_id,
        isBooked: appointment.isBooked
      };
    }).filter(event => event !== null)
  )

  const fetchAllAppointments = async () => {
    try {
      setLoading(true);
      const data = await getAppointments(user.id);
      setAppointments(data);
      setEvents(mapToEvents(data));
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }

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

  useEffect(() => {
    if (!appointments) {
      fetchAllAppointments();
    } else {
      setEvents(mapToEvents(appointments));
    }
  }, [appointments]);

  return (
    <>
      <div>
        <NavBar
          showPhysicianLink={false}
          showPatientLink={true}
          linksArray={physicianNavLinks}
        />
        <div className="px-10 py-3">
          <h1 className="text-center font-montserrat text-4xl my-6 text-blue-950">
            Your appointments
          </h1>
          {loading ? 
            <LoadingPage />
          :
            <div className="py-5">
              <CalendarView 
                step={30} 
                events={events} 
                onSelectEvent={openAppointmentDetails}
                onSelectSlot={selectSlot}
                selectable
                eventPropGetter={(event) => (
                  {
                    style: {
                      backgroundColor: event.isBooked ? "#265985" : "transparent",
                      borderColor: "#265985",
                      color: event.isBooked ? "#FFFFFF" : "#265985",
                      borderWidth: event.isBooked ? 1 : 2,
                      opacity: event.end < new Date() ? 0.3 : 1,
                    },
                  }
                )}
              />
            </div>
          }
        </div>
      </div>
      {selectedEvent && (
        <Modal isOpen={isModalOpen} onClose={closeModal}>
          <div className="p-6">
            <p className="mt-1 mb-4">{selectedEvent.isBooked ? "BOOKED" : "OPEN"}</p>
            <p><strong>Start Time:</strong> {selectedEvent.start.toLocaleString()}</p>
            <p><strong>End Time:</strong> {selectedEvent.end.toLocaleString()}</p>
            <p><strong>Duration:</strong> 1 hour</p>
          </div>
        </Modal>
      )}
      {isSlotModalOpen && (
        <Modal isOpen={isSlotModalOpen} onClose={closeSlotModal}>
          <div className="p-6">
            <p>Are you sure you want to book this slot?</p>
            <p>{slotToBook && new Date(slotToBook).toLocaleString()}</p>
            
            <div className="mt-4 flex justify-end">
              <button onClick={cancelSlotBooking} className="mr-2 bg-gray-300 px-4 py-2 rounded-md">No</button>
              <button onClick={confirmSlotBooking} className="bg-blue-500 text-white px-4 py-2 rounded-md">Yes</button>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
}

export default PhysicianAppointments;
