import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Checkbox,
    Table,
    TableRow,
    TableCell,
    TableHead,
    TableBody,
} from "@mui/material";

import { useVendors } from "../../api/vendor";
import { useState } from "react";
import { useToast } from "../../components/Toast/MuiToastProvider";
import { useSendEmail } from "../../api/email";

export default function RfpVendorSelectModal({ open, onClose, emailBody, rfpId }: any) {
    const { showToast } = useToast();
    const { data: vendors, isLoading } = useVendors(0, 100, "");
    const sendEmail = useSendEmail();

    const [selected, setSelected] = useState<string[]>([]);

    const toggle = (id: string) =>
        setSelected(prev =>
            prev.includes(id)
                ? prev.filter(v => v !== id)
                : [...prev, id]
        );

    const handleSend = () => {
        if (selected.length === 0) {
            showToast("Select at least one vendor", "error");
            return;
        }

        const subject = emailBody.split("\n")[0];
        const content = emailBody.substring(subject.length).trim();

        sendEmail.mutate({
            rfpId: rfpId!,
            vendorIds: selected,
            subject,
            content
        },
            {
                onSuccess: (res) => {
                    showToast(`Emails sent to ${res.count} vendors`, "success");
                    onClose();
                },
                onError: () => showToast("Failed to send email", "error")
            }
        );
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>Select Vendors</DialogTitle>

            <DialogContent dividers>
                {isLoading ? (
                    "Loading..."
                ) : (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell />
                                <TableCell><strong>Name</strong></TableCell>
                                <TableCell><strong>Email</strong></TableCell>
                            </TableRow>
                        </TableHead>

                        <TableBody>
                            {vendors?.map((v: any) => (
                                <TableRow key={v.id}>
                                    <TableCell>
                                        <Checkbox
                                            checked={selected.includes(v.id)}
                                            onChange={() => toggle(v.id)}
                                        />
                                    </TableCell>
                                    <TableCell>{v.name}</TableCell>
                                    <TableCell>{v.email}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </DialogContent>

            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>

                <Button
                    variant="contained"
                    onClick={handleSend}
                    disabled={isLoading || sendEmail.isPending}
                >
                    {sendEmail.isPending
                        ? "Sending..."
                        : `Send Email to ${selected.length} vendor(s)`
                    }
                </Button>
            </DialogActions>
        </Dialog>
    );
}
