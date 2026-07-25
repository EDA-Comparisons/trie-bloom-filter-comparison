use std::collections::BTreeMap;

pub struct TrieNode {
    children: BTreeMap<char, Box<TrieNode>>,
    is_end: bool,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: BTreeMap::new(),
            is_end: false,
        }
    }
}

pub struct TrieStructure {
    root: TrieNode,
}

impl TrieStructure {
    pub fn new() -> Self {
        TrieStructure {
            root: TrieNode::new(),
        }
    }

    pub fn add(&mut self, username: &str) -> bool {
        let mut node = &mut self.root;
        for ch in username.chars() {
            node = node.children.entry(ch).or_insert_with(|| Box::new(TrieNode::new()));
        }

        let was_end = node.is_end;
        node.is_end = true;
        !was_end
    }

    pub fn contains(&self, username: &str) -> bool {
        let mut node = &self.root;
        for ch in username.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return false,
            }
        }
        node.is_end
    }

    pub fn suggest(&self, username: &str) -> String {
        let mut node = &self.root;
        let mut prefix = String::new();

        for ch in username.chars() {
            match node.children.get(&ch) {
                Some(child) => {
                    prefix.push(ch);
                    node = child;
                }
                None => return String::new(),
            }
        }

        self.find_next_word(node, prefix)
    }

    fn find_next_word(&self, node: &TrieNode, mut prefix: String) -> String {
        if node.is_end {
            return prefix;
        }

        for (ch, child) in &node.children {
            prefix.push(*ch);
            let result = self.find_next_word(child, prefix.clone());
            if !result.is_empty() {
                return result;
            }
            prefix.pop();
        }

        String::new()
    }
}
