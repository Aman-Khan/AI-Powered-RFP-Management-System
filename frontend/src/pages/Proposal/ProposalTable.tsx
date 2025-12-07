import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Collapse,
  FormControlLabel,
  IconButton,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import RecommendationDrawer from "../../components/Recommendation/RecommendationDrawer";
import RecommendIcon from "@mui/icons-material/Recommend";


import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";

import { useAllRfps } from "../../api/rfp"; // Fetch /rfps-tree

export default function ProposalTable() {
  const { data, isLoading } = useAllRfps();
  const [openRfp, setOpenRfp] = useState<string | null>(null);
  // openVendorByRfp maps rfpId -> opened vendorId (or null)
  const [openVendorByRfp, setOpenVendorByRfp] = useState<Record<string, string | null>>({});
  // viewMode per proposal id (true = table view, false = JSON view)
  const [viewMode, setViewMode] = useState<Record<string, boolean>>({});
  const [selectedRfpId, setSelectedRfpId] = useState<string | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const openRecommendation = (rfpId: string) => {
    setSelectedRfpId(rfpId);
    setDrawerOpen(true);
  };

  if (isLoading) return <div>Loading...</div>;

  const toggleVendor = (rfpId: string, vendorId: string) => {
    setOpenVendorByRfp(prev => {
      const current = prev[rfpId] ?? null;
      return { ...prev, [rfpId]: current === vendorId ? null : vendorId };
    });
  };

  return (
    <Box>
      <Typography variant="h4" mb={2}>
        RFP Proposal Overview
      </Typography>

      <Card>
        <CardContent>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell />
                <TableCell><strong>RFP Title</strong></TableCell>
                <TableCell><strong>Vendor</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell><strong>Submitted At</strong></TableCell>
                <TableCell><strong>Proposals</strong></TableCell>
                <TableCell><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {data?.map((rfp: any) => {
                const rfpExpanded = openRfp === rfp.id;
                const anyProposals = (rfp.rfpVendors || []).some((rv: any) => (rv.proposals || []).length > 0);

                return (
                  <React.Fragment key={`rfp-${rfp.id}`}>
                    {/* RFP Row */}
                    <TableRow key={`rfp-row-${rfp.id}`}>
                      <TableCell>
                        <IconButton onClick={() => setOpenRfp(rfpExpanded ? null : rfp.id)}>
                          {rfpExpanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                        </IconButton>
                      </TableCell>

                      <TableCell colSpan={2}>
                        <strong>{rfp.title}</strong>
                      </TableCell>

                      <TableCell>
                        <Chip label={rfp.status ?? "—"} color="primary" size="small" />
                      </TableCell>

                      <TableCell>
                        {new Date(rfp.createdAt).toLocaleString()}
                      </TableCell>

                      <TableCell>
                        {rfp.rfpVendors?.reduce((acc: number, v: any) => acc + ((v.proposals?.length) || 0), 0) || 0}
                      </TableCell>

                      <TableCell>
                        {rfp.rfpVendors.some((v: any) => v.proposals?.length > 0) && (
                          <Chip
                            label="Recommendation"
                            color="secondary"
                            icon={<RecommendIcon />}
                            onClick={() => openRecommendation(rfp.id)}
                            sx={{ cursor: "pointer" }}
                          />
                        )}
                      </TableCell>

                    </TableRow>

                    {/* Expanded RFP -> Vendors */}
                    <TableRow key={`rfp-expand-${rfp.id}`}>
                      <TableCell colSpan={7} style={{ paddingBottom: 0, paddingTop: 0 }}>
                        <Collapse in={rfpExpanded} timeout="auto" unmountOnExit>
                          <Box ml={4} mt={2}>
                            {(rfp.rfpVendors || []).map((rv: any) => {
                              const vendorExpanded = (openVendorByRfp[rfp.id] ?? null) === rv.id;
                              const hasProposal = (rv.proposals?.length || 0) > 0;

                              return (
                                <React.Fragment key={`rv-${rv.id}`}>
                                  {/* Vendor Row */}
                                  <TableRow key={`rv-row-${rv.id}`}>
                                    <TableCell>
                                      <IconButton onClick={() => toggleVendor(rfp.id, rv.id)}>
                                        {vendorExpanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                                      </IconButton>
                                    </TableCell>

                                    <TableCell />

                                    <TableCell>
                                      {rv.vendor?.name}
                                      {hasProposal && (
                                        <Chip
                                          label="Proposal Received"
                                          color="success"
                                          size="small"
                                          sx={{ ml: 1 }}
                                        />
                                      )}
                                    </TableCell>

                                    <TableCell>
                                      <Chip label={rv.status ?? "—"} color="primary" size="small" />
                                    </TableCell>

                                    <TableCell>
                                      {rv.sentAt ? new Date(rv.sentAt).toLocaleString() : "-"}
                                    </TableCell>

                                    <TableCell>{rv.proposals?.length || 0}</TableCell>

                                    {/* <TableCell>
                                      <Button
                                        size="small"
                                        onClick={() => console.log("Open vendor detail", rv.id)}
                                      >
                                        Open
                                      </Button>
                                    </TableCell> */}
                                  </TableRow>

                                  {/* Proposals list for vendor */}
                                  <TableRow key={`rv-proposals-${rv.id}`}>
                                    <TableCell colSpan={7} style={{ paddingBottom: 0, paddingTop: 0 }}>
                                      <Collapse in={vendorExpanded} timeout="auto" unmountOnExit>
                                        <Box ml={4} mt={1}>
                                          {(!rv.proposals || rv.proposals.length === 0) && (
                                            <Typography variant="body2"><em>No proposals submitted yet.</em></Typography>
                                          )}

                                          {(rv.proposals || []).map((proposal: any) => {
                                            const mode = viewMode[proposal.id] ?? false; // false => JSON view

                                            return (
                                              <Box
                                                key={`proposal-${proposal.id}`}
                                                sx={{
                                                  border: "1px solid #ccc",
                                                  borderRadius: 2,
                                                  p: 2,
                                                  mb: 2,
                                                  bgcolor: "#f9f9f9",
                                                }}
                                              >
                                                <Typography variant="subtitle2">
                                                  Submitted At:{" "}
                                                  {proposal.submittedAt ? new Date(proposal.submittedAt).toLocaleString() : "-"}
                                                </Typography>

                                                {/* Toggle JSON/Table View */}
                                                <FormControlLabel
                                                  control={
                                                    <Switch
                                                      checked={mode}
                                                      onChange={() =>
                                                        setViewMode(prev => ({ ...prev, [proposal.id]: !mode }))
                                                      }
                                                    />
                                                  }
                                                  label={mode ? "Table View" : "JSON View"}
                                                  sx={{ mt: 1 }}
                                                />

                                                {/* JSON VIEW */}
                                                {!mode && (
                                                  <Box
                                                    sx={{
                                                      mt: 1,
                                                      p: 1,
                                                      bgcolor: "#e0f7fa",
                                                      borderRadius: 1,
                                                      fontFamily: "monospace",
                                                      whiteSpace: "pre-wrap",
                                                      wordBreak: "break-word",
                                                    }}
                                                  >
                                                    {proposal.extractedData
                                                      ? JSON.stringify(proposal.extractedData, null, 2)
                                                      : "(No extracted data)"}
                                                  </Box>
                                                )}

                                                {/* TABLE VIEW */}
                                                {mode && (
                                                  <Box mt={2}>
                                                    <Typography variant="subtitle1" fontWeight={700}>
                                                      Items
                                                    </Typography>

                                                    <Table size="small">
                                                      <TableHead>
                                                        <TableRow>
                                                          <TableCell><strong>Name</strong></TableCell>
                                                          <TableCell><strong>Qty</strong></TableCell>
                                                          <TableCell><strong>Unit Price</strong></TableCell>
                                                          <TableCell><strong>Total</strong></TableCell>
                                                        </TableRow>
                                                      </TableHead>
                                                      <TableBody>
                                                        {(proposal.extractedData?.items || []).map((item: any, idx: number) => (
                                                          <TableRow key={`item-${proposal.id}-${idx}`}>
                                                            <TableCell>{item.name ?? "-"}</TableCell>
                                                            <TableCell>{item.quantity ?? "-"}</TableCell>
                                                            <TableCell>{item.unit_price ?? "-"}</TableCell>
                                                            <TableCell>{item.total_price ?? "-"}</TableCell>
                                                          </TableRow>
                                                        ))}
                                                      </TableBody>
                                                    </Table>

                                                    <Box mt={2}>
                                                      <Typography><strong>Total Price:</strong> {proposal.extractedData?.total_price ?? "-"}</Typography>
                                                      <Typography><strong>Warranty:</strong> {proposal.extractedData?.warranty ?? "-"}</Typography>
                                                      <Typography><strong>Payment Terms:</strong> {proposal.extractedData?.payment_terms ?? "-"}</Typography>
                                                      <Typography><strong>Notes:</strong> {proposal.extractedData?.notes ?? "-"}</Typography>
                                                    </Box>
                                                  </Box>
                                                )}
                                              </Box>
                                            );
                                          })}
                                        </Box>
                                      </Collapse>
                                    </TableCell>
                                  </TableRow>
                                </React.Fragment>
                              );
                            })}
                          </Box>
                        </Collapse>
                      </TableCell>
                    </TableRow>
                  </React.Fragment>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
      <RecommendationDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        rfpId={selectedRfpId}
      />

    </Box>
  );
}

