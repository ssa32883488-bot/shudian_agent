import http from '@/api/http'
import type { StudentProfileData } from '@/api/profile'

export interface ClassRosterItem {
  student_id: number
  nickname: string
  weak_points: string[]
  mastery_avg: number
  updated_at?: string | null
}

export interface ClassLearningData {
  ok: boolean
  class_code: string
  n_students: number
  mastery_avg: Record<string, number>
  weak_top: Array<{ name: string; count: number }>
  progress: Record<string, unknown>
  mistake_top?: Array<{ name: string; count: number }>
  practice?: {
    n_sessions?: number
    n_students?: number
    avg_accuracy?: number | null
  }
  exam_signals: Record<string, unknown>
  computed_at?: string | null
  roster: ClassRosterItem[]
}

export async function getClassLearning(
  refresh = false,
  classCode?: string,
): Promise<ClassLearningData> {
  const { data } = await http.get<ClassLearningData>('/api/admin/learning/class', {
    params: {
      refresh,
      class_code: classCode || undefined,
    },
  })
  return data
}

export async function getStudentLearning(studentId: number): Promise<StudentProfileData> {
  const { data } = await http.get<StudentProfileData>(
    `/api/admin/learning/student/${studentId}`,
  )
  return data
}

export async function exportClassLearningWord(classCode?: string): Promise<Blob> {
  const { data } = await http.get('/api/admin/learning/class/export-word', {
    params: { class_code: classCode || undefined },
    responseType: 'blob',
  })
  return data as Blob
}
