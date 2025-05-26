<template>
  <Card class="channel-card">
    <template #title>{{ channel }}</template>
    <template #content>
      <div class="stat-section">
        <div class="stat-label">Average Conversion Rate</div>
        <div class="stat-value">{{ avgConversionRate.toFixed(2) }}%</div>
      </div>

      <div class="stat-section">
        <div class="stat-label">Average Engagement Score</div>
        <div class="stat-value">{{ avgEngagement.toFixed(2) }}</div>
      </div>
    </template>
  </Card>
</template>

<script setup>
import Card from "primevue/card";
defineProps({
  channel: String,
  avgEngagement: Number,
  avgConversionRate: Number,
});
</script>

<style scoped>
.channel-card {
  background-color: #1b1e3c;
  color: #fff;
  padding: 0.5rem;
  border-radius: 12px;
  flex: 1 1 calc(30% - 1rem);
}

.stat-section {
  margin-top: 1rem;
  text-align: center;
}

.stat-value {
  font-size: 1rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9rem;
  color: #bbb;
  margin-bottom: 0.5rem;
}
</style>
