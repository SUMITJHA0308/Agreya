import { useEffect, useState } from "react";

import { getWorkers } from "../../services/workerService";

import WorkerTable from "../../components/workers/WorkerTable";
import WorkerDetails from "./WorkerDetails";

import workerMockData from "../../data/workerMockData";

function WorkerDashboard() {
  const [workers, setWorkers] = useState([]);
  const [selectedWorker, setSelectedWorker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    async function loadWorkers() {
      try {
        const data = await getWorkers();

        const normalizedWorkers = data.map((worker) => ({
          ...worker,

          current_seen_node:
            worker.current_seen_node ||
            worker.last_node_id ||
            "Unknown",

          last_seen_node:
            worker.last_seen_node ||
            worker.last_node_id ||
            "Unknown",
        }));

        setWorkers(normalizedWorkers);
      } catch (error) {
        console.warn(
          "Backend unavailable. Using mock worker data.",
          error
        );

        const normalizedMockWorkers =
          workerMockData.map((worker) => ({
            ...worker,

            current_seen_node:
              worker.current_seen_node ||
              worker.location?.node_id ||
              worker.last_node_id ||
              "Unknown",

            last_seen_node:
              worker.last_seen_node ||
              worker.last_node_id ||
              worker.location?.node_id ||
              "Unknown",
          }));

        setWorkers(normalizedMockWorkers);
      } finally {
        setLoading(false);
      }
    }

    loadWorkers();
  }, []);

  function handleViewDetails(workerId) {
    const worker = workers.find(
      (item) => item.worker_id === workerId
    );

    setSelectedWorker(worker || null);
  }

  function handleBackToWorkers() {
    setSelectedWorker(null);
  }

  if (loading) {
    return (
      <div className="worker-page">
        <div className="worker-loading">
          <div className="loading-spinner"></div>
          <h2>Loading Worker Dashboard...</h2>
          <p>Fetching worker information.</p>
        </div>
      </div>
    );
  }

  if (selectedWorker) {
    return (
      <WorkerDetails
        worker={selectedWorker}
        helmet={selectedWorker.helmet}
        location={
          selectedWorker.location || {
            last_node:
              selectedWorker.current_seen_node ||
              selectedWorker.last_node_id,
            last_seen:
              selectedWorker.last_seen,
            last_seen_node:
              selectedWorker.last_seen_node ||
              selectedWorker.last_node_id,
          }
        }
        alert={
          selectedWorker.sos?.active
            ? {
                alert_type: "SOS",
                severity: "HIGH",
                message:
                  selectedWorker.sos.message,
                resolved: "NO",
              }
            : null
        }
        onBack={handleBackToWorkers}
      />
    );
  }

  const activeWorkers = workers.filter(
    (worker) =>
      worker.status === "Active" ||
      worker.status === "ACTIVE"
  ).length;

  const inactiveWorkers =
    workers.length - activeWorkers;

  const emergencyWorkers = workers.filter(
    (worker) => worker.sos?.active
  ).length;

  return (
    <div className="worker-page">
      <header className="worker-dashboard-header">
        <div>
          <p className="dashboard-label">
            WORKER SAFETY & MONITORING
          </p>

          <h1>Worker Dashboard</h1>

          <p className="dashboard-description">
            Monitor worker status, helmet connectivity,
            current location and emergency conditions
            in real time.
          </p>
        </div>

        <div className="dashboard-live-status">
          <span className="live-dot"></span>
          Live Monitoring
        </div>
      </header>

      <section className="worker-summary">
        <div className="summary-card">
          <div className="summary-card-label">
            TOTAL WORKERS
          </div>

          <div className="summary-card-value">
            {workers.length}
          </div>

          <div className="summary-card-description">
            Registered workers
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-card-label">
            ACTIVE WORKERS
          </div>

          <div className="summary-card-value">
            {activeWorkers}
          </div>

          <div className="summary-card-description">
            Currently active
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-card-label">
            INACTIVE WORKERS
          </div>

          <div className="summary-card-value">
            {inactiveWorkers}
          </div>

          <div className="summary-card-description">
            Not currently active
          </div>
        </div>

        <div className="summary-card summary-card-alert">
          <div className="summary-card-label">
            ACTIVE SOS
          </div>

          <div className="summary-card-value">
            {emergencyWorkers}
          </div>

          <div className="summary-card-description">
            Emergency alerts
          </div>
        </div>
      </section>

      <main className="worker-main-content">
        <WorkerTable
          workers={workers}
          onViewDetails={handleViewDetails}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
        />
      </main>
    </div>
  );
}

export default WorkerDashboard;