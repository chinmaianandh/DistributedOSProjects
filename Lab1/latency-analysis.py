import argparse
import glob
import os
import matplotlib.pyplot as plt
import pandas as pd
 
# Number of initial requests to discard per client.
# The first few calls include channel setup and lazy imports, so they are
# not representative of steady-state latency.
WARMUP = 20
 
 
def load_all(results_dir):
    """Read every CSV in results_dir and concatenate into one DataFrame."""
    files = sorted(glob.glob(os.path.join(results_dir, "*.csv")))
    if not files:
        raise SystemExit(f"No CSV files found in {results_dir}")
 
    frames = []
    for f in files:
        d = pd.read_csv(f)
        # Keep the source filename around - useful when debugging odd numbers.
        d["source_file"] = os.path.basename(f)
        frames.append(d)
        print(f"loaded {os.path.basename(f):40s} rows={len(d)}")
 
    return pd.concat(frames, ignore_index=True)
 
 
def clean(df):
    """Drop warmup requests and any obviously broken rows."""
    # cumcount() numbers rows 0,1,2... within each group, in file order.
    # This assumes rows were appended chronologically, which they are.
    df["req_idx"] = df.groupby(["client", "method"]).cumcount()
 
    before = len(df)
    df = df[df["req_idx"] >= WARMUP]
    print(f"dropped {before - len(df)} warmup rows ({WARMUP} per client/method)")
 
    # Sanity filter: negative or absurd latencies mean something went wrong.
    df = df[(df["latency(ms)"] > 0) & (df["latency(ms)"] < 60)]
 
    return df
 
 
def summarise(df):
    """Per-method summary stats.
 
    Mean alone hides queueing - the tail (p95/p99) is where added load
    shows up first, so report percentiles too.
    """
    return (
        df.groupby("method")["latency(ms)"]
        .agg(
            count="count",
            mean="mean",
            p50=lambda s: s.quantile(0.50),
            p95=lambda s: s.quantile(0.95),
            p99=lambda s: s.quantile(0.99),
            max="max",
        )
        .reset_index()
    )
 
 
def plot_bar_by_method(summary, out_dir):
    """Bar chart comparing mean vs p95 latency across the three methods.
 
    This is the plot that answers Q3 (lookup vs trade): if your locking
    made writes more expensive than reads, it shows up here.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
 
    x = range(len(summary))
    width = 0.35
 
    ax.bar([i - width / 2 for i in x], summary["mean"], width, label="mean")
    ax.bar([i + width / 2 for i in x], summary["p95"], width, label="p95", alpha=0.7)
 
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["method"])
    ax.set_xlabel("gRPC method")
    ax.set_ylabel("latency (ms)")
    ax.set_title("Latency by method")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
 
    path = os.path.join(out_dir, "latency_by_method.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path}")
 
 
def plot_distributions(df, out_dir):
    """Overlaid histograms - shows the SHAPE of the latency distribution.
 
    A tight spike means the server is keeping up. A long right tail means
    requests are queueing behind busy workers. This is usually the most
    convincing single figure in a load-test report.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
 
    for method, g in df.groupby("method"):
        ax.hist(g["latency(ms)"], bins=50, alpha=0.5, label=method)
 
    ax.set_xlabel("latency (ms)")
    ax.set_ylabel("number of requests")
    ax.set_title("Latency distribution by method")
    ax.legend()
    ax.grid(alpha=0.3)
 
    path = os.path.join(out_dir, "latency_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path}")
 
 
def plot_over_time(df, out_dir):
    """Latency vs request index, one line per method.
 
    Useful for spotting drift: does latency creep up as trading volume
    approaches max_volume, or as the server accumulates state?
    """
    fig, ax = plt.subplots(figsize=(8, 5))
 
    for method, g in df.groupby("method"):
        # Rolling mean smooths out per-request noise so the trend is visible.
        g = g.sort_values("req_idx")
        smoothed = g["latency(ms)"].rolling(window=10, min_periods=1).mean()
        ax.plot(g["req_idx"], smoothed, label=method, alpha=0.8)
 
    ax.set_xlabel("request number")
    ax.set_ylabel("latency (ms, 10-request rolling mean)")
    ax.set_title("Latency over the course of the run")
    ax.legend()
    ax.grid(alpha=0.3)
 
    path = os.path.join(out_dir, "latency_over_time.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path}")
 
 
def main():
    parser = argparse.ArgumentParser(description="Analyse load test results")
    parser.add_argument("--results_dir", default="results")
    parser.add_argument("--out_dir", default="results/plots")
    args = parser.parse_args()
 
    os.makedirs(args.out_dir, exist_ok=True)
 
    df = load_all(args.results_dir)
    df = clean(df)
 
    summary = summarise(df)
    print("\n=== summary ===")
    print(summary.to_string(index=False))
 
    # Save the table too - you will want these exact numbers in the report.
    csv_path = os.path.join(args.out_dir, "summary.csv")
    summary.to_csv(csv_path, index=False)
    print(f"wrote {csv_path}\n")
 
    plot_bar_by_method(summary, args.out_dir)
    plot_distributions(df, args.out_dir)
    plot_over_time(df, args.out_dir)
 
 
if __name__ == "__main__":
    main()