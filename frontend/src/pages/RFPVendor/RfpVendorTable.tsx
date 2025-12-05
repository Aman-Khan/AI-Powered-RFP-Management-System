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

import { useAllRfpVendors } from "../../api/rfpVendor";
import { useState } from "react";

export default function RfpVendorTable() {
  const { data, isLoading } = useAllRfpVendors();
  const [openRow, setOpenRow] = useState<string | null>(null);

  if (isLoading) return <div>Loading...</div>;

  return (
    <Box>
      <Typography variant="h4" mb={2}>
        RFP Vendor Overview
      </Typography>

      <Card>
        <CardContent>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell />
                <TableCell><strong>Vendor</strong></TableCell>
                <TableCell><strong>RFP Title</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell><strong>Sent At</strong></TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {data?.map((rv: any) => {
                const expanded = openRow === rv.id;

                return (
                  <>
                    <TableRow key={rv.id}>
                      <TableCell>
                        <IconButton onClick={() => setOpenRow(expanded ? null : rv.id)}>
                          {expanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                        </IconButton>
                      </TableCell>

                      <TableCell>{rv.vendor?.name}</TableCell>
                      <TableCell>{rv.rfp?.title}</TableCell>

                      <TableCell>
                        <Chip label={rv.status} color="primary" />
                      </TableCell>

                      <TableCell>
                        {rv.sentAt ? new Date(rv.sentAt).toLocaleString() : "-"}
                      </TableCell>
                    </TableRow>

                    {/* -------- EXPANDED DETAIL ROW -------- */}
                    <TableRow>
                      <TableCell colSpan={5} style={{ paddingBottom: 0, paddingTop: 0 }}>
                        <Collapse in={expanded} timeout="auto" unmountOnExit>
                          <Box m={2}>
                            <Typography variant="h6">Details</Typography>

                            <Box mt={1}>
                              <strong>Vendor Email:</strong> {rv.vendor?.email}
                            </Box>

                            <Box mt={1}>
                              <strong>RFP Description:</strong>
                              <div>{rv.rfp?.description}</div>
                            </Box>

                            <Box mt={2}>
                              <Typography variant="subtitle1">Email Logs</Typography>
                              {rv.emailLogs?.length === 0 && <em>No emails yet</em>}
                              {rv.emailLogs?.map((log: any) => (
                                <Box key={log.id} sx={{ mt: 1, p: 1, borderLeft: "3px solid #1976d2" }}>
                                  <strong>{log.subject}</strong>
                                  <div dangerouslySetInnerHTML={{ __html: log.body }} />
                                  <div style={{ fontSize: "12px", color: "#666" }}>
                                    {new Date(log.createdAt).toLocaleString()}
                                  </div>
                                </Box>
                              ))}
                            </Box>

                            <Box mt={2}>
                              <Typography variant="subtitle1">Proposals</Typography>
                              {rv.proposals?.length === 0 && <em>No proposals yet</em>}
                              {rv.proposals?.map((p: any) => (
                                <Box key={p.id} sx={{ mt: 1, p: 1, bgcolor: "#f5f5f5", borderRadius: 1 }}>
                                  <div><strong>Submitted:</strong> {new Date(p.submittedAt).toLocaleString()}</div>
                                  <div><strong>Raw:</strong> {p.rawText}</div>
                                </Box>
                              ))}
                            </Box>
                          </Box>
                        </Collapse>
                      </TableCell>
                    </TableRow>
                  </>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </Box>
  );
}
