use deepsize::{Context, DeepSizeOf};
use fastbloom::BloomFilter;

use crate::structure::DataStructure;

pub struct BloomFilterStructure {
    filter: BloomFilter,
}

impl BloomFilterStructure {
    pub fn new() -> Self {
        let filter = BloomFilter::with_false_pos(0.01).expected_items(10_000_000);
        BloomFilterStructure { filter }
    }
}

impl DataStructure for BloomFilterStructure {
    fn add(&mut self, key: &str) -> bool {
        self.filter.insert(key)
    }

    fn contains(&self, key: &str) -> bool {
        self.filter.contains(key)
    }

    fn suggest(&self, _prefix: &str) -> String {
        String::new()
    }

    fn new_name(&mut self, key: &str) -> String {
        if !self.contains(key) {
            return key.to_string();
        }
        let mut i = 1;
        loop {
            let candidate = format!("{}{}", key, i);
            if !self.contains(&candidate) {
                return candidate;
            }
            i += 1;
        }
    }

    fn name(&self) -> &'static str {
        "bloom_filter"
    }
}

impl DeepSizeOf for BloomFilterStructure {
    fn deep_size_of_children(&self, _context: &mut Context) -> usize {
        self.filter.num_bits() / 8
    }
}
