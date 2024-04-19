import React from "react";
import RouteButton from "../components/RouteButton";

function Home() {
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
          <div className="flex justify-center">
            <RouteButton routeLink={"/dashboard"} buttonText={"Get Started"} />
          </div>
        </div>
      </div>
    </>
  );
}

export default Home;
