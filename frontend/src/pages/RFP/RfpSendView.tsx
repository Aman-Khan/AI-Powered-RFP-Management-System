import {
    Box,
    Card,
    CardContent,
    CircularProgress,
    Typography,
    Divider,
    Button,
    IconButton
} from "@mui/material";

import ReplayIcon from "@mui/icons-material/Replay";
import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { useRfpById, useGenerateEmail } from "../../api/rfp";
import { useToast } from "../../components/Toast/MuiToastProvider";
import { useTypewriter } from "../../hooks/useTypewriter";
import RfpVendorSelectModal from "./RfpVendorSelectModal";

// Inject animation only once
const waveKeyframes = `
@keyframes wave {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
`;

if (typeof document !== "undefined" && !document.getElementById("wave-style")) {
    const style = document.createElement("style");
    style.id = "wave-style";
    style.innerHTML = waveKeyframes;
    document.head.appendChild(style);
}

export default function RfpSendView() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { showToast } = useToast();

    const { data: rfp, isLoading } = useRfpById(id!);
    const generateEmail = useGenerateEmail();

    const [finalEmail, setFinalEmail] = useState("");
    const [typedEmail, setTypedEmail] = useState("");
    const [loadingEmail, setLoadingEmail] = useState(false);
    const [isTypingDone, setIsTypingDone] = useState(false);
    const [openVendorModal, setOpenVendorModal] = useState(false);

    const PREVIEW_HEIGHT = "350px";

    // ——— Typewriter Effect ———
    useTypewriter({
        text: finalEmail,
        speed: 18,
        onUpdate: setTypedEmail,
        onDone: () => setIsTypingDone(true),
    });

    // ——— Load Email Template ———
    const loadEmailTemplate = () => {
        setLoadingEmail(true);
        setIsTypingDone(false);
        setTypedEmail("Generating template...");

        generateEmail.mutate(
            { rfpId: id! },
            {
                onSuccess: (res) => {
                    const full = `${res.subject}\n\n${res.content}\n\n${res.footer}`;
                    setFinalEmail(full);
                    setLoadingEmail(false);
                },
                onError: () => {
                    showToast("Failed to generate email template", "error");
                    setLoadingEmail(false);
                },
            }
        );
    };

    useEffect(() => {
        if (rfp) loadEmailTemplate();
    }, [rfp]);

    // ——— Navigate to Vendor Send Page ———
    const handleGoToVendorPage = () => {
        navigate(`/rfp/send/${id}/vendors`, {
            state: { emailBody: typedEmail }
        });
    };

    if (isLoading || !rfp) {
        return (
            <Box display="flex" justifyContent="center" py={5}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box display="flex" gap={3}>
            <RfpVendorSelectModal
                open={openVendorModal}
                onClose={() => setOpenVendorModal(false)}
                emailBody={typedEmail}
                rfpId={id!}
            />

            {/* LEFT SIDEBAR */}
            <Card sx={{ width: "45%" }}>
                <CardContent>
                    <Typography variant="h5" fontWeight={700}>
                        {rfp.title}
                    </Typography>

                    <Typography color="text.secondary" mb={2}>
                        {rfp.description}
                    </Typography>

                    <Divider sx={{ my: 2 }} />

                    <Typography variant="h6">Structured Requirements</Typography>

                    <pre
                        style={{
                            background: "#f7f7f7",
                            padding: 12,
                            borderRadius: 6,
                            whiteSpace: "pre-wrap",
                        }}
                    >
                        {JSON.stringify(rfp.structuredRequirements, null, 2)}
                    </pre>
                </CardContent>
            </Card>

            {/* RIGHT - EMAIL PREVIEW */}
            <Card sx={{ width: "55%" }}>
                <CardContent>
                    <Box display="flex" justifyContent="space-between">
                        <Typography variant="h6" fontWeight={700}>
                            Email Template Preview
                        </Typography>

                        <IconButton onClick={loadEmailTemplate}>
                            <ReplayIcon />
                        </IconButton>
                    </Box>

                    {/* FIXED HEIGHT CONTAINER */}
                    <Box sx={{ minHeight: PREVIEW_HEIGHT }}>
                        {(!isTypingDone || loadingEmail) ? (
                            <Box
                                sx={{
                                    height: PREVIEW_HEIGHT,
                                    padding: 2,
                                    border: "1px solid #ccc",
                                    borderRadius: 2,
                                    fontFamily: "monospace",
                                    whiteSpace: "pre-wrap",
                                    overflowY: "auto",
                                }}
                            >
                                {loadingEmail ? <WaveLoadingText /> : typedEmail}
                            </Box>
                        ) : (
                            <textarea
                                value={typedEmail}
                                onChange={(e) => setTypedEmail(e.target.value)}
                                style={{
                                    width: "100%",
                                    height: PREVIEW_HEIGHT,
                                    padding: 12,
                                    border: "1px solid #ccc",
                                    borderRadius: 6,
                                    fontFamily: "monospace",
                                    whiteSpace: "pre-wrap",
                                    overflowY: "auto",
                                }}
                            />
                        )}
                    </Box>

                    <Button
                        variant="contained"
                        size="large"
                        sx={{ mt: 2 }}
                        onClick={handleGoToVendorPage}
                    >
                        Continue → Select Vendors
                    </Button>
                </CardContent>
            </Card>
        </Box>
    );
}

function WaveLoadingText() {
    return (
        <div style={{ overflow: "hidden", width: "fit-content" }}>
            <span
                style={{
                    fontFamily: "monospace",
                    background: "linear-gradient(90deg, #bbb 20%, #eee 50%, #bbb 80%)",
                    backgroundSize: "200% 100%",
                    animation: "wave 3.5s ease-in-out infinite",
                    WebkitBackgroundClip: "text",
                    color: "transparent",
                }}
            >
                Generating template...
            </span>
        </div>
    );
}
