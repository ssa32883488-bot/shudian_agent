import http from '@/api/http'
import type {
  AuthResponse,
  LoginPayload,
  RegisterPayload,
  UserProfile,
} from '@/types/auth'

export async function registerStudent(
  payload: RegisterPayload,
): Promise<AuthResponse> {
  const { data } = await http.post<AuthResponse>('/api/auth/register', payload)
  return data
}

export async function loginStudent(payload: LoginPayload): Promise<AuthResponse> {
  const { data } = await http.post<AuthResponse>('/api/auth/login', payload)
  return data
}

export async function bindClassCode(classCode: string): Promise<UserProfile> {
  const { data } = await http.post<UserProfile>('/api/auth/bind-class', {
    class_code: classCode,
  })
  return data
}
