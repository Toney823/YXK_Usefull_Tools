#!/usr/bin/env python3

import sys, os, re, shutil, tempfile, subprocess, argparse, multiprocessing as mp


parser = argparse.ArgumentParser(
    description="Calculate pairwise Identity and Similarity using EMBOSS Needle."
)
parser.add_argument("fasta", help="Input FASTA file")
parser.add_argument("ids", nargs="*", help="Two sequence IDs for single-pair mode")
parser.add_argument("--pairs", help="Two-column pair file for batch mode")
parser.add_argument("--threads", type=int, default=1, help="Number of processes for batch mode [default: 1]")
parser.add_argument("--tmpdir", default="./_Tmpp_", help="Temporary directory [default: ./_Tmpp_]")
parser.add_argument("--output", help="Output result file [default: stdout]")
args = parser.parse_args()

if args.pairs:
    if args.ids:
        parser.error("Do not specify sequence IDs together with --pairs.")
    if args.threads < 1:
        parser.error("--threads must be >= 1.")
else:
    if len(args.ids) != 2:
        parser.error("Single-pair mode requires exactly two sequence IDs.")
    if args.threads != 1:
        print("WARNING: --threads is ignored in single-pair mode.", file=sys.stderr)


def read_fasta(filename):
    sequences, current_id, seq = {}, None, []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    sequences[current_id] = "".join(seq)
                current_id, seq = line[1:].split()[0], []
            else:
                seq.append(line)
    if current_id is not None:
        sequences[current_id] = "".join(seq)
    return sequences


def read_pairs(filename):
    pairs = []
    with open(filename) as f:
        for line in f:
            fields = line.strip().split()
            if len(fields) >= 2 and not line.lstrip().startswith("#"):
                pairs.append((fields[0], fields[1]))
    return pairs


def compare_pair(id1, id2, sequences, tmpdir):
    if id1 not in sequences:
        return id1, id2, "NA", "NA", f"Missing sequence: {id1}"
    if id2 not in sequences:
        return id1, id2, "NA", "NA", f"Missing sequence: {id2}"

    pair_tmp = tempfile.mkdtemp(prefix="pair_", dir=tmpdir)
    fa1, fa2 = os.path.join(pair_tmp, "seq1.fa"), os.path.join(pair_tmp, "seq2.fa")
    needle_out = os.path.join(pair_tmp, "needle.txt")

    try:
        with open(fa1, "w") as f:
            f.write(f">{id1}\n{sequences[id1]}\n")
        with open(fa2, "w") as f:
            f.write(f">{id2}\n{sequences[id2]}\n")

        result = subprocess.run(
            ["needle", "-asequence", fa1, "-bsequence", fa2, "-auto",
             "-gapopen", "10", "-gapextend", "0.5", "-outfile", needle_out],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            return id1, id2, "NA", "NA", result.stderr.strip()

        with open(needle_out) as f:
            text = f.read()

        identity = re.search(r"#\s*Identity:\s+\d+/\d+\s+\(\s*([\d.]+)%\)", text)
        similarity = re.search(r"#\s*Similarity:\s+\d+/\d+\s+\(\s*([\d.]+)%\)", text)

        return (
            id1, id2,
            identity.group(1) if identity else "NA",
            similarity.group(1) if similarity else "NA",
            None
        )
    except Exception as e:
        return id1, id2, "NA", "NA", str(e)
    finally:
        shutil.rmtree(pair_tmp, ignore_errors=True)


def worker(task):
    chunk_id, pairs, sequences, tmpdir, chunk_dir = task
    chunk_file = os.path.join(chunk_dir, f"chunk_{chunk_id:04d}.tsv")

    with open(chunk_file, "w") as out:
        for i, (id1, id2) in enumerate(pairs, 1):
            result = compare_pair(id1, id2, sequences, tmpdir)
            out.write("\t".join(result[:4]) + "\n")
            if result[4]:
                print(
                    f"[Chunk {chunk_id}] {i}/{len(pairs)} "
                    f"{id1} <-> {id2}: {result[4]}",
                    file=sys.stderr, flush=True
                )

    print(f"[Chunk {chunk_id}] finished -> {chunk_file}", file=sys.stderr, flush=True)
    return chunk_file


def make_chunks(pairs, n):
    n = min(n, len(pairs))
    chunks = [[] for _ in range(n)]
    for i, pair in enumerate(pairs):
        chunks[i % n].append(pair)
    return chunks


def output_handle():
    return open(args.output, "w") if args.output else sys.stdout


sequences = read_fasta(args.fasta)
print(f"Sequences loaded: {len(sequences)}", file=sys.stderr)

os.makedirs(args.tmpdir, exist_ok=True)


# ============================================================
# Single-pair mode
# ============================================================

if not args.pairs:
    result = compare_pair(args.ids[0], args.ids[1], sequences, args.tmpdir)
    out = output_handle()
    try:
        print("ID1\tID2\tIdentity\tSimilarity", file=out)
        print("\t".join(result[:4]), file=out)
    finally:
        if args.output:
            out.close()
    if result[4]:
        print(f"ERROR: {result[4]}", file=sys.stderr)
        shutil.rmtree(args.tmpdir, ignore_errors=True)
        sys.exit(1)
    shutil.rmtree(args.tmpdir, ignore_errors=True)
    sys.exit(0)


# ============================================================
# Batch mode
# ============================================================

pairs = read_pairs(args.pairs)
if not pairs:
    print("ERROR: no valid pairs found.", file=sys.stderr)
    shutil.rmtree(args.tmpdir, ignore_errors=True)
    sys.exit(1)

chunk_dir = os.path.join(args.tmpdir, "chunks")
os.makedirs(chunk_dir, exist_ok=True)

chunks = make_chunks(pairs, args.threads)
tasks = [
    (i, chunk, sequences, args.tmpdir, chunk_dir)
    for i, chunk in enumerate(chunks, 1)
]

print(f"Pairs: {len(pairs)}", file=sys.stderr)
print(f"Threads: {args.threads}", file=sys.stderr)

with mp.Pool(len(chunks)) as pool:
    chunk_files = pool.map(worker, tasks)

out = output_handle()
try:
    print("ID1\tID2\tIdentity\tSimilarity", file=out)
    for chunk_file in sorted(chunk_files):
        with open(chunk_file) as f:
            for line in f:
                if line.strip():
                    print(line.rstrip(), file=out)
finally:
    if args.output:
        out.close()

shutil.rmtree(args.tmpdir, ignore_errors=True)
print("Finished.", file=sys.stderr)
