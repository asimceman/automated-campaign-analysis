<template>
  <div class="chart-container">
    <div class="chart-header">
      <div class="chart-controls">
        <select v-model="interval" @change="updateChart">
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
        </select>
      </div>
    </div>
    <Chart
      ref="chartRef"
      type="line"
      :data="chartData"
      :options="chartOptions"
      style="height: 100%; width: 90%"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { getAds } from "../services/automated-analysis-be";
import dayjs from "dayjs";
import isoWeek from "dayjs/plugin/isoWeek";
dayjs.extend(isoWeek);

const interval = ref("daily");
const ads = ref([]);
const chartData = ref({});
const chartOptions = ref({});
const chartRef = ref(null);

onMounted(async () => {
  const data = await getAds();
  ads.value = data;
  updateChart();
});

function updateChart() {
  const grouped = groupAds(ads.value, interval.value);

  const labels = Object.keys(grouped);
  const conversionRates = Object.values(grouped);

  chartData.value = {
    labels,
    datasets: [
      {
        label: "Conversion Rate",
        data: conversionRates,
        borderColor: "#42A5F5",
        tension: 0.3,
        fill: false,
      },
    ],
  };

  chartOptions.value = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: "top" } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: (val) => `${val}%` },
      },
      x: {
        ticks: {
          maxRotation: 90,
          minRotation: 45,
        },
      },
    },
  };

  nextTick(() => {
    chartRef.value?.chart?.resize();
  });
}

function groupAds(data, type) {
  const grouped = {};

  for (const entry of data) {
    const date = dayjs(entry.ad_date);

    const key =
      type === "weekly"
        ? `${date.year()}-W${date.isoWeek().toString().padStart(2, "0")}`
        : date.format("YYYY-MM-DD");

    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(entry.conversion_rate * 100);
  }

  for (const key in grouped) {
    const values = grouped[key];
    grouped[key] = +(values.reduce((a, b) => a + b, 0) / values.length).toFixed(
      2
    );
  }

  return grouped;
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  position: relative;
  padding: 1rem;
  gap: 0.5rem;
}

.chart-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 0.5rem;
}

.chart-controls select {
  padding: 0.4rem 0.6rem;
  font-size: 0.9rem;
  border-radius: 4px;
}

@media (max-width: 900px) {
  .summary-section {
    flex-direction: column;
  }

  .cards-grid,
  .chart-wrapper {
    width: 100%;
  }
}
</style>
