import api from '../axios'

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