import DOMPurify from 'dompurify'

// Configure allowed HTML tags and attributes
const sanitizeConfig = {
  ALLOWED_TAGS: ['b', 'strong', 'i', 'em', 'code', 'a', 'p', 'br', 'ul', 'ol', 'li'],
  ALLOWED_ATTR: ['href', 'target'],
  FORBID_ATTR: ['style', 'onclick'],
  FORBID_TAGS: ['script', 'iframe', 'style']
}

// Custom hook to modify links to open in new tab
DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName === 'A') {
    node.setAttribute('target', '_blank')
    node.setAttribute('rel', 'noopener noreferrer')
  }
})

export function sanitizeHTML(html) {
  return DOMPurify.sanitize(html, sanitizeConfig)
}

export function stripAllHTML(html) {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [],
    ALLOWED_ATTR: []
  })
}