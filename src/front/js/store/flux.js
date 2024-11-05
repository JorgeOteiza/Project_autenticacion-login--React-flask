const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      message: null,
      demo: [
        {
          title: "FIRST",
          background: "white",
          initial: "white",
        },
        {
          title: "SECOND",
          background: "white",
          initial: "white",
        },
      ],
      user: null, // Lugar para almacenar el usuario
    },
    actions: {
      // Ejemplo de función dentro de actions
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      // Función para obtener el mensaje del backend
      getMessage: async () => {
        try {
          const resp = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/hello`, {
            method: 'GET',
            mode: 'cors',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            }
          });
          if (!resp.ok) throw new Error("Failed to fetch message from backend");
          const data = await resp.json();
          setStore({ message: data.message });
        } catch (error) {
          console.error("Error loading message from backend", error);
        }
      },

      // Cambia el color de fondo de un elemento específico en demo
      changeColor: (index, color) => {
        const store = getStore();
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });
        setStore({ demo: demo });
      },

      // Obtiene el perfil de usuario por ID
      getUserProfile: async (id) => {
        try {
          const token = localStorage.getItem("token");
          const response = await fetch(
            `${process.env.REACT_APP_BACKEND_URL}/api/user/${id}`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          if (!response.ok) throw new Error("Error fetching user profile");
          const data = await response.json();
          return data;
        } catch (error) {
          console.error("Error loading user profile:", error);
          return null;
        }
      },

      // Inicia sesión del usuario
      login: async (email, password) => {
        try {
          const response = await fetch(
            `${process.env.REACT_APP_BACKEND_URL}/api/login`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ email, password }),
            }
          );

          if (!response.ok) {
            throw new Error("Login failed");
          }

          const data = await response.json();
          sessionStorage.setItem("token", data.token); // Almacena el token en sessionStorage
          sessionStorage.setItem("userId", data.user.id); // Almacena el userId en sessionStorage
          setStore({ user: data.user }); // Guarda el usuario en el store

          return true; // Login exitoso
        } catch (error) {
          console.error("Login error:", error);
          return false; // Error en el login
        }
      },
    },
  };
};

export default getState;
