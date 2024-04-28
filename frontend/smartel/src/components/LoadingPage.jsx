import React from "react";

function LoadingPage() {
  return (
    <>
      <div className="flex justify-center h-screen items-center">
        <div className="w-fit px-4 py- font-montserrat text-red-600 flex">
          <div className="px-1">Loading...</div>
          <svg
            className="animate-spin h-5 w-5 text-red-600"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 4.418 3.582 8 8 8v-4zm12-2a7.962 7.962 0 01-2 5.291V20c4.418 0 8-3.582 8-8h-4zm-2-10.291A7.962 7.962 0 0120 12h4c0-4.418-3.582-8-8-8v4z"
            ></path>
          </svg>
        </div>
      </div>
    </>
  );
}

export default LoadingPage;
