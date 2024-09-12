import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate, Link } from "react-router-dom";
import Swal from "sweetalert2";
import "../../styles/logIn.css";

const LogIn = () => {
  const { store, actions } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const loginSuccess = await actions.login(email, password);
    if (loginSuccess) {
      Swal.fire({
        icon: "success",
        title: "Inicio de sesión exitoso",
      });
      const userId = sessionStorage.getItem("userId");
      navigate(`/private/${userId}`);
    } else {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Credenciales inválidas",
      });
    }
  };

  return (
    <div className="login-container col-12 mx-auto m-3 h-100">
      <h5 className="swal2-show">Inicio de sesión</h5>
      <form onSubmit={handleLogin}>
        <div className="input-group-login mx-5 px-2">
          <div className="input-field pt-4">
            <span className="far fa-user p-2"></span>
            <input
              value={email}
              id="email"
              type="text"
              placeholder="Correo usuario"
              className="input-field-login"
              required
              autoComplete="username"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group-login py-1 pb-2">
            <div className="input-field">
              <span className="fas fa-lock p-2"></span>
              <input
                value={password}
                id="password"
                type="password"
                placeholder="Contraseña"
                className="input-field-login"
                required
                autoComplete="current-password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
        </div>

        <div className="boton-login col-9 mx-auto m-3">
          <button type="submit" className="btn btn-dark w-100">
            Iniciar sesión
          </button>
        </div>
      </form>
      <Link to="/">
        <span className="btn btn-link" href="#" role="button">
          Volver
        </span>
      </Link>
    </div>
  );
};

export default LogIn;
