import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import { useState } from "react";
import { useAddVendor } from "../../../api/vendor";
import { useToast } from "../../../components/Toast/MuiToastProvider";

export default function AddVendorDialog({ open, onClose }: any) {
  const [form, setForm] = useState({ name: "", email: "", phone: "" });
  const addVendor = useAddVendor();
  const { showToast } = useToast();   // ⭐ MUI Toast

  const submit = () => {
    if (!form.name.trim()) {
      showToast("Name is required", "error");
      return;
    }

    addVendor.mutate(form, {
      onSuccess: () => {
        showToast(`Vendor "${form.name}" added successfully`, "success");

        // reset form
        setForm({ name: "", email: "", phone: "" });

        onClose();
      },
      onError: () => showToast("Failed to add vendor", "error"),
    });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth>
      <DialogTitle>Add Vendor</DialogTitle>

      <DialogContent>
        <Stack gap={2} mt={1}>
          <TextField
            label="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            fullWidth
          />

          <TextField
            label="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            fullWidth
          />

          <TextField
            label="Phone"
            value={form.phone}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
            fullWidth
          />
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>

        <Button variant="contained" onClick={submit}>
          Add
        </Button>
      </DialogActions>
    </Dialog>
  );
}
