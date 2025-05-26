<template>
  <main class="dashboard-layout">
    <h2>{{ campaign.name }}</h2>
    <CampaignTable />
    <div class="summary-section">
      <div class="cards-grid">
        <ChannelCard
          v-for="summary in channelSummaries"
          :key="summary.channel"
          :channel="summary.channel"
          :avgEngagement="summary.average_engagement_score"
          :avgConversionRate="summary.average_conversion_rate"
        />
      </div>
      <div class="chart-wrapper">
        <LineChart />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import CampaignTable from "./components/CampaignTable.vue";
import ChannelCard from "./components/ChannelCard.vue";
import LineChart from "./components/LineChart.vue";
import {
  getChannelSummaries,
  getCampaign,
} from "./services/automated-analysis-be";

const channelSummaries = ref([]);
const campaign = ref([]);

const loadChannelSummaries = async () => {
  try {
    const data = await getChannelSummaries();
    channelSummaries.value = data;
  } catch (err) {
    console.error("Error fetching data:", err);
  }
};

const loadCampaign = async () => {
  try {
    const data = await getCampaign();
    campaign.value = data;
  } catch (err) {
    console.error("Error fetching data:", err);
  }
};

onMounted(async () => {
  loadCampaign();
  loadChannelSummaries();
});
</script>

<style scoped>
body,
html,
#app {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-layout {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  padding: 2rem;
  box-sizing: border-box;
  background-color: #f8f8f8;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1.5rem;
  overflow-y: auto;
  padding-top: 0;
}

.summary-section {
  display: flex;
  gap: 2rem;
  width: 100vw;
  align-items: stretch;
  padding-bottom: 1rem;
}

.chart-wrapper {
  width: 60%;
  min-height: 400px;
  display: flex;
  align-items: stretch;
  justify-content: stretch;
}

.cards-grid {
  width: 40%;
  height: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-left: 2rem;
  margin-bottom: 1rem;
}
</style>
