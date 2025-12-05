import { api } from "../lib/axios";
import { useMutation, useQuery } from "@tanstack/react-query";

export const useAllRfpVendors = () => {
  return useQuery({
    queryKey: ["rfp-vendors-all"],
    queryFn: async () => {
      const res = await api.get("/rfp-vendor/");
      return res.data;
    }
  });
};

export const useRfpVendorById = (id: string) => {
  return useQuery({
    queryKey: ["rfp-vendor", id],
    queryFn: async () => {
      const res = await api.get(`/rfp-vendor/${id}`);
      return res.data;
    }
  });
};


export const useLinkVendor = () => {
  return useMutation({
    mutationFn: async (data: { rfpId: string; vendorId: string }) => {
      const res = await api.post("/rfp-vendor/link", data);
      return res.data;
    },
  });
};

export const useRfpVendors = (rfpId: string) => {
  return useQuery({
    queryKey: ["rfp-vendors", rfpId],
    queryFn: async () => {
      const res = await api.get(`/rfp-vendor/rfp/${rfpId}`);
      return res.data;
    },
    enabled: !!rfpId,
  });
};

export const useUpdateRfpVendorStatus = () => {
  return useMutation({
    mutationFn: async (data: { id: string; status: string }) => {
      const res = await api.put(`/rfp-vendor/${data.id}/status`, {
        status: data.status,
      });
      return res.data;
    },
  });
};

export const useDeleteRfpVendor = () => {
  return useMutation({
    mutationFn: async (id: string) => {
      const res = await api.delete(`/rfp-vendor/${id}`);
      return res.data;
    },
  });
};

// Fetch single RFPVendor
export const useRfpVendor = (id: string) => {
  return useQuery({
    queryKey: ["rfp-vendor", id],
    queryFn: async () => {
      const res = await api.get(`/rfp-vendor/detail/${id}`);
      return res.data;
    },
  });
};

export const useRfpVendorList = () => {
  return useQuery({
    queryKey: ["rfp-vendor-list"],
    queryFn: async () => {
      const res = await api.get("/rfp-vendor/");
      return res.data;
    },
  });
};

export const useRfpVendorTree = () => {
  return useQuery({
    queryKey: ["rfp-vendor-tree"],
    queryFn: async () => {
      const res = await api.get("/rfp-vendor/vendor-tree");
      return res.data;
    }
  });
};