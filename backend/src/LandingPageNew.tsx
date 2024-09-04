import React from "react";
import { Link } from "react-router-dom";

import "./LandingPageNew.css";

import Logo from "./assets/Scrible.svg";
import video from "../public/scrible-landing-page.mp4";

const Scriblelandingpage = () => {
  return (
    <section className="grid-container">
      <nav>
        <div>
          <img src={Logo} alt="logo" />
        </div>
        <div className="nav-link">
          <Link to="/about">About</Link>
          <a href="mailto:tausif@scible.page">Contact</a>
          <Link to="/signup">Join now </Link>
        </div>
      </nav>
      <header>
        <div className="left">
          <h1>
            Writing <br />
            Reimagined
          </h1>
          <h3>
            Scrible makes writing fast, fun and easy. <br /> It s AI features
            gives you the confidence to write anything you want.
          </h3>
        </div>
        <div className="right">
          <video autoPlay loop muted controls={false}>
            <source src={video} type="video/mp4" />
          </video>
        </div>
      </header>
      <footer>
        <span className="footertext">Become a better writer</span>
        <Link className="join-btn" to="/signup">
          Try for free -&gt;
        </Link>

        <span className="copyright">Copyright © 2023 scrible</span>
      </footer>
    </section>
  );
};

export default Scriblelandingpage;
