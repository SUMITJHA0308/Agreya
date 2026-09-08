function WorkerStatus({ status }) {
  const isSafe =
    status === "SAFE" ||
    status === "Active" ||
    status === "ACTIVE";

  return (
    <span
      className={`worker-status ${
        isSafe
          ? "worker-status-safe"
          : "worker-status-warning"
      }`}
    >
      {status || "UNKNOWN"}
    </span>
  );
}

export default WorkerStatus;