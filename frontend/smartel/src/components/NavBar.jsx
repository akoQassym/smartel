import React from "react";
import { Link } from "react-router-dom";
import RouteButton from "./RouteButton";

function NavBar() {
  return (
    <>
      <div className="flex justify-between shadow-sm">
        <Link to={"/dashboard"}>
          <div className="text-center py-3 px-4">
            <h1 className="font-montserrat font-bold text-lg  text-blue-950">
              Smartel
            </h1>
          </div>
        </Link>

        <div className="flex justify-normal">
          <Link to={"/medicaldocs"}>
            <div className="font-montserrat text-sm p-4 hover:text-[#FF3131] text-blue-950">
              Medical Documents
            </div>
          </Link>
          <Link to={"/appointmentspage"}>
            <div className="font-montserrat text-sm p-4 hover:text-[#FF3131] text-blue-950">
              Appointments
            </div>
          </Link>
          <Link to={"/consultationreports"}>
            <div className="font-montserrat text-sm p-4 hover:text-[#FF3131] text-blue-950">
              Consultation Reports
            </div>
          </Link>
          <RouteButton routeLink={"/"} buttonText={"Logout"} />
        </div>
      </div>
    </>
  );
}

export default NavBar;
