import React from "react";
import { Link } from "react-router-dom";

function RouteButton({ routeLink, buttonText }) {
  return (
    <>
      <Link to={routeLink}>
        <div className="rounded-lg bg-red-500 text-white font-montserrat py-3 px-5 max-w-fit mx-auto text-center text-sm mt-2 hover:bg-red-400">
          {buttonText}
        </div>
      </Link>
    </>
  );
}

export default RouteButton;
