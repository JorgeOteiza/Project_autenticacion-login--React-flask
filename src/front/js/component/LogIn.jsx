import React, { useState, useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
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

  const handleLogin = (e) => {
    e.preventDefault();

    actions
      .login(email, password)
      .then((res) => {
        if (res) {
          Swal.fire({
            icon: "success",
            title: "Has accedido correctamente!",
          });
          navigate(`/perfil/${store.user.id}`);
        } else {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Datos erróneos o usuario inexistente!",
          });
          setEmail("");
          setPassword("");
        }
      })
      .catch((err) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Hubo un problema en la autenticación!",
        });
      });
  };

  return (
    <div className="login-container col-12 mx-auto m-3">
      <h5>Acceso</h5>
      <form onSubmit={handleLogin}>
        <div className="input-group-login">
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

        <div className="boton-login col-12 mx-auto m-3">
          <button type="submit" className="btn btn-dark w-100">
            Ingresar
          </button>
        </div>
      </form>
    </div>
  );
};

export default LogIn;
