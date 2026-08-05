use deepsize::DeepSizeOf;
use std::collections::HashSet;

use crate::structure::DataStructure;

#[derive(DeepSizeOf)]
pub struct HashSetStructure {
    set: HashSet<String>,
}

impl HashSetStructure {
    pub fn new() -> Self {
        HashSetStructure {
            set: HashSet::new(),
        }
    }
}

impl DataStructure for HashSetStructure {
    fn add(&mut self, key: &str) -> bool {
        self.set.insert(key.to_string())
    }

    fn contains(&self, key: &str) -> bool {
        self.set.contains(key)
    }

    fn suggest(&self, prefix: &str) -> String {
        let mut candidates: Vec<_> = self.set.iter().collect();
        candidates.sort();
        candidates
            .into_iter()
            .find(|c| c.starts_with(prefix))
            .cloned()
            .unwrap_or_default()
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
        "hashset"
    }
}
