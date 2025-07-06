import api from '@/axios'

export async function fetchComments({ page, perPage, sort }) {
    const response = await api.get('/api/comments/', {
        params: {
            page,
            per_page: perPage,
            sort_by: sort.field,
            sort_dir: sort.direction,
        },
    })
    return response.data
}

export async function submitComment(commentData) {
    const formData = new FormData()

    // Add text content
    formData.append('text', commentData.text)

    // Add parent comment ID if it's a reply
    if (commentData.parentId) {
        formData.append('parent_comment', commentData.parentId)
    }

    // Add file attachment if present
    if (commentData.file) {
        formData.append('attachment', commentData.file)
    }

    formData.append('captcha', commentData.captchaToken)

    try {
        const response = await api.post('/api/comments/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        return response.data
    } catch (error) {
        if (error.response) {
            // Handle server validation errors
            if (error.response.status === 400) {
                throw new Error('Validation error: ' + JSON.stringify(error.response.data))
            }
            throw new Error(`Server error: ${error.response.status}`)
        } else if (error.request) {
            throw new Error('Network error - no response received')
        } else {
            throw new Error('Request setup error: ' + error.message)
        }
    }
}
