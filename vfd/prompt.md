Vue Project Structure and Architecture Guide
Project Overview
This is a Vue 3 + TypeScript application for financial management with features including user authentication, item management, expense/income tracking, and analytics. The application uses a REST API backend with clearly defined endpoints and PrimeVue as the component library.
Key Technologies

Vue 3 (Composition API)
TypeScript
Vue Router
Pinia (state management)
TanStack Query (API data fetching)
Axios (HTTP client)
PrimeVue (UI component library)

Directory Structure

```
.
├── api/                   # API client and type definitions
│   ├── core/              # Core API utilities
│   ├── sdk.gen.ts         # Generated API services
│   └── types.gen.ts       # API type definitions
├── assets/                # Static assets (CSS, images)
├── components/            # UI components organized by feature
│   ├── common/            # Shared components (Navbar, Sidebar)
│   ├── items/             # Item-related components
│   ├── admin/             # Admin components
│   └── ui/                # Base UI components (Button, Dialog)
├── composables/           # Reusable Vue composition functions
│   └── useAuth.ts         # useAuth composable
├── layouts/               # Page layout templates
├── router/                # Vue Router configuration
├── stores/                # Pinia stores
├── types/                 # TypeScript type definitions
├── utils/                 # Utility functions
└── views/                 # Page components organized by feature
```

---

Data Flow Architecture

API Layer: Generated SDK services (sdk.gen.ts) provide type-safe methods to interact with backend endpoints
Composables: Handle API calls and state management for specific features
Components: Consume composables and render UI based on state
Stores: Handle global state that needs to be shared across components
Router: Manages navigation between views

---

# Detailed API Information

## Available API Services and Endpoints:

### 1. AuthService:

- `login`: POST /api/v1/login/access-token (parameters: username, password)
- `testToken`: POST /api/v1/login/test-token
- `recoverPassword`: POST /api/v1/password-recovery/{email}
- `resetPassword`: POST /api/v1/reset-password

### 2. UsersService:

- `readUsers`: GET /api/v1/users/ (parameters: skip, limit)
- `createUser`: POST /api/v1/users/ (body: user data)
- `readUserMe`: GET /api/v1/users/me
- `updateUserMe`: PATCH /api/v1/users/me (body: user data)
- `updatePasswordMe`: PATCH /api/v1/users/me/password
- `registerUser`: POST /api/v1/users/signup
- `readUserById`: GET /api/v1/users/{userId}
- `updateUser`: PATCH /api/v1/users/{userId}
- `deleteUser`: DELETE /api/v1/users/{userId}

### 3. ItemsService:

- `readItems`: GET /api/v1/items/ (parameters: skip, limit)
- `createItem`: POST /api/v1/items/ (body: item data)
- `readItem`: GET /api/v1/items/{id}
- `updateItem`: PUT /api/v1/items/{id} (body: item data)
- `deleteItem`: DELETE /api/v1/items/{id}

### 4. AnalyticsService:

- `getCombinedMetrics`: GET /api/v1/analytics/combined (parameters: fromDate, toDate, currencies)

### 5. ExpensesService:

- `getExpenses`: GET /api/v1/expenses/ (parameters: fromDate, toDate, currencies, category, skip, limit)
- `getExpenseSummary`: GET /api/v1/expenses/summary (parameters: fromDate, toDate, currencies, groupBy)

### 6. IncomeService:

- `getIncomes`: GET /api/v1/income/ (parameters: fromDate, toDate, currencies, origin, skip, limit)
- `getIncomeSummary`: GET /api/v1/income/summary (parameters: fromDate, toDate, currencies, groupBy)

## Response Formats:

- All API responses follow consistent formats
- Success responses typically include requested data and metadata
- Error responses include status code, error message, and sometimes detailed validation errors
- Pagination results include items array, total count, and pagination metadata

## Error Handling Patterns:

- `ApiError` class is used for handling and normalizing API errors
- Error handling is centralized in `utils/error-handler.ts`
- Errors are captured in either component state or Pinia stores and shown in UI
- Network errors, validation errors, and authentication errors are handled differently

## Authentication Token Format and Management:

- JWT tokens are stored in localStorage under the 'access_token' key
- Tokens are automatically attached to all API requests via the OpenAPI configuration
- Token expiration is handled by detecting 401 responses and redirecting to login
- Refresh token functionality is implemented in the useAuth composable
- Tokens contain user ID, permissions, and expiration information---

---

State Management Details
Pinia Store Structure:

Each major feature has its own store module (auth.ts, items.ts, etc.)
Stores follow a consistent pattern with state, getters, and actions
Actions handle API calls and state updates

---

Example Code Patterns

API Service Usage
typescript// From sdk.gen.ts - defines API endpoints

