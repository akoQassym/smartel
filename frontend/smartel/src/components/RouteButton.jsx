import React from "react";
import { Link } from "react-router-dom";

function RouteButton({ routeLink, buttonText }) {
  return (
    <>
      <Link to={routeLink}>
        <div className="rounded-md bg-[#FF3131] text-white font-montserrat py-2 px-3 max-w-fit text-center text-sm mt-2 mx-3 hover:bg-red-400">
          {buttonText}
        </div>
      </Link>
    </>
  );
}

export default RouteButton;
