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
        `${process.env.REACT_APP_BACKEND_URL}/signup`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password }),
        }
      );

      if (response.ok) {
        Swal.fire({
          icon: "success",
          title: "User registered successfully!",
        });
        navigate("/login"); // Redirige al login
      } else {
        throw new Error("Signup failed");
      }
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Error during signup!",
      });
    }
  };

  return (
    <div className="Registro container col alert-success d-flex justify-content-center mx-auto w-50 m-3 p-3 gap-3">
      <form className="col-8" onSubmit={handleSignup}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </form>
      <button className="botónRegistro btn-dark rounded-3" type="submit">
        Registrar
      </button>
    </div>
  );
};

export default Signup;
