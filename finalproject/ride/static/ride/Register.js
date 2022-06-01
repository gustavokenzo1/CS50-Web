function Register() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPassword, setConfirmPassword] = React.useState("");
  const [email, setEmail] = React.useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (password !== confirmPassword) {
      alert("Passwords do not match");
    }
  };

  return (
    <div className="container">
      <h1 className="title">Register</h1>
      <form>
        <div className="field">
          <label htmlFor="username">Username</label>
          <input
            onChange={(e) => setUsername(e.target.value)}
            value={username}
            autoComplete="off"
            type="text"
            name="username"
            id="username"
          />
        </div>
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
          <label htmlFor="password2">Confirm Password</label>
          <input
            onChange={(e) => setConfirmPassword(e.target.value)}
            value={confirmPassword}
            autoComplete="off"
            type="password"
            name="password2"
            id="password2"
          />
        </div>
        <div className="field">
          <button onClick={handleSubmit} type="submit">
            Register
          </button>
        </div>
      </form>
    </div>
  );
}
