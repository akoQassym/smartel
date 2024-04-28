import React, { useEffect, useState } from "react";
import { SignIn, useUser, useSession } from "@clerk/clerk-react";
import RouteButton from "../components/RouteButton";
import { checkUserRole } from "../utils/checkUserRole";

const BUTTONS = [{ link: "/dashboard", text: "Patient Portal" }];

function Home() {
  const { isSignedIn } = useUser();
  const { isLoaded, session } = useSession();

  const [buttons, setButtons] = useState([...BUTTONS]);

  useEffect(() => {
    if (isLoaded) {
      const userRole = checkUserRole(session);
      console.log(userRole);
      if (userRole === "org:admin" || userRole === "org:physician") {
        setButtons((prevButtons) => [
          ...BUTTONS,
          { link: "/physicianDashboard", text: "Physician Portal" },
        ]);
      }
    }
  }, [isLoaded, session]);

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
                {buttons.map((b) => {
                  return (
                    <RouteButton
                      routeLink={b.link}
                      buttonText={b.text}
                      key={b.link}
                    />
                  );
                })}
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
