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
      navigate("/login"); // Redirige al login si no hay token
    }
  }, [navigate]);

  return <>{children}</>; // Retorna los hijos si hay token
};

// Componente de Private
const Private = () => {
  const { store, actions } = useContext(Context);
  const { id } = useParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Fetch the user data based on the id from the URL
    actions.getUserProfile(id).then((data) => setUser(data));
  }, [id, actions]);

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
        {/* Muestra más información del perfil aquí */}
        <Logout />
      </div>
    </PrivatePage>
  );
};

export default Private;
