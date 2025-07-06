<template>
    <div class="form-group">
        <div :id="containerId" class="recaptcha-container"></div>
        <div v-if="error" class="error-message">{{ error }}</div>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'

export default {
    name: 'RecaptchaVerifier',
    props: {
        modelValue: {
            type: String,
            default: false
        },
        error: {
            type: String,
            default: ''
        }
    },
    emits: ['update:modelValue', 'verified'],
    setup(props, { emit }) {
        const containerId = `recaptcha-container-${Math.random().toString(36).substr(2, 9)}`
        const widgetId = ref(null)

        const renderRecaptcha = () => {
            if (widgetId.value !== null) return

            widgetId.value = window.grecaptcha.render(containerId, {
                sitekey: '6Le_w3krAAAAAPQrQavEf7O4Wfs9kUmJdYYAY7u3',
                callback: onVerified,
                'expired-callback': onExpired
            })
        }

        const onVerified = (token) => {
            emit('update:modelValue', true)
            emit('verified', token)
        }

        const onExpired = () => {
            emit('update:modelValue', false)
        }

        const resetRecaptcha = () => {
            if (widgetId.value !== null) {
                window.grecaptcha.reset(widgetId.value)
            }
        }

        onMounted(() => {
            if (window.grecaptcha) {
                renderRecaptcha()
            } else {
                window.vueRecaptchaOnLoad = renderRecaptcha
            }
        })

        watch(() => props.error, (newError) => {
            if (newError) {
                resetRecaptcha()
            }
        })

        return {
            containerId
        }
    }
}
</script>

<style scoped>
.recaptcha-container {
    margin: 10px 0;
}

.error-message {
    color: #e74c3c;
    font-size: 0.9rem;
    margin-top: 8px;
    font-weight: 500;
}
</style>