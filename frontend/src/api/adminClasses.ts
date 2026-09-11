import http from '@/api/http'

export interface ClassRoomItem {
  id: number
  name: string
  class_code: string
  owner_id: number
  status: string
  n_students: number
  created_at?: string | null
}

export interface ClassMember {
  student_id: number
  nickname: string
  phone: string
}

export async function listClasses(): Promise<ClassRoomItem[]> {
  const { data } = await http.get<ClassRoomItem[]>('/api/admin/classes')
  return data
}

export async function createClass(name: string): Promise<ClassRoomItem> {
  const { data } = await http.post<ClassRoomItem>('/api/admin/classes', { name })
  return data
}

export async function renameClass(classCode: string, name: string): Promise<ClassRoomItem> {
  const { data } = await http.patch<ClassRoomItem>(
    `/api/admin/classes/${encodeURIComponent(classCode)}`,
    { name },
  )
  return data
}

export async function archiveClass(classCode: string): Promise<ClassRoomItem> {
  const { data } = await http.post<ClassRoomItem>(
    `/api/admin/classes/${encodeURIComponent(classCode)}/archive`,
  )
  return data
}

export async function listClassMembers(classCode: string): Promise<ClassMember[]> {
  const { data } = await http.get<ClassMember[]>(
    `/api/admin/classes/${encodeURIComponent(classCode)}/members`,
  )
  return data
}

export async function removeClassMember(classCode: string, studentId: number): Promise<void> {
  await http.delete(
    `/api/admin/classes/${encodeURIComponent(classCode)}/members/${studentId}`,
  )
}
