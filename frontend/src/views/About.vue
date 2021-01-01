<template>
  <div class="about">
    <h1 v-for="(director, index) in directors" :key="index">{{ director.name }}</h1>
  </div>
</template>

<script>
import directorsAPI from '@/api/directors';
export default {
  name: 'Directors',
  data() {
    return {
      directors: []
    };
  },
  async mounted() {
    this.directors = await directorsAPI.getDirectors();
  }
};
</script>

<style>
  
</style>
