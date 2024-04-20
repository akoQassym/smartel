import React, { useEffect, useState } from "react";
import { SignIn, useUser } from "@clerk/clerk-react";
import RouteButton from "../components/RouteButton";

function Home() {
  const { isSignedIn } = useUser();

  return (
    <>
      <div className="flex justify-center items-center h-screen">
        <div className="block text-center p-4">
          <h1 className="font-montserrat font-bold text-7xl mb-6 text-blue-950">
            Smartel
          </h1>
          <h1 className="font-montserrat text-blue-950 text-sm mb-2">
            Schedule appointments, upload medical documents, and view
            consultation reports.
          </h1>
          {isSignedIn ? (
            <>
              <div className="flex justify-center">
                <RouteButton
                  routeLink={"/dashboard"}
                  buttonText={"Patient Portal"}
                />
                <RouteButton
                  routeLink={"/physicianDashboard"}
                  buttonText={"Physician Portal"}
                />
              </div>
            </>
          ) : (
            <>
              <div className="flex justify-center">
                <RouteButton
                  routeLink={"/dashboard"}
                  buttonText={"Get Started"}
                />
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}

export default Home;
