use std::collections::HashSet;

pub struct HashSetStructure {
    set: HashSet<String>,
}

impl HashSetStructure {
    pub fn new() -> Self {
        HashSetStructure {
            set: HashSet::new(),
        }
    }

    pub fn add(&mut self, username: &str) -> bool {
        self.set.insert(username.to_string())
    }

    pub fn contains(&self, username: &str) -> bool {
        self.set.contains(username)
    }

    pub fn suggest(&self, username: &str) -> String {
        let mut candidates: Vec<_> = self.set.iter().collect();
        candidates.sort();

        for candidate in candidates {
            if candidate.as_str() > username {
                return candidate.clone();
            }
        }

        String::new()
    }
}
