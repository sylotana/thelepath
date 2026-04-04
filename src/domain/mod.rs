// Делаем перечисление доступным для других модулей
pub enum SourceType {
    LocalFile(String),
    WebPage(String),
}

pub struct Resource {
    pub id: u32,
    pub source: SourceType,
    pub content: String,
}

pub struct Tab {
    pub id: u32,
    pub name: String,
    pub context_resources: Vec<Resource>,
}

impl Tab {
    // Конструктор для вкладки (упрощаем создание в main)
    pub fn new(id: u32, name: &str) -> Self {
        Self {
            id,
            name: name.to_string(),
            context_resources: Vec::new(),
        }
    }

    // Метод добавления ресурса (та самая бизнес-логика)
    pub fn add_resource(&mut self, resource: Resource) {
        self.context_resources.push(resource);
    }
}

pub struct ThelepathApp {
    pub tabs: Vec<Tab>,
    pub active_tab_id: u32,
}