import React from "react";
import ReactDOM from "react-dom";
import ManejoError from "./component/manejoError.jsx";

//include your index.scss file into the bundle
import "../styles/index.css";

//import your own components
import Layout from "./layout";

// Renderiza la aplicación dentro del componente de manejo de errores
ReactDOM.render(
    <ManejoError>
      <Layout />
    </ManejoError>,
    document.getElementById("app")
  );
