// src/front/js/component/navbar.js
import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserLock } from "@fortawesome/free-solid-svg-icons";
import { Context } from "../store/appContext";

const Navbar = () => {
  const { store } = useContext(Context);
  const userId = store.user?.id || sessionStorage.getItem("userId");

  return (
    <nav className="navbar navbar-light bg-secondary opacity-50 py-4">
      <div className="container text-adjust-center d-flex justify-content-end w-auto">
        <div className="logoCandado m-0 p-1">
          <FontAwesomeIcon
            icon={faUserLock}
            style={{ width: "12%", height: "12%" }}
          />
        </div>
        <div className="ml-auto">
          {userId ? (
            <Link to={`/private/${userId}`}>
              <button className="btn btn-lg btn-primary rounded-pill">
                Perfil
              </button>
            </Link>
          ) : (
            <>
              <Link to="/login">
                <button className="btn btn-outline-light btn-primary rounded-pill">
                  Iniciar Sesión
                </button>
              </Link>
              <Link to="/signup">
                <button className="btn btn-outline-light btn-dark rounded-pill">
                  Registro
                </button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
