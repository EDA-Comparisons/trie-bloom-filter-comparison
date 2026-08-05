use deepsize::DeepSizeOf;

pub trait DataStructure: DeepSizeOf {
    fn add(&mut self, key: &str) -> bool;
    fn contains(&self, key: &str) -> bool;
    fn suggest(&self, prefix: &str) -> String;
    fn new_name(&mut self, key: &str) -> String;
    fn name(&self) -> &'static str;
}
