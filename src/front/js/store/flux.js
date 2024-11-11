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
      user: null,
    },
    actions: {
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      // Fetches a message from the backend
      getMessage: async () => {
        try {
          const resp = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/hello`, {
            method: "GET",
            mode: "cors",
            credentials: "include",
            headers: { "Content-Type": "application/json" }
          });
          if (!resp.ok) throw new Error("Failed to fetch message from backend");
          const data = await resp.json();
          setStore({ message: data.message });
        } catch (error) {
          console.error("Error loading message from backend", error);
        }
      },

      // Changes color of a specific demo item
      changeColor: (index, color) => {
        const store = getStore();
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });
        setStore({ demo });
      },

      // Fetches the user profile by ID
      getUserProfile: async (id) => {
        try {
          const token = sessionStorage.getItem("token");
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/users/${id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json"
            }
          });
          if (!response.ok) throw new Error("Error fetching user profile");
          const data = await response.json();
          return data;
        } catch (error) {
          console.error("Error loading user profile:", error);
          return null;
        }
      },

      // Logs in the user
      login: async (email, password) => {
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/login`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            mode: "cors",
            credentials: "include",
            body: JSON.stringify({ email, password })
          });
          if (!response.ok) throw new Error("Login failed");

          const data = await response.json();
          sessionStorage.setItem("token", data.token);
          sessionStorage.setItem("userId", data.user.id);
          setStore({ user: data.user });
          
          return true;
        } catch (error) {
          console.error("Login error:", error);
          return false;
        }
      },

      // Registers a new user
      signup: async (email, password) => {
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/signup`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
            credentials: "include"
          });
          if (!response.ok) throw new Error("Signup failed");

          const data = await response.json();
          sessionStorage.setItem("token", data.token);
          sessionStorage.setItem("userId", data.user.id);
          setStore({ user: data.user });
          return true;
        } catch (error) {
          console.error("Signup error:", error);
          return false;
        }
      },

      // Logs out the user
      logout: () => {
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("userId");
        setStore({ user: null });
      }
    },
  };
};

export default getState;
