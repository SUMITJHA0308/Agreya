import WorkerStatus from "./WorkerStatus";

function WorkerTable({
  workers,
  onViewDetails,
  searchTerm,
  onSearchChange,
}) {
  const filteredWorkers = workers.filter((worker) => {
    const search = searchTerm.toLowerCase().trim();

    if (!search) {
      return true;
    }

    return (
      worker.worker_id?.toLowerCase().includes(search) ||
      worker.name?.toLowerCase().includes(search) ||
      worker.helmet_id?.toLowerCase().includes(search) ||
      worker.last_node_id?.toLowerCase().includes(search)
    );
  });

  return (
    <div className="worker-table-container">
      <div className="worker-table-header">
        <div>
          <h2>Worker Monitoring</h2>
          <p>
            {filteredWorkers.length} of {workers.length} workers shown
          </p>
        </div>

        <div className="worker-search">
          <input
            type="text"
            placeholder="Search Worker ID, name, helmet..."
            value={searchTerm}
            onChange={(event) =>
              onSearchChange(event.target.value)
            }
          />
        </div>
      </div>

      {filteredWorkers.length === 0 ? (
        <div className="empty-workers">
          <h3>No workers found</h3>
          <p>
            Try searching with another Worker ID or name.
          </p>
        </div>
      ) : (
        <div className="worker-table-wrapper">
          <table className="worker-table">
            <thead>
              <tr>
                <th>Worker ID</th>
                <th>Name</th>
                <th>Status</th>
                <th>Helmet ID</th>
                <th>Current Seen Node</th>
                <th>Last Seen Node</th>
                <th>Last Seen</th>
              </tr>
            </thead>

            <tbody>
              {filteredWorkers.map((worker) => (
                <tr
                  key={worker.worker_id}
                  onClick={() =>
                    onViewDetails(worker.worker_id)
                  }
                  className="worker-table-row"
                >
                  <td>
                    <button
                      className="worker-id-button"
                      onClick={(event) => {
                        event.stopPropagation();
                        onViewDetails(worker.worker_id);
                      }}
                    >
                      {worker.worker_id}
                    </button>
                  </td>

                  <td>
                    <strong>{worker.name}</strong>
                  </td>

                  <td>
                    <WorkerStatus
                      status={worker.status}
                    />
                  </td>

                  <td>
                    {worker.helmet_id || "N/A"}
                  </td>

                  <td>
                    {worker.current_seen_node ||
                      worker.last_node_id ||
                      "Unknown"}
                  </td>

                  <td>
                    {worker.last_seen_node ||
                      worker.last_node_id ||
                      "Unknown"}
                  </td>

                  <td>
                    {worker.last_seen
                      ? new Date(
                          worker.last_seen
                        ).toLocaleString()
                      : "Unknown"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <p className="worker-table-hint">
        Click a Worker ID or any row to view complete worker details.
      </p>
    </div>
  );
}

export default WorkerTable;