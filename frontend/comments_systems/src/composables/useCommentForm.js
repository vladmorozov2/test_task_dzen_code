import { ref, computed } from 'vue'
import { submitComment } from '@/services/commentService'
import { sanitizeHTML } from '@/utils/htmlSanitizer'

export function useCommentForm(props, emit) {
  const form = ref({
    text: ''
  })

  const file = ref(null)
  const previewImage = ref(null)
  const fileError = ref('')
  const captchaVerified = ref('') 
  const captchaError = ref('')
  const showPreview = ref(false)
  const isSubmitting = ref(false)
  const lightboxVisible = ref(false)
  const currentImage = ref(null)
  const errors = ref({})
  const htmlErrors = ref([])

  const isReply = computed(() => props.parentId !== null)

  const combinedErrors = computed(() => {
    return [...(errors.value.text ? [errors.value.text] : []), ...htmlErrors.value]
  })

  const validateForm = () => {
    errors.value = {}
    htmlErrors.value = []

    if (!form.value.text.trim()) {
      errors.value.text = 'Comment text is required.'
    }

    if (/<script/i.test(form.value.text)) {
      htmlErrors.value.push('Script tags are not allowed.')
    }

    if (!captchaVerified.value) {
      captchaError.value = 'Please verify that you are not a robot.'
    }

    return Object.keys(errors.value).length === 0 && 
           htmlErrors.value.length === 0 && 
           captchaVerified.value
  }

  const handleFileUpload = (uploadedFile) => {
    file.value = uploadedFile
  }

  const removeFile = () => {
    file.value = null
    previewImage.value = null
    fileError.value = ''
  }

  const onCaptchaVerified = (token) => {
    captchaVerified.value = token
    captchaError.value = ''
  }

  const togglePreview = () => {
    showPreview.value = !showPreview.value
  }

  const openLightbox = (imageUrl) => {
    currentImage.value = imageUrl
    lightboxVisible.value = true
  }

  const handleSubmit = async () => {
    if (!validateForm()) return

    isSubmitting.value = true

    try {
      const commentData = {
        text: sanitizeHTML(form.value.text),
        parentId: props.parentId,
        file: file.value,
        captchaToken: captchaVerified.value
      }

      await submitComment(commentData)
      emit('submit')
      resetForm()
    } catch (error) {
      handleError(error)
    } finally {
      isSubmitting.value = false
    }
  }

  const resetForm = () => {
    form.value.text = ''
    removeFile()
    showPreview.value = false
    captchaVerified.value = ''
    errors.value = {}
    htmlErrors.value = []
  }

  const handleError = (error) => {
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      console.error('Comment submission error:', error)
      errors.value.text = 'Error submitting comment. Please try again.'
    }
  }

  return {
    form,
    file,
    previewImage,
    fileError,
    captchaVerified,
    captchaError,
    showPreview,
    isSubmitting,
    lightboxVisible,
    currentImage,
    errors,
    htmlErrors,
    combinedErrors,
    isReply,
    validateForm,
    handleFileUpload,
    removeFile,
    onCaptchaVerified,
    togglePreview,
    openLightbox,
    handleSubmit,
    resetForm
  }
}