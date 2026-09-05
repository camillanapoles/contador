import json
import os
import sqlite3
import time

from fastapi import FastAPI, HTTPException

import events
from models import Event, Project

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gov.db")
app = FastAPI(title="apk-factory gov", version="2.0")


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    c = conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS projects(
      name TEXT PRIMARY KEY, repo TEXT, created REAL);
    CREATE TABLE IF NOT EXISTS stages(
      project TEXT, id TEXT, name TEXT, objetivo TEXT, entregavel TEXT,
      requisito TEXT, stack TEXT, ucs TEXT, tests TEXT,
      status TEXT DEFAULT 'blocked', report TEXT, last_run TEXT,
      last_verdict TEXT, updated REAL,
      PRIMARY KEY(project, id));
    CREATE TABLE IF NOT EXISTS test_results(
      project TEXT, stage TEXT, test_id TEXT, passed INTEGER,
      evidence TEXT, ts REAL);
    CREATE TABLE IF NOT EXISTS events(
      id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL, type TEXT,
      payload TEXT, result TEXT);
    """)
    c.commit()
    c.close()


init_db()


@app.get("/health")
def health():
    return {"ok": True, "db": os.path.basename(DB), "ts": time.time()}


@app.post("/projects")
def create_project(p: Project):
    c = conn()
    c.execute("INSERT OR REPLACE INTO projects VALUES(?,?,?)",
              (p.name, p.repo, time.time()))
    for s in p.stages:
        c.execute(
            "INSERT OR REPLACE INTO stages(project,id,name,objetivo,entregavel,"
            "requisito,stack,ucs,tests,status,updated) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (p.name, s.id, s.name, s.objetivo, s.entregavel, s.requisito,
             s.stack, s.ucs, json.dumps(s.tests), s.status, time.time()))
    c.commit()
    c.close()
    return {"project": p.name, "stages": len(p.stages)}


@app.get("/projects")
def list_projects():
    c = conn()
    rows = [dict(r) for r in c.execute("SELECT * FROM projects").fetchall()]
    c.close()
    return rows


@app.get("/projects/{name}")
def get_project(name: str):
    c = conn()
    p = c.execute("SELECT * FROM projects WHERE name=?", (name,)).fetchone()
    if not p:
        c.close()
        raise HTTPException(404, "project not found")
    st = [dict(r) for r in c.execute(
        "SELECT * FROM stages WHERE project=? ORDER BY rowid", (name,)).fetchall()]
    c.close()
    d = dict(p)
    d["stages"] = st
    return d


@app.post("/events")
def post_event(ev: Event):
    c = conn()
    res = events.apply(c, ev.type, ev.payload)
    c.execute("INSERT INTO events(ts,type,payload,result) VALUES(?,?,?,?)",
              (time.time(), ev.type, ev.payload_json(),
               json.dumps(res, ensure_ascii=False, default=str)))
    c.commit()
    c.close()
    return res
