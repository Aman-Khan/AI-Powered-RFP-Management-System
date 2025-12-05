import { api } from "../lib/axios";
import { useMutation } from "@tanstack/react-query";

export const useSendEmail = () => {
  return useMutation({
    mutationFn: async (payload: {
      rfpId: string;
      vendorIds: string[];
      subject: string;
      content: string;
    }) => {
      const res = await api.post("/email/send", payload);
      return res.data;
    },
  });
};
