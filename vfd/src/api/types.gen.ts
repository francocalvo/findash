// This file is auto-generated by @hey-api/openapi-ts

export type Body_login_login_access_token = {
  grant_type?: string | null
  username: string
  password: string
  scope?: string
  client_id?: string | null
  client_secret?: string | null
}

/**
 * Public model for expense transactions.
 */
export type ExpensePublic = {
  date: string
  account: string
  payee?: string | null
  narration: string
  amount_ars: number
  amount_usd: number
  amount_cars: number
  category: string
  subcategory: string
  tags?: string | null
  id: string
}

/**
 * Response model for paginated expense transactions.
 */
export type ExpensesPublic = {
  data: Array<ExpensePublic>
  count: number
  pagination?: {
    [key: string]: number
  } | null
}

export type HTTPValidationError = {
  detail?: Array<ValidationError>
}

/**
 * Public model for income transactions.
 */
export type IncomePublic = {
  date: string
  account: string
  payee?: string | null
  narration: string
  amount_ars: number
  amount_usd: number
  amount_cars: number
  origin: string
  id: string
}

/**
 * Response model for paginated income transactions.
 */
export type IncomesPublic = {
  data: Array<IncomePublic>
  count: number
  pagination?: {
    [key: string]: number
  } | null
}

export type ItemCreate = {
  title: string
  description?: string | null
}

export type ItemPublic = {
  title: string
  description?: string | null
  id: string
  owner_id: string
}

export type ItemsPublic = {
  data: Array<ItemPublic>
  count: number
}

export type ItemUpdate = {
  title?: string | null
  description?: string | null
}

export type Message = {
  message: string
}

export type NewPassword = {
  token: string
  new_password: string
}

export type PrivateUserCreate = {
  email: string
  password: string
  full_name: string
  is_verified?: boolean
}

export type Token = {
  access_token: string
  token_type?: string
}

export type UpdatePassword = {
  current_password: string
  new_password: string
}

export type UserCreate = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password: string
}

export type UserPublic = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  id: string
}

export type UserRegister = {
  email: string
  password: string
  full_name?: string | null
}

export type UsersPublic = {
  data: Array<UserPublic>
  count: number
}

export type UserUpdate = {
  email?: string | null
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password?: string | null
}

export type UserUpdateMe = {
  full_name?: string | null
  email?: string | null
}

export type ValidationError = {
  loc: Array<string | number>
  msg: string
  type: string
}

export type AnalyticsGetCombinedMetricsData = {
  /**
   * Currencies to include in response
   */
  currencies?: Array<string>
  /**
   * Start date (YYYY-MM-DD)
   */
  fromDate: string
  /**
   * End date (YYYY-MM-DD)
   */
  toDate?: string | null
}

export type AnalyticsGetCombinedMetricsResponse = {
  [key: string]: unknown
}

export type ExpensesGetExpensesData = {
  /**
   * Filter by category
   */
  category?: string | null
  /**
   * Currencies to convert to
   */
  currencies?: Array<string>
  /**
   * Start date (YYYY-MM-DD)
   */
  fromDate: string
  /**
   * Number of records to return
   */
  limit?: number
  /**
   * Number of records to skip
   */
  skip?: number
  /**
   * End date (YYYY-MM-DD)
   */
  toDate?: string | null
}

export type ExpensesGetExpensesResponse = ExpensesPublic

export type ExpensesGetExpenseSummaryData = {
  /**
   * Currencies to convert to
   */
  currencies?: Array<string>
  /**
   * Start date (YYYY-MM-DD)
   */
  fromDate: string
  /**
   * Group by 'category' or 'month'
   */
  groupBy?: string
  /**
   * End date (YYYY-MM-DD)
   */
  toDate?: string | null
}

export type ExpensesGetExpenseSummaryResponse = {
  [key: string]: unknown
}

export type IncomeGetIncomesData = {
  /**
   * Currencies to convert to
   */
  currencies?: Array<string>
  /**
   * Start date (YYYY-MM-DD)
   */
  fromDate: string
  /**
   * Number of records to return
   */
  limit?: number
  /**
   * Filter by origin
   */
  origin?: string | null
  /**
   * Number of records to skip
   */
  skip?: number
  /**
   * End date (YYYY-MM-DD)
   */
  toDate?: string | null
}

export type IncomeGetIncomesResponse = IncomesPublic

export type IncomeGetIncomeSummaryData = {
  /**
   * Currencies to convert to
   */
  currencies?: Array<string>
  /**
   * Start date (YYYY-MM-DD)
   */
  fromDate: string
  /**
   * Group by 'origin' or 'month'
   */
  groupBy?: string
  /**
   * End date (YYYY-MM-DD)
   */
  toDate?: string | null
}

export type IncomeGetIncomeSummaryResponse = {
  [key: string]: unknown
}

export type ItemsReadItemsData = {
  limit?: number
  skip?: number
}

export type ItemsReadItemsResponse = ItemsPublic

export type ItemsCreateItemData = {
  requestBody: ItemCreate
}

export type ItemsCreateItemResponse = ItemPublic

export type ItemsReadItemData = {
  id: string
}

export type ItemsReadItemResponse = ItemPublic

export type ItemsUpdateItemData = {
  id: string
  requestBody: ItemUpdate
}

export type ItemsUpdateItemResponse = ItemPublic

export type ItemsDeleteItemData = {
  id: string
}

export type ItemsDeleteItemResponse = Message

export type LoginLoginAccessTokenData = {
  formData: Body_login_login_access_token
}

export type LoginLoginAccessTokenResponse = Token

export type LoginTestTokenResponse = UserPublic

export type LoginRecoverPasswordData = {
  email: string
}

export type LoginRecoverPasswordResponse = Message

export type LoginResetPasswordData = {
  requestBody: NewPassword
}

export type LoginResetPasswordResponse = Message

export type LoginRecoverPasswordHtmlContentData = {
  email: string
}

export type LoginRecoverPasswordHtmlContentResponse = string

export type PrivateCreateUserData = {
  requestBody: PrivateUserCreate
}

export type PrivateCreateUserResponse = UserPublic

export type UsersReadUsersData = {
  limit?: number
  skip?: number
}

export type UsersReadUsersResponse = UsersPublic

export type UsersCreateUserData = {
  requestBody: UserCreate
}

export type UsersCreateUserResponse = UserPublic

export type UsersReadUserMeResponse = UserPublic

export type UsersDeleteUserMeResponse = Message

export type UsersUpdateUserMeData = {
  requestBody: UserUpdateMe
}

export type UsersUpdateUserMeResponse = UserPublic

export type UsersUpdatePasswordMeData = {
  requestBody: UpdatePassword
}

export type UsersUpdatePasswordMeResponse = Message

export type UsersRegisterUserData = {
  requestBody: UserRegister
}

export type UsersRegisterUserResponse = UserPublic

export type UsersReadUserByIdData = {
  userId: string
}

export type UsersReadUserByIdResponse = UserPublic

export type UsersUpdateUserData = {
  requestBody: UserUpdate
  userId: string
}

export type UsersUpdateUserResponse = UserPublic

export type UsersDeleteUserData = {
  userId: string
}

export type UsersDeleteUserResponse = Message

export type UtilsTestEmailData = {
  emailTo: string
}

export type UtilsTestEmailResponse = Message

export type UtilsHealthCheckResponse = boolean
