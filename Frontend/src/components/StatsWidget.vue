<template>
  <div class="stats-container">
    <div class="stat-box">
      <h4>Avg. Conversion Rate</h4>
      <p>{{ (stats.conversionRate * 100).toFixed(2) }}%</p>
    </div>
    <div class="stat-box">
      <h4>Avg. Engagement Score</h4>
      <p>{{ stats.engagementScore.toFixed(2) }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: Object,
});
</script>

<style scoped>
.stats-container {
  display: flex;
  flex-direction: column;
  width: 50%;
  height: 100%;
  justify-content: space-between;
}

.stat-box {
  height: 40%;
  padding: 1rem 2rem;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-box h4 {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.stat-box p {
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0;
  color: #222;
}
</style>
