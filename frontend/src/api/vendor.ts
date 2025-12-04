// src/api/vendor.ts
import { api } from "../lib/axios";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Fetch vendors with pagination + search
export const useVendors = (page: number, limit: number, search: string) => {
  return useQuery({
    queryKey: ["vendors", page, limit, search],
    queryFn: async () => {
      const res = await api.get("/vendor/", {
        params: {
          skip: page * limit,
          limit,
          search,
        },
      });
      return res.data;
    },
  });
};

// Add vendor
export const useAddVendor = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (body: { name: string; email?: string; phone?: string }) =>
      api.post("/vendor/add", body),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["vendors"] }),
  });
};

// Update vendor
export const useUpdateVendor = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: any) =>
      api.put(`/vendor/${payload.id}`, payload.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["vendors"] }),
  });
};

// Delete vendor
export const useDeleteVendor = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => api.delete(`/vendor/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["vendors"] }),
  });
};
