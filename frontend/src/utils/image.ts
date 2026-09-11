/**
 * 图片工具：File → base64 data URL（供 solve 接口 image / image_base64 字段）
 */

const MAX_IMAGE_BYTES = 5 * 1024 * 1024 // 5MB，与宪法「上传 ≤5MB」对齐

export function assertImageFile(file: File): void {
  if (!file.type.startsWith('image/')) {
    throw new Error('请上传图片文件（jpg / png / webp 等）')
  }
  if (file.size > MAX_IMAGE_BYTES) {
    throw new Error('图片不能超过 5MB')
  }
}

/** 读取为 data URL（含 data:image/...;base64, 前缀） */
export function fileToDataUrl(file: File): Promise<string> {
  assertImageFile(file)
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      if (typeof reader.result === 'string') resolve(reader.result)
      else reject(new Error('读取图片失败'))
    }
    reader.onerror = () => reject(new Error('读取图片失败'))
    reader.readAsDataURL(file)
  })
}
