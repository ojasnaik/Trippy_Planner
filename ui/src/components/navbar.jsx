// Navbar.js
import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css"; // Make sure this path is correct

const Navbar = ({ userName }) => {
  return (
    <div className="nav-container">
      <nav className="navbar">
        <Link to="/" className="brand-link">
          <h1 className="brand">TRIPPY</h1>
        </Link>
      </nav>
    </div>
  );
};

export default Navbar;
