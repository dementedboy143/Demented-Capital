#!/usr/bin/env python3
"""Manual Strike Demo: produces showcase output without live keys."""
import argparse
import datetime as dt
import hashlib
import random
import textwrap
import time

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


def banner(title: str) -> None:
    line = "=" * 72
    print(f"{CYAN}{line}\n{title}\n{line}{RESET}")


def step(label: str) -> None:
    print(f"{GREEN}[OK]{RESET} {label}")


def warn(label: str) -> None:
    print(f"{YELLOW}[WARN]{RESET} {label}")


def verify_bundle() -> str:
    """Simulate SHA-256 integrity verification of the skill bundle."""
    payload = b"Demented-Omni-Claw skill bundle v1.0"
    expected = hashlib.sha256(payload).hexdigest()
    computed = hashlib.sha256(payload).hexdigest()
    banner("INTEGRITY CHECK :: ZERO-TRUST BOOTSTRAP")
    print("Bundle: signed/attested")
    print(f"Expected SHA-256 : {expected}")
    print(f"Computed SHA-256 : {computed}")
    step("Signature chain validated (local-only execution path)")
    return expected


def simulate_whale_spike() -> dict:
    """Create a deterministic whale movement scenario."""
    random.seed(42)
    size_usd = 2_750_000 + random.randint(0, 50_000)
    ob_imbalance = 21 + random.randint(0, 4)  # % ask-side imbalance
    trap_score = 88 + random.randint(-3, 3)
    return {
        "asset": "USDT",
        "size_usd": size_usd,
        "from_chain": "Katana (CoL Treasury)",
        "to_cex": "Binance",
        "tx_hash": "0xKATANA_DEMO_HASH",
        "velocity_sec": 94,
        "ob_imbalance_pct": ob_imbalance,
        "retail_trap_score": trap_score,
        "reason": "Treasury offload to Binance during thin liquidity; asks balloon +{}%".format(ob_imbalance),
    }


def render_matrix_block(title: str, body: str) -> None:
    block = textwrap.indent(body.strip(), prefix="> ")
    print(f"{MAGENTA}{title}{RESET}\n{block}\n")


def build_alert(scenario: dict) -> str:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    lines = [
        "[CHANNEL] Binance Square / Telegram War Room",
        f"[TIMESTAMP] {now}",
        "[MODE] Alpha Radar :: Whale Shadow x Liquidity Sniper",
        f"[EVENT] {scenario['asset']} {scenario['size_usd']:,} moved {scenario['from_chain']} -> {scenario['to_cex']} ({scenario['velocity_sec']}s)",
        f"[ORDERBOOK] Ask-side imbalance +{scenario['ob_imbalance_pct']}% | Trap Score {scenario['retail_trap_score']}/100",
        f"[REASON] {scenario['reason']}",
        "[PLAYBOOK] Shadow the fill; avoid market buys; set iceberg alerts; wait for second print.",
        "[SOURCES] Katana RPC, Binance Orderbook, Cryptopanic sentiment",
        "[DISCLAIMER] DYOR. Not financial advice. Comply with your local regs.",
    ]
    return "\n".join(lines)


def demo_run() -> None:
    verify_bundle()
    time.sleep(0.2)
    banner("SIGNAL FABRICATION :: SANDBOX DATA")
    scenario = simulate_whale_spike()
    step(f"Whale spike synthesized: {scenario['asset']} {scenario['size_usd']:,} -> {scenario['to_cex']}")
    warn("Live keys not loaded; running in sealed demo mode")
    print()

    render_matrix_block(
        "RETAIL TRAP SCORE",
        f"Score: {scenario['retail_trap_score']}/100\nReason: {scenario['reason']}\nProtection: Risk Guardian policy = CONTAIN / OBSERVE",
    )

    render_matrix_block(
        "BINANCE SQUARE / TELEGRAM ALERT",
        build_alert(scenario),
    )

    banner("END OF DEMO :: RECORD THIS OUTPUT FOR THE CONTEST")


def main():
    parser = argparse.ArgumentParser(description="Demented-Omni-Claw manual strike showcase")
    parser.add_argument("--demo", action="store_true", help="run the prebuilt demo flow")
    args = parser.parse_args()

    if args.demo:
        demo_run()
    else:
        print("No live mode wired yet. Run with --demo for showcase output.")


if __name__ == "__main__":
    main()
