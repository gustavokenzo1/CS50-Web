function Ride() {
  const [rides, setRides] = React.useState([]);

  React.useEffect(() => {
    fetch("/get_rides")
      .then((res) => res.json())
      .then((data) => setRides(data));
  }, []);

  return (
    <div className="container">
      <h1 style={{ marginTop: "2rem" }}>Ride</h1>
      <a style={{ marginTop: "2rem" }} href="/rides/new">
        <button>Offer a Ride</button>
      </a>
      <a style={{ marginTop: "2rem" }} href="/rides/personal">
        <button>My Rides</button>
      </a>
      <div className="rides">
        <h2>Available Rides</h2>
        <ul>
          {rides.map((ride) => {
            return (
              <li key={ride.id}>
                <div className="item">
                  <div>Departure:</div> {ride.departure}
                </div>
                <div className="item">
                  <div>Destination:</div> {ride.destination}
                </div>
                <div className="item">
                  <div>Schedule:</div> {ride.schedule}
                </div>
                <div className="item">
                  <div>Seats:</div> {ride.seats}
                </div>
                <div className="item">
                  <div>Price:</div> {ride.price}
                </div>
                <div className="item">
                  <div>Driver:</div> {ride.driver}
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
