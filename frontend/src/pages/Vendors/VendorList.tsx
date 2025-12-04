// src/pages/Vendor/VendorList.tsx
import {
    Box,
    Button,
    Card,
    CardContent,
    IconButton,
    TextField,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    Stack,
    Checkbox,
    TablePagination,
} from "@mui/material";

import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";

import { useState } from "react";
import { useVendors, useDeleteVendor } from "../../api/vendor";
import AddVendorDialog from "./components/AddVendorDialog";
import EditVendorDialog from "./components/EditVendorDialog";
import DeleteConfirmDialog from "../../components/Dialog/DeleteConfirmDialog";
import { useToast } from "../../components/Toast/MuiToastProvider";

export default function VendorList() {
    const { showToast } = useToast();

    const [page, setPage] = useState(0);
    const [limit, setLimit] = useState(10);
    const [search, setSearch] = useState("");

    const { data: vendors, isLoading, refetch } = useVendors(page, limit, search);

    const deleteVendor = useDeleteVendor();

    const [selected, setSelected] = useState<string[]>([]);
    const [openAdd, setOpenAdd] = useState(false);
    const [editVendor, setEditVendor] = useState<any>(null);

    // Delete modal
    const [confirmOpen, setConfirmOpen] = useState(false);
    const [deleteIds, setDeleteIds] = useState<string[]>([]);

    const rows = vendors ?? [];

    const toggleSelect = (id: string) => {
        setSelected((prev) =>
            prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
        );
    };

    const openDeleteDialogSingle = (id: string) => {
        setDeleteIds([id]);
        setConfirmOpen(true);
    };

    const openDeleteDialogMultiple = () => {
        if (selected.length === 0) {
            showToast("No vendors selected", "error");
            return;
        }
        setDeleteIds(selected);
        setConfirmOpen(true);
    };

    const confirmDelete = async () => {
        if (deleteIds.length === 0) return;

        try {
            await Promise.all(deleteIds.map((id) => deleteVendor.mutateAsync(id)));
            showToast(`Deleted ${deleteIds.length} vendor(s)`, "success");
            setSelected([]);
            refetch();
        } catch {
            showToast("Failed to delete vendors", "error");
        }

        setConfirmOpen(false);
        setDeleteIds([]);
    };

    return (
        <Box>
            <Typography variant="h4" fontWeight={700} mb={2}>
                Vendors
            </Typography>

            <Stack direction="row" justifyContent="space-between" mb={2}>
                <TextField
                    placeholder="Search vendors..."
                    value={search}
                    onChange={(e) => {
                        setSearch(e.target.value);
                        setPage(0);
                    }}
                    sx={{ width: 300 }}
                />

                <Stack direction="row" spacing={2}>
                    {selected.length > 0 && (
                        <Button
                            variant="outlined"
                            color="error"
                            startIcon={<DeleteIcon />}
                            onClick={openDeleteDialogMultiple}
                        >
                            Delete Selected ({selected.length})
                        </Button>
                    )}

                    <Button
                        variant="contained"
                        startIcon={<AddIcon />}
                        onClick={() => setOpenAdd(true)}
                    >
                        Add Vendor
                    </Button>
                </Stack>
            </Stack>

            <Card>
                <CardContent>
                    {isLoading ? (
                        <Box display="flex" justifyContent="center" py={5}>
                            <CircularProgress />
                        </Box>
                    ) : (
                        <Paper>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell padding="checkbox">
                                            <Checkbox
                                                checked={rows.length > 0 && selected.length === rows.length}
                                                indeterminate={
                                                    selected.length > 0 && selected.length < rows.length
                                                }
                                                onChange={() =>
                                                    setSelected(
                                                        selected.length === rows.length
                                                            ? []
                                                            : rows.map((v: any) => v.id)
                                                    )
                                                }
                                            />
                                        </TableCell>

                                        <TableCell><strong>Name</strong></TableCell>
                                        <TableCell><strong>Email</strong></TableCell>
                                        <TableCell><strong>Phone</strong></TableCell>
                                        <TableCell><strong>Actions</strong></TableCell>
                                    </TableRow>
                                </TableHead>

                                <TableBody>
                                    {rows.map((vendor: any) => (
                                        <TableRow key={vendor.id}>
                                            <TableCell padding="checkbox">
                                                <Checkbox
                                                    checked={selected.includes(vendor.id)}
                                                    onChange={() => toggleSelect(vendor.id)}
                                                />
                                            </TableCell>

                                            <TableCell>{vendor.name}</TableCell>
                                            <TableCell>{vendor.email || "-"}</TableCell>
                                            <TableCell>{vendor.phone || "-"}</TableCell>

                                            <TableCell>
                                                <IconButton
                                                    onClick={() => setEditVendor(vendor)}
                                                    color="primary"
                                                >
                                                    <EditIcon />
                                                </IconButton>

                                                <IconButton
                                                    onClick={() => openDeleteDialogSingle(vendor.id)}
                                                    color="error"
                                                >
                                                    <DeleteIcon />
                                                </IconButton>
                                            </TableCell>
                                        </TableRow>
                                    ))}

                                    {rows.length === 0 && (
                                        <TableRow>
                                            <TableCell colSpan={5} align="center">
                                                No vendors found
                                            </TableCell>
                                        </TableRow>
                                    )}
                                </TableBody>
                            </Table>

                            <TablePagination
                                component="div"
                                count={1000}
                                page={page}
                                onPageChange={(e, newPage) => setPage(newPage)}
                                rowsPerPage={limit}
                                onRowsPerPageChange={(e) => {
                                    setLimit(parseInt(e.target.value, 10));
                                    setPage(0);
                                }}
                            />
                        </Paper>
                    )}
                </CardContent>
            </Card>

            {/* Dialogs */}
            <AddVendorDialog open={openAdd} onClose={() => setOpenAdd(false)} />
            {editVendor && (
                <EditVendorDialog vendor={editVendor} onClose={() => setEditVendor(null)} />
            )}

            {/* Delete Confirmation */}
            <DeleteConfirmDialog
                open={confirmOpen}
                onClose={() => setConfirmOpen(false)}
                onConfirm={confirmDelete}
                title="Delete Vendor(s)?"
                message={`Are you sure you want to delete ${deleteIds.length
                    } vendor(s)? This action cannot be undone.`}
            />
        </Box>
    );
}
