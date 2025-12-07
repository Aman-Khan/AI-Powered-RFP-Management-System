import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableRow,
  TableHead,
  TableCell,
  TableBody,
  IconButton,
  Collapse,
  Chip,
} from "@mui/material";

import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";

import { useAllRfps } from "../../api/rfp"; // Fetch /rfps-tree
import { useState } from "react";
import React from "react";

export default function ProposalTable() {
  const { data, isLoading } = useAllRfps();
  const [openRfp, setOpenRfp] = useState<string | null>(null);
  const [openVendor, setOpenVendor] = useState<string | null>(null);

  if (isLoading) return <div>Loading...</div>;
  console.log(data)
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
              </TableRow>
            </TableHead>

            <TableBody>
              {data?.map((rfp: any) => {
                const rfpExpanded = openRfp === rfp.id;

                return (
                  <React.Fragment key={rfp.id}>
                    {/* RFP Row */}
                    <TableRow>
                      <TableCell>
                        <IconButton onClick={() => setOpenRfp(rfpExpanded ? null : rfp.id)}>
                          {rfpExpanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                        </IconButton>
                      </TableCell>
                      <TableCell colSpan={4}><strong>{rfp.title}</strong></TableCell>
                    </TableRow>

                    {/* RFPVendors Collapse */}
                    <TableRow>
                      <TableCell colSpan={5} style={{ paddingBottom: 0, paddingTop: 0 }}>
                        <Collapse in={rfpExpanded} timeout="auto" unmountOnExit>
                          <Box ml={4} mt={2}>
                            {rfp.rfpVendors?.map((rv: any) => {
                              const vendorExpanded = openVendor === rv.id;
                              return (
                                <React.Fragment key={rv.id}>
                                  {/* RFPVendor Row */}
                                  <TableRow>
                                    <TableCell>
                                      <IconButton onClick={() => setOpenVendor(vendorExpanded ? null : rv.id)}>
                                        {vendorExpanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                                      </IconButton>
                                    </TableCell>
                                    <TableCell />
                                    <TableCell>{rv.vendor?.name}</TableCell>
                                    <TableCell>
                                      <Chip label={rv.status} color="primary" />
                                    </TableCell>
                                    <TableCell>
                                      {rv.sentAt ? new Date(rv.sentAt).toLocaleString() : "-"}
                                    </TableCell>
                                  </TableRow>

                           {/* Proposals Collapse */}
<TableRow>
  <TableCell colSpan={5} style={{ paddingBottom: 0, paddingTop: 0 }}>
    <Collapse in={vendorExpanded} timeout="auto" unmountOnExit>
      <Box ml={4} mt={1}>
        {rv.proposals?.length === 0 && (
          <Typography variant="body2"><em>No proposals submitted yet.</em></Typography>
        )}
        {rv.proposals?.map((proposal: any) => (
          <Box
            key={proposal.id}
            sx={{
              border: "1px solid #ccc",
              borderRadius: 2,
              p: 1,
              mb: 1,
              bgcolor: "#f9f9f9",
            }}
          >
            <Typography variant="subtitle2">
              Submitted At: {new Date(proposal.submittedAt).toLocaleString()}
            </Typography>

            {/* Display extractedData JSON */}
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
          </Box>
        ))}
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
    </Box>
  );
}
