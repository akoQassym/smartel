import React from "react";
import { Link } from "react-router-dom";
import { UserButton } from "@clerk/clerk-react";
import RouteButton from "./RouteButton";

function NavBar({ linksArray, showPhysicianLink, showPatientLink }) {
  let bgColor = "bg-white";
  if (showPatientLink) {
    bgColor = "bg-blue-100";
  }
  return (
    <>
      <div className={`flex justify-between shadow-sm ${bgColor}`}>
        <div className="flex justify-normal">
          {showPatientLink ? (
            <>
              <Link to={"/physicianDashboard"}>
                <div className="text-center py-3 px-4">
                  <h1 className="font-montserrat font-bold text-lg  text-blue-950">
                    Smartel
                  </h1>
                </div>
              </Link>
            </>
          ) : (
            <>
              <Link to={"/dashboard"}>
                <div className="text-center py-3 px-4">
                  <h1 className="font-montserrat font-bold text-lg  text-blue-950">
                    Smartel
                  </h1>
                </div>
              </Link>
            </>
          )}

          {showPhysicianLink ? (
            <>
              <RouteButton
                routeLink={"/physicianDashboard"}
                buttonText={"Go to Physician Portal"}
              />
            </>
          ) : (
            <></>
          )}
          {showPatientLink ? (
            <>
              <RouteButton
                routeLink={"/dashboard"}
                buttonText={"Go to Patient Portal"}
              />
            </>
          ) : (
            <></>
          )}
        </div>

        <div className="flex justify-normal">
          {linksArray.map((l) => {
            return (
              <Link to={l.link} key={l.link}>
                <div className="font-montserrat text-sm py-4 px-3 hover:text-[#FF3131] text-blue-950">
                  {l.text}
                </div>
              </Link>
            );
          })}
          <div className="flex justify-center items-center mx-4">
            <UserButton afterSignOutUrl="/" />
          </div>
        </div>
      </div>
    </>
  );
}

export default NavBar;
