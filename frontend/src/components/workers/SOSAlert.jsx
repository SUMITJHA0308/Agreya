function SOSAlert({ alert }) {
  if (!alert) {
    return (
      <div className="sos-alert sos-safe">
        <strong>Emergency Status</strong>
        <p>No active emergency alert.</p>
      </div>
    );
  }

  const isResolved =
    alert.resolved === "YES" ||
    alert.resolved === true;

  return (
    <div
      className={`sos-alert ${
        isResolved
          ? "sos-resolved"
          : "sos-active"
      }`}
    >
      <strong>
        {isResolved
          ? "Emergency Resolved"
          : "🚨 EMERGENCY ALERT"}
      </strong>

      <p>
        Type: {alert.alert_type || "Unknown"}
      </p>

      <p>
        Severity: {alert.severity || "Unknown"}
      </p>

      <p>
        {alert.message ||
          "No message available"}
      </p>

      <small>
        {alert.timestamp
          ? new Date(
              alert.timestamp
            ).toLocaleString()
          : ""}
      </small>
    </div>
  );
}

export default SOSAlert;