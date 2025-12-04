import { api } from "../lib/axios";
import { useMutation, useQuery } from "@tanstack/react-query";

export interface CreateRFPInput {
  text: string;
  userId: string;
}

export const useCreateRfp = () => {
  return useMutation({
    mutationFn: async (data: CreateRFPInput) => {
      const res = await api.post("/rfp/create", data);
      return res.data;
    },
  });
};

export const useUserRFPs = (userId: string | null, p0: number, rowsPerPage: number) => {
  return useQuery({
    queryKey: ["rfp-list", userId],
    queryFn: async () => {
      if (!userId) return [];
      const res = await api.get(`/rfp/all/${userId}`);
      return res.data;
    },
    enabled: !!userId,
  });
};

export const useRfpById = (id: string) => {
  return useQuery({
    queryKey: ["rfp", id],
    queryFn: async () => {
      const res = await api.get(`/rfp/${id}`);
      return res.data;
    },
  });
};

export const useGenerateEmail = () => {
  return useMutation({
    mutationFn: async (body: { rfpId: string }) => {
      const res = await api.post("/rfp/generate-email", body);
      return res.data;
    },
  });
};
