# Database Design

The system's core data storage uses **MySQL 8.0**, following the third normal form design to ensure data consistency and integrity.

## ER Diagram (Logical Model)

> (Insert ER Diagram here)

## Core Table Design

### 1. User & Permissions
| Table Name | Description |
| :--- | :--- |
| `users` | Core user table, storing accounts, password hashes, status, etc. |
| `user_profiles` | User extended info (Real-name verification data, contact info). |
| `roles` | Role definition table (Admin, User, VIP). |
| `permissions` | Permission point definitions. |
| `user_memberships` | Membership subscription status records. |

### 2. Recognition Business
| Table Name | Description |
| :--- | :--- |
| `recognition_tasks` | Recognition task main table, recording task type, status, duration. |
| `recognition_results` | Recognition result details, including plate number, confidence, image path. |
| `recognition_statistics`| Daily usage statistics for quota control. |

### 3. Order & Finance
| Table Name | Description |
| :--- | :--- |
| `packages` | Package definitions (price, quota, features). |
| `orders` | Order records, associating user and payment status. |
| `payments` | Payment transaction records. |

### 4. Logs & Audit
| Table Name | Description |
| :--- | :--- |
| `operation_logs` | Key operation audit logs (who, when, what). |
| `login_logs` | User login history records. |

## Cache Design (Redis)

- **Session**: Stores JWT blocklist (logout invalidation).
- **Quota**: Daily recognition count counter (atomic increment).
- **Verification Code**: Temporary storage for verification codes (TTL).
- **Task Queue**: Asynchronous recognition task queue.
