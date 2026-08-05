use deepsize::{Context, DeepSizeOf};
use radix_trie::{Trie, TrieCommon};

use crate::structure::DataStructure;

pub struct TrieStructure {
    trie: Trie<String, bool>,
}

impl TrieStructure {
    pub fn new() -> Self {
        TrieStructure {
            trie: Trie::new(),
        }
    }
}

impl DataStructure for TrieStructure {
    fn add(&mut self, key: &str) -> bool {
        self.trie.insert(key.to_string(), true).is_none()
    }

    fn contains(&self, key: &str) -> bool {
        self.trie.get(key).is_some()
    }

    fn suggest(&self, prefix: &str) -> String {
        self.trie
            .iter()
            .map(|(k, _)| k)
            .find(|k| k.starts_with(prefix))
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
        "trie"
    }
}

impl DeepSizeOf for TrieStructure {
    fn deep_size_of_children(&self, context: &mut Context) -> usize {
        let key_size: usize = self.trie.keys().map(|k| k.deep_size_of_children(context)).sum();
        let node_overhead = self.trie.len() * 64;
        key_size + node_overhead
    }
}
