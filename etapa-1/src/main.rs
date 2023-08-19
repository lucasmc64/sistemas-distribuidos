struct KeyRequest {
    key: String,
    ver: u64,
}

struct KeyRange {
    from: KeyRequest,
    to: KeyRequest,
}

struct KeyValueRequest {
    key: String,
    val: String,
}

struct KeyValueVersionReply {
    key: String,
    val: String,
}

struct PutReply {
    key: String,
    old_val: String,
    old_ver: u64,
    ver: u64,
}

struct KeyValueStore;

impl KeyValueStore {
    fn Get(keyRequest: KeyRequest) -> KeyValueVersionReply {
        KeyValueVersionReply {
            key: String::from(""),
            val: String::from(""),
        }
    }
    
    fn GetRange(keyRequest: KeyRange) -> KeyValueVersionReply {
        KeyValueVersionReply {
            key: String::from(""),
            val: String::from(""),
        }
    }
    
    fn GetAll() {}
    
    fn Put() {}
    
    fn PutAll() {}

    fn Del() {}
    
    fn DelRange() {}
    
    fn DelAll() {}
    
    fn Trim() {}
}

fn main() {
    println!("Hello, world!");
}
