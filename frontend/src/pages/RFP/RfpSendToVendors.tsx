import {
    Box,
    Card,
    CardContent,
    Typography,
    Checkbox,
    Table,
    TableRow,
    TableHead,
    TableCell,
    TableBody,
    Button,
    Stack
} from "@mui/material";

import { useParams, useLocation } from "react-router-dom";
import { useState } from "react";
import { useVendors } from "../../api/vendor";
import { useSendEmail } from "../../api/email";
import { useToast } from "../../components/Toast/MuiToastProvider";

export default function RfpSendToVendors() {
    const { id } = useParams();
    const rfpId = id ?? "";           // <-- FIX: never undefined
    const { showToast } = useToast();

    const location = useLocation();
    const emailBody: string = location.state?.emailBody || "";

    const subject = emailBody.split("\n")[0];
    const content = emailBody.substring(subject.length).trim();

    const { data: vendors, isLoading } = useVendors(0, 100, "");
    const sendEmail = useSendEmail();

    const [selected, setSelected] = useState<string[]>([]);

    const toggle = (vendorId: string) => {
        setSelected(prev =>
            prev.includes(vendorId)
                ? prev.filter(v => v !== vendorId)
                : [...prev, vendorId]
        );
    };

    const sendEmails = () => {
        if (selected.length === 0) {
            showToast("Select at least one vendor", "error");
            return;
        }

        sendEmail.mutate({
            rfpId: rfpId!,
            vendorIds: selected,
            subject,
            content
        },
            {
                onSuccess: () => {
                    showToast(`Emails sent successfully!`, "success");
                },
                onError: () => {
                    showToast("Failed to send emails", "error");
                }
            }
        );
    };

    if (isLoading) return <div>Loading vendors…</div>;

    return (
        <Box>
            <Typography variant="h4" mb={2}>
                Select Vendors to Send Email
            </Typography>

            <Card>
                <CardContent>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell />
                                <TableCell><strong>Name</strong></TableCell>
                                <TableCell><strong>Email</strong></TableCell>
                                <TableCell><strong>Phone</strong></TableCell>
                            </TableRow>
                        </TableHead>

                        <TableBody>
                            {vendors?.map((v: any) => (
                                <TableRow key={v.id}>
                                    <TableCell padding="checkbox">
                                        <Checkbox
                                            checked={selected.includes(v.id)}
                                            onChange={() => toggle(v.id)}
                                        />
                                    </TableCell>

                                    <TableCell>{v.name}</TableCell>
                                    <TableCell>{v.email || "-"}</TableCell>
                                    <TableCell>{v.phone || "-"}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>

                    <Stack direction="row" justifyContent="flex-end" mt={2}>
                        <Button
                            variant="contained"
                            size="large"
                            onClick={sendEmails}
                            disabled={sendEmail.isPending}
                        >
                            {sendEmail.isPending
                                ? "Sending..."
                                : `Send Email to ${selected.length} Vendor(s)`
                            }
                        </Button>
                    </Stack>
                </CardContent>
            </Card>
        </Box>
    );
}
