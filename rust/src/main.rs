#[global_allocator]
static GLOBAL: crate::memory::TrackingAllocator = crate::memory::TrackingAllocator;

mod memory;
mod hashset;
mod trie;
mod bloom_filter;

use std::fs;
use std::io::{self, BufRead};
use std::time::Instant;
use serde_json::{json, Value};
use hashset::HashSetStructure;
use trie::TrieStructure;
use bloom_filter::BloomFilter;

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

fn run_benchmark(
    structure: &str,
    operations: &[Operation],
    measure_interval: i32,
    verbose: bool,
) -> Value {
    let mut stats = json!({
        "structure": structure,
        "hits": 0,
        "misses": 0,
        "memory_evolution": [],
        "total_time_ms": 0.0,
        "final_memory_mb": 0.0,
    });

    let initial_mem = memory::get_allocated_bytes();

    let start = Instant::now();

    match structure {
        "hashset" => {
            let mut hs = HashSetStructure::new();
            let mut hits = 0;
            let mut misses = 0;

            for (idx, op) in operations.iter().enumerate() {
                match op.op_type.as_str() {
                    "SET" => {
                        hs.add(&op.data);
                        if verbose {
                            println!();
                        }
                    }
                    "GET" => {
                        if hs.contains(&op.data) {
                            hits += 1;
                        } else {
                            misses += 1;
                        }
                        if verbose {
                            println!("{}", if hs.contains(&op.data) { "true" } else { "false" });
                        }
                    }
                    "SUG" => {
                        let result = hs.suggest(&op.data);
                        if verbose {
                            println!("{}", result);
                        }
                    }
                    _ => {}
                }

                if measure_interval > 0 && (idx + 1) % measure_interval as usize == 0 {
                    let current_mem = memory::get_allocated_bytes();
                    let delta_mb = (current_mem as i64 - initial_mem as i64) as f64 / 1_048_576.0;
                    stats["memory_evolution"]
                        .as_array_mut()
                        .unwrap()
                        .push(json!({
                            "operation": idx + 1,
                            "delta_memory_mb": delta_mb,
                        }));
                }
            }

            stats["hits"] = json!(hits);
            stats["misses"] = json!(misses);
        }
        "trie" => {
            let mut trie = TrieStructure::new();
            let mut hits = 0;
            let mut misses = 0;

            for (idx, op) in operations.iter().enumerate() {
                match op.op_type.as_str() {
                    "SET" => {
                        trie.add(&op.data);
                        if verbose {
                            println!();
                        }
                    }
                    "GET" => {
                        if trie.contains(&op.data) {
                            hits += 1;
                        } else {
                            misses += 1;
                        }
                        if verbose {
                            println!("{}", if trie.contains(&op.data) { "true" } else { "false" });
                        }
                    }
                    "SUG" => {
                        let result = trie.suggest(&op.data);
                        if verbose {
                            println!("{}", result);
                        }
                    }
                    _ => {}
                }

                if measure_interval > 0 && (idx + 1) % measure_interval as usize == 0 {
                    let current_mem = memory::get_allocated_bytes();
                    let delta_mb = (current_mem as i64 - initial_mem as i64) as f64 / 1_048_576.0;
                    stats["memory_evolution"]
                        .as_array_mut()
                        .unwrap()
                        .push(json!({
                            "operation": idx + 1,
                            "delta_memory_mb": delta_mb,
                        }));
                }
            }

            stats["hits"] = json!(hits);
            stats["misses"] = json!(misses);
        }
        "bloom_filter" => {
            let mut bf = BloomFilter::new(10_000_000, 3);
            let mut hits = 0;
            let mut misses = 0;

            for (idx, op) in operations.iter().enumerate() {
                match op.op_type.as_str() {
                    "SET" => {
                        bf.add(&op.data);
                        if verbose {
                            println!();
                        }
                    }
                    "GET" => {
                        if bf.contains(&op.data) {
                            hits += 1;
                        } else {
                            misses += 1;
                        }
                        if verbose {
                            println!("{}", if bf.contains(&op.data) { "true" } else { "false" });
                        }
                    }
                    "SUG" => {
                        let result = bf.suggest(&op.data);
                        if verbose {
                            println!("{}", result);
                        }
                    }
                    _ => {}
                }

                if measure_interval > 0 && (idx + 1) % measure_interval as usize == 0 {
                    let current_mem = memory::get_allocated_bytes();
                    let delta_mb = (current_mem as i64 - initial_mem as i64) as f64 / 1_048_576.0;
                    stats["memory_evolution"]
                        .as_array_mut()
                        .unwrap()
                        .push(json!({
                            "operation": idx + 1,
                            "delta_memory_mb": delta_mb,
                        }));
                }
            }

            stats["hits"] = json!(hits);
            stats["misses"] = json!(misses);
        }
        _ => {}
    }

    let elapsed = start.elapsed();
    let final_mem = memory::get_allocated_bytes();
    let delta_mb = (final_mem as i64 - initial_mem as i64) as f64 / 1_048_576.0;

    stats["total_time_ms"] = json!(elapsed.as_secs_f64() * 1000.0);
    stats["final_memory_mb"] = json!(delta_mb);

    stats
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 5 {
        eprintln!("Usage: {} <file_path> <measure_interval> <test_id> <save_path> [--verbose]", args[0]);
        std::process::exit(1);
    }

    let file_path = &args[1];
    let measure_interval: i32 = args[2].parse().expect("measure_interval must be an integer");
    let test_id = &args[3];
    let save_path = &args[4];
    let verbose = args.contains(&"--verbose".to_string());

    let operations = parse_operations(file_path).expect("Failed to read operations file");

    let mut results = json!({
        "test_id": test_id,
        "total_operations": operations.len(),
        "results": {}
    });

    for structure in &["hashset", "trie", "bloom_filter"] {
        let stats = run_benchmark(structure, &operations, measure_interval, verbose);
        results["results"][*structure] = stats;
    }

    let output_file = format!("{}/{}.json", save_path, test_id);
    fs::write(&output_file, serde_json::to_string_pretty(&results).unwrap())
        .expect("Failed to write results file");

    println!("Results saved to {}", output_file);
}
