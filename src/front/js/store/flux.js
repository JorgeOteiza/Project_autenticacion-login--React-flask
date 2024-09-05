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
      user: null, // Debo crear un lugar para almacenar el usuario*
    },
    actions: {
      // Use getActions to call a function within a function
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      getMessage: async () => {
        try {
          const resp = await fetch(
            `${process.env.REACT_APP_BACKEND_URL}/api/hello`
          );
          if (!resp.ok) {
            throw new Error("Failed to fetch message from backend");
          }
          const data = await resp.json();
          setStore({ message: data.message });
          return data;
        } catch (error) {
          console.error("Error loading message from backend", error);
        }
      },

      changeColor: (index, color) => {
        //get the store
        const store = getStore();

        //we have to loop the entire demo array to look for the respective index
        //and change its color
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });

        //reset the global store
        setStore({ demo: demo });
      },
      getUserProfile: async (id) => {
        try {
          const token = localStorage.getItem("token");
          const response = await fetch(
            `${process.env.REACT_APP_BACKEND_URL}/api/user/${id}`,
            {
              headers: {
                Authorization: `Bearer ${token}`, // Incluye el token en el encabezado
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

      // Nueva función de login
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
          localStorage.setItem("token", data.token); // Almacena el token en localStorage
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
