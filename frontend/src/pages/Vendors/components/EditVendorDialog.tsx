import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import { useState, useEffect } from "react";
import { useUpdateVendor } from "../../../api/vendor";
import { useToast } from "../../../components/Toast/MuiToastProvider";

export default function EditVendorDialog({ vendor, onClose }: any) {
  const [form, setForm] = useState(vendor);
  const updateVendor = useUpdateVendor();
  const { showToast } = useToast();

  // Sync form whenever vendor changes
  useEffect(() => {
    setForm(vendor);
  }, [vendor]);

  const submit = () => {
    if (!form.name.trim()) {
      showToast("Name is required", "error");
      return;
    }

    updateVendor.mutate(
      { id: vendor.id, data: form },
      {
        onSuccess: () => {
          showToast("Vendor updated successfully", "success");
          onClose();
        },
        onError: () => showToast("Failed to update vendor", "error"),
      }
    );
  };

  return (
    <Dialog open={!!vendor} onClose={onClose} fullWidth>
      <DialogTitle>Edit Vendor</DialogTitle>

      <DialogContent>
        <Stack gap={2} mt={1}>
          <TextField
            label="Name"
            value={form?.name ?? ""}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            fullWidth
          />

          <TextField
            label="Email"
            value={form?.email ?? ""}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            fullWidth
          />

          <TextField
            label="Phone"
            value={form?.phone ?? ""}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
            fullWidth
          />
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>

        <Button variant="contained" onClick={submit}>
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}
