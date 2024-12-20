import React, { useContext, useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext.js";
import Logout from "./LogOut.jsx";
import Swal from "sweetalert2";
import "../../styles/perfil.css";

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

const Private = () => {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/api/profile/${id}`,
          {
            headers: {
              Authorization: `Bearer ${sessionStorage.getItem("token")}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Error al obtener el perfil");
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
  }, [id, navigate]);

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
        <div className="perfil-header">
          <div className="profile-pic-container">
            <img
              src="https://via.placeholder.com/150"
              alt="Foto de perfil"
              className="profile-pic"
            />
          </div>
          <h1>Bienvenido, {user.email}!</h1>
          <p className="user-id">ID: {user.id}</p>
        </div>
        <div className="perfil-actions">
          <button className="edit-profile-button">Editar Perfil</button>
          <Logout />
        </div>
      </div>
    </PrivatePage>
  );
};

export default Private;
