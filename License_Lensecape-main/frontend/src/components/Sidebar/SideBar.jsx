import React from "react";
import { Link } from "react-router-dom";
import "./styles.css";
import logo from "../../assets/images/Logo.png";
// import Link from "react-router-dom";

const SideBar = () => {
  return (
    <div className='SideBar'>
      <div>
        <img src={logo} alt='Compony LOGO' />
      </div>
      <div className='Dashboard'>
        <h2>Dashboard</h2>
        <ul>
          <li>
            <Link to='VideoStrem'>Video Streaming</Link>{" "}
          </li>
          <li>
            <Link to='ListOfVe'>List of Vechicles</Link>{" "}
          </li>
          <li>
            <Link to='Analytics'>Analytics</Link>{" "}
          </li>
          <li>
            <Link to='Activity'>Activity</Link>{" "}
          </li>
        </ul>
      </div>
    </div>
  );
};

export default SideBar;
