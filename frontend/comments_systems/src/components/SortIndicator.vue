<template>
  <span class="sort-indicator">
    <span v-if="currentField === field">
      {{ direction === 'asc' ? '↑' : '↓' }}
    </span>
  </span>
</template>

<script>
export default {
  name: 'SortIndicator',
  props: {
    field: String,
    currentField: String,
    direction: String
  }
}
</script>

<style scoped>
.sort-indicator {
  margin-left: 5px;
  font-weight: bold;
}
</style>