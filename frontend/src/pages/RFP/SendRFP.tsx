import {
    Box,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Paper,
    IconButton,
    Collapse,
    Checkbox,
    TablePagination,
    TextField,
    Stack,
} from "@mui/material";

import SendIcon from "@mui/icons-material/Send";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import { api } from "../../lib/axios";
import { useUserRFPs } from "../../api/rfp";
import DeleteConfirmDialog from "../../components/Dialog/DeleteConfirmDialog";

export default function SendRFP() {
    const userId = localStorage.getItem("userId");
    const navigate = useNavigate();

    // Pagination
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);

    // Search
    const [search, setSearch] = useState("");

    // Expand row
    const [openRow, setOpenRow] = useState<string | null>(null);

    // Selected rows
    const [selected, setSelected] = useState<string[]>([]);

    // Single delete dialog
    const [deleteId, setDeleteId] = useState<string | null>(null);
    const [confirmSingleOpen, setConfirmSingleOpen] = useState(false);

    // Multi delete dialog
    const [confirmMultiOpen, setConfirmMultiOpen] = useState(false);

    const { data: rfps, isLoading, refetch } = useUserRFPs(
        userId,
        page * rowsPerPage,
        rowsPerPage
    );

    // Toggle checkbox
    const toggleSelect = (id: string) => {
        setSelected((prev) =>
            prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
        );
    };

    // Perform single delete
    const confirmSingleDelete = async () => {
        if (!deleteId) return;

        try {
            await api.delete(`/rfp/${deleteId}`);
            toast.success("RFP deleted");
            await refetch();
        } catch {
            toast.error("Failed to delete RFP");
        }

        setConfirmSingleOpen(false);
        setDeleteId(null);
    };

    // Perform multiple deletes
    const confirmMultiDelete = async () => {
        try {
            await Promise.all(selected.map((id) => api.delete(`/rfp/${id}`)));
            toast.success(`Deleted ${selected.length} RFPs`);
            setSelected([]);
            await refetch();
        } catch {
            toast.error("Failed to delete selected RFPs");
        }

        setConfirmMultiOpen(false);
    };

    // Navigation
    const handleSend = (id: string) => navigate(`/rfp/send/${id}`);
    const handleEdit = (id: string) => navigate(`/rfp/edit/${id}`);

    // Filter search
    const filtered =
        rfps?.filter((r: any) =>
            (r.title + r.description).toLowerCase().includes(search.toLowerCase())
        ) || [];

    return (
        <Box>
            <Typography variant="h4" fontWeight={700} mb={1}>
                Send RFP
            </Typography>

            <Typography variant="body1" color="text.secondary" mb={3}>
                Select an RFP, preview details and send to vendors.
            </Typography>

            {/* Search + Multi Delete */}
            <Stack direction="row" justifyContent="space-between" mb={2}>
                <TextField
                    placeholder="Search RFPs..."
                    size="small"
                    sx={{ width: 260 }}
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />

                {selected.length > 0 && (
                    <Button
                        color="error"
                        variant="outlined"
                        startIcon={<DeleteIcon />}
                        onClick={() => setConfirmMultiOpen(true)}
                    >
                        Delete Selected ({selected.length})
                    </Button>
                )}
            </Stack>

            <Card elevation={2}>
                <CardContent>
                    {isLoading ? (
                        <Box display="flex" justifyContent="center" py={5}>
                            <CircularProgress />
                        </Box>
                    ) : filtered.length === 0 ? (
                        <Typography textAlign="center" py={4} color="text.secondary">
                            No RFPs found
                        </Typography>
                    ) : (
                        <Paper>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell padding="checkbox">
                                            <Checkbox
                                                checked={
                                                    selected.length === filtered.length &&
                                                    filtered.length > 0
                                                }
                                                onChange={() =>
                                                    selected.length === filtered.length
                                                        ? setSelected([])
                                                        : setSelected(filtered.map((r: any) => r.id))
                                                }
                                            />
                                        </TableCell>

                                        <TableCell />
                                        <TableCell><strong>Title</strong></TableCell>
                                        <TableCell><strong>Description</strong></TableCell>
                                        <TableCell><strong>Actions</strong></TableCell>
                                    </TableRow>
                                </TableHead>

                                <TableBody>
                                    {filtered.map((rfp: any) => (
                                        <React.Fragment key={rfp.id}>
                                            {/* MAIN ROW */}
                                            <TableRow>
                                                <TableCell padding="checkbox">
                                                    <Checkbox
                                                        checked={selected.includes(rfp.id)}
                                                        onChange={() => toggleSelect(rfp.id)}
                                                    />
                                                </TableCell>

                                                <TableCell>
                                                    <IconButton
                                                        size="small"
                                                        onClick={() =>
                                                            setOpenRow(openRow === rfp.id ? null : rfp.id)
                                                        }
                                                    >
                                                        {openRow === rfp.id ? (
                                                            <KeyboardArrowUpIcon />
                                                        ) : (
                                                            <KeyboardArrowDownIcon />
                                                        )}
                                                    </IconButton>
                                                </TableCell>

                                                <TableCell>{rfp.title}</TableCell>
                                                <TableCell>{rfp.description?.slice(0, 40)}...</TableCell>

                                                <TableCell>
                                                    <Stack direction="row" spacing={1}>
                                                        <IconButton
                                                            color="primary"
                                                            onClick={() => handleSend(rfp.id)}
                                                        >
                                                            <SendIcon />
                                                        </IconButton>

                                                        <IconButton
                                                            color="success"
                                                            onClick={() => handleEdit(rfp.id)}
                                                        >
                                                            <EditIcon />
                                                        </IconButton>

                                                        <IconButton
                                                            color="error"
                                                            onClick={() => {
                                                                setDeleteId(rfp.id);
                                                                setConfirmSingleOpen(true);
                                                            }}
                                                        >
                                                            <DeleteIcon />
                                                        </IconButton>
                                                    </Stack>
                                                </TableCell>
                                            </TableRow>

                                            {/* EXPANDED ROW */}
                                            <TableRow>
                                                <TableCell colSpan={5} sx={{ p: 0 }}>
                                                    <Collapse in={openRow === rfp.id}>
                                                        <Box
                                                            sx={{
                                                                p: 2,
                                                                background: "#fafafa",
                                                                borderTop: "1px solid #eee",
                                                                fontFamily: "monospace",
                                                            }}
                                                        >
                                                            <strong>Structured Requirements</strong>
                                                            <pre style={{ whiteSpace: "pre-wrap" }}>
                                                                {JSON.stringify(
                                                                    rfp.structuredRequirements,
                                                                    null,
                                                                    2
                                                                )}
                                                            </pre>
                                                        </Box>
                                                    </Collapse>
                                                </TableCell>
                                            </TableRow>
                                        </React.Fragment>
                                    ))}
                                </TableBody>
                            </Table>

                            {/* Pagination */}
                            <TablePagination
                                component="div"
                                count={-1}
                                page={page}
                                rowsPerPage={rowsPerPage}
                                onPageChange={(_, p) => setPage(p)}
                                onRowsPerPageChange={(e) => {
                                    setRowsPerPage(parseInt(e.target.value, 10));
                                    setPage(0);
                                }}
                            />
                        </Paper>
                    )}
                </CardContent>
            </Card>

            {/* SINGLE DELETE DIALOG */}
            <DeleteConfirmDialog
                open={confirmSingleOpen}
                title="Delete RFP?"
                message="Are you sure you want to delete this RFP?"
                onClose={() => setConfirmSingleOpen(false)}
                onConfirm={confirmSingleDelete}
            />

            {/* MULTI DELETE DIALOG */}
            <DeleteConfirmDialog
                open={confirmMultiOpen}
                title="Delete Selected RFPs?"
                message={`You are about to delete ${selected.length} RFP(s). This cannot be undone.`}
                onClose={() => setConfirmMultiOpen(false)}
                onConfirm={confirmMultiDelete}
            />
        </Box>
    );
}
