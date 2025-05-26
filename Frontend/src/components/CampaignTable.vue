<template>
  <div class="table-wrapper">
    <DataTable
      v-model:filters="filters"
      :value="ads"
      :rowClass="rowClass"
      scrollable
      scrollHeight="50vh"
      style="width: auto"
      tableStyle="min-width: max-content"
      sortMode="multiple"
      paginator
      :rows="30"
      :rowsPerPageOptions="[10, 30, 50, 100]"
      dataKey="id"
      filterDisplay="row"
      :loading="loading || analysisRunning"
    >
      <template #empty> No ads found. </template>
      <template #loading>
        <div v-if="analysisRunning">
          Running campaign analysis. Please wait...
        </div>
        <div v-if="loading">Loading campaign data. Please wait...</div>
      </template>
      <Column field="id" header="ID"> </Column>
      <Column field="has_violations" header="Violations">
        <template #body="slotProps">
          {{ renderViolations(slotProps.data.has_violations) }}
        </template>
      </Column>
      <Column field="target_audience" header="Target Audience">
        <template #body="{ data }">
          {{ data.target_audience }}
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Search by target audience"
          />
        </template>
      </Column>
      <Column field="channel_used" header="Channel" sortable>
        <template #body="{ data }">
          {{ data.channel_used }}
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Search by channel"
          />
        </template>
      </Column>
      <Column field="conversion_rate" header="Conversion Rate" sortable>
        <template #body="slotProps">
          {{ formatPercentage(slotProps.data.conversion_rate) }}
        </template>
      </Column>
      <Column field="acquisition_cost" header="Acquisition Cost" sortable>
        <template #body="slotProps">
          {{ formatCurrency(slotProps.data.acquisition_cost) }}
        </template>
      </Column>
      <Column field="roi" header="ROI" sortable />
      <Column
        field="location"
        header="Location"
        sortable
        style="min-width: 12rem"
      >
        <template #body="{ data }">
          {{ data.location }}
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Search by location"
          />
        </template>
      </Column>
      <Column field="language" header="Language" />
      <Column field="clicks" header="Clicks" />
      <Column field="impressions" header="Impressions" />
      <Column field="engagement_score" header="Engagement" />
      <Column field="ad_date" header="Date" />
      <template #footer>
        <div class="footer-wrapper">
          <div class="footer-text">
            <div class="footer-legend">
              Rows with a red background indicate ads that failed one or more
              thresholds checks.
            </div>
            <div class="footer-section" v-if="campaign?.insights">
              <strong>Insights:</strong>
              <ul>
                <li
                  v-for="(line, index) in formatTextBlock(campaign.insights)"
                  :key="`insight-${index}`"
                >
                  {{ line }}
                </li>
              </ul>
            </div>
            <div class="footer-section" v-if="campaign?.recommendations">
              <strong>Recommendations:</strong>
              <ul>
                <li
                  v-for="(line, index) in formatTextBlock(
                    campaign.recommendations
                  )"
                  :key="`rec-${index}`"
                >
                  {{ line }}
                </li>
              </ul>
            </div>
          </div>
          <div class="footer-button">
            <Button
              label="Run campaign analysis"
              severity="info"
              @click="analyzeAndReload"
            />
          </div>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getAds,
  runAnalysis,
  getCampaign,
} from "../services/automated-analysis-be";

const ads = ref([]);
const campaign = ref([]);
const filters = ref({
  location: { value: null },
  target_audience: { value: null },
  channel_used: { value: null },
});
const loading = ref(false);
const analysisRunning = ref(false);

const loadAds = async () => {
  loading.value = true;
  try {
    const data = await getAds();
    ads.value = data;
  } catch (err) {
    console.error("Error fetching data:", err);
  } finally {
    loading.value = false;
  }
};

const loadCampaign = async () => {
  loading.value = true;
  try {
    const data = await getCampaign();
    campaign.value = data;
  } catch (err) {
    console.error("Error fetching data:", err);
  } finally {
    loading.value = false;
  }
};

const analyzeAndReload = async () => {
  analysisRunning.value = true;
  try {
    await runAnalysis();
    await loadAds();
    await loadCampaign();
  } catch (err) {
    console.error("Analysis failed:", err);
  } finally {
    analysisRunning.value = false;
  }
};

onMounted(async () => {
  loading.value = true;
  try {
    await Promise.all([loadAds(), loadCampaign()]);
  } finally {
    loading.value = false;
  }
});

function formatCurrency(value) {
  const num = parseFloat(value);
  if (isNaN(num)) return "-";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  }).format(num);
}

function formatPercentage(value) {
  if (isNaN(value)) return "-";
  return `${(value * 100).toFixed(2)}%`;
}

function renderViolations(value) {
  if (value) {
    return "Yes";
  }
  return "No";
}

function rowClass(data) {
  return data.has_violations ? "row-danger" : "";
}

function formatTextBlock(text) {
  if (!text) return [];
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);
}
</script>

<style scoped>
.table-wrapper {
  width: 100%;
  padding: 0 1rem;
}

.card-footer-center {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 0;
}

:deep(.p-datatable .row-danger) {
  background-color: #ffecec !important;
}

.footer-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  padding: 1rem 0;
  flex-wrap: wrap;
}

.footer-text {
  flex: 1;
  font-size: 0.9rem;
  line-height: 1.4;
}

.footer-section {
  margin-bottom: 1rem;
}

.footer-section ul {
  padding-left: 1.25rem;
  margin: 0.25rem 0;
}

.footer-button {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.footer-legend {
  display: inline-block;
  font-size: 0.85rem;
  color: #b30000;
  background-color: #fff0f0;
  padding: 0.4rem 0.6rem;
  border-left: 4px solid #ff4d4d;
  border-radius: 4px;
  margin-bottom: 1rem;
  white-space: nowrap;
}
</style>
