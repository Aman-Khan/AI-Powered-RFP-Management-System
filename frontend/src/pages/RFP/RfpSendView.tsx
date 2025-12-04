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

import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useRfpById, useGenerateEmail } from "../../api/rfp";
import { useToast } from "../../components/Toast/MuiToastProvider";
import { useTypewriter } from "../../hooks/useTypewriter";

const waveKeyframes = `
@keyframes wave {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
`;

if (typeof document !== "undefined") {
  const style = document.createElement("style");
  style.innerHTML = waveKeyframes;
  document.head.appendChild(style);
}


export default function RfpSendView() {
    const { id } = useParams();
    const { showToast } = useToast();

    const { data: rfp, isLoading } = useRfpById(id!);
    const generateEmail = useGenerateEmail();

    const [finalEmail, setFinalEmail] = useState("");
    const [typedEmail, setTypedEmail] = useState("");
    const [loadingEmail, setLoadingEmail] = useState(false);
    const [isTypingDone, setIsTypingDone] = useState(false);

    // FIX → Always keep preview box constant height
    const PREVIEW_HEIGHT = "350px";

    // TYPEWRITER
    useTypewriter({
        text: finalEmail,
        speed: 15,
        onUpdate: setTypedEmail,
        onDone: () => setIsTypingDone(true),
    });

    const loadEmailTemplate = () => {
        setLoadingEmail(true);
        setIsTypingDone(false);

        // Keep UI stable
        setTypedEmail("Generating template...");

        generateEmail.mutate(
            { rfpId: id! },
            {
                onSuccess: (res) => {
                    const fullEmail =
                        `${res.subject}\n\n${res.content}\n\n${res.footer}`;

                    setFinalEmail(fullEmail);

                    // Stop "loading..." blink but keep height stable
                    setLoadingEmail(false);
                },
                onError: () => {
                    showToast("Failed to generate email template", "error");
                    setLoadingEmail(false);
                }
            }
        );
    };

    // Load once
    useEffect(() => {
        if (rfp) loadEmailTemplate();
    }, [rfp]);

    if (isLoading || !rfp) {
        return (
            <Box display="flex" justifyContent="center" py={5}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box display="flex" gap={3}>
            {/* LEFT PANE */}
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
                            padding: "12px",
                            borderRadius: 6,
                            whiteSpace: "pre-wrap",
                            fontSize: "0.9rem",
                        }}
                    >
                        {JSON.stringify(rfp.structuredRequirements, null, 2)}
                    </pre>
                </CardContent>
            </Card>

            {/* RIGHT PANE */}
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

                    {/* FIXED SIZE CONTAINER */}
                    <Box sx={{ minHeight: PREVIEW_HEIGHT }}>
                        {/* While typing OR generating */}
                        {(!isTypingDone || loadingEmail) ? (
                            <Box
                                sx={{
                                    height: PREVIEW_HEIGHT,
                                    padding: 2,
                                    border: "1px solid #ccc",
                                    borderRadius: 2,
                                    background: "#fff",
                                    fontFamily: "monospace",
                                    whiteSpace: "pre-wrap",
                                    overflowY: "auto",
                                }}
                            >
                                {/* {loadingEmail ? <BlinkingText /> : typedEmail} */}
                                {loadingEmail ? <WaveLoadingText /> : typedEmail}

                            </Box>
                        ) : (
                            // Editable AFTER typing completes
                            <textarea
                                value={typedEmail}
                                onChange={(e) => setTypedEmail(e.target.value)}
                                style={{
                                    width: "100%",
                                    height: PREVIEW_HEIGHT,
                                    padding: "12px",
                                    border: "1px solid #ccc",
                                    borderRadius: "6px",
                                    fontFamily: "monospace",
                                    resize: "none",
                                    whiteSpace: "pre-wrap",
                                    overflowY: "auto"
                                }}
                            />
                        )}
                    </Box>

                    <Button
                        variant="contained"
                        size="large"
                        sx={{ mt: 2 }}
                        onClick={() => showToast("Email sent!", "success")}
                    >
                        Send Email
                    </Button>
                </CardContent>
            </Card>
        </Box>
    );
}

function WaveLoadingText() {
  return (
    <div style={{ position: "relative", overflow: "hidden", width: "fit-content" }}>
      <span
        style={{
          fontFamily: "monospace",
          fontSize: "1rem",
          background: "linear-gradient(90deg, #999 20%, #ccc 40%, #999 60%)",
          backgroundSize: "200% 100%",
          animation: "wave 2.2s ease-in-out infinite", // slower wave
          WebkitBackgroundClip: "text",
          color: "transparent",
        }}
      >
        Generating template...
      </span>

      {/* Keyframes */}
      <style>
        {`
          @keyframes wave {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
          }
        `}
      </style>
    </div>
  );
}

