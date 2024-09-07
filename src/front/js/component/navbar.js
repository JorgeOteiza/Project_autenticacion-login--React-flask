import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserLock } from "@fortawesome/free-solid-svg-icons";

export const Navbar = () => {
  return (
    <nav className="navbar navbar-light bg-secondary opacity-50 pt-5 pb-3">
      <div className="container text-adjust-center d-flex justify-content-end w-auto">
        <div className="logoCandado m-0 p-1">
          <FontAwesomeIcon
            icon={faUserLock}
            style={{ width: "12%", height: "12%" }}
          />
        </div>
        <Link to="/login">
          <span className="navbar-brand mb-0 h1">Registro</span>
        </Link>
        <div className="ml-auto">
          <Link to="/private/:id">
            <button className="btn btn-lg btn-primary rounded-pill">
              Perfil
            </button>
          </Link>
        </div>
      </div>
    </nav>
  );
};
