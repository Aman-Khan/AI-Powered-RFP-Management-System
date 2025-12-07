import { Drawer, CircularProgress, Box, Chip, Typography } from "@mui/material";
// Removed useEffect and useState imports, as useRecommendation handles them
// import { useEffect, useState } from "react"; 

import { useRecommendation } from "../../api/useRecommendation"; // Adjust import path as needed

// ... (Interface definitions remain the same, but they are now in useRecommendation.ts)

export default function RecommendationDrawer({ open, onClose, rfpId }: any) {
  // 1. Replace data fetching logic with the custom hook
  const { data: recommendation, isLoading, isError } = useRecommendation(rfpId, open);

  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box width={480} p={3}>
        <Typography variant="h5" fontWeight={700}>
          AI Vendor Recommendation
        </Typography>

        {/* 2. Update loading state check */}
        {isLoading && (
          <Box display="flex" justifyContent="center" mt={4}>
            <CircularProgress />
          </Box>
        )}
        
        {/* 3. Check for successful data retrieval */}
        {!isLoading && recommendation && (
          <>
            <Box mt={2}>
              <Typography variant="subtitle1" fontWeight={700}>
                Summary
              </Typography>
              <Typography>{recommendation.comparison_summary}</Typography>
            </Box>

            <Box mt={3}>
              <Typography variant="h6">Vendor Rankings</Typography>
              
              {/* Data is always present here due to TypeScript type safety 
                  and the main recommendation check, but the fix (|| []) 
                  is still good defensive coding for the API response. */}
              {(recommendation.vendors_ranked || []).map((v: any, idx: number) => (
                <Box
                  key={idx}
                  p={2}
                  mt={1}
                  border="1px solid #ddd"
                  borderRadius={2}
                  bgcolor="#fafafa"
                >
                  <Typography variant="subtitle1" fontWeight={700}>
                    {v.vendor_name} — Score: {v.score}
                  </Typography>

                  <Typography>Price Total: {v.price_total ?? "-"}</Typography>
                  <Typography>Delivery Match: {v.delivery_match}</Typography>
                  <Typography>Warranty Match: {v.warranty_match}</Typography>
                  <Typography>Payment Terms Match: {v.payment_terms_match}</Typography>
                  <Typography>Item Coverage: {v.item_coverage_score}</Typography>

                  <Typography sx={{ mt: 1 }} fontStyle="italic">
                    {v.notes}
                  </Typography>
                </Box>
              ))}
            </Box>

            <Box mt={3}>
              <Typography variant="h6">Recommended Vendor</Typography>
              <Chip label={recommendation.recommended_vendor} color="success" />
            </Box>
          </>
        )}
        
        {/* 4. Update error and no data messages */}
        {isError && (
            <Typography mt={2} color="error">An error occurred while fetching recommendations.</Typography>
        )}

        {!isLoading && !recommendation && rfpId && !isError && (
            <Typography mt={2} color="textSecondary">No recommendation data found for this RFP.</Typography>
        )}
      </Box>
    </Drawer>
  );
}