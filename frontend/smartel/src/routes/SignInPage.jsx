import { SignIn } from "@clerk/clerk-react";

function SignInPage() {
  return (
    <>
      <div className="flex justify-center items-center h-screen">
        <SignIn routing="path" path="/sign-in" />
      </div>
    </>
  );
}

export default SignInPage;
