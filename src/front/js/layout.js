import React from "react";
import Admin from "./component/admin";
import ScrollToTop from "./component/scrollToTop";
import injectContext from "./store/appContext";
import Signup from "./component/Signup.jsx";
import LogIn from "./component/LogIn.jsx";
import Private from "./component/Private.jsx";
import Navbar from "./component/navbar";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { BackendURL } from "./component/backendURL.jsx";
import { Home } from "./pages/home";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import { Footer } from "./component/footer";

const Layout = () => {
  const basename = process.env.BASENAME || "";

  if (!process.env.REACT_APP_BACKEND_URL) return <BackendURL />;

  return (
    <div>
      <BrowserRouter basename={basename}>
        <ScrollToTop>
          <Navbar />
          <Routes>
            <Route element={<Home />} path="/" />
            <Route element={<Admin />} path="/admin" />
            <Route element={<Signup />} path="/signup" />
            <Route element={<LogIn />} path="/login" />
            <Route element={<Private />} path="/private/:id" />
            <Route element={<Demo />} path="/demo" />
            <Route element={<Single />} path="/single/:theid" />
            <Route element={<h1>Not found!</h1>} />
          </Routes>
          <Footer />
        </ScrollToTop>
      </BrowserRouter>
    </div>
  );
};

export default injectContext(Layout);
