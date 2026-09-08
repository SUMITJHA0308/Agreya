import WorkerStatus from "../../components/workers/WorkerStatus";
import HelmetStatus from "../../components/workers/HelmetStatus";
import WorkerLocation from "../../components/workers/WorkerLocation";
import SOSAlert from "../../components/workers/SOSAlert";

function WorkerDetails({
  worker,
  helmet,
  location,
  alert,
  onBack,
}) {
  if (!worker) {
    return (
      <div className="worker-page">
        <div className="worker-not-found">
          <h2>Worker Not Found</h2>

          <button onClick={onBack}>
            ← Back to Workers
          </button>
        </div>
      </div>
    );
  }

  const currentSeenNode =
    worker.current_seen_node ||
    location?.node_id ||
    location?.last_node ||
    worker.last_node_id ||
    "Unknown";

  const lastSeenNode =
    worker.last_seen_node ||
    location?.last_seen_node ||
    worker.last_node_id ||
    "Unknown";

  const lastSeen =
    worker.last_seen ||
    location?.last_seen ||
    "Unknown";

  return (
    <div className="worker-page">
      <div className="worker-details-page">
        <button
          className="back-button"
          onClick={onBack}
        >
          ← Back to Workers
        </button>

        <div className="worker-details-header">
          <div>
            <p className="dashboard-label">
              WORKER PROFILE
            </p>

            <h1>{worker.name}</h1>

            <p className="worker-details-id">
              Worker ID: {worker.worker_id}
            </p>
          </div>

          <WorkerStatus
            status={worker.status}
          />
        </div>

        <section className="details-grid">
          <div className="worker-detail-section">
            <div className="detail-section-title">
              <h2>Worker Information</h2>
            </div>

            <div className="detail-list">
              <div className="detail-item">
                <span>Worker ID</span>
                <strong>
                  {worker.worker_id}
                </strong>
              </div>

              <div className="detail-item">
                <span>Name</span>
                <strong>
                  {worker.name}
                </strong>
              </div>

              <div className="detail-item">
                <span>Status</span>
                <WorkerStatus
                  status={worker.status}
                />
              </div>

              <div className="detail-item">
                <span>Helmet ID</span>
                <strong>
                  {worker.helmet_id ||
                    "Not assigned"}
                </strong>
              </div>
            </div>
          </div>

          <div className="worker-detail-section">
            <div className="detail-section-title">
              <h2>Location Information</h2>
            </div>

            <div className="location-highlight">
              <span>Current Seen Node</span>

              <strong>
                {currentSeenNode}
              </strong>
            </div>

            <div className="detail-list">
              <div className="detail-item">
                <span>Current Seen Node</span>
                <strong>
                  {currentSeenNode}
                </strong>
              </div>

              <div className="detail-item">
                <span>Last Seen Node</span>
                <strong>
                  {lastSeenNode}
                </strong>
              </div>

              <div className="detail-item">
                <span>Last Seen</span>
                <strong>
                  {lastSeen !== "Unknown"
                    ? new Date(
                        lastSeen
                      ).toLocaleString()
                    : "Unknown"}
                </strong>
              </div>
            </div>
          </div>

          <div className="worker-detail-section">
            <HelmetStatus
              helmet={helmet}
            />
          </div>

          <div className="worker-detail-section">
            <SOSAlert alert={alert} />
          </div>
        </section>
      </div>
    </div>
  );
}

export default WorkerDetails;