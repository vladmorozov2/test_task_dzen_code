<template>
  <div class="comment-form">
    <h2>{{ isReply ? 'Reply to Comment' : 'Add New Comment' }}</h2>

    <form @submit.prevent="handleSubmit">
      <CommentEditor
        v-model="form.text"
        :errors="combinedErrors"
        @insert-tag="insertTag"
        @insert-link="insertLink"
      />

      <FileUploader
        v-model="file"
        :preview-image="previewImage"
        :error="fileError"
        @remove="removeFile"
        @preview-click="openLightbox"
      />

      <RecaptchaVerifier
        v-model="captchaVerified"
        :error="captchaError"
        @verified="onCaptchaVerified"
      />

      <div class="form-actions">
        <button
          type="button"
          @click="togglePreview"
          class="preview-btn"
        >
          {{ showPreview ? 'Hide Preview' : 'Show Preview' }}
        </button>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="submit-btn"
        >
          {{ isSubmitting ? 'Submitting...' : 'Submit Comment' }}
        </button>

        <button
          v-if="isReply"
          type="button"
          @click="$emit('cancel')"
          class="cancel-btn"
        >
          Cancel Reply
        </button>
      </div>

      <CommentPreview
        v-if="showPreview"
        :text="form.text"
        :preview-image="previewImage"
        :attachment="file"
        @preview-click="openLightbox"
      />
    </form>

    <Lightbox
      v-if="lightboxVisible"
      :image-url="currentImage"
      @close="lightboxVisible = false"
    />
  </div>
</template>

<script>
import CommentEditor from './CommentEditor.vue'
import FileUploader from './FileUploader.vue'
import CommentPreview from './CommentPreview.vue'
import RecaptchaVerifier from './RecaptchaVerifier.vue'
import Lightbox from './Lightbox.vue'
import { useCommentForm } from '@/composables/useCommentForm'

export default {
  name: 'CommentForm',
  components: {
    CommentEditor,
    FileUploader,
    CommentPreview,
    RecaptchaVerifier,
    Lightbox
  },
  props: {
    parentId: {
      type: Number,
      default: null
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const {
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
      insertTag,
      insertLink
    } = useCommentForm(props, emit)

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
      insertTag,
      insertLink
    }
  }
}
</script>

<style scoped>
.comment-form {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  margin-bottom: 40px;
  border: 1px solid #eaeaea;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.comment-form:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

.comment-form h2 {
  color: #2c3e50;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 1.8rem;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 25px;
}

.preview-btn {
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 18px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.preview-btn:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

.submit-btn {
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 14px 28px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none !important;
}

.submit-btn:not(:disabled):hover {
  background: #27ae60;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
}

.cancel-btn {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 14px 28px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .comment-form {
    padding: 20px;
  }

  .form-actions {
    flex-direction: column;
  }

  .submit-btn,
  .cancel-btn {
    width: 100%;
    padding: 16px;
  }
}
</style>