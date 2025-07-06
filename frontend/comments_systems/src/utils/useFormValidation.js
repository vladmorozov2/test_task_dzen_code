import { ref } from 'vue'
import { sanitizeHTML } from '@/utils/htmlSanitizer'

export function useFormValidation(form) {
  const errors = ref({})
  const htmlErrors = ref([])

  const validateForm = () => {
    errors.value = {}
    htmlErrors.value = []

    // Required field validation
    if (!form.value.text?.trim()) {
      errors.value.text = 'Comment text is required.'
    }

    // HTML content validation
    validateHTMLContent(form.value.text)

    return Object.keys(errors.value).length === 0 && htmlErrors.value.length === 0
  }

  const validateHTMLContent = (html) => {
    const forbiddenPatterns = [
      { pattern: /<script/i, message: 'Script tags are not allowed' },
      { pattern: /on\w+\s*=/i, message: 'Event handlers are not allowed' },
      { pattern: /javascript:/i, message: 'JavaScript URLs are not allowed' }
    ]

    forbiddenPatterns.forEach(({ pattern, message }) => {
      if (pattern.test(html)) {
        htmlErrors.value.push(message)
      }
    })

    // Sanitize the content for preview
    return sanitizeHTML(html)
  }

  const resetValidation = () => {
    errors.value = {}
    htmlErrors.value = []
  }

  return {
    errors,
    htmlErrors,
    validateForm,
    resetValidation
  }
}