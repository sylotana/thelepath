mod domain;
// Импортируем наши структуры из домена
use crate::domain::{ThelepathApp, Tab, Resource, SourceType};

fn main() {
    // 1. Инициализируем приложение (пока вручную, позже сделаем ThelepathApp::new())
    let mut app = ThelepathApp {
        tabs: Vec::new(),
        active_tab_id: 0,
    };

    println!("=== Приложение Thelepath запущено ===");

    // 2. Создаем ресурс
    // В будущем это будет делать отдельный Service
    let resource = Resource {
        id: 1,
        source: SourceType::LocalFile("test.txt".to_string()),
        content: String::from("Hello from test.txt!"),
    };

    // 3. Создаем вкладку, используя конструктор Tab::new из домена
    let mut new_tab = Tab::new(1, "Моя первая вкладка");

    // 4. Добавляем ресурс во вкладку через метод домена
    new_tab.add_resource(resource);

    // 5. КРИТИЧЕСКИЙ ШАГ: Добавляем вкладку в приложение
    // Без этой строки app.tabs[0] вызовет панику!
    app.tabs.push(new_tab);

    // Проверяем результат безопасно
    println!("В приложении теперь вкладок: {}", app.tabs.len());

    // Используем .get(0) вместо [0] для безопасности (хорошая привычка в Rust)
    if let Some(first_tab) = app.tabs.get(0) {
        println!("Успех! Вкладка '{}' содержит ресурсов: {}", 
            first_tab.name, 
            first_tab.context_resources.len()
        );
    } else {
        println!("Ошибка: Вкладка не была добавлена!");
    }
}