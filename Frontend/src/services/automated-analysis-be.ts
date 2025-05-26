import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8888",
});

export async function getAds(): Promise<any> {
  try {
    const { data } = await api.get("/ads/all");
    return data;
  } catch (error: any) {
    if (error?.response?.data?.error?.code === "RESOURCE_NOT_FOUND") {
      return {};
    } else {
      throw error;
    }
  }
}

export async function runAnalysis(): Promise<any> {
  try {
    const { data } = await api.post("/ads/analyze-dataset", null, {
      params: { campaign_id: 1 },
    });
    return data;
  } catch (error: any) {
    if (error?.response?.data?.error?.code === "RESOURCE_NOT_FOUND") {
      return {};
    } else {
      throw error;
    }
  }
}

export async function getChannelSummaries(): Promise<any> {
  try {
    const { data } = await api.get("/ads/channel-summary", {
      params: { campaign_id: 1 },
    });
    return data;
  } catch (error: any) {
    if (error?.response?.data?.error?.code === "RESOURCE_NOT_FOUND") {
      return {};
    } else {
      throw error;
    }
  }
}

export async function getCampaign(): Promise<any> {
  try {
    const { data } = await api.get("/campaigns", {
      params: { id: 1 },
    });
    return data;
  } catch (error: any) {
    if (error?.response?.data?.error?.code === "RESOURCE_NOT_FOUND") {
      return {};
    } else {
      throw error;
    }
  }
}
