// Validate file against constraints
export function validateFile(file, options = {}) {
  const defaultOptions = {
    allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'text/plain'],
    maxSize: 5 * 1024 * 1024 // 5MB
  }
  
  const { allowedTypes, maxSize } = { ...defaultOptions, ...options }

  if (!allowedTypes.includes(file.type)) {
    const allowedExtensions = allowedTypes.map(t => {
      if (t.startsWith('image/')) return t.split('/')[1]
      if (t === 'text/plain') return 'txt'
      return t
    })
    return `Unsupported file type. Allowed types: ${allowedExtensions.join(', ')}`
  }

  if (file.size > maxSize) {
    return `File is too large. Maximum size is ${formatFileSize(maxSize)}`
  }

  return null
}

// Read file as Data URL
export function readFileAsDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(new Error('Failed to read file'))
    reader.readAsDataURL(file)
  })
}

// Format file size in human-readable format
export function formatFileSize(bytes) {
  if (typeof bytes !== 'number' || bytes < 0) return '0 bytes'
  
  if (bytes < 1024) return `${bytes} bytes`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`
}

// Convert Data URL to Blob
export function dataURLtoBlob(dataURL) {
  try {
    const byteString = atob(dataURL.split(',')[1])
    const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0]
    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }
    
    return new Blob([ab], { type: mimeString })
  } catch (error) {
    console.error('Error converting Data URL to Blob:', error)
    throw new Error('Failed to convert image data')
  }
}