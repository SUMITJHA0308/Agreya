function HelmetStatus({ helmet }) {
  if (!helmet) {
    return (
      <div className="helmet-status">
        <strong>Helmet</strong>
        <p>No helmet information</p>
      </div>
    );
  }

  return (
    <div className="helmet-status">
      <strong>
        Helmet: {helmet.helmet_id || "N/A"}
      </strong>

      <p>
        Status: {helmet.status || "UNKNOWN"}
      </p>

      <p>
        Battery: {helmet.battery ?? "N/A"}%
      </p>
    </div>
  );
}

export default HelmetStatus;