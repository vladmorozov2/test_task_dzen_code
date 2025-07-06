<template>
  <div class="form-group">
    <label for="comment-text">Comment*</label>
    
    <div class="editor-toolbar">
      <button 
        v-for="tag in allowedTags" 
        :key="tag.name"
        type="button" 
        @click="insertTag(tag.name)"
        :title="tag.title"
        v-html="tag.display"
      ></button>
      <button type="button" @click="insertLink" title="Link">🔗</button>
    </div>
    
    <textarea
      id="comment-text"
      ref="textarea"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :class="{ error: hasErrors }"
      rows="5"
    ></textarea>
    
    <div v-if="hasErrors" class="error-message">
      <ul>
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'CommentEditor',
  props: {
    modelValue: {
      type: String,
      required: true
    },
    errors: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const textarea = ref(null)
    const hasErrors = computed(() => props.errors.length > 0)

    const allowedTags = [
      { name: 'i', title: 'Italic', display: '<i>I</i>' },
      { name: 'strong', title: 'Bold', display: '<strong>B</strong>' },
      { name: 'code', title: 'Code', display: '<code>Code</code>' }
    ]

    const insertTag = (tag) => {
      const textareaEl = textarea.value
      if (!textareaEl) return

      const start = textareaEl.selectionStart
      const end = textareaEl.selectionEnd
      const selected = props.modelValue.substring(start, end)
      const before = props.modelValue.substring(0, start)
      const after = props.modelValue.substring(end)

      const newValue = `${before}<${tag}>${selected}</${tag}>${after}`
      emit('update:modelValue', newValue)

      // Focus and set cursor position
      setTimeout(() => {
        textareaEl.focus()
        textareaEl.selectionStart = start + tag.length + 2
        textareaEl.selectionEnd = end + tag.length + 2
      })
    }

    const insertLink = () => {
      const url = prompt('Enter the URL')
      if (!url) return

      const textareaEl = textarea.value
      if (!textareaEl) return

      const start = textareaEl.selectionStart
      const end = textareaEl.selectionEnd
      const selected = props.modelValue.substring(start, end) || 'link text'
      const before = props.modelValue.substring(0, start)
      const after = props.modelValue.substring(end)

      const newValue = `${before}<a href="${url}">${selected}</a>${after}`
      emit('update:modelValue', newValue)

      // Focus and set cursor position
      setTimeout(() => {
        textareaEl.focus()
        textareaEl.selectionStart = start + 9 + url.length
        textareaEl.selectionEnd = start + 9 + url.length + selected.length
      })
    }

    return {
      textarea,
      allowedTags,
      hasErrors,
      insertTag,
      insertLink
    }
  }
}
</script>

<style scoped>
.editor-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.editor-toolbar button {
  background: #ecf0f1;
  border: 1px solid #d6dbdf;
  border-radius: 6px;
  padding: 8px 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.editor-toolbar button:hover {
  background: #d6dbdf;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

textarea {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #fafafa;
  min-height: 150px;
  resize: vertical;
  line-height: 1.6;
}

textarea:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.15);
  background-color: #ffffff;
}

textarea.error {
  border-color: #e74c3c;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 8px;
  font-weight: 500;
}

.error-message ul {
  margin: 5px 0;
  padding-left: 20px;
}

.error-message li {
  margin-bottom: 3px;
}
</style>
