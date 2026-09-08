function WorkerLocation({ location }) {
  if (!location) {
    return (
      <div className="worker-location">
        <strong>Location</strong>
        <p>No location information</p>
      </div>
    );
  }

  return (
    <div className="worker-location">
      <strong>Location</strong>

      <p>
        <strong>Current Seen Node:</strong>{" "}
        {location.current_seen_node ||
          "Unknown"}
      </p>

      <p>
        <strong>Last Seen Node:</strong>{" "}
        {location.last_seen_node ||
          "Unknown"}
      </p>

      <p>
        <strong>Last Seen:</strong>{" "}
        {location.last_seen
          ? new Date(
              location.last_seen
            ).toLocaleString()
          : "Unknown"}
      </p>
    </div>
  );
}

export default WorkerLocation;