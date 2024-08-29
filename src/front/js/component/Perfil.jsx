import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Context } from "../store/appContext";

const Perfil = () => {
  const { store, actions } = useContext(Context);
  const { id } = useParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Fetch the user data based on the id from the URL
    actions.getUserProfile(id).then((data) => setUser(data));
  }, [id, actions]);

  if (!user) {
    return <div>Cargando perfil...</div>;
  }

  return (
    <div className="perfil-container">
      <h1>Perfil de {user.email}</h1>
      <p>ID: {user.id}</p>
      <p>Email: {user.email}</p>
      {/* Muestra más información del perfil aquí */}
    </div>
  );
};

export default Perfil;
