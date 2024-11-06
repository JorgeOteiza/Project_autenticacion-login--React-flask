import React, { useContext, useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext.js";
import Logout from "./LogOut.jsx";

// Componente para verificar el token y proteger la página
const PrivatePage = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  return <>{children}</>;
};

// Componente de Private
const Private = () => {
  const { store, actions } = useContext(Context);
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/private/:id`, {
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("token")}`,
          },
        });

        if (!response.ok) {
          throw new Error('Error al obtener el perfil');
        }

        const data = await response.json();
        setUser(data);
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: error.message || "Error loading profile!",
        });
        navigate("/login");
      }
    };

    fetchProfile();
  }, [navigate]);

  if (!user) {
    return (
      <div className="PerfilTitle d-flex justify-content-center p-5 m-1">
        Cargando perfil...
      </div>
    );
  }

  return (
    <PrivatePage>
      <div className="perfil-container">
        <h1>Perfil de {user.email}</h1>
        <p>ID: {user.id}</p>
        <p>Email: {user.email}</p>
        <Logout />
      </div>
    </PrivatePage>
  );
};

export default Private;
