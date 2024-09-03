import React, { useState, useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { useNavigate, Link } from "react-router-dom";
import Swal from "sweetalert2";
import "../../styles/logIn.css";

const LogIn = () => {
  const { store, actions } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (token && store.user?.id) {
      navigate(`/perfil/${store.user.id}`);
    }
  }, [token, navigate, store.user?.id]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem("token", data.token);
        navigate("/private");
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Datos erróneos o usuario inexistente!",
        });
        setEmail("");
        setPassword("");
      }
    } catch (error) {
      console.error("Error durante el login:", error);
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Error al intentar iniciar sesión!",
      });
    }
  };

  return (
    <div className="login-container col-12 mx-auto m-3 h-100">
      <h5 className="swal2-show">Acceso</h5>
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
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
        </div>

        <div className="boton-login col-9 mx-auto m-3">
          <button type="submit" className="btn btn-dark w-100">
            Ingresar
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
