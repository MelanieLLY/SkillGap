import api from "./auth";

export interface HistoryRecord {
  id: number;
  user_id: number;
  company_name: string | null;
  position_name: string | null;
  date_analyzed: string;
  match_score: number;
  have_skills: string[];
  missing_skills: string[];
  bonus_skills: string[];
}

export interface HistoryCreate {
  company_name?: string | null;
  position_name?: string | null;
  match_score: number;
  have_skills: string[];
  missing_skills: string[];
  bonus_skills: string[];
}

export interface HistoryUpdate {
  company_name?: string | null;
  position_name?: string | null;
}

export const historyApi = {
  getHistory: async (): Promise<HistoryRecord[]> => {
    const response = await api.get("/history/");
    return response.data;
  },

  createHistory: async (data: HistoryCreate): Promise<HistoryRecord> => {
    const response = await api.post("/history/", data);
    return response.data;
  },

  updateHistory: async (id: number, data: HistoryUpdate): Promise<HistoryRecord> => {
    const response = await api.put(`/history/${id}`, data);
    return response.data;
  },
};
