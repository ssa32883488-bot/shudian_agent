export interface UserProfile {
  id: number
  nickname: string
  phone: string
  class_code?: string | null
  role: string
}

export interface AuthResponse {
  ok: boolean
  user: UserProfile
  token: string
}

export interface RegisterPayload {
  nickname: string
  phone: string
  password: string
  class_code?: string
  role?: 'student' | 'admin' | 'teacher'
}

export interface LoginPayload {
  phone: string
  password: string
}
