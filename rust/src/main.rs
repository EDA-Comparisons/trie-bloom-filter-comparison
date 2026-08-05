mod bloom_filter;
mod hashset;
mod structure;
mod trie;

use std::collections::HashSet;
use std::fs;
use std::io::{self, BufRead};
use std::time::Instant;

use clap::Parser;
use serde_json::{json, Value};

use bloom_filter::BloomFilterStructure;
use hashset::HashSetStructure;
use structure::DataStructure;
use trie::TrieStructure;

#[derive(Parser, Debug)]
#[command(name = "benchmark", about = "Benchmark de estruturas de dados")]
struct Args {
    /// Arquivo de operações
    file_path: String,

    /// Intervalo de medição (-1 = apenas final)
    #[arg(allow_hyphen_values = true)]
    measure_interval: i32,

    /// ID do teste
    test_id: String,

    /// Diretório para salvar JSON
    save_path: String,

    /// Rodar Bloom Filter
    #[arg(long)]
    bloom: bool,

    /// Rodar Trie
    #[arg(long)]
    trie: bool,

    /// Rodar HashSet
    #[arg(long)]
    hashset: bool,

    /// Imprime resultados na stdout
    #[arg(long)]
    verbose: bool,
}

#[derive(Debug)]
struct Operation {
    op_type: String,
    data: String,
}

fn parse_operations(file_path: &str) -> io::Result<Vec<Operation>> {
    let file = fs::File::open(file_path)?;
    let reader = io::BufReader::new(file);
    let mut operations = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        let parts: Vec<&str> = trimmed.split_whitespace().collect();
        if parts.len() >= 2 {
            operations.push(Operation {
                op_type: parts[0].to_string(),
                data: parts[1..].join(" "),
            });
        }
    }
    Ok(operations)
}

fn run_benchmark<S: DataStructure>(
    mut structure: S,
    operations: &[Operation],
    measure_interval: i32,
    verbose: bool,
) -> Value {
    let mut gt: HashSet<String> = HashSet::new();
    let mut hits = 0;
    let mut misses = 0;
    let mut false_positives = 0;

    let mut memory_evolution: Vec<Value> = Vec::new();
    let mut time_evolution: Vec<Value> = Vec::new();

    let initial_mem = structure.deep_size_of();
    let start = Instant::now();

    for (idx, op) in operations.iter().enumerate() {
        match op.op_type.as_str() {
            "SET" => {
                let t = Instant::now();
                structure.add(&op.data);
                let elapsed = t.elapsed();
                gt.insert(op.data.clone());
                if verbose {
                    println!();
                }
                // tempo medido apenas na estrutura, GT fora do timer
                let _ = elapsed;
            }
            "GET" => {
                let t = Instant::now();
                let result = structure.contains(&op.data);
                let elapsed = t.elapsed();
                let gt_result = gt.contains(&op.data);

                if result {
                    hits += 1;
                    if !gt_result {
                        false_positives += 1;
                    }
                } else {
                    misses += 1;
                }

                if verbose {
                    println!("{}", result);
                }
                let _ = elapsed;
            }
            "SUG" => {
                let t = Instant::now();
                let result = structure.suggest(&op.data);
                let elapsed = t.elapsed();
                if verbose {
                    println!("{}", result);
                }
                let _ = elapsed;
            }
            "NEW" => {
                let t = Instant::now();
                let result = structure.new_name(&op.data);
                let elapsed = t.elapsed();
                if verbose {
                    println!("{}", result);
                }
                let _ = elapsed;
            }
            _ => {}
        }

        if measure_interval > 0 && (idx + 1) % measure_interval as usize == 0 {
            let current_mem = structure.deep_size_of();
            let delta_mb = (current_mem as f64 - initial_mem as f64) / 1_048_576.0;
            memory_evolution.push(json!({
                "operation": idx + 1,
                "delta_memory_mb": delta_mb,
            }));

            let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;
            time_evolution.push(json!({
                "operation": idx + 1,
                "elapsed_ms": elapsed_ms,
            }));
        }
    }

    let total_time_ms = start.elapsed().as_secs_f64() * 1000.0;
    let final_mem = structure.deep_size_of();
    let delta_mb = (final_mem as f64 - initial_mem as f64) / 1_048_576.0;
    let total_ops = operations.len();
    let ops_per_second = if total_time_ms > 0.0 {
        (total_ops as f64 / total_time_ms) * 1000.0
    } else {
        0.0
    };
    let false_positive_rate = if hits > 0 {
        false_positives as f64 / hits as f64
    } else {
        0.0
    };

    json!({
        "structure": structure.name(),
        "hits": hits,
        "misses": misses,
        "false_positives": false_positives,
        "false_positive_rate": false_positive_rate,
        "total_time_ms": total_time_ms,
        "ops_per_second": ops_per_second,
        "final_memory_mb": delta_mb,
        "memory_evolution": memory_evolution,
        "time_evolution": time_evolution,
    })
}

fn main() {
    let args = Args::parse();

    let operations = parse_operations(&args.file_path).expect("Failed to read operations file");

    let run_all = !args.bloom && !args.trie && !args.hashset;

    let mut results = json!({
        "test_id": args.test_id,
        "total_operations": operations.len(),
        "results": {},
    });

    if args.bloom || run_all {
        let stats = run_benchmark(BloomFilterStructure::new(), &operations, args.measure_interval, args.verbose);
        results["results"]["bloom_filter"] = stats;
    }
    if args.trie || run_all {
        let stats = run_benchmark(TrieStructure::new(), &operations, args.measure_interval, args.verbose);
        results["results"]["trie"] = stats;
    }
    if args.hashset || run_all {
        let stats = run_benchmark(HashSetStructure::new(), &operations, args.measure_interval, args.verbose);
        results["results"]["hashset"] = stats;
    }

    let output_file = format!("{}/{}.json", args.save_path, args.test_id);
    fs::write(&output_file, serde_json::to_string_pretty(&results).unwrap())
        .expect("Failed to write results file");

    println!("Results saved to {}", output_file);
}
