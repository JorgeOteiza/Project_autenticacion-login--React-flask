import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import "../../styles/home.css";

export const Home = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();

  const handleLoginRedirect = () => {
    navigate("/login");
  };

  return (
    <div className="text-center my-5 py-5">
      <img
        src="https://blog.orange.es/wp-content/uploads/2019/06/Login.png"
        alt="Login"
        style={{ width: "60%", height: "30%" }}
      />
    </div>
  );
};
