import React, { Component } from "react";

class ManejoError extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ManejoError detectó un error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Algo salió mal, inténtalo más tarde</h1>;
    }

    return this.props.children;
  }
}

export default ManejoError;
