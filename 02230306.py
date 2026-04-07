
def get_processes(include_priority=False):
    n = int(input("Enter the number of processes: "))
    processes = []
    for i in range(n):
        pid = input(f"  Process ID (e.g. P{i+1}): ").strip()
        at  = int(input(f"  Arrival Time for {pid}: "))
        bt  = int(input(f"  Burst Time  for {pid}: "))
        pr  = None
        if include_priority:
            pr = int(input(f"  Priority for {pid} (lower number = higher priority): "))
        processes.append({"pid": pid, "at": at, "bt": bt, "pr": pr})
    return processes


def print_results(title, results, schedule_seq=None):
    print(f"\n{'='*60}")
    print(f"  {title} Results")
    print(f"{'='*60}")

    print(f"\n{'PID':<8}{'AT':<6}{'BT':<6}{'CT':<6}{'TAT':<8}{'WT':<6}")
    print("-" * 40)

    total_tat = total_wt = 0
    last_ct = first_at = None

    for r in results:
        tat = r["ct"] - r["at"]
        wt  = tat - r["bt"]
        total_tat += tat
        total_wt  += wt
        print(f"{r['pid']:<8}{r['at']:<6}{r['bt']:<6}{r['ct']:<6}{tat:<8}{wt:<6}")
        if last_ct is None or r["ct"] > last_ct:
            last_ct = r["ct"]
        if first_at is None or r["at"] < first_at:
            first_at = r["at"]

    n = len(results)
    avg_tat    = total_tat / n
    avg_wt     = total_wt  / n
    sched_len  = last_ct - first_at
    throughput = n / sched_len

    print("-" * 40)
    print(f"{'':>8}{'':>6}{'':>6}{'':>6}{total_tat:<8}{total_wt:<6}")
    print(f"\nSchedule Length : {sched_len} time units")
    print(f"Throughput       : {throughput:.4f} processes per time unit")
    print(f"Average TAT      : {avg_tat:.2f}ms")
    print(f"Average WT       : {avg_wt:.2f}ms")
    print(f"{'='*60}\n")


# ──────────────────────────────────────────────────────────
# 1. FIRST COME FIRST SERVE (FCFS)
# ──────────────────────────────────────────────────────────
def fcfs(processes):
    procs = sorted(processes, key=lambda p: (p["at"], p["pid"]))
    time  = 0
    results = []
    seq_pids  = []
    seq_times = []

    for p in procs:
        start = max(time, p["at"])
        seq_times.append(start)
        seq_pids.append(p["pid"])
        ct = start + p["bt"]
        time = ct
        results.append({"pid": p["pid"], "at": p["at"], "bt": p["bt"], "ct": ct})

    seq_times.append(time)
    print_results("First Come First Serve (FCFS)",
                  results,
                  {"pids": seq_pids, "times": seq_times})


# ──────────────────────────────────────────────────────────
# 2. SHORTEST JOB FIRST – NON-PREEMPTIVE (SJF)
# ──────────────────────────────────────────────────────────
def sjf_non_preemptive(processes):
    remaining = sorted(processes, key=lambda p: p["at"])
    time      = 0
    results   = []
    seq_pids  = []
    seq_times = []
    done      = set()

    while len(done) < len(remaining):
        available = [p for p in remaining
                     if p["at"] <= time and p["pid"] not in done]

        if not available:
            # CPU idle – jump to next arrival
            time = min(p["at"] for p in remaining if p["pid"] not in done)
            continue

        # Pick shortest burst; break ties by arrival time then pid
        chosen = min(available, key=lambda p: (p["bt"], p["at"], p["pid"]))
        seq_times.append(time)
        seq_pids.append(chosen["pid"])
        ct   = time + chosen["bt"]
        time = ct
        done.add(chosen["pid"])
        results.append({"pid": chosen["pid"],
                        "at":  chosen["at"],
                        "bt":  chosen["bt"],
                        "ct":  ct})

    seq_times.append(time)
    print_results("Shortest Job First – Non-Preemptive (SJF)",
                  results,
                  {"pids": seq_pids, "times": seq_times})


# ──────────────────────────────────────────────────────────
# 3. PRIORITY SCHEDULING
# ──────────────────────────────────────────────────────────
def priority_scheduling(processes):
    remaining = sorted(processes, key=lambda p: p["at"])
    time      = 0
    results   = []
    done      = set()

    while len(done) < len(remaining):
        available = [p for p in remaining
                     if p["at"] <= time and p["pid"] not in done]

        if not available:
            time = min(p["at"] for p in remaining if p["pid"] not in done)
            continue

        chosen = min(available, key=lambda p: (p["pr"], p["at"], p["bt"], p["pid"]))
        ct   = time + chosen["bt"]
        time = ct
        done.add(chosen["pid"])
        results.append({"pid": chosen["pid"],
                        "at":  chosen["at"],
                        "bt":  chosen["bt"],
                        "ct":  ct})

    print_results("Priority Scheduling – Non-Preemptive", results)


# ──────────────────────────────────────────────────────────
# MAIN MENU
# ──────────────────────────────────────────────────────────
def main():
    print("\n" + "="*60)
    print("         CTE205 – CPU Scheduling")
    print("         Student ID : 02230306")
    print("="*60)
    print("  1. First Come First Serve  (FCFS)")
    print("  2. Shortest Job First      (SJF – Non-Preemptive)")
    print("  3. Priority Scheduling     (Non-Preemptive)")
    print("="*60)

    choice = input("\nSelect a scheduling algorithm (1-3): ").strip()

    if choice == "1":
        procs = get_processes()
        fcfs(procs)

    elif choice == "2":
        procs = get_processes()
        sjf_non_preemptive(procs)

    elif choice == "3":
        procs = get_processes(include_priority=True)
        priority_scheduling(procs)

    else:
        print("Invalid choice. Please run again and select 1–3.")


if __name__ == "__main__":
    main()