```
export class ItemsService {
  public static readItems(): CancelablePromise<ItemsReadItemsResponse> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/items/",
      // ...
    })
  }
}
```

Composable Pattern

typescript// composables/useAuth.ts

```
export default function useItems() {
  // State and query handling
  const { data: items, isLoading } = useQuery({
    queryKey: ['items'],
    queryFn: () => ItemsService.readItems()
  })

  // Mutations for data changes
  const createItem = useMutation({
    mutationFn: (data) => ItemsService.createItem({ requestBody: data }),
    // ...
  })

  return {
    items,
    isLoading,
    createItem: createItem.mutate
  }
}
```

Component Usage with PrimeVue

```
vue<script setup>
import useItems from '@/composables/useItems'
import { ref } from 'vue'

const { items, isLoading, createItem } = useItems()
const newItemDialog = ref(false)
const newItem = ref({ name: '', description: '' })

const submitNewItem = () => {
  createItem(newItem.value)
  newItemDialog.value = false
  newItem.value = { name: '', description: '' }
}
</script>

<template>
  <div class="card">
    <p-data-table v-if="!isLoading" :value="items" :paginator="true" :rows="10">
      <p-column field="name" header="Name"></p-column>
      <p-column field="description" header="Description"></p-column>
      <p-column header="Actions">
        <template #body="slotProps">
          <p-button icon="pi pi-pencil" class="p-button-text" />
          <p-button icon="pi pi-trash" class="p-button-text p-button-danger" />
        </template>
      </p-column>
    </p-data-table>
    <p-skeleton v-else height="400px" />

    <p-button label="Add Item" icon="pi pi-plus" @click="newItemDialog = true" />

    <p-dialog v-model:visible="newItemDialog" header="Add New Item" modal>
      <div class="field">
        <label for="name">Name</label>
        <p-input-text id="name" v-model="newItem.name" required autofocus />
      </div>
      <div class="field">
        <label for="description">Description</label>
        <p-textarea id="description" v-model="newItem.description" rows="5" />
      </div>
      <template #footer>
        <p-button label="Cancel" icon="pi pi-times" @click="newItemDialog = false" class="p-button-text" />
        <p-button label="Save" icon="pi pi-check" @click="submitNewItem" />
      </template>
    </p-dialog>
  </div>
</template>
```

---

Route Naming Conventions:

Use kebab-case for route names
Feature-based naming (items, items-new, item-detail)
Consistent pluralization (items vs. item)
Feature prefixes for related routes

Protected Route Implementation:

```
// Navigation guards in router/index.ts
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isGuest = to.matched.some(record => record.meta.guest)
  const isLoggedIn = localStorage.getItem('access_token') !== null

  if (requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (isGuest && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})
```

---

Navigation Guards:

Global Guards:
beforeEach: Authentication check, role verification
afterEach: Analytics tracking, loading state management

Route-Specific Guards:
beforeEnter: Feature-specific access control

Component Guards:
beforeRouteEnter: Data pre-fetching
beforeRouteUpdate: Handling parameter changes
beforeRouteLeave: Preventing accidental navigation from forms

---

Authentication Flow

Authentication uses token-based auth stored in localStorage
The useAuth composable handles login, signup, and user management
Token is automatically attached to API requests via the OpenAPI configuration
Protected routes check auth status before rendering
Token refresh is handled automatically when expired
Logout clears token and redirects to login page

---

Key Integration Points

Authentication & API: The auth token is stored in localStorage and attached to API requests via OpenAPI.TOKEN
Route Guards: Check authentication status before allowing access to protected routes
Data Fetching: Use TanStack Query for data fetching, caching, and synchronization
Error Handling: Centralized error handling through utility functions
UI Components: PrimeVue components are used throughout the application with prefixes like p-button, p-data-table, etc.

---

PrimeVue Integration

PrimeVue is initialized in main.ts with required components and themes
The application uses PrimeVue's built-in components for UI elements like buttons, tables, dialogs, etc.
PrimeFlex CSS utility classes are used for layout and responsive design
PrimeIcons provide consistent iconography throughout the application

---

Feature Areas

User Management: Authentication, profile management, password reset
Items Management: CRUD operations for generic items
Financial Data: Income and expense tracking with filtering and analysis
Analytics: Dashboards and reports for financial metrics

When implementing features, follow these patterns:

Create API calls using the generated services in sdk.gen.ts
Implement business logic in composables
Build UI components that consume these composables and utilize PrimeVue components
Create views that combine components into full pages
Use layouts to maintain consistent page structure

This architecture provides a scalable foundation that separates concerns and follows Vue best practices while maintaining type safety through TypeScript and leveraging PrimeVue's rich component library for a consistent, professional UI.
