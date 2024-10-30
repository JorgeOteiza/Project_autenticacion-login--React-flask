import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/signup`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          mode: 'cors',
          credentials: 'include', 
          body: JSON.stringify({ email, password }),
        }
      );

      if (!response.ok) {
        const data = await response.json();
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: data.message || "Fallo en el registro",
        });
      } else {
        const data = await response.json();

        // Verifica que el usuario y el id existan en la respuesta
        if (data.user && data.user.id) {
          sessionStorage.setItem("token", data.token);
          sessionStorage.setItem("userId", data.user.id);

          Swal.fire({
            icon: "success",
            title: "Bienvenido!",
            text: "Tu cuenta ha sido creada exitosamente.",
          });

          navigate(`/private/${data.user.id}`); // Redirige al perfil del usuario
        } else {
          throw new Error("No se pudo obtener el perfil del usuario");
        }
      }
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: error.message || "Error durante el registro",
      });
    }
  };

  return (
    <div className="Registro container col alert-success d-flex justify-content-center mx-auto w-50 m-3 p-3 gap-3">
      <form
        className="row col-8 my-1 d-flex justify-content-center"
        onSubmit={handleSignup}
      >
        <input
          className="mb-1"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="username"
        />
        <input
          className="mt1"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />
        <button
          className="botónRegistro btn-dark rounded-3 my-3 w-50"
          type="submit"
        >
          Registrar
        </button>
      </form>
    </div>
  );
};

export default Signup;
