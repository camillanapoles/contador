"""Roteador determinista de eventos: evento -> acao. Zero LLM."""
import time


def apply(c, etype, p):
    if etype == "run.finished":
        proj, sid = p["project"], p["stage"]
        tests = p.get("tests", [])
        verdict_ok = p.get("verdict") == "success"
        all_passed = len(tests) > 0 and all(t.get("passed") for t in tests)
        for t in tests:
            c.execute(
                "INSERT INTO test_results(project,stage,test_id,passed,evidence,ts)"
                " VALUES(?,?,?,?,?,?)",
                (proj, sid, t.get("test_id", "?"), 1 if t.get("passed") else 0,
                 t.get("evidence", ""), time.time()))
        report = p.get("report")
        if report:
            c.execute("UPDATE stages SET report=? WHERE project=? AND id=?",
                      (report, proj, sid))
        gate = verdict_ok and all_passed and bool(report)
        status = "done" if gate else "failed"
        c.execute("UPDATE stages SET status=?, last_run=?, last_verdict=?, updated=?"
                  " WHERE project=? AND id=?",
                  (status, str(p.get("run_id", "")), p.get("verdict", ""),
                   time.time(), proj, sid))
        nxt = _next(c, proj, sid)
        unlocked = None
        if gate and nxt:
            c.execute("UPDATE stages SET status='ready', updated=?"
                      " WHERE project=? AND id=?", (time.time(), proj, nxt))
            unlocked = nxt
        return {"event": etype, "stage": sid, "gate_passed": gate,
                "status": status, "unlocked": unlocked,
                "tests_recorded": len(tests)}
    if etype == "stage.override":
        c.execute("UPDATE stages SET status=?, updated=? WHERE project=? AND id=?",
                  (p["status"], time.time(), p["project"], p["stage"]))
        return {"event": etype, "stage": p["stage"], "status": p["status"]}
    if etype == "stage.failed":
        c.execute("UPDATE stages SET status='failed', updated=? WHERE project=? AND id=?",
                  (time.time(), p["project"], p["stage"]))
        return {"event": etype, "stage": p["stage"], "status": "failed"}
    return {"event": etype, "result": "unknown-event-type"}


def _next(c, proj, sid):
    rows = c.execute("SELECT id FROM stages WHERE project=? ORDER BY rowid",
                     (proj,)).fetchall()
    ids = [r["id"] for r in rows]
    if sid in ids:
        i = ids.index(sid)
        if i + 1 < len(ids):
            return ids[i + 1]
    return None
