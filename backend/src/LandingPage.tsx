import { PopupButton } from "@typeform/embed-react";
import React from "react";
import video from "../public/scrible-landing-page.mp4";

const LandingPage = () => {
  return (
    <section className="flex jusify-content items-center flex-col my-0 mx-auto">
      <div className="m-5">
        <div className="text lg:text-7xl title-scrible text-4xl italic text-center font-bold decoration-indigo-500">
          scrible
        </div>
      </div>
      <div className="text-intro m-2 max-w-3xl ">
        <p className="lg:mt-4 mt-2 lg:text-xl text-lg text-gray-500 text-center">
          scrible makes writing fast, fun and easy. Its AI features give you the
          confidence to write anything you want.
        </p>
      </div>
      <section className="flex flex-col mx-auto rounded bg-white lg:my-8 my-5 max-w-2xl w-full drop-shadow-lg">
        <video className="flex p-4" autoPlay={true} muted loop>
          <source src={video} type="video/mp4" />
        </video>
      </section>
      <div className="flex mx-auto max-w-2xl justify-between mt-5">
        <a
          href="https://forms.gle/gRZhGEDQfBoirAYd9"
          className="px-3 py-4 bg-indigo-500 text-white rounded font-medium"
        >
          Join the waitlist
        </a>
      </div>
    </section>
  );
};

export default LandingPage;
