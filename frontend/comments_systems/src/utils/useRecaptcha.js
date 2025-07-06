import { ref, onMounted, onUnmounted } from 'vue'

export function useRecaptcha(containerId) {
  const widgetId = ref(null)
  const isVerified = ref(false)
  const error = ref('')
  const token = ref('')

  const renderRecaptcha = () => {
    if (widgetId.value !== null || !window.grecaptcha) return

    try {
      widgetId.value = window.grecaptcha.render(containerId, {
        sitekey: '6Le_w3krAAAAAPQrQavEf7O4Wfs9kUmJdYYAY7u3',
        callback: onSuccess,
        'error-callback': onError,
        'expired-callback': onExpired,
        size: 'normal'
      })
    } catch (err) {
      console.error('reCAPTCHA render error:', err)
      error.value = 'Failed to initialize CAPTCHA'
    }
  }

  const onSuccess = (recaptchaToken) => {
    token.value = recaptchaToken
    isVerified.value = true
    error.value = ''
  }

  const onError = () => {
    error.value = 'CAPTCHA verification failed'
    isVerified.value = false
    token.value = ''
  }

  const onExpired = () => {
    error.value = 'CAPTCHA verification expired'
    isVerified.value = false
    token.value = ''
  }

  const resetRecaptcha = () => {
    if (widgetId.value !== null && window.grecaptcha) {
      window.grecaptcha.reset(widgetId.value)
    }
    isVerified.value = false
    token.value = ''
  }

  const loadRecaptchaScript = () => {
    if (window.grecaptcha) {
      renderRecaptcha()
      return
    }

    const script = document.createElement('script')
    script.src = 'https://www.google.com/recaptcha/api.js?onload=vueRecaptchaOnLoad&render=explicit'
    script.async = true
    script.defer = true
    document.head.appendChild(script)

    window.vueRecaptchaOnLoad = renderRecaptcha
  }

  onMounted(() => {
    loadRecaptchaScript()
  })

  onUnmounted(() => {
    if (window.vueRecaptchaOnLoad) {
      delete window.vueRecaptchaOnLoad
    }
  })

  return {
    isVerified,
    token,
    error,
    resetRecaptcha
  }
}