# Frontend Architecture

The frontend ecosystem is built using the **Vue 3** stack, emphasizing componentization, responsiveness, and high performance.

## Technology Stack

| Technology | Choice | Role |
| :--- | :--- | :--- |
| **Core Framework** | Vue 3 (Composition API) | Building reactive user interfaces |
| **Build Tool** | Vite 5 | Instant cold start and HMR |
| **Language** | TypeScript 5 | Static type checking, improving code robustness |
| **UI Library** | Element Plus | Quickly building high-quality B2B/C interfaces |
| **State Management** | Pinia | Lightweight, intuitive global state management |
| **Routing** | Vue Router 4 | Single Page Application (SPA) routing control |
| **HTTP Client** | Axios | Unified request interception and response handling |
| **Charting** | ECharts 5 | Complex data visualization (e.g., KPI dashboards) |
| **CSS Preprocessor** | SCSS | Modular style authoring |

## Project Structure

The frontend codebase uses a Monorepo style management (logically separated, physically in the same repo):

```
frontend/
├── official-website/   # Official Website (SEO optimized, display-oriented)
├── user-portal/        # User Console (Recognition, Recharge, History)
└── admin-portal/       # Admin Dashboard (Permissions, Monitoring, Config)
```

## Core Features

- **Internationalization (i18n)**: Built-in multi-language support (English/Chinese).
- **Theme Customization**: Supports dark mode and brand color configuration.
- **Permission Directives**: Encapsulated `v-permission` directive for fine-grained button-level permission control.
- **Dynamic Routing**: Dynamically generates frontend menus and routing tables based on user permissions returned by the backend.
