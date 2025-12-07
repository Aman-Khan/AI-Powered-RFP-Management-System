import { useQuery } from '@tanstack/react-query';
// Assuming 'api' is your configured axios instance
// You might need to adjust the import path for 'api'
import { api } from "../lib/axios"; 

// --- Interface Definitions (Copied from your component) ---

interface VendorRanking {
  vendor_name: string;
  score: number;
  price_total: string | number;
  delivery_match: string;
  warranty_match: string;
  payment_terms_match: string;
  item_coverage_score: number;
  notes: string;
}

interface Recommendation {
  comparison_summary: string;
  vendors_ranked: VendorRanking[];
  recommended_vendor: string;
}

// --- Custom Hook ---

/**
 * Fetches AI vendor recommendation data for a specific RFP.
 * @param rfpId The ID of the RFP to fetch recommendations for.
 * @param enabled Whether the query should be run (e.g., drawer is open).
 */
export const useRecommendation = (rfpId: string | null, enabled: boolean) => {
  return useQuery<Recommendation, Error>({
    // Query key: Ensures data is re-fetched when rfpId changes
    queryKey: ['rfpRecommendation', rfpId], 
    
    // Query function: Performs the API call
    queryFn: async () => {
      if (!rfpId) {
        throw new Error("RFP ID is required for recommendation query.");
      }
      // Use the api instance to make the GET request
      const response = await api.get<Recommendation>(`/recommendation/${rfpId}`);
      return response.data;
    },
    
    // Enable/Disable the query: Only run when rfpId is present AND the drawer is open
    enabled: !!rfpId && enabled, 
    
    // Optional: Keep the data fresh for 5 minutes
    staleTime: 1000 * 60 * 5, 
  });
};