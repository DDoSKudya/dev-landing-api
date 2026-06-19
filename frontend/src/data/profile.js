export const profile = {
  fullName: "Кудинов Игорь Сергеевич",
  shortName: "Игорь Кудинов",
  initials: "ИК",
  title: "Python backend-разработчик",
  location: "Краснодар",
  experienceYears: "5+ лет",
  workFormat: "удалённо, гибрид",
  tagline:
    "Backend для production-систем: API, данные, интеграции и сопровождение legacy. Опыт в видеонаблюдении и видеоаналитике.",
  contacts: {
    email: "igor@kud93.ru",
    phone: "+79649150935",
    phoneDisplay: "+7 (964) 915-09-35",
    telegram: "@ddoskudya",
    telegramUrl: "https://t.me/ddoskudya",
    setka: "https://set.ki/account/oSx4xbs",
    github: "https://github.com/DDoSKudya",
  },
  highlights: [
    { title: "5+ лет", subtitle: "Коммерческий опыт на Python в production" },
    { title: "Данные & API", subtitle: "SQLAlchemy, PostgreSQL/SQLite, REST" },
    { title: "Production", subtitle: "Legacy, интеграции, релизы" },
  ],
  skills: [
    {
      title: "Backend",
      items: ["Python 3", "FastAPI", "Flask", "SQLAlchemy", "REST API"],
    },
    {
      title: "Данные",
      items: ["PostgreSQL", "SQLite", "Alembic", "Pytest"],
    },
    {
      title: "Инфраструктура",
      items: ["Docker", "Linux", "Git", "CI/CD"],
    },
    {
      title: "Практики",
      items: ["Анализ требований", "Рефакторинг", "Legacy", "Декомпозиция"],
    },
  ],
  portfolio: {
    work: [
      {
        id: "fmpa",
        name: "FMPA",
        title: "Face Match Passage Analysis",
        platform: "TRASSIR VMS · FR 2.0",
        private: true,
        summary:
          "Модуль видеоаналитики для службы безопасности: в реальном времени отслеживает посетителей на объекте, исключая сотрудников, и помогает выявлять людей, оставшихся после закрытия.",
        architecture: [
          "7 слоёв: bootstrap → события TRASSIR → EventManager → модуль FMPA → БД → интеграция FR 2.0 → UI и HTTP API",
          "Три потока: инициализация маршрутов и pollers, real-time события входа/выхода, операторские действия через веб-интерфейс",
        ],
        features: [
          "Распознавание на камерах входа и выхода, статусы on_territory, учёт посетителей vs employee_folders",
          "REST API: /auth, /get-settings, /get-persons, /delete-persone, /clear-persons-folder и др.",
          "Синхронизация папок FR с таблицами БД, авто-сброс «остались на территории» по расписанию",
          "Фоновые задачи: ежедневные popup-уведомления, очистка старых записей, bootstrap администратора",
          "Отчёты с фото и временем пребывания, аудит действий операторов",
        ],
        stack: ["Python", "TRASSIR VMS", "FR 2.0", "SQLAlchemy", "REST API", "Web UI", "Pollers"],
      },
      {
        id: "residence-parking",
        name: "Residence Parking",
        title: "Residence Parking",
        platform: "TRASSIR VMS · LPR5",
        private: true,
        summary:
          "Автоматизация парковки в жилых комплексах: контроль въезда и выезда по пропускам, учёт свободных мест, архив визитов и веб-интерфейс для операторов КПП.",
        architecture: [
          "Ядро (LPR, accounts, sessions, clients, passes, EMBLists, database) + веб-интерфейс с таблицами и настройками",
          "Интеграция с LPR5, GPIO шлагбаумов, внутренними списками номеров и БД VMS",
        ],
        features: [
          "Цепочки каналов (bundles): фильтрация событий по направлению, связка камера → GPIO → модификация шлагбаума",
          "Пропуска со статусами (In parking, Expired, Unlimited и др.), привязка к клиентам и EMB-спискам",
          "Таблицы Parking, Archive, Passes, Clients, Accounts — фильтрация, сортировка, CRUD, отчёты CSV",
          "Роли administrator / operator, сессии активности (30 мин), шифрование данных аккаунтов",
          "Виджеты занятости мест, ручной пропуск служебного транспорта оператором",
        ],
        stack: ["Python", "TRASSIR VMS", "LPR5", "SQL", "GPIO", "Web UI", "CSV Reports"],
      },
    ],
    pet: [
      {
        id: "spend-ledger",
        title: "Spend Ledger",
        platform: "Pet · Full-stack",
        summary:
          "Личный учёт расходов с категориями, тегами, фильтрами и экспортом. Микросервисная архитектура за единым BFF и nginx.",
        highlights: [
          "Сервисы: BFF (публичный API), auth, ledger, export — каждый со своей зоной ответственности",
          "PostgreSQL для данных, Redis + Celery для фоновых задач экспорта CSV/XLSX",
          "Vue 3 SPA с Tailwind, Docker Compose для локального и production-like запуска",
        ],
        stack: ["FastAPI", "PostgreSQL", "Redis", "Celery", "Vue 3", "Docker", "nginx"],
        url: "https://github.com/DDoSKudya/spend-ledger",
      },
      {
        id: "dev-landing-api",
        title: "Dev Landing API",
        platform: "Pet · Этот сайт",
        summary:
          "Backend-лендинг разработчика: демонстрация API-first подхода, AI-интеграции и production-практик в одном репозитории.",
        highlights: [
          "POST /api/contact: валидация, rate limit (файл + flock), SQLite, email владельцу и пользователю",
          "OpenAI analyze_comment с graceful fallback при отсутствии ключа или ошибке API",
          "GET /api/metrics, слоистая архитектура router → service → repository, pytest",
          "Vue 3 SPA с формой, обработкой 422/429/502 и Docker + nginx",
        ],
        stack: ["FastAPI", "SQLite", "OpenAI", "Vue 3", "Docker", "Alembic"],
        url: "https://github.com/DDoSKudya/dev-landing-api",
      },
      {
        id: "flask-store-lab",
        title: "Flask Store Lab",
        platform: "Pet · Учебный",
        summary:
          "Каталог товаров на Flask: отработка слоистой структуры, миграций и тестируемого backend без лишней сложности.",
        highlights: [
          "SQLAlchemy 2.x, Alembic, Pydantic для валидации входных данных",
          "Pytest для API и бизнес-логики, uWSGI для деплоя",
          "Чистое разделение маршрутов, сервисов и работы с БД",
        ],
        stack: ["Flask", "SQLAlchemy", "Alembic", "Pydantic", "Pytest", "uWSGI"],
        url: "https://github.com/DDoSKudya/flask-store-lab",
      },
      {
        id: "python-task-workbench",
        title: "Python Task Workbench",
        platform: "Pet · Desktop + CLI",
        summary:
          "Тренажёр по Python collections: генерация задач из content packs, проверка решений и coach-режим.",
        highlights: [
          "PyQt6 GUI: сессии, редактор кода, история попыток, anti-repeat логика вариантов",
          "CLI: solve / check / coach — единый config.json для UI и терминала",
          "Подпроцессная проверка кода с таймаутом, домены ecommerce / analytics / devops",
        ],
        stack: ["Python 3.12", "PyQt6", "CLI", "Pytest", "JSON config"],
        url: "https://github.com/DDoSKudya/python-task-workbench",
      },
      {
        id: "study-md-desk",
        title: "Study MD Desk",
        platform: "Pet · Desktop",
        summary:
          "Офлайн desktop-приложение для изучения Markdown: дерево файлов, оглавление, рендер уроков в одном окне.",
        highlights: [
          "PyQt6: навигация по папкам, outline заголовков, встроенный просмотр контента",
          "Дополнительные панели: заметки, TTS, мини Python runner",
          "Локальная работа без обязательного интернета после настройки",
        ],
        stack: ["Python", "PyQt6", "Markdown", "Offline-first"],
        url: "https://github.com/DDoSKudya/study-md-desk",
      },
      {
        id: "ai-study-atlas",
        title: "AI Study Atlas",
        platform: "Pet · Knowledge base",
        summary:
          "Структурированный атлас технических тем: маршруты обучения, связи между разделами и self-check вместо хаотичных заметок.",
        highlights: [
          "Контент по управляемым промптам: план → генерация → итеративное улучшение → проверка",
          "Двойной режим: последовательный курс и быстрый справочник по темам",
          "Единые стандарты качества и навигация по направлениям (architecture, backend и др.)",
        ],
        stack: ["Markdown", "Docs-as-code", "Learning paths", "Self-check"],
        url: "https://github.com/DDoSKudya/ai-study-atlas",
      },
    ],
  },
  experience: [
    {
      company: "DSSL",
      url: "https://www.dssl.ru",
      location: "Краснодар",
      role: "Python-разработчик",
      period: "Сентябрь 2021 — Март 2026",
      duration: "4 года 7 месяцев",
      bullets: [
        "Backend для видеонаблюдения и видеоаналитики: события, SQLAlchemy, HTTP API",
        "Отчётность, уведомления, внутренние библиотеки и инструменты разработки",
        "Поддержка legacy, анализ требований, сопровождение релизов",
      ],
    },
    {
      company: "DSSL",
      url: "https://www.dssl.ru",
      location: "Краснодар",
      role: "Специалист технической поддержки",
      period: "Ноябрь 2020 — Сентябрь 2021",
      duration: "11 месяцев",
      bullets: [
        "Техподдержка L1/L2 по продуктам компании",
        "Диагностика прикладных инцидентов и сопровождение решений",
      ],
    },
  ],
  education: {
    university: "КубГТУ",
    fullUniversity: "Кубанский государственный технологический университет",
    year: 2019,
    degree: "Бакалавр",
    specialty: "Землеустройство и кадастры",
  },
  languages: [
    { name: "Русский", level: "Родной" },
    { name: "Английский", level: "B1" },
  ],
};
