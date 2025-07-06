import { ref } from 'vue'
import { validateFile, readFileAsDataURL, dataURLtoBlob } from '@/utils/fileUtils'

export function useFileHandling() {
  const file = ref(null)
  const previewImage = ref(null)
  const error = ref('')

  const handleFileUpload = async (fileInput) => {
    error.value = ''
    const uploadedFile = fileInput.files?.[0]
    
    if (!uploadedFile) {
      resetFileData()
      return
    }

    // Validate file
    const validationError = validateFile(uploadedFile, {
      allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'text/plain'],
      maxSize: 5 * 1024 * 1024 // 5MB
    })

    if (validationError) {
      error.value = validationError
      resetFileData()
      return
    }

    // Process file
    file.value = {
      name: uploadedFile.name,
      size: uploadedFile.size,
      type: uploadedFile.type.startsWith('image/') ? 'image' : 'text',
      file: uploadedFile
    }

    // Handle image preview
    if (file.value.type === 'image') {
      try {
        previewImage.value = await readFileAsDataURL(uploadedFile)
      } catch (err) {
        error.value = 'Failed to process image'
        console.error('Image processing error:', err)
        resetFileData()
      }
    } else {
      previewImage.value = null
    }
  }

  const resetFileData = () => {
    file.value = null
    previewImage.value = null
  }

  const getFileForUpload = () => {
    if (!file.value) return null

    if (file.value.type === 'image' && previewImage.value) {
      return dataURLtoBlob(previewImage.value)
    }
    return file.value.file
  }

  return {
    file,
    previewImage,
    error,
    handleFileUpload,
    resetFileData,
    getFileForUpload
  }
}