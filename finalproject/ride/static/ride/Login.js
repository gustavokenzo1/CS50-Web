function Login() {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (email && password) {
      fetch("/login", {
        method: "POST",
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            window.location.href = "/";
          }
        })
        .catch((error) => {
          alert(error);
        });
    }
  };

  return (
    <div className="container">
      <h1 className="title">Login</h1>
      <form>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input
            onChange={(e) => setEmail(e.target.value)}
            value={email}
            autoComplete="off"
            type="email"
            name="email"
            id="email"
          />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            onChange={(e) => setPassword(e.target.value)}
            value={password}
            autoComplete="off"
            type="password"
            name="password"
            id="password"
          />
        </div>
        <div className="field">
          <button onClick={handleSubmit} type="submit">
            Login
          </button>
        </div>
      </form>
    </div>
  );
}
