import { useUser, useSession } from "@clerk/clerk-react";
import { checkUserRole } from "../utils/checkUserRole";
import { redirect } from "react-router-dom";

export async function userRoleLoader() {
  const [isLoaded, session] = useSession();
  const userRole = checkUserRole(session);

  if (userRole != "org:admin" || userRole != "org:physician") {
    return redirect("/dashboard");
  }
  return userRole;
}
