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
      <button
        className="stylesAcess border-info p-3 my-5 rounded-pill"
        onClick={handleLoginRedirect}
      >
        <h5>Create account</h5>
      </button>
    </div>
  );
};
