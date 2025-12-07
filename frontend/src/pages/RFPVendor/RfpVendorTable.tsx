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
                          <Box mt={3}>
                            <Typography variant="h6" fontWeight={700}>
                              Email Conversation
                            </Typography>

                            {rv.emailLogs?.length === 0 && (
                              <Box mt={1}>
                                <em>No email communication yet.</em>
                              </Box>
                            )}

                            <Box
                              mt={2}
                              sx={{
                                display: "flex",
                                flexDirection: "column",
                                gap: 2,
                                maxHeight: 400,
                                overflowY: "auto",
                                pr: 1
                              }}
                            >
                              {rv.emailLogs
                                ?.sort((a: any, b: any) => new Date(a.createdAt) - new Date(b.createdAt))
                                .map((log: any) => {
                                  const isSent = log.direction === "outgoing";
                                  return (
                                    <Box
                                      key={log.id}
                                      sx={{
                                        maxWidth: "75%",
                                        alignSelf: isSent ? "flex-start" : "flex-end",
                                        bgcolor: isSent ? "#e3f2fd" : "#e8f5e9",
                                        borderLeft: `5px solid ${isSent ? "#1976d2" : "#2e7d32"}`,
                                        p: 2,
                                        borderRadius: 2,
                                        boxShadow: 1
                                      }}
                                    >
                                      {/* Direction Label */}
                                      <Typography
                                        variant="caption"
                                        sx={{ fontWeight: 700, color: isSent ? "#0d47a1" : "#1b5e20" }}
                                      >
                                        {isSent ? "Sent by You" : "Vendor Reply"}
                                      </Typography>

                                      {/* Subject */}
                                      <Typography variant="subtitle2" sx={{ mt: 1, fontWeight: 600 }}>
                                        {log.subject || "(No Subject)"}
                                      </Typography>

                                      {/* Body */}
                                      <Box
                                        sx={{ mt: 1 }}
                                        dangerouslySetInnerHTML={{
                                          __html: log.body || "<i>(Empty message)</i>"
                                        }}
                                      />

                                      {/* Timestamp */}
                                      <Typography
                                        variant="caption"
                                        sx={{ display: "block", mt: 1, color: "#777" }}
                                      >
                                        {new Date(log.createdAt).toLocaleString()}
                                      </Typography>
                                    </Box>
                                  );
                                })}
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
