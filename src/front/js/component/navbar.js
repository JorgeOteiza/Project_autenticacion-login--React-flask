import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
  return (
    <nav className="navbar navbar-light bg-secondary opacity-50 pt-5 pb-3">
      <div className="container text-adjust-center">
        <Link to="/login">
          <span className="navbar-brand mb-0 h1">Registro</span>
        </Link>
        <div className="ml-auto">
          <Link to="/private/:id">
            <button className="btn btn-lg btn-light">Perfil</button>
          </Link>
        </div>
      </div>
    </nav>
  );
};
