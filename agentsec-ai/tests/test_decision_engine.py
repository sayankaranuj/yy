from backend.core.decision_engine import DecisionEngine


def test_decision_engine_static_action():
    de = DecisionEngine()

    de.register_rule(lambda ctx: "recon-only" in (ctx.get("target") or ""), ["workers.recon.run", "workers.report.run"]) 
    action = de.decide({"target": "recon-only-example.com"})
    assert action == ["workers.recon.run", "workers.report.run"]


def test_decision_engine_callable_action():
    de = DecisionEngine()

    def action_fn(ctx):
        if ctx.get("priority") == "high":
            return ["workers.vuln.run", "workers.report.run"]
        return ["workers.recon.run", "workers.report.run"]

    de.register_rule(lambda ctx: True, action_fn)
    assert de.decide({"priority": "high"}) == ["workers.vuln.run", "workers.report.run"]
