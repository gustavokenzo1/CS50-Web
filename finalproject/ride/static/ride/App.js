function App() {
  return (
    <div className="container">
      <h1 className="title">Ride</h1>
      <h2 className="description">
        Help or get help to get to college with other students!
      </h2>
      <h3 style={{ marginBottom: "2rem" }}>A CS50 Web Final Project</h3>
      <div className="buttons">
        <button
          onClick={() => {
            window.location.href = "/login";
          }}
        >
          Login
        </button>
        <button
          onClick={() => {
            window.location.href = "/register";
          }}
        >
          Register
        </button>
      </div>
    </div>
  );
}
