import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth";
import { api } from "../api";
import type { Debtor } from "../api";
import { DebtorChart } from "../components/Chart";

export function Debtors() {
  const { username, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [debtors, setDebtors] = useState<Debtor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchedRef = useRef(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    if (fetchedRef.current) return;
    fetchedRef.current = true;

    const fetchDebtors = async () => {
      try {
        const data = await api.getDebtors();
        setDebtors(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch debtors");
      } finally {
        setLoading(false);
      }
    };

    fetchDebtors();
  }, [isAuthenticated, navigate]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const totalDebt = debtors.reduce((sum, d) => sum + Math.abs(d.balance), 0);

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Bar Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {username}</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <main className="main-content">
        <section className="card">
          <h2>Debtors</h2>
          <p className="subtitle">Users with outstanding balances</p>

          {loading && <div className="loading">Loading...</div>}

          {error && <div className="error">{error}</div>}

          {!loading && !error && debtors.length === 0 && (
            <div className="empty">No debtors found. Everyone has paid up!</div>
          )}

          {!loading && !error && debtors.length > 0 && (
            <>
              <div className="summary">
                <div className="stat">
                  <span className="stat-value">{debtors.length}</span>
                  <span className="stat-label">Debtors</span>
                </div>
                <div className="stat">
                  <span className="stat-value">€{totalDebt.toFixed(2)}</span>
                  <span className="stat-label">Total Owed</span>
                </div>
              </div>
              <DebtorChart data={debtors} />
            </>
          )}
        </section>
      </main>
    </div>
  );
}
