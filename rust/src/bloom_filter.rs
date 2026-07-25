use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

pub struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
    hash_functions: usize,
}

impl BloomFilter {
    pub fn new(size: usize, hash_functions: usize) -> Self {
        BloomFilter {
            bits: vec![false; size],
            size,
            hash_functions,
        }
    }

    fn hash(&self, data: &str, seed: u64) -> usize {
        let mut hasher = DefaultHasher::new();
        data.hash(&mut hasher);
        seed.hash(&mut hasher);
        (hasher.finish() as usize) % self.size
    }

    pub fn add(&mut self, username: &str) -> bool {
        for i in 0..self.hash_functions {
            let idx = self.hash(username, i as u64);
            self.bits[idx] = true;
        }
        true
    }

    pub fn contains(&self, username: &str) -> bool {
        for i in 0..self.hash_functions {
            let idx = self.hash(username, i as u64);
            if !self.bits[idx] {
                return false;
            }
        }
        true
    }

    pub fn suggest(&self, _username: &str) -> String {
        String::new()
    }
}
