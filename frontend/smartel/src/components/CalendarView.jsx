import PropTypes from 'prop-types';
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

moment.locale("en-US");
const localizer = momentLocalizer(moment)

const CalendarView = ({ events, onSelectEvent, ...props }) => (
  <div className='h-[700px]'>
    <Calendar
      localizer={localizer}
      events={events}
      step={20}
      defaultDate={new Date()}
      popup={false}
      defaultView='week'
      showAllEvents
      min={new Date(2023, 30, 12, 8, 0, 0)}
      onSelectEvent={onSelectEvent}
      onShowMore={(events, date) => this.setState({ showModal: true, events })}
      className="font-montserrat"
      {...props}
    />
  </div>
);

export default CalendarView;

CalendarView.propTypes = {
  events: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      title: PropTypes.string.isRequired,
      start: PropTypes.instanceOf(Date).isRequired,
      end: PropTypes.instanceOf(Date).isRequired,
      allDay: PropTypes.bool,
      resource: PropTypes.any,
    })
  ).isRequired,
  onSelectEvent: PropTypes.func,
};
